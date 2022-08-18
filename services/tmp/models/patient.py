from __main__ import app

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


