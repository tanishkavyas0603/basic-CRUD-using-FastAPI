from fastapi import FastAPI, Depends
from models import Product
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
database_models.Base.metadata.create_all(bind=engine)
# to display any message
@app.get("/")
def greet():
    return {"message": "Welcome Tanishka"}

#manually adding product
products = [
    Product(id=1, name="Phone", description="budget phone", price=99, quantity=10),
    Product(id=2, name="Laptop", description="gaming laptop", price=999, quantity=6),
    Product(id=6, name="Pen", description="dark blue pen", price=19.90, quantity=10),
    Product(id=4, name="Table", description="wooden table", price=199.99, quantity=6)
]

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db= SessionLocal()
    count=db.query(database_models.Product).count()
    if count==0:

        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
init_db()

# to fetch all products
@app.get("/products")
def get_all_products(db: Session=Depends(get_db)):
    db_products= db.query(database_models.Product).all()
    return db_products
    # db connection
    #db=SessionLocal()
    # query
    #db.query()
    #return products

#to fetch one product
@app.get("/product/{id}")
def get_all_products_by_id(id: int, db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product
    return "product not found"

# to append any product
@app.post("/products")
def add_product(product: Product,db:Session=Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

# to put:update any product
@app.put("/products/{id}")
def update_product(id: int, product: Product, db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        db_product.name=product.name
        db.commit()
        return "Product update"
    else:
        return "No product found"

#to delete any product
@app.delete("/products/{id}")
def delete_product(id: int, db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()

    else:
        return "Product not exists" 








