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
import qrcode
import image
from flask_qrcode import QRcode
import pdfkit
import random
from datetime import timedelta
import xlwt
from datetime import datetime
import locale


# from datetime import *
import datetime

app = Flask(__name__)
# wkhtmltopdf = Wkhtmltopdf(app)
app.secret_key = "fVck_1D34LiS"
app.config['PROPAGATE_EXCEPTIONS'] = True
UPLOAD_FOLDER = 'static/uploads/'
# UPLOAD_FOLDER_PERATURAN = 'static/uploads_peraturan/'
app.secret_key = "fVck_1D34LiS"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PDF_FOLDER'] = 'static/pdf/'
app.config['TEMPLATE_FOLDER'] = 'templates/'
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
    if len(session) == 0:
        return redirect('/?msg=SESSION_KOSONG')
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # request.form = request.json
        # addcart_id = request.form['upd_id_barang']
        cursor.execute(f"SELECT COUNT(id) AS hitung FROM barang")
        hitungbarang = cursor.fetchall()
        print(hitungbarang)

    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # request.form = request.json
        # addcart_id = request.form['upd_id_barang']
        cursor.execute(f"SELECT COUNT(id_penjualan) AS hitungtransaksi FROM penjualan")
        hitungtransaksi = cursor.fetchall()
        print(hitungtransaksi)

    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # request.form = request.json
        # addcart_id = request.form['upd_id_barang']
        cursor.execute(f"SELECT dayname(tanggal_transaksi) as DATE , format(SUM(`total`) ,2, 'de_DE') as totalCOunt, MAX(tanggal_aja) as tanggal, count(distinct(id_transaksi)) as perday FROM penjualan GROUP BY  DATE(tanggal_transaksi) ORDER BY tanggal desc LIMIT 7 OFFSET 1")
        transaksiperweek = cursor.fetchall()
        print(transaksiperweek)

    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # request.form = request.json
        # addcart_id = request.form['upd_id_barang']
        cursor.execute(f"SELECT count(id) as barangmasuk from `barang` WHERE DATE(`tgl_input`) = CURDATE()")
        inputbarangperday = cursor.fetchall()
        print(inputbarangperday)
    
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # request.form = request.json
        # addcart_id = request.form['upd_id_barang']
        cursor.execute(f"SELECT count(id_penjualan) as barang_keluar from penjualan where tanggal_aja = curdate();")
        outputbarangperday = cursor.fetchall()
        print(outputbarangperday)

    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # request.form = request.json
        # addcart_id = request.form['upd_id_barang']
        cursor.execute(f"SELECT count(distinct(id_transaksi)) as total_transaksi from penjualan where tanggal_aja = curdate();")
        transaksiperday = cursor.fetchall()
        print(transaksiperday)
    
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # request.form = request.json
        # addcart_id = request.form['upd_id_barang']
        cursor.execute(f"SELECT FORMAT(sum(total),2, 'id_ID') as total_penjualan from penjualan where tanggal_aja = curdate();")
        penjualanperday = cursor.fetchall()
        print(penjualanperday)

    return render_template("dashboard.html",sess_data=session,hitungbarang=hitungbarang, hitungtransaksi=hitungtransaksi, transaksiperweek=transaksiperweek, inputbarangperday=inputbarangperday, outputbarangperday=outputbarangperday, transaksiperday=transaksiperday, penjualanperday=penjualanperday)


@app.route('/apireport7day', methods=['GET','POST'])
def apireport7day():
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # request.form = request.json
        # addcart_id = request.form['upd_id_barang']
        cursor.execute(f"SELECT max(tanggal_transaksi) as DATE , format(SUM(`total`) ,2, 'de_DE') as totalCOunt, MAX(tanggal_aja) as tanggal, count(distinct(id_transaksi)) as perday FROM penjualan GROUP BY  DATE(tanggal_transaksi) ORDER BY tanggal desc LIMIT 7 OFFSET 1")
        transaksiperweek = cursor.fetchall()
        print(transaksiperweek)

        if transaksiperweek is None:
            return jsonify("data tidak ditemukan oleh server", status=404)
        else:
            return jsonify({"transaksiperweek":transaksiperweek})

@app.route('/table', methods=['GET','POST'])
def table():
    # if len(session) == 0:
    #     return redirect('/?msg=SESSION_KOSONG')

    if len(session) == 0:
        return redirect('/?msg=SESSION_KOSONG')
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id FROM db_toko.barang order by id desc limit 1; ")
        id_barang = cursor.fetchall()
        print(id_barang)
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT LPAD(id,9,'BR-00000') as modifankamu, nama_barang, filename, gram, qrcode, kadar, tgl_input ,kodeqr, tgl_new FROM db_toko.barang;")
        barang = cursor.fetchall()
        print(barang)
    
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT penjualan.id_barang, member.nm_member, penjualan.jumlah, penjualan.total, penjualan.tanggal_transaksi FROM penjualan INNER JOIN member ON penjualan.id_member = penjualan.id_member;")
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
        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=12,border=2)
        iso8601 = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        filename = secure_filename(file.filename)
        NOW = datetime.datetime.now()
        new_filename = os.path.join(NOW.strftime("%d_%m_%Y_%H_%M_%S") + '.' + file.filename.rsplit('.',1)[1])
        # filename = secure_filename(file.datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        # upload_idbarang = request.form['id_barang']
        upload_nmbarang = request.form['nama_barang']
        # upload_merk = request.form['merk_barang']
        # upload_hargajual = request.form['harga_jual']
        upload_grambarang = request.form['gram_barang']
        kadar = request.form['kadar']
        tgl_new = request.form['waduhai']
        # upload_stokbarang = request.form['stok_barang']
        random_number = random.randint(1, 10000000000) * 2 + 1
        qr.add_data(random_number)
        qr.make(fit =True)
        img = qr.make_image(fill = 'Black',back_color = 'White')
        new_filenamebarcode = os.path.join(NOW.strftime("%d_%m_%Y_%H_%M_%S_barcode.png"))
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filenamebarcode)) 
        # nama_download = os.path.join(request.form['nama_file']+ '.' + file.filename.rsplit('.',1)[1])
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.new_filename)))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO barang (nama_barang, gram,tgl_input, filename, qrcode,kadar, kodeqr, tgl_new) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)",(upload_nmbarang, upload_grambarang, iso8601, new_filename, new_filenamebarcode, kadar, random_number, tgl_new))
        connection.commit()

#print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return redirect(url_for('table'))
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/update', methods=['POST'])
def update():
    
    if request.method == 'POST':
        request.form = request.json
        upload_id = request.form['mdl_update_id']
        upload_idbarang = request.form['upd_id_barang']
        upload_nmbarang = request.form['upd_nama_barang']
        # upload_merk = request.form['upd_merk_barang']
        upload_gram = request.form['upd_gram']
        # upload_satuanbarang = request.form['upd_satuan_barang']
        # upload_stokbarang = request.form['upd_stok_barang']
        upload_tglinput = request.form['mdl_update_inputtgl']
        upload_file = request.form['mdl_update_file']
        iso8601 = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        
     
        connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE barang SET id_barang = '{upload_idbarang}', nama_barang = '{upload_nmbarang}',gram = '{upload_gram}', tgl_input = '{iso8601}',filename ='{upload_file}' WHERE id = '{upload_id}'")
            # cursor.execute(f"INSERT INTO barang (id_barang, nama_barang, merk, harga_jual, satuan_barang,stok,tgl_update, filename) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",(upload_idbarang,upload_nmbarang, upload_merk,upload_hargajual,upload_satuanbarang,upload_stokbarang, iso8601, new_filename))
        connection.commit()
        return redirect(url_for('table'))


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
    if len(session) == 0:
        return redirect('/?msg=SESSION_KOSONG')
    
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT LPAD(id,9,'BR-00000') as modifankamu, nama_barang, filename, gram, qrcode, kadar, tgl_input ,kodeqr FROM db_toko.barang")
        barang = cursor.fetchall()
        print(barang)

        cursor.execute(f"SELECT * FROM tb_cart")
        cart = cursor.fetchall()
        print(cart)

        cursor.execute(f"SELECT SUM(gram) FROM tb_cart")
        gram = cursor.fetchall()
        print(gram)

        cursor.execute(f"SELECT SUM(jumlah) AS jumlah FROM tb_cart")
        jumlah = cursor.fetchall()
        print(jumlah)

        cursor.execute(f"SELECT SUM(total) AS sub_total FROM tb_cart;")
        sub = cursor.fetchall()
        print(sub)

        
            
            # session['LEVEL'] = satudata['level']
            # session['USER_KETERANGAN'] = satudata['id_jkdt']
            # return Response("data ditemukan oleh server", status=200)
    
    return render_template("billing.html",sess_data=session, barang=barang, cart=cart, gram=gram, jumlah=jumlah,sub=sub)

@app.route("/totalan", methods=["GET", 'POST'])
def totalan():
    # Access the identity of the current user with get_jwt_identity
    if request.method == 'GET':

        connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT SUM(jumlah) AS jumlah FROM tb_cart")
            jumlah = cursor.fetchall()
            print(jumlah)

        # variabel koneksi tersebut kemudian di gunakan pada konteks with berikut sehingga pada blok with kita dapat mengakses variabel koneksi untuk kemudian kita gunakan untuk operasi CRUD ke DB
            if jumlah is None:
                return jsonify("data tidak ditemukan oleh server", status=404)
            else:
                return jsonify({"jumlah":jumlah})

@app.route("/sub", methods=["GET", 'POST'])
def sub():
    # Access the identity of the current user with get_jwt_identity
    if request.method == 'GET':

        connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT SUM(total) AS sub FROM tb_cart;")
            sub = cursor.fetchall()
            print(sub)

        # variabel koneksi tersebut kemudian di gunakan pada konteks with berikut sehingga pada blok with kita dapat mengakses variabel koneksi untuk kemudian kita gunakan untuk operasi CRUD ke DB
            if sub is None:
                return jsonify("data tidak ditemukan oleh server", status=404)
            else:
                return jsonify({"sub":sub})
            
@app.route("/totalinvo", methods=["GET", 'POST'])
def totalinvo():
    # Access the identity of the current user with get_jwt_identity
    if request.method == 'GET':

        connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT SUM(total) AS sub FROM tb_cart;")
            totalinvo = cursor.fetchall()
            print(totalinvo)

        # variabel koneksi tersebut kemudian di gunakan pada konteks with berikut sehingga pada blok with kita dapat mengakses variabel koneksi untuk kemudian kita gunakan untuk operasi CRUD ke DB
            if totalinvo is None:
                return jsonify("data tidak ditemukan oleh server", status=404)
            else:
                return jsonify({"totalinvo":totalinvo})

@app.route("/cutoff", methods=["GET", 'POST'])
def cutoff():
    # Access the identity of the current user with get_jwt_identity
    if request.method == 'GET':

        connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT SUM(potongan_harga2) AS cutoff FROM tb_cart")
            cutoff = cursor.fetchall()
            print(cutoff)

        # variabel koneksi tersebut kemudian di gunakan pada konteks with berikut sehingga pada blok with kita dapat mengakses variabel koneksi untuk kemudian kita gunakan untuk operasi CRUD ke DB
            if cutoff is None:
                return jsonify("data tidak ditemukan oleh server", status=404)
            else:
                return jsonify({"cutoff":cutoff})


@app.route('/transaksi', methods=['GET','POST'])
def transaksi():
    if len(session) == 0:
        return redirect('/?msg=SESSION_KOSONG')
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No pdf selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=12,border=2)
        iso8601 = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        filename = secure_filename(file.filename)
        NOW = datetime.datetime.now()
        new_filename = os.path.join(NOW.strftime("%d_%m_%Y_%H_%M_%S") + '.' + file.filename.rsplit('.',1)[1])
        # filename = secure_filename(file.datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        upload_idbarang = request.form['id_barang']
        upload_nmbarang = request.form['nama_barang']
        # upload_merk = request.form['merk_barang']
        # upload_hargajual = request.form['harga_jual']
        upload_grambarang = request.form['gram_barang']
        # upload_stokbarang = request.form['stok_barang']
        qr.add_data(upload_idbarang)
        qr.make(fit =True)
        img = qr.make_image(fill = 'Black',back_color = 'White')
        new_filenamebarcode = os.path.join(NOW.strftime("%d_%m_%Y_%H_%M_%S_barcode.png"))
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filenamebarcode)) 
        # nama_download = os.path.join(request.form['nama_file']+ '.' + file.filename.rsplit('.',1)[1])
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.new_filename)))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO barang (id_barang, nama_barang, gram,tgl_input, filename, qrcode) VALUES (%s, %s, %s, %s, %s, %s)",(upload_idbarang,upload_nmbarang, upload_grambarang, iso8601, new_filename, new_filenamebarcode))
            
        connection.commit()

#print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return redirect(url_for('table'))
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)
    
    


@app.route('/profil', methods=['GET','POST'])
def profil():
    # if len(session) == 0:
    #     return redirect('/?msg=SESSION_KOSONG')
    return render_template("profile.html",sess_data=session)


@app.route('/deleteallrow', methods=['GET','POST'])
def deleteallrow():
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM tb_cart")
            connection.commit()
            return redirect(url_for('billing'))

@app.route('/deleteallrowcart', methods=['DELETE'])
def deleteallrowcart():
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM tb_cart")
            connection.commit()
            return jsonify({"pesan": "sudah masuk"}), 200

@app.route('/deletedata/<filename>', methods=['DELETE'])
def deletedata(filename):
    
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM barang WHERE filename = '{filename}'   ")
        connection.commit()
        return jsonify({"pesan": "sudah terhapus"}), 200

@app.route('/delete/<filename>', methods=['GET','POST'])
def delete(filename):
    full_path =  os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM barang WHERE filename = '{filename}'   ")
        connection.commit()
        return redirect(url_for('table'))


@app.route('/deletecart/<filename>', methods=['GET','POST'])
def deletecart(filename):
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM tb_cart WHERE filename = '{filename}'   ")
        connection.commit()
        return redirect(url_for('billing'))

@app.route('/deletetransaksi/<id_transaksi>', methods=['GET','POST'])
def deletetransaksi(id_transaksi):
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM penjualan WHERE id_transaksi = '{id_transaksi}'   ")
        connection.commit()
        return redirect(url_for('invoice'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/?msg=ANDA_SUDAH_LOGOUT')


@app.route('/addcart', methods=['GET','POST'])
def addcart():
    if len(session) == 0:
        return redirect('/?msg=SESSION_KOSONG')
    if request.method == 'POST':
        request.form = request.json
        addcart_id = request.form['upd_id_barang']
        addcart_filename = request.form['ini']
        addcart_nama = request.form['upd_nama_barang']
        addcart_gram = request.form['gram_barang']
        # addcart_hargajual = request.form['harga_jual']
        # addcart_hargajual2 = request.form['harga_jual2']
        # addcart_potonganharga = request.form['potongan_harga']
        # addcart_potonganharga2 = request.form['potongan_harga2']
        addcart_tglinput = request.form['mdl_input']
        addcart_tglupdate = request.form['mdl_update']
        addcart_qrcode = request.form['qr_code']
        addcart_total = request.form['total_harga']
        addcart_removerupiah = request.form['jumlah_aja']
        addcart_qty = request.form['qty']
        kadar = request.form['kadar']
        kodeqr = request.form['kodeqr']
        

       
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO tb_cart (id_barang,filename,nama_barang,gram,qty, tanggal_input, tanggal_update, qrcode, total, jumlah, kadar, kodeqr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (addcart_id, addcart_filename, addcart_nama, addcart_gram,addcart_qty, addcart_tglinput, addcart_tglupdate, addcart_qrcode, addcart_total, addcart_removerupiah, kadar, kodeqr))
        connection.commit()

        # cursor.execute(f"INSERT INTO tb_penjualan (id_barang,filename,nama_barang,gram,harga_jual,harga_jual2,qty, tanggal_input, tanggal_update, qrcode, potongan_harga,potongan_harga2, total, jumlah) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)", (addcart_id, addcart_filename, addcart_nama, addcart_gram,addcart_hargajual,addcart_hargajual2,addcart_qty, addcart_tglinput, addcart_tglupdate, addcart_qrcode, addcart_potonganharga,addcart_potonganharga2, addcart_total, addcart_removerupiah))
        # connection.commit()
        return redirect(url_for('billing'))


@app.route('/transaksisukses', methods=['GET','POST'])
def transaksisukses():
    if request.method == 'POST':
        iso8601 = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        NOW = datetime.datetime.now()
        request.form = request.json
        namabrg = request.form['namabrg']
        filenamebrg = request.form['filenamebrg']
        idbrg = request.form['idbrg']
        grambrg = request.form['grambrg']
        hargajualbrg = request.form['hargajualbrg']
        hargajual2brg = request.form['hargajual2brg']
        qtybrg = request.form['qtybrg']
        tglinputbrg = request.form['tglinputbrg']
        qrcodebrg = request.form['qrcodebrg']
        potonganhargabrg = request.form['potonganhargabrg']
        potonganharga2brg = request.form['potonganharga2brg']
        totalbrg = request.form['totalbrg']
        jumlahbrg = request.form['jumlahbrg']
        codeinvoice = request.form['codeinvoice']
        namapembelibrg = request.form['namapembelibrg']
        # grandtotalbrg = request.form['grandtotalbrg']
        subtotalbrg = request.form['subtotalbrg']
        # cutoff = request.form['cutoff']
        kasir = request.form['kasir']
        tgl_nota =  request.form['tgl_nota']
        number_phone = request.form['number_phone']
        kodeqrbrg = request.form['kodeqrbrg']
        kadar = request.form['kadar']
        subtotalrp = request.form['sub_totalrp']
        tanggalaja = datetime.datetime.now().strftime('%Y-%m-%d')
        id_member = '1'
        qrcodetransaksi = 'no'
        print(idbrg)
        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=12,border=2)
        qr.add_data(codeinvoice)
        qr.make(fit =True)
        img = qr.make_image(fill = 'Black',back_color = 'White')
        new_filenamebarcode = os.path.join(NOW.strftime("%d_%m_%Y_%H_%M_%S_barcode.png"))
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filenamebarcode)) 

       
        connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO penjualan (id_barang,id_member,filename,nama_konsumen,id_transaksi, harga_jual, jumlah,potongan_harga, total, gram,tanggal_transaksi,qrcode,qrcode_transaksi,nama_barang, sub_total ,  kasir, note, qtybrg, tgl_nota,no_hp,kodeqr,kadar, sub_totalrp,tanggal_aja) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (idbrg,id_member, filenamebrg, namapembelibrg, codeinvoice,hargajualbrg,jumlahbrg,potonganhargabrg, totalbrg, grambrg, iso8601, qrcodebrg,new_filenamebarcode, namabrg, subtotalbrg, kasir,qrcodetransaksi, qtybrg, tgl_nota, number_phone, kodeqrbrg, kadar, subtotalrp, tanggalaja))
            connection.commit()

        # cursor.execute(f"INSERT INTO tb_penjualan (id_barang,filename,nama_barang,gram,harga_jual,harga_jual2,qty, tanggal_input, tanggal_update, qrcode, potongan_harga,potongan_harga2, total, jumlah) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)", (addcart_id, addcart_filename, addcart_nama, addcart_gram,addcart_hargajual,addcart_hargajual2,addcart_qty, addcart_tglinput, addcart_tglupdate, addcart_qrcode, addcart_potonganharga,addcart_potonganharga2, addcart_total, addcart_removerupiah))
        # connection.commit()
            
            return jsonify({"pesan": "sudah masuk"}), 200
   

@app.route('/printqrcode/<id_transaksi>', methods=['GET','POST'])
def printqrcode(id_transaksi):
    
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # request.form = request.json
        # addcart_id = request.form['upd_id_barang']
        cursor.execute(f"SELECT * FROM penjualan where id_transaksi = '{id_transaksi}'")
        invoice = cursor.fetchall()
        print(invoice)
        cursor.execute(f"SELECT LPAD(id_penjualan,11,'EMB-000000') as modifankamu FROM db_toko.penjualan where id_transaksi = '{id_transaksi}'")
        invoiceemb = cursor.fetchall()
        print(invoiceemb)
        # if qrcodebarang is None:
        #     return jsonify("data tidak ditemukan oleh server", status=404)
        # else:
        #     return jsonify({"qrcodebarang":qrcodebarang})
            
        #     session['LEVEL'] = satudata['level']
        #     session['USER_KETERANGAN'] = satudata['id_jkdt']
        #     return Response("data ditemukan oleh server", status=200)
    
        return render_template("qrcode.html", invoice=invoice, invoiceemb=invoiceemb)

@app.route('/cartapi', methods=['GET','POST'])
def cartapi():
    
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # request.form = request.json
        # addcart_id = request.form['upd_id_barang']
        cursor.execute(f"SELECT * FROM tb_cart")
        cart = cursor.fetchall()
        print(cart)
        
        if cart is None:
            return jsonify("data tidak ditemukan oleh server", status=404)
        else:
            return jsonify({"cart":cart})

@app.route('/invoice', methods=['GET','POST'])
def invoice():
    if len(session) == 0:
        return redirect('/?msg=SESSION_KOSONG')
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # request.form = request.json
        # addcart_id = request.form['upd_id_barang']
        cursor.execute(f"SELECT  DISTINCT id_transaksi,tgl_nota,nama_konsumen,kasir,sub_total from penjualan ORDER BY id_transaksi DESC")
        invoicedone = cursor.fetchall()
        print(invoicedone)

        

        return render_template("transaksi.html",sess_data=session, invoicedone=invoicedone)
        

@app.route("/printbilling")
def printbilling():
    iso8601 = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
    htmlfile = app.config['TEMPLATE_FOLDER'] + 'qrcode.html'
    pdffile = app.config['PDF_FOLDER'] +  iso8601 +'.pdf'
    print(pdffile)
    pdfkit.from_string(htmlfile, pdffile, options={"enable-local-file-access": ""})
    return render_template("qrcode.html")
    # return '''Click here to open the <a href="https://tokoemasmuliaberau.com/static/pdf/demo.pdf">pdf</a>.'''
   

@app.route("/download/report/excelbulan", methods=['POST'])
def download_report_bulan():
    if request.method == "POST":
        input_tanggal = request.form['tanggal_laporan']
        # input_tahun = request.form['tahun']
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        iso8601 = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        cursor.execute(f"SELECT * FROM  penjualan WHERE tanggal_transaksi  LIKE '%{input_tanggal}%'  ORDER BY id_penjualan DESC ")
        result_dtg = cursor.fetchall()
        print(result_dtg)

        # CSV GENERATORRRRRRRRR
        output = io.BytesIO()
        workbook = xlwt.Workbook()
		
        sh = workbook.add_sheet('Employee Report')
        
        sh.write(0, 0, 'TANGGAL TRANSAKSI')
        sh.write(0, 1, 'ID TRANSAKSI')
        sh.write(0, 2, 'ID BARANG')
        sh.write(0, 3, 'KASIR')
        sh.write(0, 4, 'NAMA BARANG')
        sh.write(0, 5, 'GRAM')
        sh.write(0, 6, 'QTY')
        sh.write(0, 7, 'SUB TOTAL')
        sh.write(0, 8, 'TOTAL HARGA')

        idx = 0

        for row in result_dtg:
            
            sh.write(idx+1, 0, row['tgl_nota'])
            sh.write(idx+1, 1, row['id_transaksi'])
            sh.write(idx+1, 2, row['id_barang'])
            sh.write(idx+1, 3, row['kasir'])
            sh.write(idx+1, 4, row['nama_barang'])
            sh.write(idx+1, 5, row['gram'])
            sh.write(idx+1, 6, row['qtybrg'])
            sh.write(idx+1, 7, row['total'])
            sh.write(idx+1, 8, row['sub_total'])


            idx += 1

            workbook.save(output)
            output.seek(0)
            print(output)

        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Transaksi - "+ str(input_tanggal) + ".xls"})

@app.route("/download/report/excelday", methods=['POST'])
def download_report_day():
    if request.method == "POST":
        input_tanggal = request.form['tanggal_laporan']
        # input_tahun = request.form['tahun']
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        iso8601 = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        cursor.execute(f"SELECT LPAD(id,9,'BR-00000') as modifankamu, nama_barang, filename, gram, qrcode, kadar, tgl_input ,kodeqr, tgl_new FROM db_toko.barang WHERE tgl_input  LIKE '%{input_tanggal}%'  ORDER BY modifankamu DESC ")
        result_dtg = cursor.fetchall()
        print(result_dtg)

        # CSV GENERATORRRRRRRRR
        output = io.BytesIO()
        workbook = xlwt.Workbook()
		
        sh = workbook.add_sheet('Employee Report')
        
        sh.write(0, 0, 'ID BARANG')
        sh.write(0, 1, 'NAMA BARANG')
        sh.write(0, 2, 'GRAM')
        sh.write(0, 3, 'DATA QR')
        sh.write(0, 4, 'TANGGAL INPUT')
        # sh.write(0, 5, 'GRAM')
        # sh.write(0, 6, 'QTY')
        # sh.write(0, 7, 'SUB TOTAL')
        # sh.write(0, 8, 'TOTAL HARGA')

        idx = 0

        for row in result_dtg:
            
            sh.write(idx+1, 0, row['modifankamu'])
            sh.write(idx+1, 1, row['nama_barang'])
            sh.write(idx+1, 2, row['gram'])
            sh.write(idx+1, 3, row['kodeqr'])
            sh.write(idx+1, 4, row['tgl_new'])
            # sh.write(idx+1, 5, row['gram'])
            # sh.write(idx+1, 6, row['qtybrg'])
            # sh.write(idx+1, 7, row['total'])
            # sh.write(idx+1, 8, row['sub_total'])


            idx += 1

            workbook.save(output)
            output.seek(0)
            print(output)

        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Data Barang - "+ str(input_tanggal) + ".xls"})

@app.route("/detailapi", methods=['GET','POST'])
def detailapi():
    request.form = request.json
    id_transaksi = request.form['id_transaksi']
    connection = pymysql.connect(host='128.199.195.208',user='tokoemas',password='pusamania',database='db_toko',cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        # request.form = request.json
        # addcart_id = request.form['upd_id_barang']
        cursor.execute(f"SELECT * FROM penjualan where id_transaksi = '{id_transaksi}'")
        detail = cursor.fetchall()
        print(detail)
        
        if detail is None:
            return jsonify("data tidak ditemukan oleh server", status=404)
        else:
            return jsonify({'detail':detail})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)