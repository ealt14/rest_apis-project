from db import db

class ItemModel(db.Model):
    __tablename__ = "items" #tells sqlalchemy that we want to use a table called 'items' for all entries in this class

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
        #ForeignKey tells the db that store_id in Items is the SAME as ID in Stores
        #big benefit is that you wont be able to create an item with a storeId if that storeID is NOT in the stores table
    store = db.relationship("StoreModel", back_populates="items") #lnks this store object to the StoreModel Object with the same store ID
    tags = db.relationship("TagModel", back_populates="items", secondary = "items_tags")