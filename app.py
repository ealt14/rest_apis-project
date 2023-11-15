import os, secrets

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from blocklist import BLOCKLIST
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None): #puts everything into a function so we can call it when needed
    app= Flask(__name__)

    #register the blueprint with the API

    #Configuration Options
    ##propagate exceptions: if there is an exception that occurs that is hidden inside an extension of flask, 
        ##propagate it into the main app so we can see it
    app.config["PROPAGATE_EXCEPTIONS"]=True
    app.config["API_TITLE"] = "Stores REST API" #API Title
    app.config["API_VERSION"] = "v1" #version we are working on
    app.config["OPENAPI_VERSION"] = "3.0.3" #documentation version from OpenAPI
    app.config["OPENAPI_URL_PREFIX"] = "/" #tells API to start in the route of the directory tree
    #use swagger
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" #where to load swagger code from
    #if db_url exists, use it. If not, use the sqlite connection string and environment variable
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db") #define database url connection string with an environment variable
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #slows down sqlalchemy which we don't want so we set it to False
    db.init_app(app) #initializes the flask-sqlalchemy extension and connect our app to sqlalchemy
    migrate = Migrate(app, db)
    api = Api(app) #connects app to flask_smorest extension

    app.config["JWT_SECRET_KEY"] = "jose" #creates the secret key to sign the JWT
    #secrets.SystemRandom().getrandbits(128) will generate a secret key for you. best practice is to create and store in env variable. 
    ##for now, we will hard code something simple
    jwt = JWTManager(app) #create instance of JWT manager

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"description": "The token has been revoked", "error": "token_revoked"}
            ),
            401
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {
                    "description": "the token is not fresh.",
                    "error": "fresh_token_required"
                }
            ), 401
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401)
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify(
                {"description": "Request does not contain an access token.",
                 "error": "authorization_required"}
            ),
            401
        )

    #creates all tables in our database. will only run if tables do NOT exist
    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app