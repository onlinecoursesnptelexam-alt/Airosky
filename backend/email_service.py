import os
import smtplib
from email.message import EmailMessage

# =====================================================
# AIRO Institute - Email Service
# =====================================================

# Gmail SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Sender Email
EMAIL = "hashmikhan847@gmail.com"
PASSWORD = "rpkk kgxc mbzu tteu"

# Institute Email (to receive enrollment notifications)
INSTITUTE_EMAIL = "hashmikhan847@gmail.com"

# Project Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, "generated_pdfs")


def send_enrollment_email(
    student_name,
    student_email,
    enrollment_id,
    pdf_filename
):
    """
    Send Enrollment Confirmation Email with PDF Attachment.

    Args:
        student_name (str)
        student_email (str)
        enrollment_id (str)
        pdf_filename (str)
    """

    pdf_path = os.path.join(PDF_FOLDER, pdf_filename)

    if not os.path.exists(pdf_path):
        print(f"PDF not found: {pdf_path}")
        return False

    # Create Email
    msg = EmailMessage()

    msg["Subject"] = f"AIRO Institute | Enrollment Confirmation ({enrollment_id})"
    msg["From"] = EMAIL
    msg["To"] = student_email

    msg.set_content(f"""
Dear {student_name},

Greetings from AIRO Institute!

Congratulations!

Your enrollment has been completed successfully.

Enrollment ID:
{enrollment_id}

Please find your Enrollment PDF attached with this email.

Kindly keep this document safe, as it may be required for future verification and reference.

If you have any questions or need assistance, feel free to contact us.

We wish you success in your learning journey.

--------------------------------------------------

AIRO Institute

Website:
https://airoinstitute.in

Email:
support@airoinstitute.in

Thank you for choosing AIRO Institute.

--------------------------------------------------
""")

    # Attach PDF
    with open(pdf_path, "rb") as pdf:
        msg.add_attachment(
            pdf.read(),
            maintype="application",
            subtype="pdf",
            filename=pdf_filename
        )

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        print("======================================")
        print("Email sent successfully.")
        print("Student :", student_name)
        print("Email   :", student_email)
        print("PDF     :", pdf_filename)
        print("======================================")

        return True

    except Exception as e:
        print("======================================")
        print("Email sending failed.")
        print(e)
        print("======================================")

        return False


def send_institute_notification_email(
    student_name,
    student_email,
    enrollment_id,
    pdf_filename
):
    """
    Send notification email to institute about new enrollment.

    Args:
        student_name (str)
        student_email (str)
        enrollment_id (str)
        pdf_filename (str)
    """

    pdf_path = os.path.join(PDF_FOLDER, pdf_filename)

    if not os.path.exists(pdf_path):
        print(f"PDF not found: {pdf_path}")
        return False

    # Create Email
    msg = EmailMessage()

    msg["Subject"] = f"New Enrollment: {student_name} ({enrollment_id})"
    msg["From"] = EMAIL
    msg["To"] = INSTITUTE_EMAIL

    msg.set_content(f"""
Dear Institute Administration,

A new student has enrolled successfully.

Student Details:
----------------
Name: {student_name}
Email: {student_email}
Enrollment ID: {enrollment_id}

Please find the enrollment PDF attached with this email for your records.

--------------------------------------------------

AIRO Institute

--------------------------------------------------
""")

    # Attach PDF
    with open(pdf_path, "rb") as pdf:
        msg.add_attachment(
            pdf.read(),
            maintype="application",
            subtype="pdf",
            filename=pdf_filename
        )

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        print("======================================")
        print("Institute notification email sent successfully.")
        print("Student :", student_name)
        print("Email   :", student_email)
        print("PDF     :", pdf_filename)
        print("======================================")

        return True

    except Exception as e:
        print("======================================")
        print("Institute notification email sending failed.")
        print(e)
        print("======================================")

        return False


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    send_enrollment_email(
        student_name="Altaf Khan",
        student_email="im.altafkhan19@gmail.com",
        enrollment_id="AIRO-2026-000001",
        pdf_filename="AIRO-2026-000001.pdf"
    )