import redis.asyncio as redis
from app.config import REDIS_URL
import hashlib
import json
from typing import List, Union

redis_client = None

async def connect_redis():
    """Establish a connection to the Redis server."""
    global redis_client
    try:
        redis_client = redis.from_url(REDIS_URL)
        await redis_client.ping()
        print("INFO: Redis connections successful")
    except Exception as e:
        print(f"ERROR: Redis connection failed - {e}")
        
async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
        print("INFO: Redis connection closed")

async def get_redis_client() -> redis.Redis:
    if not redis_client:
        raise ConnectionError("Redis client is not initialized.")
    return redis_client

async def get_cache_key(parts: Union[List[str],str]) -> str:
    if isinstance(parts, list):
        sorted_parts = sorted(parts)
        key_string = ":".join(sorted_parts)
    elif isinstance(parts, str):
        key_string = parts.lower().strip()
    else:
        raise ValueError("Parts must be a list of strings or a single string.")
    
    return hashlib.sha256(key_string.encode()).hexdigest()

