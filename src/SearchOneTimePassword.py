import datetime
import json

import firebase_admin
import pysnooper
from firebase_admin import firestore

# 初期化済みのアプリが存在しないか確認する。
from flask import Flask, request

if len(firebase_admin._apps) == 0:
    # アプリを初期化する
    default_app = firebase_admin.initialize_app()
db = firestore.client()

'''
ワンタイムパスワードの検索
'''


@pysnooper.snoop()
def search_one_password(request):
    if request.method == 'GET':
        return "GETリクエストは使用できません。"

    request_json = request.get_json()

    # パメータの指定が誤っている場合
    if request_json and "name" in request_json and "password" in request_json:
        user_name = request_json["name"]
        password = request_json["password"]

    else:
        return "引数が正確ではありません。"

    # ユーザ-名とパシワードのチェック
    return json.dumps(check_personal_date(user_name=user_name, password=password))


'''
ユーザ名とパスワードのチェック
'''


def check_personal_date(user_name, password):
    doc_ref = db.collection(u'PersonalOneTimePassword').document(user_name)
    doc_list = doc_ref.get().to_dict()

    if doc_list is None:
        return False

    # str -> datetime
    # FIXME firestore自体がtimestampで保存して、DatetimeWithNanosecondsで返却されるから比較できない。
    limit_time_str = doc_list["limit_time"].split(".")[0]
    limit_time = datetime.datetime.strptime(limit_time_str, '%Y-%m-%d %H:%M:%S')

    if doc_list["user_name"] == user_name and doc_list["password"] == password and limit_time > datetime.datetime.now():
        return True

    return False


'''
個別実行テスト用
'''
if __name__ == "__main__":
    app = Flask(__name__)


    @app.route('/', methods=['GET', 'POST'])
    def index():
        return search_one_password(request)


    app.run(port=50001, debug=True)
