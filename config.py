import os 


class Config:
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
    SQLALCEHMY_DATABASE_URI=os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS= False


# FLASK JWT EXTENDED

JWT_SECRET_KEY='kittycakes'
JWT_TOKEN_LOCATION=["headers"]