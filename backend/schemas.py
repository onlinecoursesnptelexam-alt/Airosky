from pydantic import BaseModel

class CertificateResponse(BaseModel):

    certificate_id:str

    student_name:str

    father_name:str

    course:str

    duration:str

    issue_date:str

    status:str

    certificate:str

    class Config:

        from_attributes=True