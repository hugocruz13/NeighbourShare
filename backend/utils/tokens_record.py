import json
from datetime import datetime, timezone
from pathlib import Path
import time
import os

TOKENS_FILE = Path("tokens.json")
BLACK_LIST_FILE = Path("blacklist.json")

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

def _load_blacklist():
    """Carrega os tokens do ficheiro blacklist.json"""
    if not BLACK_LIST_FILE.exists():
        return []
    try:
        with open(BLACK_LIST_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def _save_blacklist(tokens):
    """Salva os tokens no ficheiro blacklist.json"""
    with open(BLACK_LIST_FILE, "w") as f:
        json.dump(tokens, f, indent=4, default=str)

def revoke_token(token: str, user_id: int, time):
    """Adiciona um token para ser revogado e salva no ficheiro"""
    tokens = _load_blacklist()
    tokens.append({
        "user_id": user_id,
        "token": token,
        "time": time,
    })
    _save_blacklist(tokens)

def verify_token_is_revoked(user_id: str, token: str, role: str):
    """Verifica se o token está na blacklist"""
    tokens = _load_blacklist()

    if tokens is None:
        return False
    for tk in tokens:
        difference_seconds = time.time() - tk["time"]
        if tk["token"] is token and difference_seconds < 1800 and tk["user_id"] is user_id:
            return True
        if tk["token"] is None and difference_seconds < 1800 and tk["user_id"] is user_id:
            with open("tokens_login_log.json", "r") as fh:
                data = json.load(fh)
                for entry in data:
                    difference_seconds = time.time() - tk["time"]
                    if entry["user_id"] == user_id and difference_seconds < 1800 and role == entry["role"]:
                        tk["token"] = entry["token"]
                        _save_blacklist(tokens)
                        return True

    return False

def save_tokens_record_list_login(user_id: str, token: str, role:str):
    # Create a record with timestamp
    filename = 'tokens_login_log.json'
    record = {
        "user_id": user_id,
        "token": token,
        "role": role,
        "timestamp": time.time()
    }

    # Check if the file exists
    if os.path.exists(filename):
        # Load existing data
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append the new record
    data.append(record)

    # Save back to the file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)