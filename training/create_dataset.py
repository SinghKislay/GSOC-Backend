import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd


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
    image_normalized = image_resized / 255.0
    print(image_normalized.shape)
    return image_normalized, label

BATCH_SIZE = 128
AUTOTUNE = tf.data.experimental.AUTOTUNE
SHUFFLE_BUFFER_SIZE = 1024

def give_label(strng):
    labels_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    strng_list = strng.split("|")
    for wrd in strng_list:
        if(wrd == "No Finding"):
            labels_list[0] = 1
        if(wrd == "Infiltration"):
            labels_list[1] = 1
        if(wrd == "Cardiomegaly"):
            labels_list[2] = 1
        if(wrd == "Effusion"):
            labels_list[3] = 1
        if(wrd == "Emphysema"):
            labels_list[4] = 1
        if(wrd == "Pneumothorax"):
            labels_list[5] = 1
        if(wrd == "Atelectasis"):
            labels_list[6] = 1
        if(wrd == "Consolidation"):
            labels_list[7] = 1
        if(wrd == "Mass"):
            labels_list[8] = 1
        if(wrd == "Pleural_Thickening"):
            labels_list[9] = 1
        if(wrd == "Nodule"):
            labels_list[10] = 1
        if(wrd == "Fibrosis"):
            labels_list[11] = 1
    return labels_list

def create_data_path():
    #file_list = os.listdir("C:/Users/Kislay/Desktop/GSOC/data/sample/images")
    data_path = []
    label_list = []
    label = pd.read_csv("C:/Users/Kislay/Desktop/GSOC/data/sample_labels.csv", usecols=["Image Index", "Finding Labels"])
    
    for img_name in label.values:
        data_path.append(os.path.join("C:/Users/Kislay/Desktop/GSOC/data/sample/images", img_name[0]))
        label_list.append(give_label(img_name[1]))
        
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
    
    return dataset
