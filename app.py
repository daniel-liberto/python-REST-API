import uuid
from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
from db import items, stores

app = Flask(__name__)  # Initializing flask app


@app.get("/store")
def get_stores():
    # stores recebe conteudo de stores em list
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    # **store_data vai "unpack" o store_data e guardar tudo em 1 lugar, exceto id que fica separado
    store = {**store_data, "id": store_id}
    # a nova loja será salva na lista stores na posição [store_id] com uuid hex
    stores[store_id] = store
    return store, 201


@app.post("/item")  # Criando item dentro da loja
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Item not found"}, 404
# retornar [] ou {}?
# retornando uma [], isso impede que novas propriedades sejam adicionadas
# com {} poderia adicionar novas propriedades e ficar assim:
# return {"items": store["items"], "message": "Sua requisição foi um sucesso!"}
# então no front end é só puxar store.message


# Running app
if __name__ == '__main__':
    app.run(debug=True)
