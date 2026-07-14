from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import shutil
from datetime import datetime
from sqlalchemy.orm import Session

from pdf_generator import generate_pdf
from email_service import send_enrollment_email, send_institute_notification_email
from database import Base, engine, get_db
from models import Certificate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AEROSKY Institute API"
)

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Upload folder for photos
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# PDF folder
PDF_FOLDER = os.path.join(BASE_DIR, "generated_pdfs")
os.makedirs(PDF_FOLDER, exist_ok=True)

# Counter file for registration numbers
COUNTER_FILE = os.path.join(BASE_DIR, "registration_counter.txt")

# Base URL for certificate verification
BASE_URL = "https://aerosky-institute-vvot.onrender.com"


def generate_registration_number():
    """
    Generate registration number in format: AIR-DDMMYY-XXXXX
    Example: AIR-011226-00001
    """
    # Get current date in DDMMYY format
    current_date = datetime.now().strftime("%d%m%y")
    
    # Read or initialize counter
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            counter = int(f.read().strip())
    else:
        counter = 0
    
    # Increment counter
    counter += 1
    
    # Save counter back to file
    with open(COUNTER_FILE, "w") as f:
        f.write(str(counter))
    
    # Format counter as 5-digit number with leading zeros
    counter_str = f"{counter:05d}"
    
    # Generate registration number
    reg_number = f"AIR-{current_date}-{counter_str}"
    
    return reg_number

# Enable CORS
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

# Serve PDF Certificates
app.mount(
    "/certificates",
    StaticFiles(directory="certificates"),
    name="certificates"
)


class Student(BaseModel):
    student_name: str
    father_name: str
    email: str
    age: int


@app.get("/")
def home():
    return {"message": "AEROSKY API Running Successfully"}


@app.post("/submit")
def submit(
    background_tasks: BackgroundTasks,
    student_name: str = Form(...),
    date_of_birth: str = Form(...),
    gender: str = Form(...),
    nationality: str = Form(...),
    father_name: str = Form(...),
    mother_name: str = Form(...),
    parent_mobile: str = Form(...),
    email: str = Form(...),
    age: int = Form(...),
    photo: UploadFile = File(...),
    village: str = Form(...),
    post_office: str = Form(...),
    district: str = Form(...),
    state: str = Form(...),
    pincode: str = Form(...),
    passport_photo: UploadFile = File(None),
    mobile: str = Form(...),
    contact_email: str = Form(...),
    emergency_name: str = Form(...),
    emergency_mobile: str = Form(...),
    emergency_relation: str = Form(...),
    qualification: str = Form(...),
    board_college: str = Form(...),
    passing_year: str = Form(...),
    signature: UploadFile = File(None)
):

    try:
        # Generate automatic registration number
        reg_number = generate_registration_number()

        # Save uploaded photo
        photo_extension = photo.filename.split('.')[-1]
        photo_filename = f"{student_name.replace(' ', '_')}_photo.{photo_extension}"
        photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)

        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        # Save passport photo if provided
        passport_photo_path = None
        if passport_photo:
            passport_extension = passport_photo.filename.split('.')[-1]
            passport_filename = f"{student_name.replace(' ', '_')}_passport.{passport_extension}"
            passport_photo_path = os.path.join(UPLOAD_FOLDER, passport_filename)

            with open(passport_photo_path, "wb") as buffer:
                shutil.copyfileobj(passport_photo.file, buffer)

        # Save signature if provided
        signature_path = None
        if signature:
            signature_extension = signature.filename.split('.')[-1]
            signature_filename = f"{student_name.replace(' ', '_')}_signature.{signature_extension}"
            signature_path = os.path.join(UPLOAD_FOLDER, signature_filename)

            with open(signature_path, "wb") as buffer:
                shutil.copyfileobj(signature.file, buffer)

        # Generate PDF with new naming convention: STUDENTNAME-AIR-DDMMYY-XXXXX
        pdf_name = generate_pdf(
            student_name,
            date_of_birth,
            gender,
            nationality,
            father_name,
            mother_name,
            parent_mobile,
            email,
            age,
            photo_path,
            village,
            post_office,
            district,
            state,
            pincode,
            passport_photo_path,
            reg_number,
            mobile,
            contact_email,
            emergency_name,
            emergency_mobile,
            emergency_relation,
            qualification,
            board_college,
            passing_year,
            signature_path
        )

        # Rename PDF to new format: STUDENTNAME-AIR-DDMMYY-XXXXX
        old_pdf_path = os.path.join(BASE_DIR, "generated_pdfs", pdf_name)
        new_pdf_name = f"{student_name.replace(' ', '_')}-{reg_number}.pdf"
        new_pdf_path = os.path.join(BASE_DIR, "generated_pdfs", new_pdf_name)

        if os.path.exists(old_pdf_path):
            os.rename(old_pdf_path, new_pdf_path)

        # Send emails in background - don't wait for them to complete
        def send_emails():
            try:
                send_enrollment_email(
                    student_name=student_name,
                    student_email=email,
                    enrollment_id=reg_number,
                    pdf_filename=new_pdf_name
                )
                send_institute_notification_email(
                    student_name=student_name,
                    student_email=email,
                    enrollment_id=reg_number,
                    pdf_filename=new_pdf_name
                )
            except Exception as e:
                print(f"Error sending emails: {e}")

        background_tasks.add_task(send_emails)

        # Return immediately with registration ID after PDF generation
        return {
            "status": "success",
            "message": "PDF Generated Successfully",
            "pdf": new_pdf_name,
            "registration_number": reg_number
        }

    except Exception as e:

        print("ERROR:", e)

        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/download-pdf/{pdf_filename}")
def download_pdf(pdf_filename: str):
    """
    Download PDF by filename
    """
    pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
    
    if not os.path.exists(pdf_path):
        return {"status": "error", "message": "PDF not found"}
    
    return FileResponse(
        path=pdf_path,
        filename=pdf_filename,
        media_type="application/pdf"
    )


# ------------------------------------
# Verify Certificate
# ------------------------------------

@app.get("/api/verify/{certificate_id}")
def verify_certificate(
    certificate_id: str,
    db: Session = Depends(get_db)
):
    certificate = (
        db.query(Certificate)
        .filter(
            Certificate.certificate_id == certificate_id
        )
        .first()
    )

    if certificate is None:
        raise HTTPException(
            status_code=404,
            detail="Certificate Not Found"
        )

    return {
        "certificate_id": certificate.certificate_id,
        "student_name": certificate.student_name,
        "father_name": certificate.father_name,
        "course": certificate.course,
        "duration": certificate.duration,
        "issue_date": certificate.issue_date,
        "status": certificate.status,
        "certificate_url": f"{BASE_URL}/certificates/{certificate.certificate}"
    }


# ------------------------------------
# Add Certificate (Admin)
# ------------------------------------

@app.post("/api/admin/add-certificate")
def add_certificate(
    certificate_id: str = Form(...),
    student_name: str = Form(...),
    father_name: str = Form(...),
    course: str = Form(...),
    duration: str = Form(...),
    issue_date: str = Form(...),
    status: str = Form("Valid"),
    certificate: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if certificate already exists
    existing = db.query(Certificate).filter(
        Certificate.certificate_id == certificate_id
    ).first()
    
    if existing:
        return {"status": "error", "message": "Certificate ID already exists"}
    
    # Create new certificate
    new_certificate = Certificate(
        certificate_id=certificate_id,
        student_name=student_name,
        father_name=father_name,
        course=course,
        duration=duration,
        issue_date=issue_date,
        status=status,
        certificate=certificate
    )
    
    db.add(new_certificate)
    db.commit()
    db.refresh(new_certificate)
    
    return {
        "status": "success",
        "message": "Certificate added successfully",
        "certificate": {
            "certificate_id": new_certificate.certificate_id,
            "student_name": new_certificate.student_name
        }
    }


# ------------------------------------
# List All Certificates (Admin)
# ------------------------------------

@app.get("/api/admin/certificates")
def list_certificates(db: Session = Depends(get_db)):
    certificates = db.query(Certificate).all()
    return {
        "certificates": [
            {
                "certificate_id": cert.certificate_id,
                "student_name": cert.student_name,
                "course": cert.course,
                "status": cert.status,
                "issue_date": cert.issue_date
            }
            for cert in certificates
        ]
    }