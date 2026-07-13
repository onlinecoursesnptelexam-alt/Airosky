from sqlalchemy import Column, Integer, String
from database import Base


class Certificate(Base):

    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)

    certificate_id = Column(String(50), unique=True, nullable=False)

    student_name = Column(String(100), nullable=False)

    father_name = Column(String(100))

    course = Column(String(200))

    duration = Column(String(50))

    issue_date = Column(String(50))

    status = Column(String(20))

    certificate = Column(String(255))