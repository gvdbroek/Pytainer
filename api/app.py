from io import BytesIO
from logging import Logger
import dotenv

from flask import Flask, render_template, request
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
    return render_template("dev.html")


@app.route("/status")
def status():
    docker_status = "Ok!" if client is not None else "Not Running"
    return {"docker": docker_status}


@app.route("/containers", methods=["POST"])
def new_container():
    c_id = pytainer.create_bucker()
    return {"created": c_id}


@app.route("/containers/<container_id>", methods=["PUT"])
def upload_script(container_id):
    container_id = str("0147f5965a")

    # todo: get file from request
    # Note: the zip is constructed by the frontend in a predefined format

    import utils

    zip_file_path = "../assets/generated.zip"
    utils.zip_directory("../assets/sample_script/", zip_file_path)

    # unzip file into bucket
    with open(zip_file_path, mode="rb") as zip_file:
        zip_content = zip_file.read()

    image_name = pytainer.create_image(container_id, BytesIO(zip_content))
    pytainer.run_container(image_name)

    return "Ok"


@app.route("/commands/run", methods=["POST"])
def start_container():
    # accepts image_name filter
    image_id = request.args.get("image_id")
    if not image_id:
        return "Image not found"
    print("Starting container: %s" % image_id)
    pytainer.run_container(image_id)
    return "Starting container: %s" % image_id


@app.route("/web/<container_id>", methods=["GET"])
def web_container(container_id):
    return container_id
