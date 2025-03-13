from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env automaticamente
load_dotenv()
app = Flask(__name__)


# Obtendo a SECRET_KEY do ambiente para garantir segurança nas sessões
if not os.environ.get('SECRET_KEY'):
    raise ValueError("SECRET_KEY não está definido! Defina no ambiente antes de rodar o app.")
app.secret_key = os.environ['SECRET_KEY']

# Função para inicializar o banco de dados SQLite
# Cria as tabelas 'users' e 'tasks' caso ainda não existam
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL
                            );
                       """)
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        userid INTEGER,
                        title TEXT NOT NULL,
                        description TEXT,
                        due_date DATE,
                        status TEXT,
                        FOREIGN KEY (userid) REFERENCES users (id)
                            );
                       """)
        conn.commit()

# Inicializa o banco de dados ao iniciar o aplicativo
init_db()

# Função para executar queries no banco de dados de forma reutilizável
def query_db(query, args=(), one=False):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        result = cursor.fetchall()
        conn.commit()
        return (result[0] if result else None) if one else result

# Rota de Login
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_db('SELECT * FROM users WHERE username = ?', (username,), one=True)

        # Verifica se o usuário existe e se a senha está correta
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['user_email'] = user[3]
            return redirect(url_for("show_tasks"))
        else:
            flash('Usuário ou senha inválidos!')
            return render_template('index.html')
    return render_template('index.html')

app.route("/", methods=['GET', 'POST'])(login)

# Rota de Registro de Usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if not username or not password or not email:
            flash('Todos os campos são obrigatórios!', 'error')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        try:
            query_db('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                     (username, hashed_password, email))
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Usuário já existe!", 'error')
            return render_template('register.html')
    return render_template('register.html')

# Rota de Logout
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('Você foi deslogado!')
    return redirect('/')

# Rota para visualizar e adicionar tarefas
@app.route('/tasks', methods=['GET', 'POST'])
def show_tasks():
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar essa página.', 'error')
        return redirect(url_for('login'))

    userid = session['user_id']
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        duedate = request.form['duedate']
        status = request.form['status']
        try:
            query_db('INSERT INTO tasks (userid, title, description, due_date, status) VALUES (?, ?, ?, ?, ?)',
                     (userid, title, description, duedate, status))
            flash("Tarefa cadastrada com sucesso!", 'success')
        except sqlite3.Error as e:
            flash(f'Houve um problema ao cadastrar sua tarefa: {e}', 'error')
        return redirect(url_for("show_tasks"))

    tasks = query_db('SELECT * FROM tasks WHERE userid = ?', (userid,))
    return render_template('tasks.html', tasks=tasks)

# Rota para deletar uma tarefa
@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    try:
        query_db('DELETE FROM tasks WHERE id = ?', (id,))
        flash('Tarefa deletada com sucesso!', 'success')
    except sqlite3.Error as e:
        flash(f'Houve um erro ao tentar deletar a tarefa: {e}', 'error')
    return redirect(url_for("show_tasks"))

# Rota para atualizar uma tarefa
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task_to_update = query_db('SELECT * FROM tasks WHERE id = ?', (id,), one=True)
    if not task_to_update:
        flash("Tarefa não encontrada!", "error")
        return redirect(url_for("show_tasks"))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        duedate = request.form['duedate']
        status = request.form['status']
        try:
            query_db('UPDATE tasks SET title = ?, description = ?, due_date = ?, status = ? WHERE id = ?',
                     (title, description, duedate, status, id))
            flash('Tarefa atualizada com sucesso!', 'success')
            return redirect(url_for("show_tasks"))
        except sqlite3.Error as e:
            flash(f'Houve um erro ao atualizar a tarefa: {e}', 'error')
    return render_template('update.html', task=task_to_update)

if __name__ == '__main__':
    app.run(debug=True)
