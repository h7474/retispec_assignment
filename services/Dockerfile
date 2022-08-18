
FROM python:3.9.13-bullseye

COPY requirements.txt .

RUN pip --trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["flask", "--debug", "run", "--host=0.0.0.0", "--port=80"]
