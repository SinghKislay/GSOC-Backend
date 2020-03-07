import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import cv2
from create_dataset import *
import tensorflow_hub as hub



new_model = tf.keras.models.load_model('mymodel.h5', custom_objects={'KerasLayer':hub.KerasLayer})

new_model.summary()
img = cv2.imread("C:/Users/Kislay/Desktop/GSOC/data/sample/images/00000013_005.png")
img_resized = cv2.resize(img, (224, 224))
gray_image_3ch = np.stack(img_resized, axis=0)/255
gray_image_3ch = np.array([gray_image_3ch])
#cv2.imshow('',gray_image_3ch)
#cv2.waitKey(0)
predictions = new_model.predict(gray_image_3ch)
winner_class_index = np.argmax(predictions, axis=-1)
print(winner_class_index)
