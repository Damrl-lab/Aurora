FROM python:3.11-slim

# install SWI‐Prolog etc.
RUN apt-get update \
 && apt-get install -y swi-prolog libpq-dev gcc \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt  rules_loader.pl   planner_rules.pl   validator_rules.pl   course_titles.pl ./
COPY flowchart_rules   ./flowchart_rules        
COPY validator.py  entrypoint.sh  ./

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
