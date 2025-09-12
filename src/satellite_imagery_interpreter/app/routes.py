from flask import render_template, request, jsonify, current_app
from . import utils
from flask import Blueprint

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/download", methods=["POST"])
def download_geotiff():
    data = request.get_json()
    coords = data.get("coords")

    if not coords or len(coords) < 4:
        return jsonify({"error": "Invalid coordinates"}), 400

    try:
        utils.get_geotiff_from_rectangle(coords)
        return jsonify({"status": "success"})
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({"error": str(e)}), 500