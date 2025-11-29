FROM postgres:16
RUN apt-get update && apt-get install -y postgresql-server-dev-16 \
    && pip install pgvector[pg16]
COPY ./postgresDB/init.sql /docker-entrypoint-initdb.d/
