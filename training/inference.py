import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import cv2
from create_dataset import *
import tensorflow_hub as hub



new_model = tf.keras.models.load_model('mymodel.h5', custom_objects={'KerasLayer':hub.KerasLayer})


img = cv2.imread("C:/Users/Kislay/Desktop/GSOC/data/sample/images/00000013_005.png")
img_resized = cv2.resize(img, (224, 224))
img_resized = img_resized.reshape(1, 224, 224, 3).astype(float)
predictions = new_model.predict(img_resized)
print(predictions)