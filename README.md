
# Flask App for Image Restoration

When you upload an image, you can view the restored verison of it using this app.
apply_nonlinear_filter: Applies a non-linear filter to the input image using a median filter.

richardson_lucy_deconvolution: Implements the Richardson-Lucy deconvolution algorithm. It iteratively refines an estimate of the original image based on a given kernel and number of iterations.

utilizes two image processing techniques: a median filter (non-linear filter) and the Richardson-Lucy deconvolution algorithm for image restoration.

a random sampling algorithm.

## Installation

First clone the project and open the folder using an IDE like VS Code, Pycharm.
Then open the terminal and create a virtual environment.

```bash
  python -m venv env
```
    
Then activate virtual environment

```bash
  env/Scripts/activate
``` 
Next install the required packages.

```bash
  pip install -r requirements.txt
``` 
Create a 'static' folder in the root directory.
Run the app

```bash
  python app.py
``` 
