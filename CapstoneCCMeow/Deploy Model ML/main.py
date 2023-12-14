import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import io
import tensorflow as tf
from tensorflow import keras
import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from tensorflow.keras.models import load_model
import tensorflow_hub as hub
import time
import pandas as pd
import json

# Fungsi ini digunakan untuk mendaftarkan objek khusus
# def load_keras_layer():
#     return KerasLayer

# path = 'Model_meowfinder.h5'
# model = tf.keras.models.load_model(
#        (path),
#        custom_objects={'KerasLayer':hub.KerasLayer}
# )
# model = keras.models.load_model("Model_meowfinder.h5", custom_objects={'KerasLayer': load_keras_layer})
model = keras.models.load_model("Model_meowfinder.h5", )

def read_image(file_path):
    image = load_img(file_path, target_size=(200, 300, 3))
    image = img_to_array(image)
    image /= 255
    
    x = np.expand_dims(image, axis=0)
    return x

def test_single_image(image_array):
    df = pd.read_excel('kucing.xlsx')

    # images = np.expand_dims(image_array, axis=0)
    view = ['Bengal', 'Domestic_Shorthair', 'Maine_Coon', 'Ragdoll' , 'Siamese']
    # time.sleep(.5)

    classes = model.predict(image_array, batch_size=1)

    # Mengambil indeks kelas dengan probabilitas tertinggi
    predicted_class_index = classes.argmax()

    # Mengonversi indeks kelas menjadi label
    predicted_label = view[predicted_class_index]

    # Mengambil indeks kelas dengan probabilitas tertinggi
    top_classes = 31  # Mengambil 5 kelas dengan probabilitas tertinggi
    top_class_indices = np.argsort(classes)[0, ::-1][:top_classes]

    ingredients_detected = []

    # Menampilkan label berdasarkan probabilitas tertinggi
    print("Kucing: ")
    for index in top_class_indices:
        label = view[index]
        prob = classes[0, index]
        if prob > 0.05:
            print(f"{label}: {prob:.4f}")
            ingredients_detected.append(label)
            # print(label)
    data_to_send = {"Ras Kucing": ingredients_detected}

    # Menyimpan nilai dalam variabel global
    detected_results = {}

    for label in ingredients_detected:
        query_pattern = label
        conditions = [df['ras'].str.contains(query_pattern, case=False, regex=True, na=False) for query_pattern in
                      ingredients_detected]


        result_df = df[pd.DataFrame(conditions).all(axis=0)]


        for index, row in result_df.iterrows():
            nama = row['ras']
            foto = row['link']
            deskripsi = row['deskripsi']
            # url = row['URL']


            detected_results[index] = {'Ras':nama, ' foto':foto, 'deskripsi':deskripsi}

    return detected_results

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            file.save('static/uploads/file.jpg')
            tensor = read_image('static/uploads/file.jpg')
            prediction = test_single_image(tensor)


            json_data = json.dumps(prediction, indent=2)
            return jsonify({
                "status": {
                    "code": 200,
                    "message": "Success predicting"
                },
                "data": json.loads(json_data)  # mengonversi string JSON kembali menjadi objek Python
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)})

    # else:
    #     return jsonify({
    #         "status": {
    #             "code": 405,
    #             "message": "Method not allowed"
    #         },
    #         "data": None,
    #     }), 405

    return "Service Activated"


if __name__ == "__main__":
    app.run(debug=True)



