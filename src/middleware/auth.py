from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
import os

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    """Validate API key from header"""
    expected_api_key = os.getenv("API_KEY")
    
    if not expected_api_key:
        # Development mode - allow requests without API key
        return "development"
    
    if api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "X-API-Key"},
        )
    
    return api_key
