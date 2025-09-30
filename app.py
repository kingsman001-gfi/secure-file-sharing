from flask import Flask, render_template, request, send_file
import os
from encryption.aes_utils import encrypt_file, decrypt_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.enc')]
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        data = file.read()
        encrypted = encrypt_file(data)
        enc_path = os.path.join(UPLOAD_FOLDER, file.filename + '.enc')
        with open(enc_path, 'wb') as f:
            f.write(encrypted)
        # Get updated file list
        files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.enc')]
        return render_template('index.html', message=f'✅ File \"{file.filename}\" uploaded and encrypted successfully.', files=files)
    else:
        files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.enc')]
        return render_template('index.html', message='⚠️ No file selected.', files=files)

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)

    # Check if the encrypted file exists
    if not os.path.exists(path):
        files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.enc')]
        return render_template('index.html', message=f'❌ File \"{filename}\" not found.', files=files)

    # Read and decrypt the file
    try:
        with open(path, 'rb') as f:
            encrypted = f.read()
        decrypted = decrypt_file(encrypted)
    except Exception as e:
        files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.enc')]
        return render_template('index.html', message=f'❌ Decryption failed: {str(e)}', files=files)

    # Save decrypted file temporarily
    decrypted_filename = 'decrypted_' + filename.replace('.enc', '')
    decrypted_path = os.path.join(UPLOAD_FOLDER, decrypted_filename)
    with open(decrypted_path, 'wb') as f:
        f.write(decrypted)

    # Send decrypted file to user
    return send_file(decrypted_path, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
        message = f'🗑️ File "{filename}" deleted successfully.'
    else:
        message = f'⚠️ File "{filename}" not found.'

    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.enc')]
    return render_template('index.html', message=message, files=files)

if __name__ == '__main__':
    app.run(debug=True)
