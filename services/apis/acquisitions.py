#from __main__ import app

from flask import Blueprint, request, jsonify, send_file
import os
import os.path

from werkzeug.utils import secure_filename

acquisitions_api = Blueprint('acquisitions_api', __name__)

#UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):     
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

# To create a new acquisition:

@acquisitions_api.route('/acquisitions', methods=['POST'])
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

@acquisitions_api.route('/acquisitions/<patient_id>', methods=['GET'])
def get_acquisitions(patient_id):
    patients = [] 
   
    for patient in db.session.query(Acquisition).filter_by(patient_id=patient_id).all():
        del patient.__dict__['_sa_instance_state']
        patients.append(patient.__dict__)
    return jsonify(patients)

# To delete an existing patient:

@acquisitions_api.route('/acquisitions/<id>', methods=['DELETE'])
def delete_acquisition(id):
    db.session.query(Acquisition).filter_by(id=id).delete()
    db.session.commit()
    return "acquisition deleted"

@acquisitions_api.route('/acquisitions/download/<id>', methods=['GET'])
def download_image(id):
        
    for ext in ALLOWED_EXTENSIONS:
        acquisition_filename = "acquisition_" + str(id) + "." + ext
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], acquisition_filename)
         
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True) 

    return "image not found"


