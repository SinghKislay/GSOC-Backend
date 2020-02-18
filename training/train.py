import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import cv2
from create_dataset import *
import tensorflow_hub as hub
from datetime import datetime
import tensorflowjs as tfjs

dataset = create_dataset()

feature_extractor_url = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/4"
feature_extractor_layer = hub.KerasLayer(feature_extractor_url, input_shape=(224,224,3))

feature_extractor_layer.trainable = False

model = tf.keras.Sequential([
    feature_extractor_layer,
    tf.keras.layers.Dense(1024, activation='relu', name='hidden_layer1'),
    tf.keras.layers.Dense(512, activation='relu', name='hidden_layer2'),
    tf.keras.layers.Dense(12, activation='sigmoid', name='predictions')
])

def macro_f1(y, y_hat, thresh=0.5):
    """Compute the macro F1-score on a batch of observations (average F1 across labels)
    
    Args:
        y (int32 Tensor): labels array of shape (BATCH_SIZE, N_LABELS)
        y_hat (float32 Tensor): probability matrix from forward propagation of shape (BATCH_SIZE, N_LABELS)
        thresh: probability value above which we predict positive
        
    Returns:
        macro_f1 (scalar Tensor): value of macro F1 for the batch
    """
    y_pred = tf.cast(tf.greater(y_hat, thresh), tf.float32)
    tp = tf.cast(tf.math.count_nonzero(y_pred * y, axis=0), tf.float32)
    fp = tf.cast(tf.math.count_nonzero(y_pred * (1 - y), axis=0), tf.float32)
    fn = tf.cast(tf.math.count_nonzero((1 - y_pred) * y, axis=0), tf.float32)
    f1 = 2*tp / (2*tp + fn + fp + 1e-16)
    macro_f1 = tf.reduce_mean(f1)
    return macro_f1

LR = 1e-5 # Keep it small when transfer learning
EPOCHS = 100

model.compile(
  optimizer=tf.keras.optimizers.Adam(learning_rate=LR),
  loss='binary_crossentropy',
  metrics=[macro_f1])

history = model.fit(dataset, epochs=EPOCHS)
model.summary()

model.save("mymodel.h5")

#tfjs.converters.save_keras_model(model, 'C:/Users/Kislay/Desktop/GSOC/json')
#tf.keras.experimental.export_saved_model(model, export_path)
#print("Model with macro soft-f1 was exported in this path: '{}'".format(export_path))
