from flask import Flask, render_template, request, send_file, url_for, session, redirect
from werkzeug.utils import secure_filename
import os
import secrets
import time
from pca_image_compressor import load_image, apply_pca_compression, save_image

app = Flask(__name__, static_folder='static')
app.secret_key = secrets.token_hex(16)

UPLOAD_FOLDER = 'static/uploads'
COMPRESSED_FOLDER = 'static/compressed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    original_image_url = None
    compressed_image_url = None
    clean_compressed_filename = None
    runtime = None
    information_retained = None
    compression_level_applied = None
    error_message = None
    image_uploaded = False
    original_filename = session.get('original_filename', None)

    if original_filename:
        original_image_url = url_for('static', filename=f'uploads/{original_filename}')
        image_uploaded = True

    if request.method == 'POST':
        if 'image_file' in request.files and request.files['image_file'].filename != '':
            file = request.files['image_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                try:
                    clean_static_folders()
                    file.save(original_image_path)
                    session['original_filename'] = filename
                    return redirect(url_for('index'))
                except Exception as e:
                    error_message = f"Failed to save original image: {e}"
            else:
                error_message = 'Invalid file type. Allowed types: png, jpg, jpeg, gif, bmp'

        elif 'compression_percentage' in request.form and original_filename:
            try:
                compression_percentage_str = request.form.get('compression_percentage')
                compression_level_applied = float(compression_percentage_str)
                original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
                image_array = load_image(original_image_path)

                if image_array is None:
                    error_message = "Failed to load image for compression. Please re-upload the image."
                    session.pop('original_filename', None)
                    image_uploaded = False
                else:
                    compressed_image_array, runtime, information_retained, _, _, _, _, pca_error_message = \
                        apply_pca_compression(image_array, compression_percentage_str, 'percentage')
                    
                    if pca_error_message:
                        error_message = pca_error_message
                    elif compressed_image_array is not None:
                        clean_compressed_filename = f"compressed_{original_filename}"
                        compressed_image_path = os.path.join(app.config['COMPRESSED_FOLDER'], clean_compressed_filename)
                        
                        # Meneruskan nilai persentase kompresi ke fungsi save_image
                        if save_image(compressed_image_array, compressed_image_path, compression_level_applied):
                            timestamp = int(time.time())
                            compressed_image_url = url_for('static', filename=f'compressed/{clean_compressed_filename}', t=timestamp)
                        else:
                            error_message = "Failed to save compressed image."
                    else:
                        error_message = "Failed to compress image."
            except ValueError:
                error_message = "Invalid compression percentage value. Please enter a number."
            except Exception as e:
                error_message = f"An unexpected error occurred during compression: {e}"
    
    return render_template('index.html',
                           original_image_url=original_image_url,
                           compressed_image_url=compressed_image_url,
                           clean_compressed_filename=clean_compressed_filename,
                           runtime=runtime,
                           information_retained=information_retained,
                           compression_level_applied=compression_level_applied,
                           error_message=error_message,
                           image_uploaded=image_uploaded)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['COMPRESSED_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found!", 404

@app.route('/reset')
def reset():
    clean_static_folders()
    session.pop('original_filename', None)
    return redirect(url_for('index'))

def clean_static_folders():
    """Removes all files in the uploads and compressed folders."""
    for folder in [app.config['UPLOAD_FOLDER'], app.config['COMPRESSED_FOLDER']]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

if __name__ == '__main__':
    app.run(debug=True)
