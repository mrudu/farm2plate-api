import os
#import magic
import urllib.request
from flask import Flask
from flask_cors import CORS
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import keras
import numpy as np
from keras.models import model_from_json
from PIL import Image
from flask import jsonify

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
CORS(app)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_mango_data(index):
	json_data = {}
	if index == 0:
		json_data["type_mango"] = "raw"
		json_data["color_mango"] = "green"
		json_data["texture_mango"] = "smooth and hard"
		json_data["life_left"] = "12 days"
	elif index == 1:
		json_data["type_mango"] = "partially ripe"
		json_data["color_mango"] = "green yellow"
		json_data["texture_mango"] = "smooth and mildly soft with few spots"
		json_data["life_left"] = "8 days"
	elif index == 2:
		json_data["type_mango"] = "ripe"
		json_data["color_mango"] = "yellow"
		json_data["texture_mango"] = "soft with lots of sports"
		json_data["life_left"] = "3 days"
	else:
		json_data["type_mango"] = "overripe"
		json_data["color_mango"] = "yellow brown"
		json_data["texture_mango"] = "shrivelled and smelly"
		json_data["life_left"] = "0 days"
	return json_data
	
@app.route('/', methods=['GET'])
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		print(request.files.to_dict(flat=False))
		print(request.args)
		print(request.data)
		print(request.get_json())
		print(request.form)
		print(request.get_data())
        # check if the post request has the file part
		if 'mango_pic' not in request.files:
			flash('No file part')
			return jsonify(data="")
		file = request.files['mango_pic']
		json_file = open('model.json', 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		mango_trainer = model_from_json(loaded_model_json)
		# load weights into new model
		mango_trainer.load_weights("model.h5")
		if file.filename == '':
			flash('No file selected for uploading')
			return jsonify(data="")
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			img = Image.open('uploads/'+filename).resize((256, 256))
			img =  np.array(img)/255.0
			test_images = []
			test_images.append(img)
			test_images = np.array(test_images)

			prediction = list(list(mango_trainer.predict(test_images))[0])
			print(prediction)
			print(max(prediction))
			mango_data = get_mango_data(prediction.index(max(prediction)))
			print(prediction.index(max(prediction)))
			print(mango_data)
			flash('File successfully uploaded -  It is a ' + mango_data["type_mango"] + " mango")
			return jsonify(data=mango_data)
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return jsonify(data="")

if __name__ == "__main__":
    app.run()
