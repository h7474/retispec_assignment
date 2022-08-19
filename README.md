# Retispec Assignment

### Build application
- Install Docker Compose version v2.6.0
- Navigate to `/backend`
- Run `docker compose up --build retispec` to run db and assignment
- Run `docker ps` to see that both db and assignment are running

### Monitor Application
- Open new shell, run `docker exec -it db psql -U postgres` to login to db
- Run `\dt` inside postgres shell to view tables
- Run `select * from patient;` to grab all patients
- Run `select * from acquisition;` to grab all acquisitions
- Open new shell, run `docker exec -it assignment bash` to login to assignment container
- Check `\uploads` directory inside the assignment container for images uploaded

### Patients API
- Install Postman to send queries to docker container running at `http://localhost:80/`
- Send POST request to http://localhost:80/patients with body to create new patient:
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
- Send POST request to http://localhost:80/acquisitions with formdata to create new acquisition:
```
    {
        "patient_id": "Nir",
        "eye": "LEFT",
        "site": "Ottawa",
        "date":"2022-09-27"
        "operator":"Nir Oren"
        "image": attach file on Postman
    }
```
- Send GET request to http://localhost:80/acquisitions/id to get all acquisitions for a given patient
- Send DELETE request to http://localhost:80/patients/id to delete an acquisition by id
- Send GET request to http://localhost:80/download/id to download an image for an acquisition where id is acquisition id.

### Frontend
- Open home.html to upload an acquisition instead of using Postman
