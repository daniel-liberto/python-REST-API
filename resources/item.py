import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id) #get or 404 é auto explicativo (flask-sqlalchemy)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        # se item existe então UPDATE nele
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        # se item não existe então POST ele
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()
        
        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True)) # many = true, cria uma lista de itens.
    def get(self):
        return ItemModel.query.all()
    
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