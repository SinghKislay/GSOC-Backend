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

feature_extractor_url = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/4"
feature_extractor_layer = hub.KerasLayer(feature_extractor_url, input_shape=(224,224,3))

feature_extractor_layer.trainable = True

model = tf.keras.Sequential([
    feature_extractor_layer,
    tf.keras.layers.Dense(12, activation='softmax', name='predictions')
])

LR = 1e-6
EPOCHS = 100

model.compile(
  optimizer=tf.keras.optimizers.Adam(learning_rate=LR),
  loss='categorical_crossentropy',
  metrics = ['accuracy']
  )

history = model.fit(dataset, epochs=EPOCHS)
model.summary()
model.save("mymodel.h5")
