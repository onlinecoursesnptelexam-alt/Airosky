import os
import base64
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# AIRO Institute - Email Service
# =====================================================

# Email Configuration - SendGrid only
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDER_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "info@airoskyinstitute.com")
INSTITUTE_EMAIL = os.getenv("INSTITUTE_EMAIL", "info@airoskyinstitute.com")

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

    if not SENDGRID_API_KEY or SENDGRID_API_KEY == "your_sendgrid_api_key_here":
        print("SendGrid API key is not configured or is still set to placeholder.")
        print("Please set SENDGRID_API_KEY in .env file with your actual SendGrid API key.")
        return False

    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
            pdf_base64 = base64.b64encode(pdf_data).decode()

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

        attachment = Attachment(
            FileContent(pdf_base64),
            FileName(pdf_filename),
            FileType('application/pdf'),
            Disposition('attachment')
        )
        message.add_attachment(attachment)

        sg.send(message)

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

    if not SENDGRID_API_KEY or SENDGRID_API_KEY == "your_sendgrid_api_key_here":
        print("SendGrid API key is not configured or is still set to placeholder.")
        print("Please set SENDGRID_API_KEY in .env file with your actual SendGrid API key.")
        return False

    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
            pdf_base64 = base64.b64encode(pdf_data).decode()

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

        attachment = Attachment(
            FileContent(pdf_base64),
            FileName(pdf_filename),
            FileType('application/pdf'),
            Disposition('attachment')
        )
        message.add_attachment(attachment)

        sg.send(message)

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