#!/Users/hoyi/opt/anaconda3/bin/python
from flask import Flask, render_template, request, jsonify,url_for
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

app = Flask(__name__)
model = load_model('/Users/hoyi/CGI/cgi-bin/CNNmodel.h5')

@app.route("/index", methods=['GET'])
def index():
    return render_template('糖尿病單張照片上傳區.html')

@app.route("/againload1", methods=['GET'])
def againload1():
    return render_template('糖尿病單張照片上傳區.html')


@app.route("/startread1", methods=['POST'])
def startread1():
    # 從 request.files 中獲取檔案
    file = request.files['file']

    file_name_from_frontend = request.form.get('fileName', '')

    file.save('/Users/hoyi/CGI/cgi-bin/pictures/' + file_name_from_frontend)

    img = Image.open('/Users/hoyi/CGI/cgi-bin/pictures/' + file_name_from_frontend)
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    predicted_class = int(np.argmax(prediction))
    # print(prediction_class)
    return jsonify({'predicted_class': predicted_class})

if __name__ == '__main__':
    app.run(debug=True)


