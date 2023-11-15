from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on stores")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id) #a feature from flask-sqlalchemy that allows us to grab things from the db using the primary key. 
                                          #if there is no key that matched, it will automatically abort
        return item
    
    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privelage required")

        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return{"message": "Item Deleted."}
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema) #response decorator
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()

        return item
        

@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True)) #handles a list
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        #Error Handling to make sure data exists and is in the correct format (now done in marshmallow)
        #Make sure you can't add the same data twice
        item = ItemModel(**item_data) #**turns dict into keyword arguements

        try: 
            db.session.add(item) #add items to d
            db.session.commit() #saves to db. ID gets generated here
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item