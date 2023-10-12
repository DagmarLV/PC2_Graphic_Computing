from github import Github
import tempfile
import os
from flask import Flask, request, redirect, send_file, render_template
from tensorflow.python.keras.models import load_model
from skimage import io
import base64
import glob
import numpy as np
import cv2


username = 'DagmarLV'
access_token = os.environ.get("token")
github_repo_name = 'PC2_Graphic_Computing'

g = Github(access_token)

repo = g.get_user().get_repo(github_repo_name)

modelo_cargado = load_model('modelo_entrenado.h5')

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        
        img_data = request.form.get('myImage').replace("data:image/png;base64,","")
        aleatorio = request.form.get('numero')
        print(aleatorio)
        with tempfile.NamedTemporaryFile(delete = False, mode = "w+b", suffix='.png', dir=str(aleatorio)) as fh:
            fh.write(base64.b64decode(img_data))
            
        file_path = f"{aleatorio}/{os.path.basename(fh.name)}"
        repo.create_file(file_path, f"Uploading {aleatorio} image", open(fh.name, 'rb').read(), branch="main")
       
        print("Image uploaded")
    except Exception as err:
        print("Error occurred")
        print(err)

    return redirect("/", code=302)


@app.route('/prepare', methods=['GET'])
def prepare_dataset():
    images = []
    d = ["owo", "unu", "uwu","7u7"]
    digits = []
    for digit in d:
      filelist = glob.glob('{}/*.png'.format(digit))
      images_read = io.concatenate_images(io.imread_collection(filelist))
      images_read = images_read[:, :, :, 3]
      digits_read = np.array([d.index(digit)] * images_read.shape[0], dtype=np.int32)
      images.append(images_read)
      digits.append(digits_read)
   
    images = np.vstack(images)
    digits = np.concatenate(digits)
    np.save('X.npy', images)
    np.save('y.npy', digits)
    
    return "El dataset se ha generado exitosamente"

@app.route('/X.npy', methods=['GET'])
def download_X():
    return send_file('./X.npy')
@app.route('/y.npy', methods=['GET'])
def download_y():
    return send_file('./y.npy')

@app.route('/predict')
def predict_page():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        img_data = request.form.get('myImage').replace("data:image/png;base64,","")
        img_binary = base64.b64decode(img_data)
        image = cv2.imdecode(np.frombuffer(img_binary, np.uint8), cv2.IMREAD_COLOR)
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_resized = cv2.resize(img_gray, (28, 28))
        img_array = img_resized.reshape(1, 28, 28, 1)

        prediction = modelo_cargado.predict(img_array)
        print(prediction)
        etiquetas = {0: "owo", 1: "unu", 2: "uwu", 3: "7u7"}

        valor = np.argmax(prediction)

        if valor in etiquetas:
            kind = etiquetas[valor]
            print(f"Kind: {kind}")
        else:
            print("El valor predicho no tiene una etiqueta asociada.")
     
        print("Image charged")
        return render_template('predict.html',value=kind)  
            
    except Exception as err:
        print("Error occurred")
        print(err)


if __name__ == "__main__":
    digits = ["owo", "unu", "uwu","7u7"]
    for d in digits:
        if not os.path.exists(str(d)):
            os.mkdir(str(d))
    app.run()
