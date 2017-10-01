import face_recognition
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER1 = './known'
UPLOAD_FOLDER2 = './unknown'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/user_upload', methods=['GET', 'POST'])
def upload_file1():
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER1
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'SUCCESS'
    return '''
    <!doctype html>
    <style>
    html, body {
  margin: 0;
  padding: 0;
  background: #CB356B;  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #BD3F32, #CB356B);  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #BD3F32, #CB356B); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
    
    label, h1, h2, p {
  color: white;
  font-family: 'Roboto', sans-serif;
  font-weight: 300;
}

p {
  padding: 20px;
}

input[type="text"]{
  margin: 7px;
  padding: 10px;
  width: 30%;
  border: none;
  border-radius: 10px;
}

.header a {
  text-decoration: none;
  color: white;
  font-family: 'Roboto', sans-serif;
  font-weight: 300;
  padding: 20px;
}

.header {
  padding: 20px;
  background: black;
}

    </style>
    
    <div class="header">
  <a href="http://dc8590fc.ngrok.io/main">Jixel</a>
  <a href="http://dc8590fc.ngrok.io/dashboard">Admin Dashboard</a>
  <a href="http://dc8590fc.ngrok.io/about">About</a>
</div>
   <title>Upload New File</title>
   <h1 align=center>Upload New File</h1>
   <form method=post enctype=multipart/form-data align=center>
     <p><input type=file name=file>
        <input type=submit value=Upload>
   </form>
    '''


@app.route('/api/admin_upload', methods=['GET', 'POST'])
def upload_file2():
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER2
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return match_found(filename)
    return '''
    <!doctype html>
    <style>
    html, body {
  margin: 0;
  padding: 0;
  background: #CB356B;  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #BD3F32, #CB356B);  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #BD3F32, #CB356B); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
    
    label, h1, h2, p {
  color: white;
  font-family: 'Roboto', sans-serif;
  font-weight: 300;
}

p {
  padding: 20px;
}

input[type="text"]{
  margin: 7px;
  padding: 10px;
  width: 30%;
  border: none;
  border-radius: 10px;
}

.header a {
  text-decoration: none;
  color: white;
  font-family: 'Roboto', sans-serif;
  font-weight: 300;
  padding: 20px;
}

.header {
  padding: 20px;
  background: black;
}

    </style>
    
    <div class="header">
  <a href="http://dc8590fc.ngrok.io/main">Jixel</a>
  <a href="http://dc8590fc.ngrok.io/dashboard">Admin Dashboard</a>
  <a href="http://dc8590fc.ngrok.io/about">About</a>
</div>
    <title>Upload New File</title>
   <h1 align=center>Upload New File</h1>
   <form method=post enctype=multipart/form-data align=center>
     <p><input type=file name=file>
        <input type=submit value=Upload>
   </form>
    '''


def match_found(picture):
    unknown_picture = face_recognition.load_image_file("/Users/soyadiaoune/pycharmprojects/jixelapi/src/unknown/%s" % picture)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
    found = False
    picture2 = ''
    for tmp_picture in os.listdir(UPLOAD_FOLDER1):
        if not tmp_picture.startswith('.'):
            known_picture = face_recognition.load_image_file("/Users/soyadiaoune/pycharmprojects/jixelapi/src/known/%s" % tmp_picture)
            known_face_encoding = face_recognition.face_encodings(known_picture)[0]

            # Now we can see the two face encodings are of the same person with `compare_faces`!
            is_match = face_recognition.compare_faces([unknown_face_encoding], known_face_encoding)

            if is_match[0] == True:
                found = True
                picture2 = tmp_picture
                return 'Missing Person Name: %s' % (tmp_picture)
    if found:
        os.remove('/Users/soyadiaoune/pycharmprojects/jixelapi/src/unknown/%s' % picture)
        os.remove('/Users/soyadiaoune/pycharmprojects/jixelapi/src/known/%s' % picture2)

    return '''
    <!doctype html>
    <html>   
    <style>
    html, body {
  margin: 0;
  padding: 0; 
  background: #CB356B;  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #BD3F32, #CB356B);  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #BD3F32, #CB356B); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
    
    label, h1, h2, p {
  color: white;
  font-family: 'Roboto', sans-serif;
  font-weight: 300;
}

p {
  padding: 20px;
}

input[type="text"]{
  margin: 7px;
  padding: 10px;
  width: 30%;
  border: none;
  border-radius: 10px;
}

.header a {
  text-decoration: none;
  color: white;
  font-family: 'Roboto', sans-serif;
  font-weight: 300;
  padding: 20px;
}

.header {
  padding: 20px;
  background: black;
}
</style>
<body>
<h1>No facial recognition matches yet.</h2>
</body>
 </html>
    '''

@app.route('/', methods=['GET', 'POST'])
def deny_access():
    return '''
    <!doctype html>
    <html>   
    <style>
    html, body {
  margin: 0;
  padding: 0;
  background: #CB356B;  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #BD3F32, #CB356B);  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #BD3F32, #CB356B); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
    
    label, h1, h2, p {
  color: white;
  font-family: 'Roboto', sans-serif;
  font-weight: 300;
}

p {
  padding: 20px;
}

input[type="text"]{
  margin: 7px;
  padding: 10px;
  width: 30%;
  border: none;
  border-radius: 10px;
}

.header a {
  text-decoration: none;
  color: white;
  font-family: 'Roboto', sans-serif;
  font-weight: 300;
  padding: 20px;
}

.header {
  padding: 20px;
  background: black;
}
</style>
<body>
<h1><a href="http://dc8590fc.ngrok.io">Please go here </a></h2>
</body>
 </html>
    '''

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)