from flask import Flask, render_template, request, jsonify
from database import db, Categoria, Usuario, Ideia # Importe os novos modelos
import os
from datetime import datetime
import urllib.parse

app = Flask(__name__)

SERVER = 'localhost'       # Geralmente 'localhost' para instância padrão local.
DATABASE = 'FlaskDB'       # Nome do seu banco de dados criado no SQL Server. Confirme que é 'FlaskDB'.
USERNAME = 'flask_user'    # Seu usuário SQL Server.
PASSWORD = 'SenhaSegura123!' # Sua senha.
DRIVER = 'ODBC Driver 17 for SQL Server'

encoded_password = urllib.parse.quote_plus(PASSWORD)

# Construa a string de conexão SQLAlchemy usando as variáveis definidas
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mssql+pyodbc://{USERNAME}:{encoded_password}@{SERVER}/{DATABASE}?'
    f'driver={DRIVER}'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contato.html')
def contato():
    return render_template('contato.html')

@app.route('/sobre.html')
def sobre():
    return render_template('sobre.html')

# rota para cadastrar uma ideia 
@app.route('/cadastrar_ideia', methods=['POST'])
def cadastrar_ideia():
    if request.method == 'POST':
        data = request.get_json()

        # Os campos do formulário HTML precisarão corresponder a esses nomes
        # Você pode precisar mapear o "Nome do Autor (CEO)" para um Usuario existente
        # ou criar um novo Usuario se ele não existir.
        # Por simplicidade, vamos assumir que o formulário envia o id_usuario e o id_categoria
        # ou informações que permitam buscar esses IDs.

        # Para este exemplo, vamos assumir que o formulário envia:
        # 'titulo' (Nome da Startup)
        # 'descricao' (Problema resolvido + Solução proposta + Diferencial)
        # 'nome_usuario' (Nome do Autor/CEO)
        # 'email_usuario' (Email do Autor/CEO) - para buscar/criar o usuário
        # 'categoria_nome' (Nome da Categoria) - para buscar/criar a categoria

        titulo = data.get('titulo') # Mapeia de 'Nome da Startup'
        descricao_problema = data.get('problemaResolvido')
        descricao_solucao = data.get('solucaoProposta')
        descricao_diferencial = data.get('diferencial')
        descricao_completa = f"Problema: {descricao_problema}\nSolução: {descricao_solucao}\nDiferencial: {descricao_diferencial}"

        nome_usuario = data.get('nomeAutor') # Mapeia de 'Nome do Autor (CEO)'
        # Para este exemplo, vamos assumir um email de usuário padrão ou que o email seja enviado no formulário
        email_usuario = data.get('emailUsuario', f"{nome_usuario.replace(' ', '').lower()}@example.com") # Adicione um campo para email no HTML se quiser ser mais preciso

        categoria_nome = data.get('categoria') # Mapeia de 'Categoria'

        # --- Validação e Busca/Criação de Categoria e Usuário ---
        if not all([titulo, descricao_problema, descricao_solucao, descricao_diferencial, nome_usuario, categoria_nome]):
            return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios!'}), 400

        # Buscar ou criar Categoria
        categoria = Categoria.query.filter_by(nome=categoria_nome).first()
        if not categoria:
            # Se a categoria não existir, crie-a. Você pode adicionar mais detalhes aqui.
            categoria = Categoria(nome=categoria_nome, descricao=f"Categoria de {categoria_nome}")
            db.session.add(categoria)
            db.session.commit() # Commit para que a categoria tenha um id_categoria

        # Buscar ou criar Usuário
        usuario = Usuario.query.filter_by(email=email_usuario).first()
        if not usuario:
            # Se o usuário não existir, crie-o. Senha fictícia para exemplo.
            # Em um cenário real, o usuário se registraria com uma senha.
            usuario = Usuario(nome=nome_usuario, email=email_usuario, senha="senha_temporaria_hash")
            db.session.add(usuario)
            db.session.commit() # Commit para que o usuário tenha um id_usuario

        nova_ideia = Ideia(
            titulo=titulo,
            descricao=descricao_completa,
            id_categoria=categoria.id_categoria,
            id_usuario=usuario.id_usuario,
            data_criacao=datetime.utcnow() # Use datetime.utcnow() para SQL Server
        )
        try:
            db.session.add(nova_ideia)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Ideia (Startup) cadastrada com sucesso!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Erro ao cadastrar ideia: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)





# @app.route('/')
# def index():
#     return render_template('index.html')  

# @app.route('/enviar', methods=['POST'])
# def enviar():
#     nome = request.form['nome']
#     email = request.form['email']

#     try:
#         conn = pyodbc.connect(conn_str)
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO Contatos (nome, email) VALUES (?, ?)", (nome, email))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return f"<h2>Dados salvos com sucesso!</h2><a href='/'>Voltar</a>"

#     except Exception as e:
#         return f"<h2>Erro ao salvar no banco:</h2><pre>{e}</pre>"
# if __name__ == '__main__':
#     app.run(debug=True)

