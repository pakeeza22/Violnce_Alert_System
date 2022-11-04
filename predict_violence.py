import pandas as pd
import numpy as np
import cv2
from tensorflow import keras
from PIL import Image

def predict_job(file):
    
    img = cv2.imread(file, cv2.IMREAD_COLOR)
    loadModelData = keras.models.load_model('modelnew.h5')
    img = cv2.resize(img,(128,128))
    im_pil = Image.fromarray(img)
    im_np = np.asarray(im_pil)
    img_reshape = im_np[np.newaxis, ...]
    pred = loadModelData.predict(img_reshape)

    i = (pred > 0.50)[0]
    label = i

    return label

