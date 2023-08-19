import os
from datetime import timedelta

ACCESS_EXPIRES = timedelta(hours=1)
REFRESH_EXPIRES = timedelta(days=3)

db_redis = os.getenv("DATABASE_URL_REDIS")