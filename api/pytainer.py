"""
Contains all functionality for Docker manipulation
"""

import hashlib
from io import BytesIO
import logging
import dotenv
import os
import docker
import uuid
from uuid import UUID
import zipfile
import shutil

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv()

logger.info("Loading Module Pytainer")
CONTAINER_DIR = os.environ.get("CONTAINER_DIR", "")
TEMPLATE_DIR = os.environ.get("IMAGE_TEMPLATE", "")
CLIENT = None

assert CONTAINER_DIR, "Expected CONTAINER_DIR env variable"
assert TEMPLATE_DIR, "Expected IMAGE_TEMPLATE env variable"

logger.info("Container Directory: %s" % CONTAINER_DIR)
if not CONTAINER_DIR:
    raise EnvironmentError("Missing environment Variable %s" % CONTAINER_DIR)


def _generate_id() -> str:
    new_id = uuid.uuid4()
    hash_obj = hashlib.sha256(str(new_id).encode())
    return hash_obj.hexdigest()[:10]


def _get_client():
    global CLIENT
    if CLIENT:
        return CLIENT
    try:
        CLIENT = docker.DockerClient()
    except Exception as e:
        raise EnvironmentError("Could not connect to docker: %s" % e)
    return CLIENT


def _get_container_path(container_id: str) -> str:
    container_path = os.path.join(CONTAINER_DIR, str(container_id))
    return container_path


def _get_image_name(container_id: str, version: str = "1.0.0"):
    return "pytainer-%s" % container_id


def create_bucker() -> str:
    logger.info("Creating new bucket")
    if not os.path.exists(CONTAINER_DIR):
        os.mkdir(CONTAINER_DIR)

    new_id = _generate_id()
    container_path = os.path.join(CONTAINER_DIR, str(new_id))
    os.mkdir(container_path)
    return new_id


def create_image(bucket_id: str, zip_content: BytesIO) -> str:
    logger.info("Creating image: %s" % bucket_id)
    client = _get_client()
    container_path = _get_container_path(bucket_id)

    # place container template in there

    logger.info("Copying Template")
    shutil.copytree(TEMPLATE_DIR, container_path, dirs_exist_ok=True)

    # debug: create zip image from template

    logger.info("Unzipping User code")
    with zipfile.ZipFile(zip_content) as zp:
        zp.extractall(container_path + "/app")

    logger.info("Building Image from %s" % container_path)
    name = _get_image_name(bucket_id)
    client.images.build(path=container_path, tag=name)
    logger.info("Image created")
    return name


def run_container(image_id):
    assert image_id
    client = _get_client()
    image_name = _get_image_name(image_id)
    logger.info("Starting Container for image: %s" % image_id)
    client.containers.run(image_name, detach=True)


def delete_container(id):
    logger.info("Delete container %s" % id)
