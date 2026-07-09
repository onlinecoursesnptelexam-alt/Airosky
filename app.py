from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Certificate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AEROSKY Certificate Verification"
)
BASE_URL = "https://aerosky-institute-vvot.onrender.com"
# ------------------------------------
# Enable CORS
# ------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://airoskyinstitute.com",
        "https://www.airoskyinstitute.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------
# Serve PDF Certificates
# ------------------------------------

app.mount(
    "/certificates",
    StaticFiles(directory="certificates"),
    name="certificates"
)

# ------------------------------------
# Home
# ------------------------------------

@app.get("/")
def home():

    return {
        "message":"AEROSKY API Running Successfully"
    }

# ------------------------------------
# Verify Certificate
# ------------------------------------

@app.get("/api/verify/{certificate_id}")

def verify_certificate(
    certificate_id:str,
    db:Session=Depends(get_db)
):

    certificate = (

        db.query(Certificate)

        .filter(
            Certificate.certificate_id==certificate_id
        )

        .first()

    )

    if certificate is None:

        raise HTTPException(
            status_code=404,
            detail="Certificate Not Found"
        )

    return {

        "certificate_id":certificate.certificate_id,

        "student_name":certificate.student_name,

        "father_name":certificate.father_name,

        "course":certificate.course,

        "duration":certificate.duration,

        "issue_date":certificate.issue_date,

        "status":certificate.status,

        "certificate_url":
        f"{BASE_URL}/certificates/{certificate.certificate}"


    }