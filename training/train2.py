import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import cv2
from create_dataset import *
import tensorflow_hub as hub
from datetime import datetime
import tensorflow as tf

dataset = create_dataset()

IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)

# Create the base model from the pre-trained model MobileNet V2
base_model = tf.keras.applications.VGG16(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet')
'''
base_model.trainable = False
base_model.summary()
base_model.layers.pop()
base_model.summary()
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(12, activation='softmax', name='predictions')
model = tf.keras.Sequential([
  base_model,
  global_average_layer,
  prediction_layer
])
'''

model = tf.keras.Sequential()
for layer in base_model.layers[:-1]:
    model.add(layer)


base_model.trainable = False
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(12, activation='softmax', name='predictions')

model.add(global_average_layer)
model.add(prediction_layer)

print(model.summary())




LR = 1e-4
EPOCHS = 5




model.compile(
  optimizer=tf.keras.optimizers.Adam(learning_rate=LR),
  loss="categorical_crossentropy",
  metrics=["accuracy"]
  )

history = model.fit(dataset, epochs=EPOCHS)
model.summary()
model.save("mymodel.h5")
