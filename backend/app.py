from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import os
import os.path

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
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
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
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

db.create_all()

# To retrieve a patient with id:

@app.route('/patients/<id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.get(id)
    del patient.__dict__['_sa_instance_state']
    return jsonify(patient.__dict__)

# To retrieve all patients with fname, name:

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = []
    
    fname = request.args.get('fname', None)
    lname = request.args.get('lname', None)
    
    if fname != None and lname != None:
        for patient in db.session.query(Patient).filter_by(fname=fname, lname=lname).all():
            del patient.__dict__['_sa_instance_state']
            patients.append(patient.__dict__)
        return jsonify(patients)

# To create a new patient:

@app.route('/patients', methods=['POST'])
def create_patient():
    body = request.get_json()
    db.session.add(Patient(body['fname'], \
                           body['lname'], \
                           body['dob'], \
                           body['sex']
                  ))
    db.session.commit()
    return "patient created in table"

# To delete an existing patient:

@app.route('/patients/<id>', methods=['DELETE'])
def delete_patient(id):
    db.session.query(Patient).filter_by(id=id).delete()
    db.session.commit()
    return "patient deleted"

def allowed_file(filename):     
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

# To create a new acquisition:

@app.route('/acquisitions', methods=['POST'])
def create_acquisition():
    file = request.files['image']

    if file.filename == '':
        return "No selected file"
    elif file and allowed_file(file.filename): 
        
        form = request.form
        filename = file.filename
        ext = "." + filename.rsplit('.', 1)[1].lower()

        acquisition = Acquisition(form['patient_id'], \
                                  form['eye'], \
                                  form['site'], \
                                  form['date'], \
                                  form['operator'])                  

        db.session.add(acquisition)
        db.session.commit()

        acquisition_filename = "acquisition_" + str(acquisition.id) + ext
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], acquisition_filename))

        return "acquisition created in table"

# To retrieve all acquisitions for a patient:

@app.route('/acquisitions/<patient_id>', methods=['GET'])
def get_acquisitions(patient_id):
    patients = [] 
   
    for patient in db.session.query(Acquisition).filter_by(patient_id=patient_id).all():
        del patient.__dict__['_sa_instance_state']
        patients.append(patient.__dict__)
    return jsonify(patients)

# To delete an existing acquisition:

@app.route('/acquisitions/<id>', methods=['DELETE'])
def delete_acquisition(id):
    db.session.query(Acquisition).filter_by(id=id).delete()
    db.session.commit()
    return "acquisition deleted"

# To download an acquisition image:

@app.route('/acquisitions/download/<id>', methods=['GET'])
def download_image(id):
        
    for ext in ALLOWED_EXTENSIONS:
        acquisition_filename = "acquisition_" + str(id) + "." + ext
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], acquisition_filename)
         
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True) 

    return "image not found"

if __name__ == '__main__':
    app.run(debug=True)
