import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
import io

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIC_SUPPORT = True
except ImportError:
    HEIC_SUPPORT = False
    print("Warning: pillow-heif not installed. HEIC images will not be supported.")

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# PDF folder
PDF_FOLDER = os.path.join(BASE_DIR, "generated_pdfs")
os.makedirs(PDF_FOLDER, exist_ok=True)

# Logo path
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")


def convert_heic_to_jpeg(heic_path):
    """
    Convert HEIC image to JPEG format for PDF compatibility.
    Returns the path to the converted JPEG file.
    """
    try:
        if not HEIC_SUPPORT:
            print("Error: HEIC support not available. Please install pillow-heif: pip install pillow-heif")
            return None
            
        # Open HEIC image using PIL (with pillow-heif registered)
        img = PILImage.open(heic_path)
        
        # Create JPEG path
        jpeg_path = heic_path.rsplit('.', 1)[0] + '.jpg'
        
        # Convert to RGB if necessary (HEIC might be in RGBA or other modes)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        # Save as JPEG
        img.save(jpeg_path, 'JPEG', quality=95)
        
        return jpeg_path
    except Exception as e:
        print(f"Error converting HEIC to JPEG: {e}")
        return None


def add_watermark(canvas, doc):
    """
    Add watermark logo to the center of the page with low opacity.
    """
    canvas.saveState()
    
    # Set opacity for watermark (very low like a watermark)
    canvas.setFillAlpha(0.1)
    canvas.setStrokeAlpha(0.1)
    
    # Get page dimensions
    page_width, page_height = doc.pagesize
    
    # Load and draw watermark in center
    if os.path.exists(LOGO_PATH):
        try:
            img = ImageReader(LOGO_PATH)
            img_width, img_height = img.getSize()
            
            # Scale watermark to be large but fit on page
            scale = min(page_width / img_width, page_height / img_height) * 0.5
            scaled_width = img_width * scale
            scaled_height = img_height * scale
            
            # Center the watermark
            x = (page_width - scaled_width) / 2
            y = (page_height - scaled_height) / 2
            
            canvas.drawImage(img, x, y, scaled_width, scaled_height, mask='auto')
        except Exception as e:
            print(f"Error loading watermark: {e}")
    
    canvas.restoreState()


def generate_pdf(student_name, date_of_birth, gender, nationality, father_name, mother_name, parent_mobile, email, age, photo_path=None, village=None, post_office=None, district=None, state=None, pincode=None, passport_photo_path=None, reg_number=None, mobile=None, contact_email=None, emergency_name=None, emergency_mobile=None, emergency_relation=None, qualification=None, board_college=None, passing_year=None, signature_path=None):
    """
    Generate a simple student enrollment PDF.
    """

    # Use registration number in filename if provided
    if reg_number:
        filename = f"{student_name.replace(' ', '_')}-{reg_number}.pdf"
    else:
        filename = f"{student_name.replace(' ', '_')}.pdf"
    pdf_path = os.path.join(PDF_FOLDER, filename)

    # Color scheme
    BACKGROUND_COLOR = colors.HexColor('#F8E7D0')
    YELLOW_HEADER = colors.HexColor('#F4B400')
    ORANGE = colors.HexColor('#F68B00')
    BLUE = colors.HexColor('#1B3C88')
    BORDER_COLOR = colors.HexColor('#D89B00')
    LABEL_BACKGROUND = colors.HexColor('#FFF2C6')
    VALUE_BACKGROUND = colors.HexColor('#FFF8EE')
    
    styles = getSampleStyleSheet()
    
    # Create custom styles for visual hierarchy
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=42,
        textColor=ORANGE,
        spaceAfter=2,
        alignment=1  # center
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=16,
        textColor=colors.black,
        spaceAfter=2,
        alignment=1  # center
    )
    
    form_title_style = ParagraphStyle(
        'FormTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=BLUE,
        spaceAfter=8,
        alignment=1  # center
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.black,
        spaceAfter=0,
        spaceBefore=0,
        alignment=0  # left
    )
    
    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.black,
        alignment=0
    )
    
    value_style = ParagraphStyle(
        'Value',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=colors.black,
        alignment=0
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=16,
        textColor=colors.black,
        alignment=0,
        leading=20
    )
    
    declaration_heading_style = ParagraphStyle(
        'DeclarationHeading',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.black,
        spaceAfter=8,
        alignment=0
    )
    
    # Create document with 10mm margins
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=(794, 1123),
        leftMargin=28,
        rightMargin=28,
        topMargin=28,
        bottomMargin=28
    )

    elements = []

    # HEADER - Logo top left, centered text
    # Use a 2-column table to position logo and text
    header_row = []
    
    # Column 1: Logo on left
    if os.path.exists(LOGO_PATH):
        try:
            logo = Image(LOGO_PATH, width=75, height=75)
            header_row.append(logo)
        except Exception as e:
            print(f"Error loading logo: {e}")
            header_row.append("")
    else:
        header_row.append("")
    
    # Column 2: Centered institute name
    institute_text = Paragraph("AiRosKy Institute of Fire and Safety Excellence", form_title_style)
    header_row.append(institute_text)
    
    # Create header table with 2 columns
    header_table = Table([header_row], colWidths=[100, 638])
    header_table.setStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    elements.append(header_table)
    elements.append(Spacer(1, 8))

    # SECTION 1: Student Personal Details
    # Yellow title bar - 28px height
    section1_title_data = [["1. Student Personal Details"]]
    section1_title_table = Table(section1_title_data, colWidths=[738], rowHeights=[28])
    section1_title_table.setStyle([
        ('BACKGROUND', (0, 0), (-1, -1), YELLOW_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 20),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ])
    elements.append(section1_title_table)
    
    # Add student photo
    photo_cell = ""
    if photo_path and os.path.exists(photo_path):
        try:
            # Convert HEIC to JPEG if needed
            if photo_path.lower().endswith('.heic'):
                photo_path = convert_heic_to_jpeg(photo_path)
            if photo_path:
                student_photo = Image(photo_path, width=100, height=120)
                photo_cell = student_photo
        except Exception as e:
            print(f"Error loading student photo: {e}")
    
    # Three-column table (labels, values, photo)
    # Photo spans all rows in the right column
    table_data = [
        [Paragraph("Full Name", label_style), Paragraph(student_name or "Not Provided", value_style), photo_cell],
        [Paragraph("Date of Birth", label_style), Paragraph(date_of_birth or "Not Provided", value_style), ""],
        [Paragraph("Gender", label_style), Paragraph(gender or "Not Provided", value_style), ""],
        [Paragraph("Nationality", label_style), Paragraph(nationality or "Not Provided", value_style), ""]
    ]
    
    table = Table(table_data, colWidths=[0.30*738, 0.40*738, 0.30*738], rowHeights=[34, 34, 34, 34])
    table.setStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('BACKGROUND', (0, 0), (0, -1), LABEL_BACKGROUND),
        ('BACKGROUND', (1, 0), (1, -1), VALUE_BACKGROUND),
        ('BACKGROUND', (2, 0), (2, -1), VALUE_BACKGROUND),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('SPAN', (2, 0), (2, 3)),  # Span photo column across all 4 rows
    ])
    
    elements.append(table)
    elements.append(Spacer(1, 8))

    # SECTION 2: Two columns - Address on left, Contact Details on right
    # LEFT COLUMN: Address
    address_title_data = [["2. Address of Student"]]
    address_title_table = Table(address_title_data, colWidths=[0.50*738], rowHeights=[28])
    address_title_table.setStyle([
        ('BACKGROUND', (0, 0), (-1, -1), YELLOW_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 20),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ])
    
    address_data = [
        [Paragraph("Village", label_style), Paragraph(village or "Not Provided", value_style)],
        [Paragraph("Post Office", label_style), Paragraph(post_office or "Not Provided", value_style)],
        [Paragraph("District", label_style), Paragraph(district or "Not Provided", value_style)],
        [Paragraph("State", label_style), Paragraph(state or "Not Provided", value_style)],
        [Paragraph("Pincode", label_style), Paragraph(pincode or "Not Provided", value_style)]
    ]
    
    address_table = Table(address_data, colWidths=[0.50*738*0.4, 0.50*738*0.6], rowHeights=[34]*5)
    address_table.setStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('BACKGROUND', (0, 0), (0, -1), LABEL_BACKGROUND),
        ('BACKGROUND', (1, 0), (1, -1), VALUE_BACKGROUND),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ])
    
    # RIGHT COLUMN: Contact Details
    contact_title_data = [["Contact Details"]]
    contact_title_table = Table(contact_title_data, colWidths=[0.50*738], rowHeights=[28])
    contact_title_table.setStyle([
        ('BACKGROUND', (0, 0), (-1, -1), YELLOW_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 20),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ])
    
    contact_data = [
        [Paragraph("Mobile Number", label_style), Paragraph(mobile or "Not Provided", value_style)],
        [Paragraph("Email ID", label_style), Paragraph(contact_email or "Not Provided", value_style)]
    ]
    
    contact_table = Table(contact_data, colWidths=[0.50*738*0.4, 0.50*738*0.6], rowHeights=[34]*2)
    contact_table.setStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('BACKGROUND', (0, 0), (0, -1), LABEL_BACKGROUND),
        ('BACKGROUND', (1, 0), (1, -1), VALUE_BACKGROUND),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ])
    
    # Create a 2-column table for titles
    section2_titles = Table([[address_title_table, contact_title_table]], colWidths=[0.50*738, 0.50*738])
    section2_titles.setStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ])
    elements.append(section2_titles)
    
    # Create a 2-column table for content
    section2_content = Table([[address_table, contact_table]], colWidths=[0.50*738, 0.50*738])
    section2_content.setStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ])
    elements.append(section2_content)
    elements.append(Spacer(1, 8))

    # SECTION 4: Parents Details
    section4_title_data = [["4. Parents Details"]]
    section4_title_table = Table(section4_title_data, colWidths=[738], rowHeights=[28])
    section4_title_table.setStyle([
        ('BACKGROUND', (0, 0), (-1, -1), YELLOW_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 20),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ])
    elements.append(section4_title_table)
    
    parents_data = [
        [Paragraph("Father Name", label_style), Paragraph(father_name or "Not Provided", value_style)],
        [Paragraph("Mother Name", label_style), Paragraph(mother_name or "Not Provided", value_style)],
        [Paragraph("Parent Mobile Number", label_style), Paragraph(parent_mobile or "Not Provided", value_style)]
    ]
    
    parents_table = Table(parents_data, colWidths=[0.40*738, 0.60*738], rowHeights=[34]*3)
    parents_table.setStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('BACKGROUND', (0, 0), (0, -1), LABEL_BACKGROUND),
        ('BACKGROUND', (1, 0), (1, -1), VALUE_BACKGROUND),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ])
    
    elements.append(parents_table)
    elements.append(Spacer(1, 8))

    # SECTION 5 & 6: Simplified - add elements sequentially to avoid nested table errors
    # LEFT: Emergency Contact
    emergency_title_data = [["Emergency Contact"]]
    emergency_title_table = Table(emergency_title_data, colWidths=[738], rowHeights=[28])
    emergency_title_table.setStyle([
        ('BACKGROUND', (0, 0), (-1, -1), YELLOW_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 20),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ])
    elements.append(emergency_title_table)
    
    emergency_data = [
        [Paragraph("Name", label_style), Paragraph(emergency_name or "Not Provided", value_style)],
        [Paragraph("Mobile Number", label_style), Paragraph(emergency_mobile or "Not Provided", value_style)],
        [Paragraph("Relation With Student", label_style), Paragraph(emergency_relation or "Not Provided", value_style)]
    ]
    
    emergency_table = Table(emergency_data, colWidths=[0.40*738, 0.60*738], rowHeights=[34]*3)
    emergency_table.setStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('BACKGROUND', (0, 0), (0, -1), LABEL_BACKGROUND),
        ('BACKGROUND', (1, 0), (1, -1), VALUE_BACKGROUND),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ])
    elements.append(emergency_table)
    elements.append(Spacer(1, 8))
    
    # RIGHT: Qualification Details
    qualification_title_data = [["Qualification Details"]]
    qualification_title_table = Table(qualification_title_data, colWidths=[738], rowHeights=[28])
    qualification_title_table.setStyle([
        ('BACKGROUND', (0, 0), (-1, -1), YELLOW_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 20),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ])
    elements.append(qualification_title_table)
    
    qualification_data = [
        [Paragraph("Qualification", label_style), Paragraph("Board / College", label_style), Paragraph("Passing Year", label_style)],
        [Paragraph(qualification or "Not Provided", value_style), Paragraph(board_college or "Not Provided", value_style), Paragraph(passing_year or "Not Provided", value_style)]
    ]
    
    qualification_table = Table(qualification_data, colWidths=[0.33*738, 0.33*738, 0.34*738], rowHeights=[34, 34])
    qualification_table.setStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('BACKGROUND', (0, 0), (-1, 0), YELLOW_HEADER),
        ('BACKGROUND', (0, 1), (-1, 1), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ])
    elements.append(qualification_table)
    elements.append(Spacer(1, 8))

    # DECLARATION
    declaration_heading = Paragraph("Declaration", declaration_heading_style)
    elements.append(declaration_heading)
    elements.append(Spacer(1, 8))

    declaration_text = Paragraph(
        "I hereby declare that the information provided above is true and correct to the best of my knowledge.",
        normal_style
    )
    elements.append(declaration_text)
    elements.append(Spacer(1, 8))

    # BOTTOM AREA: Signature + Date boxes side by side
    # LEFT: Signature Box - 300x65px
    if signature_path and os.path.exists(signature_path):
        try:
            # Convert HEIC to JPEG if needed
            if signature_path.lower().endswith('.heic'):
                signature_path = convert_heic_to_jpeg(signature_path)
            if signature_path:
                signature_img = Image(signature_path, width=300, height=65)
                signature_box = signature_img
            else:
                signature_box = Paragraph("Student Signature", normal_style)
        except Exception as e:
            print(f"Error loading signature: {e}")
            signature_box = Paragraph("Student Signature", normal_style)
    else:
        signature_box = Paragraph("Student Signature", normal_style)
    
    signature_table = Table([[signature_box]], colWidths=[300], rowHeights=[65])
    signature_table.setStyle([
        ('GRID', (0, 0), (-1, -1), 1, ORANGE),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    
    # RIGHT: Date Box - 230x45px
    current_date = datetime.now().strftime("%d-%m-%Y")
    date_box = Paragraph(f"Date: {current_date}", normal_style)
    
    date_table = Table([[date_box]], colWidths=[230], rowHeights=[45])
    date_table.setStyle([
        ('GRID', (0, 0), (-1, -1), 1, ORANGE),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ])
    
    # Create 2-column table for signature and date side by side with space
    bottom_table = Table([[signature_table, "", date_table]], colWidths=[300, 50, 230])
    bottom_table.setStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
    ])
    elements.append(bottom_table)
    
    # Add signature label below
    signature_label = Paragraph("Student Signature", ParagraphStyle(
        'SignatureLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.gray,
        alignment=1
    ))
    elements.append(signature_label)

    doc.build(elements, onFirstPage=add_watermark, onLaterPages=add_watermark)

    return filename