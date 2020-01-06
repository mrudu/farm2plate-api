import os
#import magic
import urllib.request
from flask import Flask
from flask_cors import CORS
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
from flask import jsonify

from dummy_model_code import mango_trainer_predict

# App configuration

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
CORS(app)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_prediction(filename):
	img = Image.open('uploads/'+filename).resize((256, 256))
	img =  np.array(img)/255.0
	test_images = []
	test_images.append(img)
	test_images = np.array(test_images)


	mango_data = mango_trainer_predict(test_images, filename)
	return mango_data

# Route Handlers

@app.route('/', methods=['GET'])
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		# get form data parameter
		form_data = request.form.to_dict(flat=False)
        # check if the post request has the file part
		if 'mango_pic' not in request.files:
			flash('No file part')
			return jsonify(data='No file part')

		file = request.files['mango_pic']
		if file.filename == '':
			flash('No file selected for uploading')
			return jsonify(data='No file selected for uploading')
		if file and allowed_file(file.filename):
			filename = form_data["filename"][0]
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			mango_data = get_prediction(filename)
			flash('File successfully uploaded -  It is a ' + mango_data["grade_stage"] + " mango")
			return jsonify(data=mango_data)
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return jsonify(data="")

if __name__ == "__main__":
    app.run()
