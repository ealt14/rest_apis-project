from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    #an item that knows nothing about any store
    id = fields.Int(dump_only=True) #specify when it should be used (only return it)
    name = fields.Str(required=True) #something we receive in the JSON payload
    price = fields.Float(required=True)
    
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True) 
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
     id = fields.Int(dump_only=True)
     name = fields.Str()

class ItemUpdateSchema(Schema):
    name = fields.Str() 
    price = fields.Float()
    store_id = fields.Int()

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only = True)
    store=fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only = True)
    store=fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

#for info on how tags and items are related
class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required = True)
    password = fields.Str(required = True, load_only=True) 
    #load_only makes sure the password never gets returned to the client