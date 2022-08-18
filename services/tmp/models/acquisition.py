from __main__ import app

class Acquisition(db.Model):
    __tablename__ = "acquisition"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    eye = db.Column(db.String(50), nullable=False, default=None)
    site = db.Column(db.String(50), nullable=False, default=None)
    date = db.Column(db.Date, nullable=False, default=None)
    operator = db.Column(db.String(50), nullable=False, default=None)

    def __init__(self, patient_id, eye, site, date, operator):
        self.patient_id = patient_id
        self.eye = eye
        self.site = site
        self.date = date
        self.operator = operator


