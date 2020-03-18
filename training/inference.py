import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import cv2
import tensorflow_hub as hub
import tensorflow as tf
import scipy.misc as sci
from matplotlib.pylab import cm

new_model = tf.keras.models.load_model('mymodel.h5', custom_objects={'KerasLayer':hub.KerasLayer})
img = cv2.imread("C:/Users/Kislay/Desktop/GSOC/data/sample/images/00000324_001.png")
img_resized = cv2.resize(img, (224, 224))
img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
gray_image_3ch = np.stack(img_resized, axis=0)/255
gray_image_3ch = np.array([gray_image_3ch])
print(gray_image_3ch.shape)

new_model.summary()
W = new_model.get_layer('predictions').get_weights()[0]

conv_output = new_model.layers[-3].output

fcc_output = new_model.layers[-2].output
intermediate_model1 = tf.keras.Model(inputs=new_model.input, outputs=fcc_output)
intermediate_prediction1 = intermediate_model1.predict(gray_image_3ch)


intermediate_model2 = tf.keras.models.Model(inputs=new_model.input, outputs=conv_output)
intermediate_prediction2 = intermediate_model2.predict(gray_image_3ch)


predictions = new_model.predict(gray_image_3ch)
winner = np.argmax(predictions, axis=-1)
W = np.transpose(W[:,winner])
updated_weights = ((W*intermediate_prediction1)+10)/10

print(predictions)
mask = np.multiply(intermediate_prediction2, updated_weights)

mask = np.mean(mask[0,:,:,:], axis=-1)

mask = cv2.resize(mask, (224, 224))

m = np.uint8(mask*5000)

m = cm.jet(m)*255
#m = cv2.cvtColor(m, cv2.COLOR_RGBA2RGB)
m = np.uint8(m)
#m = cv2.cvtColor(m, cv2.COLOR_RGBA2BGR)
m = cv2.cvtColor(m, cv2.COLOR_RGBA2RGB)
fin = cv2.addWeighted(m, 0.5, img_resized, 0.5, 0)
plt.imshow(fin)
plt.show()


