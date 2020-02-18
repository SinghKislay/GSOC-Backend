from rest_framework import views
from rest_framework.response import Response
import numpy as np
import tensorflow as tf
import cv2
from .serializers import ImageUnAutheticatedSerializer
import os
import tensorflow as tf
import pandas as pd
import tensorflow_hub as hub

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

class ImageUnAutheticatedView(views.APIView):

    def post(self, request):
        print(request.data['image'])
        img = tf.image.decode_png(request.data['image'].read(), channels=3)
        #img = cv2.imdecode(np.fromstring(request.data['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)/255
        #results = ImageUnAutheticatedSerializer(request.data['image'], many=True).data
        new_model = tf.keras.models.load_model('./../mymodel.h5', custom_objects={'KerasLayer':hub.KerasLayer, 'macro_f1':macro_f1})
        img_resized = tf.image.resize(img, [224, 224])/225.0
        img_reshaped = tf.reshape(img_resized, (1, 224, 224, 3))
        predictions = new_model.predict(img_reshaped)
        return Response(list(predictions))