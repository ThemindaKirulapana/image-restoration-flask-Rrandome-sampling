#Random Sampling Algorithm: The second algorithm is based on the random sampling algorithm described in also used for image restoration
from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

app = Flask(__name__)

def apply_nonlinear_filter(image):
    # Apply the non-linear filter (median filter)
    filtered_image = cv2.medianBlur(image, 3)
    return filtered_image

def richardson_lucy_deconvolution(image, kernel, iterations):
    restored_image = image.copy()

    for _ in range(iterations):
        estimated_blur = cv2.filter2D(restored_image, -1, kernel)
        
        # Convert relative_blur to the same data type as restored_image
        relative_blur = image / (estimated_blur + 1e-10)
        relative_blur = relative_blur.astype(restored_image.dtype)

        restored_image *= relative_blur
        restored_image = np.clip(restored_image, 0, 255)

    return restored_image

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            return redirect(request.url)

        # Check if the file is allowed and has the right extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
            # Read the image
            image = Image.open(BytesIO(file.read())).convert("L")
            image_array = np.array(image)

            # Apply the non-linear filter
            filtered_image_array = apply_nonlinear_filter(image_array)

            # Richardson-Lucy deconvolution
            kernel = np.ones((5, 5), np.float32) / 25  # Example kernel, you can adjust this
            iterations = 10  # Adjust the number of iterations as needed
            restored_image_array = richardson_lucy_deconvolution(filtered_image_array, kernel, iterations)

            # Convert NumPy array back to PIL image for display
            restored_image = Image.fromarray(restored_image_array)

            # Save the restored image
            restored_image_path = "static/restored_image.png"
            restored_image.save(restored_image_path)

            return render_template("index.html", original_image=image, restored_image_path=restored_image_path)

    return render_template("index.html", original_image=None, restored_image_path=None)

if __name__ == "__main__":
    app.run(debug=True)
