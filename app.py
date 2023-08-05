"""
# ANOTAÇÕES
retornar [] ou {}?
retornando uma [], isso impede que novas propriedades sejam adicionadas.
Já com {} poderia adicionar novas propriedades e ficar assim:
return {"items": store["items"], "message": "Sua requisição foi um sucesso!"}
então no front end é só puxar store.items[item_id].message.
"""

from flask import Flask
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

app = Flask(__name__)  # Initializing flask app

app.config["PROPAGATE_EXCEPTIONS"] = True # facilita exceções de extensões para o arquivo main do Flask
app.config["API_TITLE"] = "Stores REST API" # titulo da api
app.config["API_VERSION"] = "v1" # versão da api
app.config["OPENAPI_VERSION"] = "3.0.3" # versão do flask smorest
app.config["OPENAPI_URL_PREFIX"] = "/" # declara qual prefixo para iniciar um endpoint.(ex: /store)
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui" # para ver a documentação(localhost:5000/swagger-ui)
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" # npm do swagger

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)

# Running app
# if __name__ == '__main__':
#     app.run(debug=True)
