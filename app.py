from flask import Flask, render_template, request, send_file, jsonify, flash
from cryptography.fernet import Fernet
import os
import io
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Mude para uma chave segura em produção
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Diretório para armazenar arquivos temporários
UPLOAD_FOLDER = 'temp_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    """Página principal com interface para criptografia e descriptografia"""
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    """Endpoint para criptografar arquivo"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo foi enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Gerar chave para criptografia
        key = Fernet.generate_key()
        f = Fernet(key)
        
        # Ler o arquivo
        file_data = file.read()
        
        # Criptografar os dados
        encrypted_data = f.encrypt(file_data)
        
        # Criar arquivo temporário com dados criptografados
        encrypted_filename = secure_filename(file.filename) + '.enc'
        encrypted_path = os.path.join(UPLOAD_FOLDER, encrypted_filename)
        
        with open(encrypted_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
        
        # Retornar chave em formato base64 para exibição
        key_str = key.decode('utf-8')
        
        return jsonify({
            'success': True,
            'key': key_str,
            'filename': encrypted_filename,
            'original_filename': file.filename
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro ao criptografar arquivo: {str(e)}'}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    """Endpoint para descriptografar arquivo"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo foi enviado'}), 400
        
        file = request.files['file']
        key_str = request.form.get('key', '').strip()
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not key_str:
            return jsonify({'error': 'Chave de descriptografia não fornecida'}), 400
        
        # Processar a chave
        try:
            key = key_str.encode('utf-8')
            f = Fernet(key)
        except Exception:
            return jsonify({'error': 'Chave inválida. Verifique o formato da chave.'}), 400
        
        # Ler arquivo criptografado
        encrypted_data = file.read()
        
        # Descriptografar
        try:
            decrypted_data = f.decrypt(encrypted_data)
        except Exception:
            return jsonify({'error': 'Falha na descriptografia. Verifique se a chave está correta.'}), 400
        
        # Determinar nome do arquivo original
        original_filename = file.filename
        if original_filename.endswith('.enc'):
            original_filename = original_filename[:-4]  # Remove .enc
        else:
            original_filename = 'arquivo_descriptografado.txt'
        
        # Salvar arquivo descriptografado
        decrypted_path = os.path.join(UPLOAD_FOLDER, 'decrypted_' + secure_filename(original_filename))
        
        with open(decrypted_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
        
        return jsonify({
            'success': True,
            'filename': 'decrypted_' + secure_filename(original_filename),
            'original_filename': original_filename
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro ao descriptografar arquivo: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Endpoint para download de arquivos"""
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        return send_file(file_path, as_attachment=True, download_name=filename)
    
    except Exception as e:
        return jsonify({'error': f'Erro ao baixar arquivo: {str(e)}'}), 500

@app.route('/cleanup')
def cleanup_files():
    """Endpoint para limpar arquivos temporários"""
    try:
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return jsonify({'success': True, 'message': 'Arquivos temporários removidos'})
    except Exception as e:
        return jsonify({'error': f'Erro ao limpar arquivos: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6100)
