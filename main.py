#!/Users/hoyi/opt/anaconda3/bin/python
from flask import Flask, render_template, request, jsonify,url_for
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sa:Passw0rd@localhost/register'
db = SQLAlchemy(app)

#資料庫registers
class registers(db.Model):
    account_number = db.Column(db.String(20), primary_key=True, nullable=False)
    password_number = db.Column(db.String(20), nullable=False)

#資料庫like_animail
class like_animail(db.Model):
    __tablename__ = 'like_animail'
    account_number = db.Column(db.String(20), primary_key=True, nullable=False)
    animal = db.Column(db.String(20), nullable=False)


 # 登入頁面
@app.route("/login1", methods=['GET', 'POST'])
def login1():
    return render_template('login.html')

# 判斷登入
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        Compare = registers.query.filter_by(account_number=username, password_number=password).first()
        if Compare:
            return render_template('糖尿病單張照片上傳區.html')
        else:
            return render_template('login_false.html', message="登入失敗，帳號或密碼錯誤")
    else:
        return render_template('login_false.html')


# 註冊帳號
@app.route("/register", methods=['GET'])
def register():
    return render_template('register.html')


# 判斷註冊
@app.route("/register_success", methods=['POST'])
def register_success():
    username = request.form['username']
    password = request.form['password']
    Like_animal = request.form['Like_animal']

    existing_user = registers.query.filter_by(account_number=username).first()
    if existing_user:
        return render_template('register_fail.html', message="帳號已經存在，換一個")

    if not username or not password or not Like_animal:
        return render_template('register_fail.html', message="請填寫所有的欄位")

    new_register = registers(account_number=username, password_number=password)
    new_animal = like_animail(account_number=username, animal=Like_animal)
    db.session.add(new_register)
    db.session.add(new_animal)
    db.session.commit()
    return render_template('register_success.html', message="註冊成功")


# 找回密碼
@app.route("/Findpassword", methods=['GET'])
def Findpassword():
    return render_template('Findpassword.html')


# 判斷找回密碼
@app.route("/Findpassword_success", methods=['POST'])
def find_password_success():
    username = request.form['username']
    password = request.form['password']
    Like_animal = request.form['Like_animal']

    Compare = like_animail.query.filter_by(account_number=username, animal=Like_animal).first()

    if Compare:
        Newuser = registers.query.filter_by(account_number=username).first()
        Newuser.password_number = password
        db.session.commit()
        return render_template('findpassword_success.html', message="密碼更新成功")

    else:
        return render_template('findpassword_fail.html', message="帳號或動物驗證錯誤")


# 刪除帳號
@app.route("/Deleteaccount", methods=['GET'])
def Deleteaccount():
    return render_template('Deleteaccount.html')


# 判斷刪除帳號
@app.route("/Deleteaccount_successful", methods=['GET', 'POST'])
def Deleteaccount_successful():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        Like_animal = request.form['Like_animal']

        Compare = registers.query.filter_by(account_number=username, password_number=password).first()
        Compare1 = like_animail.query.filter_by(account_number=username, animal=Like_animal).first()

        if Compare:
            if Compare1:
                db.session.delete(Compare)
                db.session.delete(Compare1)
                db.session.commit()
                return render_template('deleteaccount_success.html', message="成功刪除帳號")
            else:
                return render_template('deleteaccount_false.html', message="帳號或密碼或動物驗證錯誤")
        else:
            return render_template('deleteaccount_false.html', message="帳號或密碼或動物驗證錯誤")
    else:
        return render_template('deleteaccount_false.html')


model = load_model('/Users/hoyi/CGI/cgi-bin/CNNmodel1.h5')

@app.route("/index", methods=['GET'])
def index():
    return render_template('糖尿病單張照片上傳區.html')

@app.route("/againload1", methods=['GET'])
def againload1():
    return render_template('糖尿病單張照片上傳區.html')

@app.route("/twice", methods=['GET'])
def twice():
    return  render_template('糖尿病多張照片上傳區.html')

@app.route("/startread1", methods=['POST'])
def startread1():
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
