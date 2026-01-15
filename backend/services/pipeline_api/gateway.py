"""
Pipeline API Gateway

Orchestrates the full RAG pipeline: intent_ner → router_api → deepseek_llm.
Provides a single /recommend endpoint for end-to-end processing.
"""
import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Optional

INTENT_URL = os.getenv("INTENT_URL", "http://intent_ner:8000")
LLM_URL    = os.getenv("LLM_URL",    "http://deepseek_llm:8001") + "/recommend"


class Query(BaseModel):
    q: str
    user_id: int | None = None


class RecommendResponse(BaseModel):
    thought: str
    advice: str
    plan:    Optional[Any] = Field(
        None, description="Upstream multi-semester roadmap, if any"
    )


# -----------------------------------------------------------------------------
TIMEOUT = httpx.Timeout(
    connect=5.0,   # TCP handshake
    read=1200.0,    # streaming the long-ish model reply
    write=1200.0,   # tiny payload, but required by httpx
    pool=5.0       # idle-pool checkout
)

app = FastAPI(title="Full-pipeline gateway")


@app.post("/recommend", response_model=RecommendResponse)
async def recommend(query: Query) -> RecommendResponse:
    """
    End-to-end recommendation pipeline.
    1) Calls intent_ner for query parsing and retrieval
    2) Calls deepseek_llm for natural language response generation
    """
    async with httpx.AsyncClient() as cli:

        # 1) symbolic / vector pipeline
        try:
            resp = await cli.post(
                f"{INTENT_URL}/recommend",
                json=query.model_dump(),
                timeout=TIMEOUT
            )
            resp.raise_for_status()
            envelope = resp.json()
        except Exception as e:
            raise HTTPException(502, f"intent_ner chain failed: {e}")

        # 2) LLM call
        try:
            llm_resp = await cli.post(
                LLM_URL,
                json=envelope,
                timeout=TIMEOUT
            )
            llm_resp.raise_for_status()
        except Exception as e:
            raise HTTPException(502, f"deepseek_llm failed: {e}")

    # 3) remap fields
    data   = llm_resp.json()
    thought= data.get("thought", "").strip()
    advice = data.get("advice", data.get("text", "")).strip()
    plan   = data.get("plan", None)

    return RecommendResponse(
        thought=thought,
        advice=advice,
        plan=plan,
    )
