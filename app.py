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

from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
import models  # this trigger __init__.py in models folder

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

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

  with app.app_context(): 
    db.create_all() # este comando vai criar todas as tabelas no banco
    # SQLAlchemy sabe exatamente quais tabelas criar graças ao "__tablename__" dentro dos models

  api.register_blueprint(ItemBlueprint)
  api.register_blueprint(StoreBlueprint)
  api.register_blueprint(TagBlueprint)

  return app
