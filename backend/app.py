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
    
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=True, default=None)
    sex = db.Column(db.String(50), nullable=True, default=None)
    acquisitions = db.relationship('Acquisition', backref='patient', lazy=True, single_parent=True, cascade="all, delete, delete-orphan")

    def __init__(self, fname, lname, dob, sex):
        self.fname = fname
        self.lname = lname
        self.dob = dob
        self.sex = sex

class Acquisition(db.Model):
    __tablename__ = "acquisition"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
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
    
    patient_exists = db.session.query(
        db.session.query(Patient).filter_by(id=id).exists()
    ).scalar()

    if (not patient_exists):
        return "patient " + str(id) + " doesn't exist", 404
    else:
        patient = Patient.query.get(id)
        del patient.__dict__['_sa_instance_state']
        return jsonify(patient.__dict__), 200

# To retrieve all patients with fname, name:

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = []
    
    fname = request.args.get('fname', None)
    lname = request.args.get('lname', None)
   
    if (fname==None or lname==None):
        if fname==None:
            return "missing first name in request", 422
        elif lname==None:
            return "missing last name in request", 422
    elif fname != None and lname != None:

        patient_exists = db.session.query(
            db.session.query(Patient).filter_by(fname=fname, lname=lname).exists()
        ).scalar()

        if (not patient_exists):
            return "no patients with name " + str(fname)+" "+str(lname)+" exist", 404
        else:
            patients = []
            for patient in db.session.query(Patient).filter_by(fname=fname, lname=lname).all():
                del patient.__dict__['_sa_instance_state']
                patients.append(patient.__dict__)
            return jsonify(patients), 200

# To create a new patient:

@app.route('/patients', methods=['POST'])
def create_patient():

    body = request.get_json()

    patient_exists = db.session.query(
        db.session.query(Patient).filter_by(fname=body['fname'], \
                                          lname=body['lname'], \
                                          dob=body['dob'], \
                                          sex=body['sex']).exists()
    ).scalar()

    if (patient_exists):
        return "patient already exists", 409
    else:
        
        new_patient = Patient(body['fname'], \
                              body['lname'], \
                              body['dob'], \
                              body['sex'])

        db.session.add(new_patient)
        db.session.commit()


        return "new patient with id "+ str(new_patient.id) + " created", 201

# To delete an existing patient:

@app.route('/patients/<id>', methods=['DELETE'])
def delete_patient(id):

    patient_exists = db.session.query(
        db.session.query(Patient).filter_by(id=id).exists()
    ).scalar()

    if (not patient_exists):
        return "patient doesn't exist", 204
    else:
        patient = db.session.query(Patient).filter(Patient.id==id).first()
        db.session.delete(patient)
        
        #db.session.query(Patient).filter_by(id=id).delete()
        db.session.commit()
        return "patient " + str(id) + " deleted", 200

def allowed_file(filename):     
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

# To create a new acquisition:

@app.route('/acquisitions', methods=['POST'])
def create_acquisition():
    file = request.files['image']

    if file.filename == '':
        return "missing image file in request", 422
    elif file and not allowed_file(file.filename):
        return "attachment not a valid image file", 422
    elif file and allowed_file(file.filename): 
        
        form = request.form

        patient_exists = db.session.query(
            db.session.query(Patient).filter_by(id=form['patient_id']).exists()
        ).scalar()
    
        if (not patient_exists):
            return "patient " + str(form['patient_id']) + " doesn't exist.", 400
        else:

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

            return "new acquisition with " + str(acquisition.id) +" created.", 201

# To retrieve all acquisitions for a patient:

@app.route('/acquisitions/<patient_id>', methods=['GET'])
def get_acquisitions(patient_id):
    
    patient_exists = db.session.query(
        db.session.query(Patient).filter_by(id=patient_id).exists()
    ).scalar()

    if (not patient_exists):
        return "patient " + str(patient_id) + "  doesn't exist", 409
    elif (patient_exists):
        acquisition_exists = db.session.query(
            db.session.query(Acquisition).filter_by(patient_id=patient_id).exists()
        ).scalar()

        if (not acquisition_exists):
            return "no acquisitions exist for patient " + str(patient_id), 404
        else:
            patients = [] 
   
            for patient in db.session.query(Acquisition).filter_by(patient_id=patient_id).all():
                del patient.__dict__['_sa_instance_state']
                patients.append(patient.__dict__)
            return jsonify(patients), 200

# To delete an existing acquisition:

@app.route('/acquisitions/<id>', methods=['DELETE'])
def delete_acquisition(id):
    
    acquisition_exists = db.session.query(
        db.session.query(Acquisition).filter_by(id=id).exists()
    ).scalar()

    if (not acquisition_exists):
        return "acquisition doesn't exist", 204
    else:
        #db.session.query(Acquisition).filter_by(id=id).delete()
        
        acquisition = db.session.query(Acquisition).filter(Acquisition.id==id).first()
        db.session.delete(acquisition)
 
        db.session.commit()
        return "acquisition "+str(id)+" deleted", 200

# To download an acquisition image:

@app.route('/acquisitions/download/<id>', methods=['GET'])
def download_image(id):
       
    acquisition_exists = db.session.query(
        db.session.query(Acquisition).filter_by(id=id).exists()
    ).scalar()

    if (not acquisition_exists):
        return "acquisition " + str(id) + " doesn't exist", 204
    else:
        for ext in ALLOWED_EXTENSIONS:
            acquisition_filename = "acquisition_" + str(id) + "." + ext
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], acquisition_filename)
         
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True), 200

        return "image not found for acquisition " + str(id), 404

if __name__ == '__main__':
    app.run(debug=True)
