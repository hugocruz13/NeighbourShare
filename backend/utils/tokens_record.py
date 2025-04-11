import json
from datetime import datetime, timezone
from pathlib import Path

TOKENS_FILE = Path("tokens.json")

def _load_tokens():
    """Carrega os tokens do ficheiro tokens.json"""
    if not TOKENS_FILE.exists():
        return []
    with open(TOKENS_FILE, "r") as f:
        return json.load(f)

def _save_tokens(tokens):
    """Salva os tokens no ficheiro tokens.json"""
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=4, default=str)

def add_save_token(token: str, user_id: int, email: str, token_type: str, exp):
    """Adiciona um novo token e salva no ficheiro"""
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

def validate_token_entry(token: str):
    """Valida se o token está expirado ou usado (mais para verificar se está usado)"""
    tokens = _load_tokens()
    now = datetime.now(timezone.utc)

    for entry in tokens:
        if entry["token"] == token:
            if entry["used"]:
                return False, "Token já foi usado"
            if datetime.fromisoformat(entry["exp"]) < now:
                return False, "Token expirado"
            return True, entry

    return False, "Token não encontrado"

def mark_token_as_used(token: str):
    """Marca um token como usado"""
    tokens = _load_tokens()
    for entry in tokens:
        if entry["token"] == token:
            entry["used"] = True
            break
    _save_tokens(tokens)

def clean_expired_tokens():
    """Limpa tokens expirados do ficheiro"""
    tokens = _load_tokens()
    now = datetime.now(timezone.utc)
    valid_tokens = [t for t in tokens if datetime.fromisoformat(t["exp"]) > now and not t["used"]]
    _save_tokens(valid_tokens)