# -*- coding: UTF-8 -*-

import flask
from flask import *
import pymysql
# import hashlib

# 创建Flask程序并定义模板位置
app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            template_folder='templates'
            )


# 将所有对主页面的访问都跳转到登录框
@app.route('/', methods=['GET', 'POST'])
def index():
    return flask.redirect(flask.url_for('log_in'))


@app.route('/log_handle', methods=['POST'])
def log_handle():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # encrypass = hashlib.md5()
        # encrypass.update(password.encode(encoding='utf-8'))
        # password = encrypass.hexdigest()

        db = pymysql.connect(host="localhost", user="root", password="root", db="data")
        cursor = db.cursor()

        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        print(sql)
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()

        db.close()

        if user is None:
            return flask.render_template("log_fail.html")
        else:
            # return flask.render_template("log_success.html", username=username)
            return redirect("http://39.107.97.152:8077/#/home")



# 处理注册
@app.route('/register_handle', methods=['POST'])
def register_handle():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password == confirm_password:
            # 对密码进行加密处理
            # encrypass = hashlib.md5()
            # encrypass.update(password.encode(encoding='utf-8'))
            # password = encrypass.hexdigest()

            db = pymysql.connect(host="localhost", user="root", password="root", db="data")
            cursor = db.cursor()

            search_sql = "SELECT * FROM users"
            cursor.execute(search_sql)
            # cursor.fetchall()返回的结果是一个元组的列表
            user_list = []

            # 将查询结果转换为列表字典
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                user_dict = dict(zip(columns, row))
                user_list.append(user_dict)


            # 判断是否存在相同用户名
            if any(user['username'] == username for user in user_list):
                have_same_username = 1
                return flask.render_template("register_fail.html", have_same_username=have_same_username)

            # 将用户名和加密后的密码插入数据库
            sql = "INSERT INTO users VALUES('%s', '%s')" % (username, password)
            cursor.execute(sql)
            db.commit()

            db.close()
            return flask.redirect(flask.url_for('log_in'))

        else:
            two_passwd_wrong = 1
            return flask.render_template("register_fail.html", two_passwd_wrong=two_passwd_wrong)


@app.route('/log_in', methods=['GET'])
def log_in():
    return render_template('log_in.html')


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/log_success')
def log_success():
    return render_template('log_success.html')


# 自定义404页面
@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template("404.html"), 404


if __name__ == '__main__':
    # 调试时需要debug=True
    app.run()
