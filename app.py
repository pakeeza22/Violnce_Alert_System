import os
import predict_violence
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, render_template
import environ

env = environ.Env()
environ.Env.read_env(env.str('ENV_PATH', '.env'))
print(env.str('EMAIL', multiline=True))

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg')



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email():
    try:
        message = "Violence Alert!"
        sender_mail = env.str('EMAIL', multiline=True)
        receiver_mail = ['pakeeza15pa@gmail.com']    # PUT ALL Recipients emails here
        s_msg = Message(message, sender = sender_mail , recipients = receiver_mail)
        s_msg.body = "Violence is Detect in this image!!"
        mail.send(s_msg)
        return "Sent"
    except Exception as e:
        return e

@app.route('/', methods=['GET', 'POST'])
def main_index():
    return render_template("index.html", msg = "")


@app.route('/upload_file/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fpath)
            flag = predict_violence.predict_job(fpath)
            if flag:
                send_email()
            os.remove(fpath)
            return render_template('index.html', msg = "Successfully Upload!!")
    return ""

if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465 
    app.config['MAIL_USERNAME'] = env.str('EMAIL', multiline=True)   # PUT YOUR EMAIL in the ".env" file
    app.config['MAIL_PASSWORD'] = os.environ['PASSWORD']      # PUT YOUR EMAIL PASSWORD in the ".env" file
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    app.run(debug=True)