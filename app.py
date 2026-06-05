"""
Aplicación Flask con interfaz web para extractor CFDI
Proporciona interfaz moderna con drag & drop
"""

import os
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from processor import ZIPProcessor
from pathlib import Path

# Configuración
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'zip'}
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB máximo

# Crea carpetas si no existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


def allowed_file(filename):
    """Verifica si el archivo tiene extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Maneja la carga de archivo ZIP
    """
    try:
        # Verifica que se enviaron archivos
        if 'file' not in request.files:
            return jsonify({'error': 'No se envió archivo'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Solo se permiten archivos ZIP'}), 400
        
        # Guarda el archivo
        filename = secure_filename(file.filename)
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(zip_path)
        
        # Genera nombre para el Excel
        base_name = Path(filename).stem
        excel_filename = f"{base_name}_reporte.xlsx"
        excel_path = os.path.join(app.config['OUTPUT_FOLDER'], excel_filename)
        
        # Procesa el ZIP
        processor = ZIPProcessor()
        success, message, stats = processor.process_zip(zip_path, excel_path)
        
        # Limpia el archivo ZIP después de procesar
        try:
            os.remove(zip_path)
        except:
            pass
        
        if not success:
            return jsonify({
                'error': message,
                'stats': stats
            }), 400
        
        return jsonify({
            'success': True,
            'message': message,
            'excel_file': excel_filename,
            'stats': stats
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error en servidor: {str(e)}'}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """
    Descarga el archivo Excel generado
    """
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Archivo no encontrado'}), 404
        
        return send_file(
            file_path,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({'error': f'Error al descargar: {str(e)}'}), 500


@app.route('/health')
def health():
    """Endpoint de salud para verificar que la app está funcionando"""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
