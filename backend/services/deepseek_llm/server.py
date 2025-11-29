# services/deepseek_llm/server.py
import os
import re
import textwrap
from typing import Any, Optional
import html 
import torch
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field, ConfigDict
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import BitsAndBytesConfig

# ──────────────────────────────────────────────────────────────────────
#  0.  Global system message 
# ──────────────────────────────────────────────────────────────────────
SYSTEM_MSG = (
    "### System\n"
    "You are *Aurora*, an academic-advising assistant. Speak in a friendly, first-person voice, similar to a human advisor.\n"
    "Always use a warm, encouraging tone—write as if you care personally about the student's success.\n"
    "When you answer, always output exactly two sections:\n"
    "  1) A `<think>…</think>` block containing your chain-of-thought,\n"
    "  2) A `<response>…</response>` block **as your advisor**, beginning with “As your academic advisor, I recommend…”\n"
    "Use **only** the supplied context.  Treat any `plan` or `COURSE_FACT` data in the prompt as fully correct and do **not** question, contradict, or re-evaluate it.\n"
    "  • **STUDENT_HISTORY** (courses the student has already completed)\n"
    "  • **COURSE_FACT** blocks (course metadata)\n"
    "  • **PREREQ_CHAIN** blocks (prerequisite chains)\n"
    "\n"
    "### Example\n"
    "<think>\n"
    "I see you've completed COP_3502 and CGS_1920…\n"
    "</think>\n"
    "<response>\n"
    "As your academic advisor, I'm really excited to help you stay on track! I recommend …\n"
    "</response>\n"
    "If at any point you need info you don't see, reply exactly:\n"
    "```\nINSUFFICIENT_CONTEXT\n```"
)


# ──────────────────────────────────────────────────────────────────────
#  0.5 RAW-LLM only system prompt (no RAG context, just role + format)
# ──────────────────────────────────────────────────────────────────────
RAW_SYS_PROMPT = textwrap.dedent("""
You are *Aurora*, an academic-advising assistant speaking in a warm, first-person voice.
Do **not** ask for more context—just answer the question below.

Answer **only** with a `<response>…</response>` block that:
  1. Begins exactly: “As your academic advisor, I recommend:”
  2. Contains up to **5** bullet-pointed courses, each with a 1–2 sentence rationale.
  
Do **not** emit any `<think>` block or any text outside `</response>`.
""").strip()



# ──────────────────────────────────────────────────────────────────────
#  1.  Model loading
# ──────────────────────────────────────────────────────────────────────
MODEL_ID = os.getenv("MODEL_ID", "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")
dtype = torch.float16 if torch.cuda.is_available() else torch.float32

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)

tokenizer.add_special_tokens(                 
    {"additional_special_tokens": ["<think>", "</think>", "<response>", "</response>"]}
)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",
    quantization_config=bnb_config,
    trust_remote_code=True,
)
model.resize_token_embeddings(len(tokenizer))
model.eval()

# ──────────────────────────────────────────────────────────────────────
#  2.  FastAPI micro-service
# ──────────────────────────────────────────────────────────────────────
app = FastAPI(title="DeepSeek-LLM micro-service")


class GatewayPayload(BaseModel):
    intent:      str
    long_term:   bool = False
    prompt:      Optional[str] = None
    explanation: Optional[str] = None
    plan:        Optional[Any] = None
    text:        Optional[str] = None
    
    filters:     dict[str,Any]   = None
    course_ids:  list[str]       = Field(default_factory=list)
    warning:     Optional[str]    = None
    
    model_config = ConfigDict(extra="allow")


class LLMResponse(BaseModel):
    thought: str = Field(..., description="Model chain-of-thought")
    advice:  str = Field(..., description="Final narrative explanation")
    plan:    Optional[Any] = Field(None, description="The upstream roadmap, if any")


# ──────── Helper to strip any immediately-repeated n-gram of length ≥3 ───────
def remove_repeated_ngrams(text: str, n_min: int = 3) -> str:
    words = text.split()  # split on any whitespace
    L = len(words)
    # scan from largest to n_min n-grams
    for n in range(min(10, L//2), n_min-1, -1):
        i = 0
        while i + 2*n <= L:
            if words[i:i+n] == words[i+n:i+2*n]:
                # delete the repeated block
                del words[i+n:i+2*n]
                L -= n
                i = 0
                continue
            i += 1
    return " ".join(words)

# ──────── Helper to strip any repeated sentences ────────────────────────
def remove_repeated_sentences(text: str) -> str:
    # split on end-of-sentence punctuation + whitespace
    sentences = re.split(r'(?<=[\.!?])\s+|(?=```)', text)
    seen = set()
    out  = []
    for s in sentences:
        if s not in seen:
            seen.add(s)
            out.append(s)
    # re-join with single spaces
    return " ".join(out)



@app.post("/recommend_raw", response_model=LLMResponse)
def recommend_raw(
    q: str       = Body(..., example="What courses next semester?"),
    user_id: int = Body(None),
):
    # 1) Build prompt + tail
    tail = "\n\nNow produce your answer:"
    full_input = RAW_SYS_PROMPT + "\n\n" + q + tail

    # 2) Tokenize & move to device
    inputs = tokenizer(full_input, return_tensors="pt").to(model.device)

    # 3) Stop on </response>
    stop_id = tokenizer.convert_tokens_to_ids("</response>")

    with torch.no_grad():
        out_ids = model.generate(
            **inputs,
            max_new_tokens=200,
            min_new_tokens=30,
            num_beams=3,
            repetition_penalty=1.1,
            no_repeat_ngram_size=4,
            early_stopping=True,
            eos_token_id=stop_id,
        )

    # 4) Decode only the new tokens
    raw = tokenizer.decode(
        out_ids[0][ inputs["input_ids"].shape[1] : ],
        skip_special_tokens=True
    ).strip()

    # 5) Extract the <response> body
    m = re.search(r"<response>\s*(.*?)\s*</response>", raw, re.DOTALL)
    advice = m.group(1).strip() if m else raw

    return LLMResponse(thought="", advice=advice, plan=None)



@app.post("/recommend", response_model=LLMResponse)
def recommend(payload: GatewayPayload) -> LLMResponse:
    # 1 ── short-circuit, but **skip** it for "recommend-courses" and "generic" calls
    if payload.intent not in ("recommend-courses", "generic"):
        for field in ("explanation", "text"):
            ready = getattr(payload, field)
            if ready is not None:
                return LLMResponse(thought="", advice=str(ready).strip(),
                                   plan=payload.plan)

    # else: generate
    if not (payload.prompt or payload.text):
            return LLMResponse(thought="", advice="INSUFFICIENT_CONTEXT", plan=payload.plan)

    # assemble user‐facing prompt
    if payload.intent == "generic":
        full_prompt = SYSTEM_MSG
    else:
        full_prompt = "\n\n".join([SYSTEM_MSG, payload.prompt.strip()])
    
    # choose your tail
    if payload.intent == "recommend-courses":
        if payload.long_term:
            if not payload.plan:
                return LLMResponse(thought="", advice="INSUFFICIENT_CONTEXT", plan=payload.plan)
            
            # roadmap bullets + one-sentence placeholders
            plan_lines = "\n".join(
                f"- **{blk['semester']}**: {', '.join(blk['courses'])}"
                for blk in payload.plan or [])

            plan_lines = html.unescape(re.sub(r"<[^>]+>", "", plan_lines))

            tail = textwrap.dedent(f"""
            ### ROADMAP_REFERENCE
            {plan_lines}

            (Now produce your answer.)

            — Your reply **must contain exactly two blocks**:
            1. `<think>…</think>` with your private reasoning
            2. `<response>…</response>` - your public answer.
                Immediately after the first line, switch to a **bulleted list**.  
                For each bullet include a brief (1-2 sentence) rationale explaining *why* you grouped those courses together (e.g. “This semester focuses on core theory to unlock advanced electives next term”).
                Do **not** repeat “As your academic advisor…”—that phrase goes at the top and nowhere else.
            Only output those two blocks - nothing else.
            — DO NOT repeat any instruction or “remember” lines in your <response>.
            """)
        
        else:
            facts = []
            for block in re.split(r"###\s*COURSE_FACT",
                                  payload.prompt, flags=re.IGNORECASE)[1:]:
                lines  = block.strip().splitlines()
                cid    = lines[0].split(":", 1)[1].strip()
                title  = lines[1].split(":", 1)[1].strip().title()
                creds  = lines[-1].split(":", 1)[1].strip()
                facts.append(f"- **{cid}** ({title}, {creds} credits)")

            fact_list = "\n".join(facts)

            # ── guard: if **no** COURSE_FACT blocks were supplied ────
            if not facts:
                return LLMResponse(
                    thought="",
                    advice="INSUFFICIENT_CONTEXT",
                    plan=payload.plan,
                )

            # otherwise continue building the normal prompt
            fact_list = "\n".join(facts)
            fact_list = html.unescape(re.sub(r"<[^>]+>", "", fact_list))

            tail = textwrap.dedent(f"""
            ### COURSE_REFERENCE
            {fact_list}

            (Now produce your answer.)

            — Your reply **must contain exactly two blocks**:
            1. `<think>…</think>` with your private reasoning
            2. `<response>…</response>` - your public answer.
                For *each* course, include a brief (1-2 sentence) rationale explaining *why* you selected it. If you notice *more than 7 courses*, make sure to pick the best matches for the given query!
                Do **not** repeat “As your academic advisor…”—that phrase goes at the top and nowhere else.
            Only output those two blocks—nothing else.
            — DO NOT repeat any instruction or “remember” lines in your <response>.
            """)
    elif payload.intent == "explain-requirements":
        tail = "<think>\n\n<response>\nList each program requirement and status."

    elif payload.intent == "check-prerequisite":
        tail = "<think>\n\n<response>\nAnswer yes/no and list missing prereqs if any."

    elif payload.intent == "credit-info":
        tail = "<think>\n\n<response>\nReport total and any overloads per semester."

    elif payload.intent == "generic":
        tail = textwrap.dedent("""
        <think>
        This question falls outside of academic‐planning scope.
        </think>
        <response>
        As your academic advisor, I’m sorry but I can’t help with that type of question. Please refer to the appropriate campus resources for assistance.
        </response>
        <!-- ONLY output the contents of the <think> and <response> blocks above — do NOT repeat any system, except *INSUFFICIENT_CONTEXT* if you think suitable.-->""")

    else:
        tail = "<think>\n\n<response>\nGive a helpful answer."

    full_prompt += "\n" + tail + "\n"

    try:
        inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            out_ids = model.generate(
                **inputs,
                max_new_tokens=800,
                min_new_tokens=30, 
                num_beams=3,         
                repetition_penalty=1.1,
                do_sample=False,
                # temperature=1.0,
                # top_p=1.0,
                # no_repeat_ngram_size=4,
                early_stopping=True,
            ) 

        raw = tokenizer.decode(
            out_ids[0][ inputs["input_ids"].shape[1] : ],
            skip_special_tokens=True
        ).strip()

        # extracting what’s inside <think>…</think> and <response>…</response>
        think_m = re.search(r"<think>\s*(.*?)\s*</think>", raw, re.DOTALL)
        resp_m = re.search(r"<response>\s*(.*?)\s*</response>", raw, re.DOTALL)

        thought = think_m.group(1).strip() if think_m else ""
        advice  = resp_m.group(1).strip() if resp_m   else raw

        # strip any block of ≥3 words repeated back-to-back
        advice = remove_repeated_ngrams(advice, n_min=3)
        # then strip any repeated sentences (e.g. duplicate “If at any point…”)
        advice = remove_repeated_sentences(advice)

        # ward: if the lead phrase appears more than once, drop everything after the second copy
        lead = "As your academic advisor"
        parts = advice.split(lead)
        if len(parts) > 2:
            # parts[0] is before the first lead (usually empty),
            # parts[1] is the text between first and second lead,
            # parts[2:] is anything after the second lead — drop that.
            advice = lead + parts[1]

        return LLMResponse(thought=thought,
                           advice=advice,
                           plan=payload.plan)

    except Exception as e:
        print(f"[deepseek_llm] Exception occurred: {repr(e)}", flush=True)
        raise HTTPException(500, detail=f"{type(e).__name__}: {e}")