
#Random Sampling Algorithm: The second algorithm is based on the random sampling algorithm described in also used for image restoration
from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)

# Set the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def restore_image(input_image, selected_pixels, iterations=10):
    # Assuming a degradation model (e.g., blurring) before restoration
    kernel = np.ones((5, 5), np.float32) / 25
    blurred_image = cv2.filter2D(input_image.astype(np.float32), -1, kernel)

    # Richardson-Lucy deconvolution algorithm
    restored_image = input_image.astype(np.float32).copy()

    for _ in range(iterations):
        estimated_blur = cv2.filter2D(restored_image, -1, kernel)
        relative_blur = blurred_image / (estimated_blur + 1e-10)
        restored_image *= relative_blur
        restored_image = np.clip(restored_image, 0, 255)

    # Apply restoration only to the selected pixels
    for i, j in selected_pixels:
        restored_image[i, j] = input_image[i, j]

    return np.uint8(restored_image)


def random_sampling(image, fraction=0.1):
    # Get the number of pixels to sample
    total_pixels = image.shape[0] * image.shape[1]
    num_pixels_to_sample = int(fraction * total_pixels)

    # Randomly sample pixels
    selected_pixels = np.random.randint(0, image.shape[0], size=(num_pixels_to_sample, 2))

    return selected_pixels

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        input_image = cv2.imread(filepath)

        # Call the random sampling function
        selected_pixels = random_sampling(input_image)

        # Call the image restoration function
        output_image = restore_image(input_image, selected_pixels)

        # Save the output image
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'restored_' + filename)
        cv2.imwrite(output_filepath, output_image)

        return render_template('index.html', input_image=filename, output_image='restored_' + filename)

    return redirect(request.url)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)

# Set the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def restore_image(input_image, selected_pixels, iterations=10):
    # Assuming a degradation model (e.g., blurring) before restoration
    kernel = np.ones((5, 5), np.float32) / 25
    blurred_image = cv2.filter2D(input_image, -1, kernel)

    # Richardson-Lucy deconvolution algorithm
    restored_image = input_image.copy()

    for _ in range(iterations):
        estimated_blur = cv2.filter2D(restored_image, -1, kernel)
        relative_blur = blurred_image / (estimated_blur + 1e-10)
        restored_image *= relative_blur
        restored_image = np.clip(restored_image, 0, 255)

    # Apply restoration only to the selected pixels
    for i, j in selected_pixels:
        restored_image[i, j] = input_image[i, j]

    return np.uint8(restored_image)

def random_sampling(image, fraction=0.1):
    # Get the number of pixels to sample
    total_pixels = image.shape[0] * image.shape[1]
    num_pixels_to_sample = int(fraction * total_pixels)

    # Randomly sample pixels
    selected_pixels = np.random.randint(0, image.shape[0], size=(num_pixels_to_sample, 2))

    return selected_pixels

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        input_image = cv2.imread(filepath)

        # Call the random sampling function
        selected_pixels = random_sampling(input_image)

        # Call the image restoration function
        output_image = restore_image(input_image, selected_pixels)

        # Save the output image
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'restored_' + filename)
        cv2.imwrite(output_filepath, output_image)

        return render_template('index.html', input_image=filename, output_image='restored_' + filename)

    return redirect(request.url)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
