from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from models import User, Item
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class ItemBase(BaseModel):
    userId: int
    itemName: str
    itemDescription: str
    itemQuantity: int

class ItemModel(ItemBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    firstName: str
    lastName: str
    username: str
    password: str

class UserModel(UserBase):
    id: int

    class Config:
        orm_mode = True


#auth setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#JWT secret and algorithm
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_db():
    db = SessionLocal()
    try:
        yield  db
    finally:
        db.close()

#db setup
db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)

#helper functions


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserBase):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(firstName=user.firstName, lastName=user.lastName, username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    return "complete"

#API posts/gets

#creates an item
@app.post("/items/", response_model=ItemModel)
async def create_item(item: ItemBase, db: db_dependency):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#returns all items for a given user (based on user id)
@app.get("/user_items/", response_model=List[ItemModel])
async def read_user_items(db: db_dependency, userId):
    all_items = db.query(models.Item).all()
    user_items = []
    for item in all_items:
        if (item.userId == int(userId)):
            user_items.append(item)
    return user_items

#returns all items (assumes <100 items in db)
@app.get("/items/", response_model=List[ItemModel])
async def read_items(db: db_dependency, skip: int = 0, limit: int = 100):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items

#creates a user -- deprecated. adds a user to the database
""" @app.post("/users/", response_model=UserModel)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user """

#returns all users
@app.get("/users/", response_model=List[UserModel])
async def read_users(db: db_dependency, skip: int = 0, limit: int = 100):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

#register a user
@app.post("/register/")
def register_user(user: UserBase, db: db_dependency):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)

#Authenticate user
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

#create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.now(datetime.UTC) + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token/")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")

@app.get("/verify-token/{token}")
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message": "Token is valid"}