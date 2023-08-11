"""
blocklist.py

Este arquivo apenas contém o blocklist do JWT token. Ele será importado pelo
app e será utilizado para logout, jogando os tokens numa blocklist(lixeira a grosso modo),
quando o usuário desloga.

LEMBRETE: use este blocklist apenas para desenvolvimento. Quando o python reseta
todos os tokens revogados são aceitos novamente, assim um usuário deslogado,
poderia realizar ações normalmente.
Para resolver isso use um Redis(db de memória) para salvar o blocklist.
"""
import redis
from datetime import timedelta

ACCESS_EXPIRES = timedelta(hours=1) # expira em 60 minutos
  
# -----------Redis proxy config---------------------------
jwt_redis_blocklist = redis.StrictRedis(
  host="localhost", port=6379, db=0, decode_responses=True
)
# -----------Redis proxy config---------------------------
# PING test
value = jwt_redis_blocklist.set("key33", "value33")
print(value)

# BLOCKLIST = set()