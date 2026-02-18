from flask import Flask, json, render_template
from werkzeug.exceptions import HTTPException
from os import abort


app = Flask(__name__)

# Images stored here
IMAGES_DIR = "images"

# Retrieve list of available PNG images in /images.
@app.route("/image-list", methods=["GET"])
def image_list():
    "Return list of available PNG images in /images."
    # TODO: list .png files in IMAGES_DIR
    return {"images": []}

# Retrieve image and properties (format, original size, mode).
@app.route("/get-image/<filename>", methods=["GET"])
def get_image(filename):
    """GET: Return requested image and properties (format, original size, mode)."""
    # TODO: serve image + properties using image_converter
    return {"filename": filename, "format": None, "size": None, "mode": None}, 404

# Accept image upload, save to /images, convert to PNG.
@app.route("/uploads", methods=["POST"])
def uploads():
    """POST: Accept image upload, save to /images, convert to PNG."""
    # TODO: save file to IMAGES_DIR, convert to PNG, update image list
    return {"message": "TODO"}, 501


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5000, host="0.0.0.0")

@app.errorhandler(400)
def bad_request(error):
    print(error)
    return render_template("400.html")

@app.errorhandler(404)
def not_found(error):
    print(error)
    return render_template("404.html")

@app.errorhandler(500)
def internal_error(error):
    print(error)
    return render_template("500.html")

@app.errorhandler(502)
def bad_gateway(error):
    print(error)
    return render_template("502.html")

