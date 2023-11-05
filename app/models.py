from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4 
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy

class User(db.Model): 
    id = db.Column(db.String(64), primary_key = True)
    created_at = db.Column(db.DateTime(), default = datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default = datetime.utcnow, onupdate = datetime.utcnow)
    username= db.Column(db.String(25), unqiue = True, nullable = False)
    password = db.Column(db.String(256), nullable = False)
    products = db.relationship("Product", backref= "created_by")


    def __init__(self, username, password): 
        self.id = str(uuid4())
        self.username = username 
        self.password = generate_password_hash(password)

    def compare_password(self, password): 
        return check_password_hash(self.password, password)
    
    def create(self): 
        db.session.add(self)
        db.session.commit()

    def delete(self): 
        db.session.delete(self)

    def update(self, **kwargs):
        for key, value in kwargs.items(): 
            if key == "password": 
                setattr(self, key , generate_password_hash(value))
            else: 
                setattr(self,key,value)
            db.session.commit() 

    def to_response(self):
        return { 
            "id": self.id, 
            "created_at": self.created_at,
            "updated_at": self.updated_at, 
            "username": self.username, 
            "products": [product.to_response() for product in self.products ]
            
        }
    
class Product(db.Model): 
    id = db.Column(db.String(64), primary_key= True)
    created_at = db.Column(db.DateTime(), default = datetime.utcnow)
    updated_at= db.Column(db.DateTime(), default = datetime.utcnow, onupdate= datetime.utcnow)
    name = db.Column (db.String(64), unique = True, nullable = False)
    description= db.Column(db.Text)
    price = db.Column(db.Numeric(8,2), nullable = False )
    created_by = db.Column(db.String(64), db.ForeignKey("user.id"), nullable= False)

    receipts= db.relationship("Receipt", backref="Product")

    def __init__(self,name,description,price,created_by):
        self.id = str(uuid4())
        self.name = name
        self.description = description
        self.price = price
        self.created_by = created_by

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self): 
        db.session.add(self)
        db.session.commit()

    def update(self,**kwargs): 
        for key, value in kwargs.items(): 
            setattr(self, key , value)
        db.session.commit()

    def to_response(self): 
         return{
            "id": self.id, 
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "name": self.name, 
            "description": self.description, 
            "price": self.price,
            "created_by": self.created_by.username
            }
        

class Receipt(db.Model): 
    id = db.Column(db.String(64), primary_key= True)
    created_at=db.Column(db.DateTime(), default = datetime.utcnow)
    updated_at= db.Column(db.DateTime(), default = datetime.utcnow, onupdate=datetime.utcnow)
    product_price =db.Column(db.Integer, db.ForeignKey("product.price"), nullable=False)
    product_name = db.Column(db.String(64), db.ForeignKey("product.name"), nullable= False)

    def __init__(self,product_price,product_name): 
        self.id = (str(uuid4()))
        self.product_price= product_price
        self.product_name= product_name

    def create(self): 
        db.session.add(self)
        db.session.commit()

    def delete(self): 
        db.session.delete(self)

    def update(self,**kwargs):
        for key, value in kwargs.items():
            setattr(self,key,value)
        db.session.commit()


    def to_reponse(self):
        return{
            "id": self.id, 
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "product_price": self.product_price, 
            "product_name": self.product_name, 
            "reciepts": [receipt.to_response() for receipt in self.receipts]
            }


