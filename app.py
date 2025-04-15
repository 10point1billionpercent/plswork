from flask import Flask, render_template, request, jsonify
import os
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)

# Configure upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fileUpload' not in request.files:
        return jsonify(status='error', message='No file part'), 400

    file = request.files['fileUpload']
    if file.filename == '':
        return jsonify(status='error', message='No selected file'), 400

    if file and allowed_file(file.filename):
        try:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(status='success', message='Upload successful!'), 200
        except Exception as e:
            return jsonify(status='error', message=f'Failed to save file: {e}'), 500
    else:
        return jsonify(status='error', message='Invalid file type'), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # This binds it to Render's environment
