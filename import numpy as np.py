import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import matplotlib.pyplot as plt
import requests
import tensorflow as tf



model = load_model("/home/lightning/Downloads/eggs/mobilenetv2_egg_classifier_stage1.h5")


img_path = r"/home/lightning/Downloads/eggs/cracked2.jpeg"
IMG_SIZE = (224, 224)
img = image.load_img(img_path, target_size=IMG_SIZE)
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)


pred = model.predict(img_array)[0][0]
print("first")
if pred < 0.5:
    r = requests.post("https://avibot-dashboard-api-nh7v.onrender.com/record", json={"value": 0})
else:
    r = requests.post("https://avibot-dashboard-api-nh7v.onrender.com/record", json={"value": 1})

print("second")
label = "Cracked" if pred < 0.5 else "Uncracked"
confidence = 1 - pred if pred < 0.5 else pred


print(f"{label} ({confidence*100:.2f}%)")
plt.imshow(img)
plt.title(f"{label} ({confidence*100:.2f}%)")
plt.axis('off')
plt.show()