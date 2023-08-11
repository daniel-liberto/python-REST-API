"""
# ANOTAÇÕES
retornar [] ou {}?
retornando uma [], isso impede que novas propriedades sejam adicionadas.
Já com {} poderia adicionar novas propriedades e ficar assim:
return {"items": store["items"], "message": "Sua requisição foi um sucesso!"}
então no front end é só puxar store.items[item_id].message.
"""
import os
import secrets

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
from blocklist import BLOCKLIST
import models  # this trigger __init__.py in models folder

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url=None):
  app = Flask(__name__)  # Initializing flask app

  app.config["PROPAGATE_EXCEPTIONS"] = True # facilita exceções de extensões para o arquivo main do Flask
  app.config["API_TITLE"] = "Stores REST API" # titulo da api
  app.config["API_VERSION"] = "v1" # versão da api
  app.config["OPENAPI_VERSION"] = "3.0.3" # versão do flask smorest
  app.config["OPENAPI_URL_PREFIX"] = "/" # declara qual prefixo para iniciar um endpoint.(ex: /store)
  app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui" # para ver a documentação(localhost:5000/swagger-ui)
  app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" # npm do swagger
  
  # primeiro tenta conectar em db_url, se não haver conexão então DATABASE_URL será o proximo, ou em ultimo caso o sqlite
  app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db") # database connection
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.init_app(app) # inicia flask SQLAlchemy e ainda "invoca" o proprio Flask(app = Flask(__name__)) em si para se conectarem

  api = Api(app)
  
  app.config["JWT_SECRET_KEY"] = "227908941795316218633443429225171957379"
  jwt = JWTManager(app)
  
  # -------------- Logout section-----------------
  @jwt.token_in_blocklist_loader
  def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST
  
  @jwt.revoked_token_loader
  def revoked_token_callback(jwt_header, jwt_payload):
    return (jsonify({"description": "The token has been revoked.", "error": "token_revoked"}), 401)
  # -------------- Logout section-----------------
  
  # optional extra info para o jwt em todas as vezes que um token é gerado
  @jwt.additional_claims_loader
  def add_claims_to_jwt(identity): # identity(user.id) = vem do user.py(resource)/access_token(linha 35)
    if identity == 1:
      return {"is_admin": True}
    return {"is_admin": False}
  
  @jwt.expired_token_loader
  def expired_token_callback(jwt_header, jwt_payload):
    return (jsonify({"message": "The token has expired.", "error": "token_expired"}), 401)

  @jwt.invalid_token_loader
  def invalid_token_callback(error):
    return (jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401)
  
  @jwt.unauthorized_loader
  def missing_token_callback(error):
    return(jsonify({"description": "Request does not contain an access token.", "error": "authorization_required"}), 401)

  with app.app_context(): 
    db.create_all() # este comando vai criar todas as tabelas no banco
    # SQLAlchemy sabe exatamente quais tabelas criar graças ao "__tablename__" dentro dos models

  api.register_blueprint(ItemBlueprint)
  api.register_blueprint(StoreBlueprint)
  api.register_blueprint(TagBlueprint)
  api.register_blueprint(UserBlueprint)

  return app
