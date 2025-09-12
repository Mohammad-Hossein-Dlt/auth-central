from redis import Redis

def init_redis_client(
    host: str,
    port: str | int,
    password: str,
) -> Redis:
    redis_client = Redis(
        host=host,
        port=port,
        password=password,
    )
    
    return redis_client
