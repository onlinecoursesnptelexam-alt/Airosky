import os
import base64
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# AIRO Institute - Email Service
# =====================================================

# Email Configuration - Use SendGrid for Render compatibility
# Get SendGrid API key from environment variables
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "hashmikhan847@gmail.com")
INSTITUTE_EMAIL = os.getenv("INSTITUTE_EMAIL", "hashmikhan847@gmail.com")

# Fallback to SMTP if SendGrid not configured (for local development)
USE_SENDGRID = bool(SENDGRID_API_KEY)

if not USE_SENDGRID:
    import smtplib
    from email.message import EmailMessage
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL = os.getenv("EMAIL", "hashmikhan847@gmail.com")
    PASSWORD = os.getenv("EMAIL_PASSWORD", "rpkk kgxc mbzu tteu")

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

    # Use SendGrid if API key is available (Render compatible)
    if USE_SENDGRID:
        try:
            import sendgrid
            from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

            sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

            # Read PDF file
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
                pdf_base64 = base64.b64encode(pdf_data).decode()

            # Create email
            message = Mail(
                from_email=SENDER_EMAIL,
                to_emails=student_email,
                subject=f"AIRO Institute | Enrollment Confirmation ({enrollment_id})",
                html_content=f"""
                <h2>Dear {student_name},</h2>
                <p>Greetings from AIRO Institute!</p>
                <p><strong>Congratulations!</strong></p>
                <p>Your enrollment has been completed successfully.</p>
                <h3>Enrollment ID: {enrollment_id}</h3>
                <p>Please find your Enrollment PDF attached with this email.</p>
                <p>Kindly keep this document safe, as it may be required for future verification and reference.</p>
                <p>If you have any questions or need assistance, feel free to contact us.</p>
                <p>We wish you success in your learning journey.</p>
                <hr>
                <p><strong>AIRO Institute</strong></p>
                <p>Website: https://airoinstitute.in</p>
                <p>Email: support@airoinstitute.in</p>
                <p>Thank you for choosing AIRO Institute.</p>
                """
            )

            # Attach PDF
            attachment = Attachment(
                FileContent(pdf_base64),
                FileName(pdf_filename),
                FileType('application/pdf'),
                Disposition('attachment')
            )
            message.add_attachment(attachment)

            response = sg.send(message)

            print("======================================")
            print("SendGrid Email sent successfully.")
            print("Student :", student_name)
            print("Email   :", student_email)
            print("PDF     :", pdf_filename)
            print("======================================")

            return True

        except Exception as e:
            print("======================================")
            print("SendGrid Email sending failed.")
            print(e)
            print("======================================")
            return False

    # Fallback to SMTP for local development
    else:
        try:
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

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL, PASSWORD)
                server.send_message(msg)

            print("======================================")
            print("SMTP Email sent successfully.")
            print("Student :", student_name)
            print("Email   :", student_email)
            print("PDF     :", pdf_filename)
            print("======================================")

            return True

        except Exception as e:
            print("======================================")
            print("SMTP Email sending failed.")
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

    # Use SendGrid if API key is available (Render compatible)
    if USE_SENDGRID:
        try:
            import sendgrid
            from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

            sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

            # Read PDF file
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
                pdf_base64 = base64.b64encode(pdf_data).decode()

            # Create email
            message = Mail(
                from_email=SENDER_EMAIL,
                to_emails=INSTITUTE_EMAIL,
                subject=f"New Enrollment: {student_name} ({enrollment_id})",
                html_content=f"""
                <h2>Dear Institute Administration,</h2>
                <p>A new student has enrolled successfully.</p>
                <h3>Student Details:</h3>
                <p><strong>Name:</strong> {student_name}</p>
                <p><strong>Email:</strong> {student_email}</p>
                <p><strong>Enrollment ID:</strong> {enrollment_id}</p>
                <p>Please find the enrollment PDF attached with this email for your records.</p>
                <hr>
                <p><strong>AIRO Institute</strong></p>
                """
            )

            # Attach PDF
            attachment = Attachment(
                FileContent(pdf_base64),
                FileName(pdf_filename),
                FileType('application/pdf'),
                Disposition('attachment')
            )
            message.add_attachment(attachment)

            response = sg.send(message)

            print("======================================")
            print("SendGrid Institute notification email sent successfully.")
            print("Student :", student_name)
            print("Email   :", student_email)
            print("PDF     :", pdf_filename)
            print("======================================")

            return True

        except Exception as e:
            print("======================================")
            print("SendGrid Institute notification email sending failed.")
            print(e)
            print("======================================")
            return False

    # Fallback to SMTP for local development
    else:
        try:
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

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL, PASSWORD)
                server.send_message(msg)

            print("======================================")
            print("SMTP Institute notification email sent successfully.")
            print("Student :", student_name)
            print("Email   :", student_email)
            print("PDF     :", pdf_filename)
            print("======================================")

            return True

        except Exception as e:
            print("======================================")
            print("SMTP Institute notification email sending failed.")
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