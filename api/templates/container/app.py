from flask import Flask
import logging
import sys
from flask import request

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

app = Flask(__name__)


@app.route("/run", methods=["POST"])
def run():
    import sys

    logger.info("Run Command Recieved")
    try:
        sys.path.append("./bucket/")
        import main
        import json

        d = request.json
        # print(d)
        # dct = json.loads(d)

        logger.info("Running main")
        main.run(**d)
        pass
    except Exception as e:
        print("Run command Failed: %s" % e)
        return str(e)
    logger.info("Run Command Finsihed")
    return "Run command Finished"


@app.route("/status")
def status():
    logger.info("Status Called")
    print("Status request recieved")
    return "Ok"
