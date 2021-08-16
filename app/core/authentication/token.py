from typing import Any, Optional
import jwt

from app.bootstrap.configmanager import ConfigManager

def issue_token(claims):
    return jwt.encode(claims, ConfigManager.get('main.token_key'), algorithm="HS256")

def decode_token(token) -> Optional[dict]:
    try:
        return jwt.decode(token, ConfigManager.get('main.token_key'), algorithms=["HS256"], verify=True)
    except:
        return None