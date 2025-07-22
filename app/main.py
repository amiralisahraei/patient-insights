from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pymongo import MongoClient
from starlette_graphene3 import GraphQLApp
from app.graphql_schema import schema
import os
from app.models import SessionLocal, Patient, Base, engine
from contextlib import asynccontextmanager
from pydantic import BaseModel

# JWT config
SECRET_KEY = "your_secret_key" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user
fake_user = {
    "username": "admin",
    "hashed_password": pwd_context.hash("password123")  
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    if username != fake_user["username"]:
        return False
    if not verify_password(password, fake_user["hashed_password"]):
        return False
    return {"username": username}

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"username": username}

# Pydantic for token response
class Token(BaseModel):
    access_token: str
    token_type: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

db_session = SessionLocal()
mongo_client = MongoClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
mongo_db = mongo_client["patients_db"]
reports = mongo_db["reports"]

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected endpoints
@app.get("/patients", dependencies=[Depends(get_current_user)])
def get_patients():
    return db_session.query(Patient).all()

@app.get("/patients/{patient_id}", dependencies=[Depends(get_current_user)])
def get_patient(patient_id: int):
    patient = db_session.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.get("/patients/{patient_id}/report", dependencies=[Depends(get_current_user)])
def get_patient_report(patient_id: int):
    report = reports.find_one({"patient_id": patient_id})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"summary": report["summary"]}

@app.get("/metrics", dependencies=[Depends(get_current_user)])
def metrics():
    return {"api_status": "healthy", "total_patients": db_session.query(Patient).count()}

app.add_route("/graphql", GraphQLApp(schema=schema))
