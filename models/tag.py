from db import db

class TagModel(db.Model):
  __tablename__ = "tags"
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=False, nullable=False)
  store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
  
  store = db.relationship("StoreModel", back_populates="tags") # back_populates = __tablename__
  items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")
  # secondary é a tabela secundaria pq podem existir N tags para N items
  # secondary vai em busca do tags.id em item_tags.py que retorna para o tag.py e usa a id daqui.