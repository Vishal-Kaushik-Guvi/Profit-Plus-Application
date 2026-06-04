from fastapi import FastAPI
from app.core.database import engine, Base

# Import ALL models
from app.models import user
from app.models import business
from app.models import customer
from app.models import supplier
from app.models import product
from app.models import inventory
from app.models import purchase
from app.models import sales
from app.models import emipayment
from app.models import referral

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Profit Plus API",
    description="SaaS backend for local business management",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Profit Plus API is running 🚀"}