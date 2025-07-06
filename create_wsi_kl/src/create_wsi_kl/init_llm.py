from __future__ import annotations

"""Central place to configure the default LLM for the package.

This is executed on import (see __init__.py) so every Agent/Task that
omits an explicit ``llm=...`` parameter will automatically use the
Gemini model selected when you ran ``crewai create``.

If you later want to change temperature/model etc. you only need to
edit this file.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from crewai import LLM  # type: ignore

# ---------------------------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------------------------
# We look for a .env file in the project root (one level above this file). If
# it exists we load it so that GEMINI_API_KEY and other secrets are available
# via ``os.getenv``. This mirrors what the CLI generated for you.
# ---------------------------------------------------------------------------
_project_root = Path(__file__).resolve().parents[2]
load_dotenv(_project_root / ".env", override=True)  # silently skip if missing

# ---------------------------------------------------------------------------
# Create the default Gemini LLM instance
# ---------------------------------------------------------------------------
_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not _GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found in environment. Add it to your .env file or "
        'export it in your shell (e.g. `export GEMINI_API_KEY="sk-..."`).'
    )

# You can tweak temperature, max_tokens, etc. here if desired.
_default_llm = LLM(
    model="gemini/gemini-2.5-flash-preview-04-17",
    api_key=_GEMINI_API_KEY,
    temperature=0.2,
)

# Value re-exported for other modules to import.
