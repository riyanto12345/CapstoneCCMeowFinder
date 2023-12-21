import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import io
import tensorflow as tf
from tensorflow import keras
import numpy as np
from flask import Flask, request, jsonify
import tensorflow_hub as hub
import pandas as pd
from tensorflow.keras.models import load_model
import json
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img




model = keras.models.load_model("Model_meowfinder.h5", )

def read_image(file_path):
    image = load_img(file_path, target_size=(200, 300, 3))
    image = img_to_array(image)
    image /= 255
    x = np.expand_dims(image, axis=0)
    return x

def test_single_image(image_array):
    df = pd.read_excel('kucing.xlsx')

    view = ['Bengal', 'Domestic Shorthair', 'Maine Coon', 'Ragdoll', 'Siamese']

    classes = model.predict(image_array, batch_size=1)

    predicted_class_index = classes.argmax()


    predicted_label = view[predicted_class_index]

    
    top_classes = 5  
    top_class_indices = np.argsort(classes)[0, ::-1][:top_classes]

    kucing_terdeteksi = []

   
    print("Kucing: ")
    for index in top_class_indices:
        label = view[index]
        prob = classes[0, index]
        if prob > 0.75:
            print(f"{label}: {prob:.4f}")
            kucing_terdeteksi.append(label)
            # print(label)
    data_to_send = {"Ras Kucing": kucing_terdeteksi}

    
    hasil_deteksiKucing = {}

    for label in kucing_terdeteksi:
        query_pattern = label
        kondisi = [df['ras'].str.contains(query_pattern, case=False, regex=True, na=False) for query_pattern in
                      kucing_terdeteksi]
        result_df = df[pd.DataFrame(kondisi).all(axis=0)]

        for index, row in result_df.iterrows():
            nama = row['ras']
            foto = row['link']
            deskripsi = row['deskripsi']
           
            hasil_deteksiKucing[index] = {'Ras':nama, ' foto':foto, 'deskripsi':deskripsi}
    return hasil_deteksiKucing

app = Flask(__name__)


from collections import OrderedDict

# ...

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

            # Ubah dari objek menjadi array
            data_array = []  # Hapus header yang sebelumnya ditambahkan

            for key, value in prediction.items():
                ras = value['Ras']
                foto = value[' foto']
                deskripsi = value['deskripsi']
                
                # Format data kucing menjadi objek dengan urutan properti
                kucing_data = OrderedDict([('Ras', ras), ('Foto', foto), ('Deskripsi', deskripsi)])
                data_array.append(kucing_data)

            return jsonify({
                "status": {
                    "code": 200,
                    "message": "Success predicting"
                },
                "data": data_array
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)})
    return "Service MeowFinder Aktiff"

# ...






if __name__ == "__main__":
    app.run(debug=True)



