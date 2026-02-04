from fastapi import Header, HTTPException, status

API_KEY = "ds_live_8f2a1c9e7b4d3f0a1c9e8f2a1c9e7b4d"

async def verify_api_key(x_api_key: str = Header(...)):
    """
    Enforces the x-api-key header check.
    FastAPI automatically converts 'x-api-key' to 'x_api_key' in Python.
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    return x_api_key