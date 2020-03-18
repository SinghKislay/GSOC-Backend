import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import cv2
import matplotlib.pyplot as plt

CHANNELS = 3
IMG_SIZE = 224


def parse_function(filename, label):
    """Function that returns a tuple of normalized image array and labels array.
    Args:
        filename: string representing path to image
        label: 0/1 one-dimensional array of size N_LABELS
    """
    
    # Read an image from a file
    image_string = tf.io.read_file(filename)
    # Decode it into a dense vector
    image_decoded = tf.image.decode_png(image_string, channels=CHANNELS)
    # Resize it to fixed shape
    image_resized = tf.image.resize(image_decoded, [IMG_SIZE, IMG_SIZE])
    # Normalize it from [0, 255] to [0.0, 1.0]
    image_normalized = image_resized/255
    print(filename, label)

    #cv2.imshow('', np.array(image_normalized))
    #cv2.waitKey(0)

    return image_normalized, label

BATCH_SIZE = 200
AUTOTUNE = tf.data.experimental.AUTOTUNE
SHUFFLE_BUFFER_SIZE = 10000


def give_label2(strng, args, flag):
    labels_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    strng_list = strng.split("|")
    for wrd in strng_list:
        
        if(wrd == "No Finding"):
            labels_list = False
            flag = False

        if(wrd == "Infiltration" and args['c1'] < args['c0']):
            labels_list[1] = 1
            args['c1'] += 1
            flag = False
        
        if(wrd == "Cardiomegaly" and args['c2'] < args['c0']):
            labels_list[2] = 1
            args['c2'] += 1
            flag = False
        
        if(wrd == "Effusion" and args['c3'] < args['c0']):
            labels_list[3] = 1
            args['c3'] += 1
            flag = False
        
        if(wrd == "Emphysema" and args['c4'] < args['c0']):
            labels_list[4] = 1
            args['c4'] += 1
            flag = False
        
        if(wrd == "Pneumothorax" and args['c5'] < args['c0']):
            labels_list[5] = 1
            args['c5'] += 1
            flag = False
        
        if(wrd == "Atelectasis" and args['c6'] < args['c0']):
            labels_list[6] = 1
            args['c6'] += 1
            flag = False
        
        if(wrd == "Consolidation" and args['c7'] < args['c0']):
            labels_list[7] = 1
            args['c7'] += 1
            flag = False
        
        if(wrd == "Mass" and args['c8'] < args['c0']):
            labels_list[8] = 1
            args['c8'] += 1
            flag = False
        
        if(wrd == "Pleural_Thickening" and args['c9'] < args['c0']):
            labels_list[9] = 1
            args['c9'] += 1
            flag = False
        
        if(wrd == "Nodule" and args['c10'] < args['c0']):
            labels_list[10] = 1
            args['c10'] += 1
            flag = False
        
        if(wrd == "Fibrosis" and args['c11'] < args['c0']):
            labels_list[11] = 1
            args['c11'] += 1
            flag = False
        
    return labels_list, args ,flag



def give_label(strng, args):
    labels_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    strng_list = strng.split("|")
    for wrd in strng_list:
        
        if(wrd == "No Finding"):
            labels_list[0] = 1
            args['c0'] += 1

        if(wrd == "Infiltration"):
            labels_list[1] = 1
            args['c1'] += 1
        
        if(wrd == "Cardiomegaly"):
            labels_list[2] = 1
            args['c2'] += 1
        
        if(wrd == "Effusion"):
            labels_list[3] = 1
            args['c3'] += 1
        
        if(wrd == "Emphysema"):
            labels_list[4] = 1
            args['c4'] += 1
        
        if(wrd == "Pneumothorax"):
            labels_list[5] = 1
            args['c5'] += 1
        
        if(wrd == "Atelectasis"):
            labels_list[6] = 1
            args['c6'] += 1
        
        if(wrd == "Consolidation"):
            labels_list[7] = 1
            args['c7'] += 1
        
        if(wrd == "Mass"):
            labels_list[8] = 1
            args['c8'] += 1
        
        if(wrd == "Pleural_Thickening"):
            labels_list[9] = 1
            args['c9'] += 1
        
        if(wrd == "Nodule"):
            labels_list[10] = 1
            args['c10'] += 1
        
        if(wrd == "Fibrosis"):
            labels_list[11] = 1
            args['c11'] += 1
        
    return labels_list, args

def create_data_path():
    #file_list = os.listdir("C:/Users/Kislay/Desktop/GSOC/data/sample/images")
    args = {}
    for i in range(12):
        args['c'+str(i)] = 0
    data_path = []
    label_list = []
    label = pd.read_csv("C:/Users/Kislay/Desktop/GSOC/data/sample_labels.csv", usecols=["Image Index", "Finding Labels"])
    c = 0
    
    for img_name in label.values:
        data_path.append(os.path.join("C:/Users/Kislay/Desktop/GSOC/data/sample/images", img_name[0]))
        temp_list, args = give_label(img_name[1], args)
        label_list.append(temp_list)
        c = c + 1
    
    
    while True:
        flag = True
        for img_name in label.values:
            
            temp_list, args, flag = give_label2(img_name[1], args, flag)
            if(temp_list):
                data_path.append(os.path.join("C:/Users/Kislay/Desktop/GSOC/data/sample/images", img_name[0]))
                label_list.append(temp_list)
            if(flag):
                break
        if(flag):
            break
    
    
    return data_path, label_list


def create_dataset( is_training=True):
    """Load and parse dataset.
    Args:
        filenames: list of image paths
        labels: numpy array of shape (BATCH_SIZE, N_LABELS)
        is_training: boolean to indicate training mode
    """
    datapath, labels = create_data_path()
    
    # Create a first dataset of file paths and labels
    dataset = tf.data.Dataset.from_tensor_slices((datapath, labels))
    # Parse and preprocess observations in parallel
    dataset = dataset.map(parse_function, num_parallel_calls=AUTOTUNE)
    
    if is_training == True:
        
        # Shuffle the data each buffer size
        dataset = dataset.shuffle(buffer_size=SHUFFLE_BUFFER_SIZE)
        
    # Batch the data for multiple steps
    dataset = dataset.batch(BATCH_SIZE)
    # Fetch batches in the background while the model is training.
    dataset = dataset.prefetch(buffer_size=AUTOTUNE)
    
    return dataset.repeat(3)



