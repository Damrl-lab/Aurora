# Aurora Backend — Deployment Walkthrough

This is a step-by-step guide to bringing the Aurora backend up on a new
host, based on the debugging work done on `bhimani-s04` (a CPU-only
shared Linux server). It covers everything from `git clone` to a working
end-to-end `/recommend` call, plus the specific pitfalls you're likely
to hit. Section 8 has extra notes for GPU hosts like FIU's `ruby`.

**Read this instead of (or alongside) `README.md`.** The README describes
the project at a high level; this doc is the "here's exactly what to
type" version.

---

## 0. Prerequisites

- **Docker Engine ≥ 20.10** and **Docker Compose v2** (the `docker compose`
  command, not legacy `docker-compose`).
  - Linux: prefer Docker CE installed via https://get.docker.com. Snap-
    packaged docker has bind-mount restrictions that the compose file
    works around, but CE is smoother.
  - macOS / Windows: Docker Desktop. Give it 8 GB RAM / 4 CPUs / 50 GB
    disk in Settings → Resources.
- **Git**.
- **Memory.** 8 GB RAM is enough for the non-LLM services (Postgres,
  Prolog, router, pipeline). For CPU inference of `deepseek_llm` you
  need **32+ GB RAM** — Qwen-7B at fp32 occupies ~28 GB and you will
  OOM on load with anything less. On an NVIDIA GPU (≥16 GB VRAM),
  host-RAM requirements drop back to ~8 GB.
- **~50 GB free disk** where Docker stores images. Most of it is the
  `deepseek_llm` image (~38 GB — the model weights are baked in).
- `sudo` rights on `docker` commands, or membership in the `docker` group.

### Sanity checks before you start

```bash
docker compose version            # expect v2.x
docker info                       # should connect to the daemon
df -h /var/lib/docker             # need ~50 GB free where images live
```

---

## 1. Clone the repo and switch to `linux`

```bash
git clone https://github.com/Damrl-lab/Aurora.git
cd Aurora
git checkout linux
```

The `linux` branch carries the fixes this doc assumes: pgvector adapter
registration in `db_init`, per-host env overrides, updated README. Do
NOT try to run from `master` — it's the "clean public" branch and will
fail at `db_init`.

---

## 2. Set up the TWO `.env` files

Aurora uses two separate `.env` files. They are different and both
matter.

### 2a. `backend/postgresDB/.env` — Postgres credentials (REQUIRED)

Injected into the Postgres-touching containers at runtime. Create it
manually (gitignored):

```bash
cat > backend/postgresDB/.env <<'EOF'
POSTGRES_DB=course_advisor
POSTGRES_USER=postgres
POSTGRES_PASSWORD=pick_your_own_here
POSTGRES_HOST=vector_db
POSTGRES_PORT=5432
EOF
```

> **Important.** Pick a real password NOW and don't change it later.
> Once `docker compose up` has run even once, the `backend_pgdata`
> volume is initialized with that password and Postgres **ignores**
> subsequent `POSTGRES_PASSWORD` edits in this file. If you need to
> change it later, see Troubleshooting §7a.
>
> Also: avoid single quotes, double quotes, backticks, `$`, and
> backslashes in the password. The `ALTER USER ... WITH PASSWORD '...'`
> command in §7a is awkward to escape if the password itself contains
> quoting characters.

### 2b. `backend/.env` — per-host compose overrides (OPTIONAL)

Only needed if the defaults don't fit your host:

```bash
cp backend/.env.example backend/.env
# edit backend/.env only if necessary
```

Two variables it controls:

| Variable | Default | When to change |
|----------|---------|----------------|
| `PIPELINE_API_PORT` | `8010` | `:8010` is already taken on your host. |
| `CUDA_VISIBLE_DEVICES` | *(empty)* | You see the "No GPU found" crash in §7b. Set to `-1` to force CPU. Leave empty if you have a real GPU or no GPU at all — the code's fallback handles the genuine-no-GPU case. |

Skip this step entirely on a clean machine with nothing on `:8010`.

---

## 3. First bring-up

From `backend/`:

```bash
cd backend
sudo docker compose up -d
```

First run builds 7 images and pulls `pgvector/pgvector:pg16`. Budget
**20–30 minutes** — the `deepseek_llm` build downloads the Qwen-7B
model weights and bakes them into the image, which alone is ~15 min
on a decent connection.

If the `deepseek_llm` build fails partway through (network blip, disk
pressure, etc.), just re-run `sudo docker compose build deepseek_llm`.
Docker's layer cache picks up where it left off — you do not restart
the whole multi-gigabyte download from scratch.

After the command returns:

```bash
sudo docker compose ps -a
```

You should see:
- `vector_db`, `prolog_kb`, `embedding_svc`, `pipeline_api`,
  `deepseek_llm`, `intent_ner`, `router_api` — all `Up`
- `db_init` — `Exited (0)` (one-shot seeder, exit 0 is success)

Anything `Exited (1)` or `Restarting` → jump to §7.

---

## 4. Wait for seeding + LLM startup

`db_init` runs for 30–60 s. `deepseek_llm` takes **2–5 min on CPU** to
load the model into RAM (fast on GPU). Tail each until it's ready:

```bash
sudo docker compose logs -f db_init
# ctrl-c once you see "🎉 All data loaded!"

sudo docker compose logs -f deepseek_llm
# ctrl-c once you see "Uvicorn running on http://0.0.0.0:8001"
```

---

## 5. Verify the pipeline

### 5a. `router_api` routes are registered

```bash
curl -s http://localhost:8002/openapi.json | python3 -m json.tool | grep -E '"/[a-z]'
```

Expect `/candidate_ids`, `/roadmap`, `/check_prerequisite`,
`/explain_requirement`, `/credit_info`. If `/candidate_ids` is missing,
`router_api` didn't finish starting — check its logs.

### 5b. Find a real `user_id` (IMPORTANT)

The README's example `6304012` is **not** in the seeded data and will
give you a 404. Find an actual one from your instance:

```bash
sudo docker compose exec vector_db psql -U postgres -d course_advisor \
  -c "SELECT user_id, program_id FROM User_Program WHERE status='active' LIMIT 5;"
```

Pick any row and remember its `user_id` (e.g., `3869484`). Use that
below.

### 5c. LLM-only smoke test (doesn't touch the DB)

```bash
curl -s --max-time 600 -X POST http://localhost:8011/recommend_raw \
  -H 'Content-Type: application/json' \
  -d '{"q":"What courses should I take next semester?"}' \
  | python3 -m json.tool
```

Expect JSON with a non-empty `advice` string. CPU: 2–3 minutes. GPU:
seconds.

### 5d. Full pipeline end-to-end

Terminal line-wrapping on long prompts can corrupt inline `-d`. Write
the body to a file first:

```bash
cat > /tmp/q.json <<'EOF'
{"q":"What classes should I take if I want to focus on Machine Learning?","user_id":3869484}
EOF

# Replace :8010 with your PIPELINE_API_PORT if overridden.
curl -s --max-time 600 -X POST http://localhost:8010/recommend \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/q.json | python3 -m json.tool
```

Success = JSON with a coherent `advice` string that mentions real
courses (e.g., `CAP_4630`).

---

## 6. Daily / post-reboot workflow

The compose file currently does **not** set a `restart:` policy. After
a host reboot, containers are down but images persist. Bring them back:

```bash
cd backend
sudo docker compose up -d        # no --build; reuses existing images
sudo docker compose ps -a        # confirm
```

Usually finishes in seconds.

`db_init` re-runs on every `docker compose up` and exits 0. Its
loaders use UPSERT patterns throughout, so running it against an
already-seeded database just prints `✅` lines and exits cleanly —
nothing is wiped or duplicated.

Tear down without losing data:

```bash
sudo docker compose down
```

Tear down AND wipe the DB (re-runs `db_init` on next `up`):

```bash
sudo docker compose down -v
```

---

## 7. Troubleshooting — things that bit us, and the fixes

### 7a. `router_api` / `intent_ner` crash with `password authentication failed for user "postgres"`

The `backend_pgdata` volume was initialized with a different password
than the one currently in `backend/postgresDB/.env`. Postgres ignores
`POSTGRES_PASSWORD` after the first init.

**Non-destructive fix** — change the DB's password to match `.env`:

```bash
sudo docker compose exec vector_db psql -U postgres \
  -c "ALTER USER postgres WITH PASSWORD 'YOUR_ENV_PASSWORD_HERE';"
sudo docker compose up -d     # restarts failing services
```

**Destructive fix** — wipe and re-seed (loses any hand-edited data;
`db_init` re-loads everything it originally seeded):

```bash
sudo docker compose down
sudo docker volume rm backend_pgdata
sudo docker compose up -d
```

### 7b. `deepseek_llm` exits with `RuntimeError: No GPU found. A GPU is needed for quantization.`

`torch.cuda.is_available()` returned `True` on your host, but CUDA
can't actually be used (partial NVIDIA driver install, NVML stub, etc.).
Force CPU:

```bash
echo 'CUDA_VISIBLE_DEVICES=-1' >> backend/.env
sudo docker compose up -d deepseek_llm
sudo docker compose logs -f deepseek_llm   # wait for "Uvicorn running"
```

On CPU, Qwen-7B fp32 runs at ~1 token/sec. Responses take 2–5 min.

### 7c. `/recommend` returns `{"detail":"...404...No active program found for this user"}`

Your `user_id` isn't in the seeded data. Re-run §5b.

### 7d. `db_init` exits with `psycopg.ProgrammingError: cannot adapt type 'Vector' using placeholder '%s'`

You're on `master` (or a stale image built before the pgvector-adapter
fix). Get on `linux` and rebuild:

```bash
git checkout linux && git pull
sudo docker compose build db_init
sudo docker compose up -d db_init
```

### 7e. `port is already allocated` on `:8010` (or similar)

Something else on the host holds that port. Add an override:

```bash
echo 'PIPELINE_API_PORT=8020' >> backend/.env
sudo docker compose up -d
```

### 7f. `docker compose up -d` reports "Started" but `docker compose ps` shows only some containers

Observed once on a freshly rebooted host — the compose network wasn't
attached to all services. Clean fix:

```bash
sudo docker compose down
sudo docker compose up -d
sudo docker network inspect backend_default \
  --format '{{range .Containers}}{{.Name}} {{end}}'
# expect 8 container names
```

### 7g. `db_init` errors with `No such file or directory: /workdir/postgresDB/init_schema.py`

The `db_init` image was built from an older Dockerfile that didn't bake
source in. Rebuild:

```bash
sudo docker compose build db_init
sudo docker compose up -d db_init
```

---

## 8. Deploying on `ruby` (FIU GPU server) — untested, verify

> **Heads up:** the repo maintainer who wrote this doc does **not**
> currently have access to `ruby`. Everything below is standard Docker
> + NVIDIA practice, but nobody has actually run it on ruby for this
> project yet. Test carefully. If you succeed, please update this
> section with the real commands that worked.

The payoff is large: LLM inference drops from minutes to seconds.

### 8a. Confirm ruby's GPU + Docker NVIDIA integration

```bash
nvidia-smi                                # list GPUs + driver version
docker info | grep -i runtime             # expect "nvidia" in Runtimes
```

If `nvidia-smi` works but Docker doesn't list the `nvidia` runtime,
the sysadmin needs to install
[nvidia-container-toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
and restart the docker daemon.

Quick test that Docker can actually reach a GPU:

```bash
sudo docker run --rm --gpus all nvidia/cuda:12.2-base nvidia-smi
```

### 8b. Turn on the GPU path in `docker-compose.yml`

Find the `deepseek_llm:` block and:

1. Uncomment `runtime: nvidia`.
2. Uncomment `NVIDIA_VISIBLE_DEVICES: all` in `environment:`.
3. Ensure `CUDA_VISIBLE_DEVICES` is **not** set to `-1`. Either
   remove `backend/.env` entirely, or comment that line out.

The edited block should look like:

```yaml
  deepseek_llm:
    build: ./services/deepseek_llm
    runtime: nvidia
    working_dir: /app
    volumes:
      - ./services/deepseek_llm/.hf_cache:/hf_cache
    environment:
      MODEL_ID: deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
      HF_HOME: /hf_cache
      CUDA_VISIBLE_DEVICES: "${CUDA_VISIBLE_DEVICES:-}"
      NVIDIA_VISIBLE_DEVICES: all
    ...
```

### 8c. Recreate just `deepseek_llm`

```bash
cd backend
sudo docker compose up -d --force-recreate deepseek_llm
sudo docker compose logs -f deepseek_llm
```

### 8d. Sanity-check CUDA is actually used inside the container

```bash
sudo docker compose exec deepseek_llm python3 -c \
  "import torch; print(torch.cuda.is_available(), torch.cuda.device_count())"
```

Expect: `True 1` (or more).

### 8e. Things likely to need attention on ruby

- **Disk location.** If `/var/lib/docker` is small on ruby, point the
  daemon at a bigger volume. Edit `/etc/docker/daemon.json`:
  ```json
  { "data-root": "/path/to/big/disk/docker" }
  ```
  Then `sudo systemctl restart docker`. **Do this BEFORE the first
  build** so the 38 GB `deepseek_llm` image lands in the right place.
- **Group membership.** You'll likely still need `sudo docker ...`
  (most FIU servers don't put regular users in the `docker` group).
- **Port collisions.** Other users on ruby may already use `:8010`,
  `:5432`, `:8001`, etc. Use `backend/.env` to remap (§2b).
- **CUDA version.** The current `deepseek_llm` image assumes a modern
  CUDA driver. If ruby's driver is older than what the image expects,
  the container may exit at load. Try `docker run --rm --gpus all
  nvidia/cuda:12.2-base nvidia-smi` first — if that fails, the image
  will too.
- **Once GPU works**, you can probably drop `CUDA_VISIBLE_DEVICES=-1`
  globally and re-enable the 4-bit-quantization code path in
  `services/deepseek_llm/server.py` for even faster / lighter
  inference. That's an optional optimization; the default CPU-fallback
  code on GPU still uses `float16` and is plenty fast.

---

## 9. What's on `linux` vs `master`

- `master` — public-facing README snapshot. Will NOT run end-to-end as
  of this writing (pgvector adapter bug in `db_init`, no per-host env
  overrides, README example user_id doesn't exist).
- `linux` — everything in this doc. Use this branch for actual work.
  Merge via PR when the stack is proven on your host.

---

## 10. Contacts

- Aurora maintainer: **Lorena A. Quincoso** — GitHub `@lquincoso`
- Lab: **Damrl-lab**
