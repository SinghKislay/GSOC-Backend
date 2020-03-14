from rest_framework import views
from rest_framework.response import Response
from django.http import HttpResponse
import numpy as np
import tensorflow as tf
import cv2
from .serializers import ImageUnAutheticatedSerializer
import os
import tensorflow as tf
import pandas as pd
import tensorflow_hub as hub
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
class ImageUnAutheticatedView(views.APIView):

    def post(self, request):
        print(request.data['image'])
        img = tf.image.decode_png(request.data['image'].read(), channels=3)
        new_model = tf.keras.models.load_model('./../mymodel.h5', custom_objects={'KerasLayer':hub.KerasLayer})
        img_resized = tf.image.resize(img, [224, 224])/225.0
        gray_image_3ch = np.array([img_resized])
        print(gray_image_3ch.shape)
        #gray_image_3ch = tf.reshape(img_resized, (1, 224, 224, 3))
        #predictions = new_model.predict(img_reshaped)
        
        #img_resized = cv2.resize(img, (224, 224))
        #gray_image_3ch = np.stack(img_resized, axis=0)/255
        #gray_image_3ch = np.array([gray_image_3ch])

        
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
        updated_weights = W*intermediate_prediction1

        mask = np.multiply(intermediate_prediction2, updated_weights)

        mask = np.mean(mask[0,:,:,:], axis=-1)
        mask = cv2.resize(mask, (224, 224))
        mask = np.maximum(mask, 0)
        mask = np.repeat(mask[:,:,np.newaxis], 3, axis=2)*255
        mask = cv2.applyColorMap(np.uint8(255*mask), cv2.COLORMAP_JET)
        mask = mask/np.max(mask)
        
        masked_image = np.add(gray_image_3ch, mask)
        
        masked_image = masked_image[0,:,:,:]
        
        image = Image.fromarray(np.uint8(masked_image*100))

        response = HttpResponse(content_type="image/png")
        image.save(response, "PNG")

        return response
