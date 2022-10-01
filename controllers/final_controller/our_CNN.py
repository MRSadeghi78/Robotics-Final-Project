from keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf

model = None

def process_image(image_directory):
    global model
    if model is None:
        model = load_model('CNN_model.h5')
    test_image = image.load_img(image_directory, target_size = (28,28))
    test_image = test_image.convert(mode='RGB')
    test_image = tf.keras.preprocessing.image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    test_image = tf.keras.applications.inception_v3.preprocess_input(test_image)
    result = model.predict(x = test_image)
    if result[0][0] > result[0][1] + result[0][2] + result[0][3]:
        return 'circle'
    elif result[0][1] > result[0][0] + result[0][2] + result[0][3]:
        return 'square'
    elif result[0][2] > result[0][0] + result[0][1] + result[0][3]:
        return 'star'
    elif result[0][3] > result[0][0] + result[0][1] + result[0][2]:
        return 'triangle' 
