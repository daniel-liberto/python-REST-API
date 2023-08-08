from marshmallow import Schema, fields
# marshmallow is used for better validation

class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True) # required 0
    name = fields.Str(required=True) # required 1
    price = fields.Float(required=True) # required 1

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True) # required 0
    name = fields.Str(required=True) # required 1

class ItemUpdateSchema(Schema):
    name = fields.Str() # required 0 or 1
    price = fields.Float() # required 0 or 1  

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True) # receiving data from client (POST,UPDATE)
    store = fields.Nested(PlainStoreSchema(), dump_only=True) # returning data from client (GET)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)