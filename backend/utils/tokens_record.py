import json
from datetime import datetime, timezone
from pathlib import Path

TOKENS_FILE = Path("tokens.json")

def _load_tokens():
    if not TOKENS_FILE.exists():
        return []
    with open(TOKENS_FILE, "r") as f:
        return json.load(f)

def _save_tokens(tokens):
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=4, default=str)

def add_save_token(token: str, user_id: int, email: str, token_type: str, exp):
    tokens = _load_tokens()
    tokens.append({
        "token": token,
        "user_id": user_id,
        "email": email,
        "type": token_type,
        "exp": exp.isoformat(),
        "used": False
    })
    _save_tokens(tokens)
