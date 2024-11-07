from io import BytesIO
import dotenv

import uuid
from uuid import UUID
from flask import Flask
import docker
import pytainer

dotenv.load_dotenv()

try:
    client = docker.DockerClient()
except Exception as e:
    client = None
app = Flask(__name__)


@app.route("/")
def home():
    return "Home"


@app.route("/status")
def status():
    docker_status = "Ok!" if client != None else "Not Running"
    return {"docker": docker_status}
    return client


@app.route("/containers", methods=["POST"])
def new_container():
    c_id = pytainer.create_bucker()
    return {"created": c_id}


@app.route("/containers/<container_id>", methods=["PUT"])
def upload_script(container_id):
    import os
    import shutil

    container_id = str("0147f5965a")

    # todo: get file from request
    # Note: the zip is constructed by the frontend in a predefined format

    import utils

    zip_file_path = "../assets/generated.zip"
    utils.zip_directory("../assets/sample_script/", zip_file_path)
    # unzip file into bucket
    with open(zip_file_path, mode="rb") as zip_file:
        zip_content = zip_file.read()

    pytainer.create_image(container_id, BytesIO(zip_content))

    return "Ok"


@app.route("/web/<container_id>", methods=["GET"])
def web_container(container_id):
    return container_id
