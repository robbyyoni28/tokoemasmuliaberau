from flask import Flask,render_template, request, redirect, url_for, Response, session, jsonify, flash, send_file, send_from_directory
import requests
import pymysql.cursors, os
import hashlib
import json
from passlib.hash import sha256_crypt
import io
import os
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
# from datetime import *
import datetime

app = Flask(__name__)
app.secret_key = "fVck_1D34LiS"
UPLOAD_FOLDER = 'static/uploads/'
# UPLOAD_FOLDER_PERATURAN = 'static/uploads_peraturan/'
app.secret_key = "fVck_1D34LiS"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['UPLOAD_FOLDER_PERATURAN'] = UPLOAD_FOLDER_PERATURAN
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xls', 'xml','doc','csv','dot','exe','rar', 'zip','docx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        cursor.execute(f"SELECT id_barang FROM db_toko.barang order by id_barang desc limit 1; ")
        id_barang = cursor.fetchall()
        print(id_barang)
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

    
    return render_template("table.html",sess_data=session, penjualan=penjualan, barang=barang, id_barang=id_barang )

# @app.route('/api_id_barang', methods=['GET','POST'])
# def api_id_barang():
#     connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
#     with connection.cursor() as cursor:
#         cursor.execute(f"SELECT id_barang FROM db_toko.barang order by id_barang desc limit 1; ")
#         id_barang = cursor.fetchall()
#         print(id_barang)
#         if id_barang is None:
#                 return jsonify("data tidak ditemukan oleh server", status=404)
#         else:
#             return jsonify({"msg": 'You Are Logged Succesfully', "userdata":id_barang} )

@app.route('/tambah', methods=['GET','POST'])
def tambah():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No pdf selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        iso8601 = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        filename = secure_filename(file.filename)
        NOW = datetime.datetime.now()
        new_filename = os.path.join(NOW.strftime("%d_%m_%Y_%H_%M_%S") + '.' + file.filename.rsplit('.',1)[1])
        # filename = secure_filename(file.datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        upload_idbarang = request.form['id_barang']
        upload_nmbarang = request.form['nama_barang']
        upload_merk = request.form['merk_barang']
        upload_hargajual = request.form['harga_jual']
        upload_satuanbarang = request.form['satuan_barang']
        upload_stokbarang = request.form['stok_barang']
        
        # nama_download = os.path.join(request.form['nama_file']+ '.' + file.filename.rsplit('.',1)[1])
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.new_filename)))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO barang (id_barang, nama_barang, merk, harga_jual, satuan_barang,stok,tgl_input, filename) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",(upload_idbarang,upload_nmbarang, upload_merk,upload_hargajual,upload_satuanbarang,upload_stokbarang, iso8601, new_filename))
        connection.commit()

#print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return redirect(url_for('table'))
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/update', methods=['POST'])
def update():
    # if 'file' not in request.files:
    #     flash('No file part')
    #     return redirect(request.url)
    # file = request.files['file']
    # if file.filename == '':
    #     flash('No pdf selected for uploading')
    #     return redirect(request.url)
    # if file and allowed_file(file.filename):
    #     iso8601 = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
    #     filename = secure_filename(file.filename)
    #     NOW = datetime.datetime.now()
    #     new_filename = os.path.join(NOW.strftime("%d_%m_%Y_%H_%M_%S") + '.' + file.filename.rsplit('.',1)[1])
        # filename = secure_filename(file.datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    if request.method == 'POST':
        request.form = request.json
        upload_id = request.form['mdl_update_id']
        upload_idbarang = request.form['upd_id_barang']
        upload_nmbarang = request.form['upd_nama_barang']
        upload_merk = request.form['upd_merk_barang']
        upload_hargajual = request.form['upd_harga_jual']
        upload_satuanbarang = request.form['upd_satuan_barang']
        upload_stokbarang = request.form['upd_stok_barang']
        upload_tglinput = request.form['mdl_update_inputtgl']
        upload_file = request.form['mdl_update_file']
        iso8601 = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        
        # nama_download = os.path.join(request.form['nama_file']+ '.' + file.filename.rsplit('.',1)[1])
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.new_filename)))
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE barang SET id_barang = '{upload_idbarang}', nama_barang = '{upload_nmbarang}', merk = '{upload_merk}', harga_jual = '{upload_hargajual}', satuan_barang = '{upload_satuanbarang}', stok = '{upload_stokbarang}',tgl_input = '{upload_tglinput}',filename ='{upload_file}', tgl_update = '{iso8601}' WHERE id = '{upload_id}'")
            # cursor.execute(f"INSERT INTO barang (id_barang, nama_barang, merk, harga_jual, satuan_barang,stok,tgl_update, filename) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",(upload_idbarang,upload_nmbarang, upload_merk,upload_hargajual,upload_satuanbarang,upload_stokbarang, iso8601, new_filename))
        connection.commit()
        return redirect(url_for('table'))
#print('upload_image filename: ' + filename)
    #     flash('Image successfully uploaded and displayed below')
    #     return redirect(url_for('table'))
    # else:
    #     flash('Allowed image types are -> png, jpg, jpeg, gif')
    #     return redirect(request.url)


# @app.route('/detail/<id_barang>', methods=['GET','POST'])
# def detail(id_barang):
#     if request.method == 'POST':
       
    
#         inputan_idbarang = request.form['detail_id']
#         connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
#         with connection.cursor() as cursor:
#             cursor.execute(f"SELECT * FROM barang WHERE id_barang='{id_barang}' ")
#             detail = cursor.fetchone()
#             print(detail)
#     # if len(session) == 0:
#     #     return redirect('/?msg=SESSION_KOSONG')
    
#     return render_template("table.html",detail=detail)


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


@app.route('/delete/<filename>', methods=['GET','POST'])
def delete(filename):
    full_path =  os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM barang WHERE filename = '{filename}'   ")
        connection.commit()
        return redirect(url_for('table'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/?msg=ANDA_SUDAH_LOGOUT')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)