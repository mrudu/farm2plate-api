## main.py

import numpy as np
from PIL import Image
import sys, json

from dummy_model_code import mango_trainer_predict

def get_prediction(input_data):
	img = Image.open(input_data["image_file"]).resize((256, 256))
	img =  np.array(img)/255.0
	test_images = []
	test_images.append(img)
	test_images = np.array(test_images)


	mango_data = mango_trainer_predict(test_images, input_data)
	return mango_data

def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def main():
    #get our data as an array from read_in()
    lines = read_in()

    print(get_prediction(lines))

#start process
if __name__ == '__main__':
    main()