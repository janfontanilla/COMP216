import uuid
import os
from flask import Flask, jsonify, send_from_directory, request
from werkzeug.exceptions import HTTPException
from PIL import Image

app = Flask(__name__)

# Images stored here
IMAGES_DIR = "images"

# Retrieve list of available PNG images in /images.
@app.route("/image-list", methods=["GET"])
def image_list():
    # Return list of available PNG images in /images.
    return {"images": []}

# above code was not working for me so added this but commented it out
# @app.route("/image-list", methods=["GET"]) def image_list(): # >>> ADD THIS images = [] for f in os.listdir(IMAGES_DIR): if f.lower().endswith(".png"): images.append(f) return {"images": images}

# Retrieve image and properties (format, original size, mode).
@app.route("/get-image/<filename>", methods=["GET"])
def get_image(filename):
    # Return requested image and properties (format, original size, mode).
    return {"filename": filename, "format": None, "size": None, "mode": None}, 404

# above code was not working for me so I added this but commented it out
# @app.route("/get-image/<filename>", methods=["GET"]) def get_image(filename): filepath = os.path.join(IMAGES_DIR, filename) if not os.path.exists(filepath): return {"filename": filename, "format": None, "size": None, "mode": None}, 404 img = Image.open(filepath) return { "filename": filename, "format": img.format, "size": img.size, "mode": img.mode, "url": f"{request.host_url}images/{filename}" }

# Accept image upload, save to /images, convert to PNG.
@app.route("/uploads", methods=["POST"])
def uploads():
    # Accept image upload and save to /images, convert to PNG.
    return {"message": "TODO"}, 501

# above code was not working for me so I added this but commented it out
# @app.route("/uploads", methods=["POST"]) def uploads(): if "file" not in request.files: return {"message": "No file uploaded"}, 400 file = request.files["file"] img = Image.open(file) new_name = f"{uuid.uuid4().hex}.png" save_path = os.path.join(IMAGES_DIR, new_name) img.save(save_path, "PNG") return {"message": "Image uploaded", "filename": new_name}

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

# Extra: Retrieval of images in other formats
@app.route("/convert-image/<filename>", methods=["GET"])
def convert_image(filename):
    filepath = os.path.join(IMAGES_DIR, filename)

    if not os.path.exists(filepath):
        return {"error": "File not found"}, 404

    requested_format = request.args.get("format")
    if not requested_format:
        return {"error": "Missing ?format= parameter"}, 400

    try:
        img = Image.open(filepath)

        # Create a unique temporary filename
        unique = uuid.uuid4().hex
        temp_name = f"temp_{unique}.{requested_format.lower()}"
        temp_path = os.path.join(IMAGES_DIR, temp_name)

        # Convert and save
        img.save(temp_path, requested_format.upper())

        return {
            "filename": temp_name,
            "format": requested_format.upper(),
            "size": img.size,
            "mode": img.mode,
            "url": f"{request.host_url}images/{temp_name}"
        }

    except Exception as e:
        return {"error": str(e)}, 500

# Serve image files
@app.route("/images/<filename>", methods=["GET"])
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

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
