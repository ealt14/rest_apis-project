from db import db

class StoreModel(db.Model):
    __tablename__ = "stores" #tells sqlalchemy that we want to use a table called 'stores' for all entries in this class

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete") #cascade will delete child records (items) if parent store is deleted
        #lnks this items object to the ItemModel Object with the same itemID
        #lazy=dynamic means it won't fetch items from the db until we tell it to (won't do it pre-emptively)
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")