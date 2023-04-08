from flask import Flask,render_template, request, redirect, url_for, Response, session, jsonify, flash, send_file, send_from_directory
import pymysql.cursors, os
import hashlib
from passlib.hash import sha256_crypt
import io
import os
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
# from datetime import *
import datetime


app = Flask(__name__)
app.secret_key = "fVck_1D34LiS"


@app.route('/',methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        session.clear()
        return render_template('sign-in.html')
    if request.method == 'POST':
        request.form = request.json
    
        inputan_username = request.form['inputan_username']
        inputan_password = request.form['inputan_password']
        submitted_device_hash = request.cookies.get('device_hash')
        string=inputan_password
        encoded=string.encode()
        result = hashlib.sha256(encoded)
        hasil_hash = result.hexdigest()

    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM member WHERE username='{inputan_username}' AND password='{hasil_hash}'")
        satudata = cursor.fetchone()
        print(satudata)
        if satudata is None:
            return Response("data tidak ditemukan oleh server", status=404)
        if satudata['level'] == 'admin' :
            session['USER_ID'] = satudata['id_member']
            session['USER_FULL_NAME'] = satudata['nm_member']
            session['USERNAME'] = satudata['username']
            # session['LEVEL'] = satudata['level']
            # session['USER_KETERANGAN'] = satudata['id_jkdt']
            return Response("data ditemukan oleh server", status=200)


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    # if len(session) == 0:
    #     return redirect('/?msg=SESSION_KOSONG')
    
    return render_template("dashboard.html",sess_data=session)

@app.route('/table', methods=['GET','POST'])
def table():
    # if len(session) == 0:
    #     return redirect('/?msg=SESSION_KOSONG')

    if len(session) == 0:
        return redirect('/?msg=SESSION_KOSONG')

    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM barang")
        barang = cursor.fetchall()
        print(barang)
    
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT penjualan.id_barang, member.nm_member, penjualan.jumlah, penjualan.total, penjualan.tanggal_input FROM penjualan INNER JOIN member ON penjualan.id_member = penjualan.id_member;")
        penjualan = cursor.fetchall()
        print(penjualan)

    
    return render_template("table.html",sess_data=session, penjualan=penjualan, barang=barang)

@app.route('/billing', methods=['GET','POST'])
def billing():
    # if len(session) == 0:
    #     return redirect('/?msg=SESSION_KOSONG')
    
    return render_template("billing.html",sess_data=session)

@app.route('/profil', methods=['GET','POST'])
def profil():
    # if len(session) == 0:
    #     return redirect('/?msg=SESSION_KOSONG')
    
    return render_template("profile.html",sess_data=session)

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/?msg=ANDA_SUDAH_LOGOUT')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)