#from __main__ import app

from flask import Blueprint, request, jsonify, send_file
import os
import os.path

patients_api = Blueprint('patients_api', __name__)

# To retrieve a patient with id:

@patients_api.route('/patients/<id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.get(id)
    del patient.__dict__['_sa_instance_state']
    return jsonify(patient.__dict__)

# To retrieve all patients with fname, name:

@patients_api.route('/patients', methods=['GET'])
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

@patients_api.route('/patients', methods=['POST'])
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

@patients_api.route('/patients/<id>', methods=['DELETE'])
def delete_patient(id):
    db.session.query(Patient).filter_by(id=id).delete()
    db.session.commit()
    return "patient deleted"


