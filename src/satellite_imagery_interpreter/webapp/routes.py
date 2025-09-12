from flask import Flask, request, jsonify, render_template
from satellite_imagery_interpreter.core.create_tiles import get_geotiff_from_rectangle

def init_routes(app: Flask):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/get_geotiff", methods=["POST"])
    def get_geotiff():
        data = request.json
        rectangle = data.get("rectangle")
        if not rectangle or len(rectangle) != 4:
            return jsonify({"error": "Invalid rectangle data"}), 400

        # Call the function to get GeoTIFF
        get_geotiff_from_rectangle(rectangle)
        return jsonify({"message": "GeoTIFF downloaded successfully"})
