import configure_logging
logger = configure_logging.configure(__name__)
from flask import Flask, render_template, url_for, request, jsonify, make_response
import datetime
import json
import sys
import os
import auto_shades
# sys.path.insert(1, os.path.abspath('./'))
# from helpers import object_equals
# import copy

# dir()

app = Flask(__name__)

# width=800
# height=480

# # ====== MAIN SCREEN ====== #
# @app.route('/')
# def home():
#     return render_template('home.html', width=width, height=height, scenes=scenes)


# ====== REQUEST FROM HOME AUTOMATION TO RUN THE SHADES UP OR DOWN ====== #

# sunlight scene AJAX data request
@app.route('/run_shades', methods=['POST'])
def run_shades():
    data = request.get_json()
    logger.debug(data)

    # try:
    #     # with open(f"{home_auto_path}/data_2023-07-08-2122.json", "r") as f :
    #     with open(f"{home_auto_path}/data.json", "r") as f :
    #         sunlight_data = json.load(f)["scenes"]["sunlight"]
    #     results = sunlight_data
    # except Exception as e:
    #     logger.error(repr(e))
    #     results = {"error" : repr(e)}

    # return jsonify(results)

    try:
        dir = data["dir"]
        assert dir in ["up","down"]
        auto_shades.run(dir) # call function to actually move the window shades
        return f"accepted request: moving windows {dir}"
    except KeyError as e:
        logger.error(f"received bad data from home-automation: {json.dumps(data)}")
        return f"Error: bad request: data did not include a direction to move the shades"
    except AssertionError as e:
        logger.error(f"received bad data from home-automation: {json.dumps(data)}")
        return f"Error: bad request: 'dir' value should be either 'up' or 'down'"


if __name__ == '__main__':
   app.run(debug=False,use_reloader=True,host="0.0.0.0") # use host="0.0.0.0" to make visible to other machines on the network; use debug=False when doing this, for security