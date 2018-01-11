import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
from passwordhelper import PasswordHelper
from flask_mail import Mail, Message


from emails import send_email

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
PROJECT_URL = 'http://uploads.lanbilling.ru/'
PH = PasswordHelper()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = "sISH72eQKgv9LpFcfnKdjR1"
mail = Mail(app)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    filesdata = []
    if request.method == 'POST':
        for file in request.files.getlist('files'):
            # print(request.files)
            # print(file.filename, file.content_type, file.stream, file.name)
            # check if the post request has the file part
            if not file.name == 'files':
                flash('No file part')
                return redirect(request.url)
            # file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No file selected')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                salt = str(PH.get_salt())
                hashed = PH.get_hash(filename + salt)[:16]
                file_dirhash = os.path.join(app.config['UPLOAD_FOLDER'], hashed)
                os.makedirs(file_dirhash)
                fdata = {
                    'filehash': file_dirhash,
                    'filename': filename
                }
                filesdata.append(fdata)
                file.save(os.path.join(file_dirhash, filename))
                flash("files are uploaded")
        # return 'Upload complete.'
        #
        return render_template('preview.html',
                               fdata=filesdata,
                               purl=PROJECT_URL,
                               )
    return render_template('home.html')


@app.route('/uploads/<file_dir>/<filename>')
def uploaded_file(filename, file_dir):
    file_dirhash = os.path.join(app.config['UPLOAD_FOLDER'], file_dir)
    print(file_dirhash)
    return send_from_directory(file_dirhash, filename)


@app.route('/sentemail', methods=["POST"])
def sendemail():
    app.config.update(
        DEBUG=True,
        # EMAIL SETTINGS
        MAIL_SERVER='mx.lanbilling.ru',
        MAIL_PORT=25,
        MAIL_USE_TLS=True,
        MAIL_USERNAME='tkachenko@lanbilling.ru',
        MAIL_PASSWORD='XsKtu8thaW6'
    )
    mail = Mail(app)
    print(request.form.get('filesurl'))
    try:
        email = send_email(subject='Files',
                       sender='support@lanbilling.ru',
                        recipients=[request.form.get('email')],
                        text_body=render_template('template_email',files=files,user=))
        mail.send(email)
        flash('Thanks your email is sent')
    except Exception as e:
        return(str(e))
    # if request.method == 'POST' and request.form['email']:
    #     send_email(subject='files',
    #                sender='files@lanbilling.ru',
    #                recipients=request.form['email'],
    #                text_body='')


#
# send_email(subject='files',
#            sender='files@lanbilling.ru',
#            recipients=request.form.)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
