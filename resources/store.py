import uuid
from flask import request, abort
from flask.views import MethodView
from flask_smorest import Blueprint

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commiit()
        return {"message":"store deleted."}

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True)) #change to handle a list
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data) #**turns dict into keyword arguements

        try: 
            db.session.add(store) #add items to d
            db.session.commit() #saves to db. ID gets generated here
        except IntegrityError: #error when causing an inconsistency in the data (i.e. violate  a constraing defined in the model)
            abort(400, message='A store with that name already exists')
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store.")
        
        return store
