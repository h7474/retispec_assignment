from services.app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app) 

class Patient(db.Model):
    __tablename__ = "patient"
    
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=True, default=None)
    sex = db.Column(db.String(50), nullable=True, default=None)
    acquisitions = db.relationship('Acquisition', backref='patient', lazy=True)

    def __init__(self, fname, lname, dob, sex):
        self.fname = fname
        self.lname = lname
        self.dob = dob
        self.sex = sex

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


