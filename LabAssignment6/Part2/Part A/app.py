from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Images stored here
IMAGES_DIR = "images"

# Retrieve list of available PNG images in /images.
@app.route("/image-list", methods=["GET"])
def image_list():
    # Return list of available PNG images in /images.
    return {"images": []}

# Retrieve image and properties (format, original size, mode).
@app.route("/get-image/<filename>", methods=["GET"])
def get_image(filename):
    # Return requested image and properties (format, original size, mode).
    return {"filename": filename, "format": None, "size": None, "mode": None}, 404

# Accept image upload, save to /images, convert to PNG.
@app.route("/uploads", methods=["POST"])
def uploads():
    # Accept image upload and save to /images, convert to PNG.
    return {"message": "TODO"}, 501

# Extra: DELETE functionality
@app.route("/delete-image/<filename>", methods=["DELETE"])
def delete_image(filename):
    filepath = os.path.join(IMAGES_DIR, filename)

    if not os.path.exists(filepath):
        return {"error": "File not found"}, 404

    try:
        os.remove(filepath)
        return {"message": f"{filename} deleted successfully"}
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5000, host="0.0.0.0")

@app.errorhandler(400)
def bad_request(error, code):
    return jsonify({error: "Bad Request", code: 400})

@app.errorhandler(404)
def not_found(error, code):
    return jsonify({error: "Not Found", code: 404})

@app.errorhandler(500)
def internal_error(error, code):
    return jsonify({error: "Internal Server Error", code: 500})

@app.errorhandler(502)
def bad_gateway(error, code):
    return jsonify({error: "Bad Gateway", code: 502})

# Error handlers for OS and HTTP exceptions

@app.errorhandler(HTTPException)
def handle_http_error(exc, code):
    # HTTP-related exceptions (400, 404, 500, etc.)
    return jsonify(error=exc.description or str(exc), code=exc.code), exc.code


@app.errorhandler(FileNotFoundError)
def handle_file_not_found(exc, code):
    # OS-related exception: (file or directory does not exist)
    return jsonify(error="Not found", detail=str(exc), code=404), 404


@app.errorhandler(PermissionError)
def handle_permission_error(exc, code):
    # OS-related exception: (cannot read or write)
    return jsonify(error="Permission denied", detail=str(exc), code=403), 403


@app.errorhandler(OSError)
def handle_os_error(exc, code):
    # OS-related exception: (other filesystem errors (path invalid, disk full, etc.))
    return jsonify(error="Server filesystem error", detail=str(exc), code=500), 500


@app.errorhandler(Exception)
def handle_generic_error(exc, code):
    # Unhandled exceptions.
    return jsonify(error="Internal server error", detail=str(exc), code=500), 500
