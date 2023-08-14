import redis
from datetime import timedelta

ACCESS_EXPIRES = timedelta(hours=1)
REFRESH_EXPIRES = timedelta(days=3)

# -----------Redis proxy config---------------------------
# jwt_redis_blocklist = redis.StrictRedis(
#   host="localhost", port=6379, db=0, decode_responses=True
# )
# -----------Redis proxy config---------------------------

# -----------Redis proxy config---------------------------
jwt_redis_blocklist = redis.StrictRedis(
  host="redis://red-cjd6c745kgrc73atcu2g", port=6379, db=0, decode_responses=True
)
# -----------Redis proxy config---------------------------