from rest_framework import views
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
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
from django.http import JsonResponse
import base64
import json
from matplotlib.pylab import cm
from yolov3_tf2.models import (
    YoloV3, YoloV3Tiny
)
from yolov3_tf2.dataset import transform_images, load_tfrecord_dataset
from yolov3_tf2.utils import draw_outputs
class ImageUnAutheticatedGradView(views.APIView):

    def post(self, request):
        print(request.data['image'])
        img = tf.image.decode_png(request.data['image'].read(), channels=3)
        new_model = tf.keras.models.load_model('./../mymodel.h5', custom_objects={'KerasLayer':hub.KerasLayer})
        img_resized = tf.image.resize(img, [224, 224])
        gray_image_3ch = np.array([img_resized/225.0])
        print(img_resized.shape)
        
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
        img_resized = np.uint8(img_resized)
        print(type(img_resized))
        print(type(m))
        fin = cv2.addWeighted(m, 0.5, img_resized, 0.5, 0)
        image = Image.fromarray(fin)

        response = HttpResponse(content_type="image/png")
        image.save(response, "PNG")
        
        #image = Image.fromarray(np.uint8(masked_image*100))
        #retval, buffer_img= cv2.imencode('.jpg', masked_image)
        #final = base64.b64encode(buffer_img)
        #base64_string = final.decode('utf-8')
        #response = HttpResponse(content_type="image/png")
        #image.save(response, "PNG")

        return response


class ImageUnAutheticatedPredView(views.APIView):

    def post(self, request):
        img = tf.image.decode_png(request.data['image'].read(), channels=3)
        new_model = tf.keras.models.load_model('./../mymodel.h5', custom_objects={'KerasLayer':hub.KerasLayer})
        img_resized = tf.image.resize(img, [224, 224])/225.0
        gray_image_3ch = np.array([img_resized])
        predictions = new_model.predict(gray_image_3ch)
        print(predictions)
        label = give_label(np.argmax(predictions[0]))
        return HttpResponse(label)

class ImageUnAutheticatedBBoxView(views.APIView):

    def post(self, request):
        yolo = YoloV3(classes=8)

        yolo.load_weights('./checkpoints/yolov3_train.tf').expect_partial()
        

        class_names = [c.strip() for c in open('./checkpoints/chestx.names').readlines()]
        

        img_raw = tf.image.decode_image(
            request.data['image'].read(), channels=3)

        img = tf.expand_dims(img_raw, 0)
        img = transform_images(img, 416)

        
        boxes, scores, classes, nums = yolo(img)
        
        img = cv2.cvtColor(img_raw.numpy(), cv2.COLOR_RGB2BGR)
        img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
        image = Image.fromarray(img)
        response = HttpResponse(content_type="image/png")
        image.save(response, "PNG")
        return response

class ImageUnAutheticatedBBoxPredView(views.APIView):

    def post(self, request):
        yolo = YoloV3(classes=8)

        yolo.load_weights('./checkpoints/yolov3_train.tf').expect_partial()
        

        class_names = [c.strip() for c in open('./checkpoints/chestx.names').readlines()]
        

        img_raw = tf.image.decode_image(
            request.data['image'].read(), channels=3)

        img = tf.expand_dims(img_raw, 0)
        img = transform_images(img, 416)

        
        boxes, scores, classes, nums = yolo(img)
        
        

        arr = []
        for i in range(nums[0]):
            arr.append(class_names[int(classes[0][i])])
        
        
        return JsonResponse({'pred':arr})


def give_label(num):
    res=''
    if(num == 0):
        res = "No Finding"
    if(num == 1):
        res = "Infiltration"
    if(num == 2):
        res = "Cardiomegaly"
    if(num == 3):
        res = "Effusion"
    if(num == 4):
        res = "Emphysema"
    if(num == 5):
        res = "Pneumothorax"
    if(num == 6):
        res = "Atelectasis"
    if(num == 7):
        res = "Consolidation"
    if(num == 8):
        res = "Mass"
    if(num == 9):
        res = "Pleural_Thickening"
    if(num == 10):
        res = "Nodule"
    if(num == 11):
        res = "Fibrosis"
    return res
