# Retispec Assignment

### Build application
- Install Docker Compose version v2.6.0.
- Navigate to `/backend` directory.
- Run `docker compose up --build retispec` to run `db` and `assignment` containers.

### Monitor Application
- Run `docker ps` to check if both db and assignment are up and running.
- Open new shell, run `docker exec -it db psql -U postgres` to login to db.
- Run `\dt` inside postgres shell to view tables.
- Run `select * from patient;` to grab all patients.
- Run `select * from acquisition;` to grab all acquisitions.
- Open new shell, run `docker exec -it assignment bash` to login to assignment container.
- Check `\uploads` directory in the assignment container for acquisition images uploaded.

### Patients API
- Install Postman to send queries to docker container running at `http://localhost:80/`
- Send POST request to http://localhost:80/patients to create new patient with body as:
```
    {
        "fname": "Nir",
        "lname": "Oren",
        "sex": "M",
        "dob":"2022-09-27"
    }
```
- Send GET request to http://localhost:80/patients/id to get patient details by patient id.
- Send GET request to http://localhost:80/patients?fname=Nir&lname=Oren to get patient details using first name and last name of patient.
- Send DELETE request to http://localhost:80/patients/id to delete patient by patient id.

### Acquisitions API
- Install Postman to send queries to docker container running at `http://localhost:80/`
- Send POST request to http://localhost:80/acquisitions to create new acquisition with formdata as:
```
    {
        "patient_id": "Nir",
        "eye": "LEFT",
        "site": "Ottawa",
        "date":"2022-09-27"
        "operator":"Nir Oren"
        "image": ..this is a file key
    }
```
- Send GET request to http://localhost:80/acquisitions/id to retrieve all acquisitions belonging to a patient id.
- Send DELETE request to http://localhost:80/acquisitions/id to delete an acquisition by acquisition id.
- Send GET request to http://localhost:80/acquisitions/download/id to download an image belonging to an acquisition where id is acquisition id.

### Frontend
- Open `/frontend/home.html` to upload an acquisition instead of using Postman.
