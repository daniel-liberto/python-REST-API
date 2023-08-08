import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]

            # https://blog.teclado.com/python-dictionary-merge-update-operators/
            item |= item_data

            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    # ItemSchema não está apenas validando o tipo de dado recebido, mas tambem fazendo:
    # item_data = request.get_json(), ou seja um "auto-fetch"
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data) 
        # item_data são os dados "brutos" vindo do front end
        # São "extraidos" as informações, e são enviadas ao model de item(ItemModel)
        # ItemModel vai formatar os dados para ficarem no formato de SQL.
        
        try:
            # add e commit estão separados para que você possa adicionar multiplos items
            # e após isso, realizar apenas 1 único commit em todos eles.
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occorred while inserting the item.")
            
        return item