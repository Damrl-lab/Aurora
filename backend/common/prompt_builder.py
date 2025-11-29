from __future__ import annotations
from textwrap import dedent
from typing import Sequence

PROMPT_TEMPLATE = """\
**Student Query**
{question}

**Context Blocks**
{context_blocks}

{extra_blocks}

### CHAIN-OF-THOUGHT FRAME
- WHO: {who}
- WHAT: {what}
- WHEN: {when}
- WHERE: {where}
- WHY: {why}
- HOW: {how}

{closing}
"""

def build_prompt(
    *,
    question: str,
    context_blocks: str = "",
    extra_blocks: str = "",
    who: str = "unknown",
    what: str = "",
    when: str = "any time",
    where: str = "n/a",
    why: str = "…",
    how: str = "…",
    closing: str = (
        "Please think through the frame, then answer with a short rationale "
        "and your recommendation list."
    ),
) -> str:
    """Return a fully-rendered augmented prompt."""
    return dedent(PROMPT_TEMPLATE.format(**locals()))
