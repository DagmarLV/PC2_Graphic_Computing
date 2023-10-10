from github import Github
import tempfile
import os
from flask import Flask, request, redirect, send_file, render_template
from skimage import io
import base64
import glob
import numpy as np

username = 'DagmarLV'
access_token = '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'
github_repo_name = 'PC2_Graphic_Computing'

g = Github(access_token)

repo = g.get_user().get_repo(github_repo_name)

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # check if the post request has the file part
        img_data = request.form.get('myImage').replace("data:image/png;base64,","")
        aleatorio = request.form.get('numero')
        print(aleatorio)
        with tempfile.NamedTemporaryFile(delete = False, mode = "w+b", suffix='.png', dir=str(aleatorio)) as fh:
            fh.write(base64.b64decode(img_data))
            
        file_path = f"aleatorio/{os.path.basename(fh.name)}"
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
    with open('X.npy', 'rb') as file:
        repo.create_file('X.npy', 'Uploading X.npy file', base64.b64encode(file.read()).decode())

    with open('y.npy', 'rb') as file:
        repo.create_file('y.npy', 'Uploading y.npy file', base64.b64encode(file.read()).decode())

    
    return "OK!"

@app.route('/X.npy', methods=['GET'])
def download_X():
    return send_file('./X.npy')
@app.route('/y.npy', methods=['GET'])
def download_y():
    return send_file('./y.npy')

if __name__ == "__main__":
    digits = ["owo", "unu", "uwu","7u7"]
    for d in digits:
        if not os.path.exists(str(d)):
            os.mkdir(str(d))
    app.run()
