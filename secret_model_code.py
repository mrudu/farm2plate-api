import keras
from keras import backend as K
from keras.models import model_from_json
from PIL import Image
from flask import jsonify
import mysql.connector
from cie_lab import process_cie_lab

# load model from file
json_file = open('classifier_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
mango_trainer = model_from_json(loaded_model_json)
# load weights into new model
mango_trainer.load_weights("classifier_model.h5")
# compiling stage
mango_trainer.compile(optimizer = 'Adam' , loss = "sparse_categorical_crossentropy", metrics=["accuracy"])
mango_trainer._make_predict_function()

# Setting Up MySql Connection
db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="my_first_db1"
)
db_cursor = db_connection.cursor(buffered=True)

def get_mango_data(index, cie_data):
	json_data = {}
	if index == 0:
		json_data["grade_stage"] = "raw"
	elif index == 1:
		json_data["grade_stage"] = "partially ripe"
	elif index == 2:
		json_data["grade_stage"] = "ripe"
	else:
		json_data["grade_stage"] = "overripe"

	if cie_data["major_axis"] > 150 and cie_data["major_axis"] <= 180:
		json_data["size"] = "big"
	elif cie_data["major_axis"] <= 150 and cie_data["major_axis"] > 120:
		json_data["size"] = "medium"
	else:
		json_data["size"] = "small"
	
	json_data["color"] = "dummy"
	json_data["physical_appearance"] = "dummy"
	json_data["shape"] = "dummy"
	json_data["quality"] = "dummy"
	json_data["shelf_life"] = "dummy"
	return json_data

def mango_trainer_predict(test_images, filename):
	predictions = mango_trainer.predict(test_images)

	prediction = list(list(predictions)[0])
	cie_data = process_cie_lab(filename)


	write_to_database(predictions, cie_data, filename)
	mango_data = get_mango_data(prediction.index(max(prediction)), cie_data)
	return mango_data

def write_to_database(predictions, cie_data, filename):
	db_cursor.execute("INSERT INTO Results_full_classifier (img_name,prediction,stage1,stage2,stage3,stage4) VALUES ('"+filename+"','"+str(predictions)+"',"+str(100*predictions[0][0])+","+str(100*predictions[0][1])+","+str(100*predictions[0][2])+","+str(100*predictions[0][3])+")")
	db_cursor.execute("INSERT INTO CIELAB (type,fruit_id,L_value,a_value,b_value,minor_axis,major_axis,count_spots,count_mango,ratio,ratio_spots) VALUES ("+
        "'FULL', '" +
        filename +
        "', '" + str(cie_data["L_value"]) +
        "', " + str(cie_data["a_value"]) +
        "," + str(cie_data["b_value"]) +
        "," + str(cie_data["minor_axis"]) +
        "," + str(cie_data["major_axis"]) +
        "," + str(cie_data["count_spots"]) +
        "," + str(cie_data["count_mango"]) +
        "," + str(cie_data["ratio"]) +
        "," + str(cie_data["ratio_spots"]) +
    ")")
	db_connection.commit()