from marshmallow import Schema, fields
# marshmallow is used for better validation

class ItemSchema(Schema):
    id = fields.Str(dump_only=True) # required 0
    name = fields.Str(required=True) # required 1
    price = fields.Float(required=True) # required 1
    store_id = fields.Str(required=True)  # required 1

class ItemUpdateSchema(Schema):
    name = fields.Str() # required 0 or 1
    price = fields.Float() # required 0 or 1  

class StoreSchema(Schema):
    id = fields.Str(dump_only=True) # required 0
    name = fields.Str(required=True) # required 1
