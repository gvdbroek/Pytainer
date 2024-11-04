import dotenv
import uuid
from flask import Flask
import docker

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
    import shutil
    import os

    app_dir = os.environ["APP_DIR"]

    if not os.path.exists(app_dir):
        os.mkdir(app_dir)

    new_id = str(uuid.uuid4())
    container_path = os.path.join(app_dir, new_id)
    os.mkdir(container_path)

    return new_id


@app.route("/containers/<container_id>", methods=["PUT"])
def upload_script(container_id):
    import os
    import shutil

    # ensure folder is empty
    container_dir = os.path.join(os.environ["APP_DIR"], container_id)
    try:
        shutil.rmtree(container_dir)
    except Exception as e:
        return str(e)
    os.mkdir(container_dir)

    # copy template into container_dir

    # copy recieved files into template
    #
    # Create image from template

    return "Ok"


@app.route("/web/<container_id>", methods=["GET"])
def web_container(container_id):
    return container_id
