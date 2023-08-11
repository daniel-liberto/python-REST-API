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

BLOCKLIST = set()