import datetime
import firebase_admin
import pysnooper
from firebase_admin import firestore
from password_generator import PasswordGenerator
from flask import Flask, request

# 初期化済みのアプリが存在しないか確認する。
if len(firebase_admin._apps) == 0:
    # アプリを初期化する
    default_app = firebase_admin.initialize_app()
db = firestore.client()

'''
ワンタイムパスワードの生成
'''


@pysnooper.snoop()
def create_one_password(request):
    if request.method == 'GET':
        return "GETリクエストは使用できません。"

    request_json = request.get_json()

    # パメータの指定が誤っている場合
    if request_json and "name" in request_json and "password" in request_json:
        user_name = request_json["name"]
        password = request_json["password"]

    else:
        return "引数が正確ではありません。"

    # ユーザ-名誉とパシワードのチェック
    if not check_personal_date(user_name=user_name, password=password):
        return "登録ユーザが存在しないか、ユーザ、パスワードが間違っています。"

    # パスワードの生成
    one_password = password_generater()

    # DBへの挿入
    insert_password(user_name, one_password)

    return one_password


'''
ユーザ名とパスワードのチェック
'''


def check_personal_date(user_name, password):
    doc_ref = db.collection(u'Users').document(user_name)
    doc_list = doc_ref.get().to_dict()

    if doc_list is None:
        return False

    if doc_list["user_name"] == user_name and doc_list["password"] == password:
        return True

    return False


'''
パスワードの生成
'''


def password_generater():
    pwo = PasswordGenerator()
    pwo.minlen = 15
    pwo.maxlen = 20

    return pwo.generate()


'''
パスワードの挿入
'''


def insert_password(user_name, password):
    data = {
        u'user_name': user_name,
        u'password': password,
        u'limit_time': str(datetime.datetime.now() + datetime.timedelta(minutes=1))
    }
    try:
        db.collection(u'PersonalOneTimePassword').document(user_name).set(data)
    except:
        return False

    return True


'''
個別実行テスト用
'''
if __name__ == "__main__":
    app = Flask(__name__)


    @app.route('/', methods=['GET', 'POST'])
    def index():
        return create_one_password(request)


    app.run(port=50000, debug=True)
