# 📌 Gerenciador de Tarefas - Flask

## 📖 Sobre o Projeto
Este é um **Gerenciador de Tarefas** desenvolvido com **Flask** e **SQLite**. O projeto permite que os usuários:
- Criem contas e façam login/logout 🔑
- Adicionem, atualizem e excluam tarefas ✅
- Gerenciem o status das tarefas (Pendente, Atrasada, Concluída) 📌


## 🛠 Tecnologias Utilizadas
O projeto foi desenvolvido utilizando as seguintes tecnologias:
- **Python** (Flask, SQLite, Werkzeug, Dotenv)
- **HTML, CSS & Bootstrap** (Interface responsiva)
- **JavaScript** (Interatividade básica)
- **Jinja2** (Template engine do Flask)

## 📂 Estrutura do Projeto
```
📦 gerenciador_tarefas
 ┣ 📂 static
 ┃ ┣ 📂 css
 ┃ ┣ 📂 js
 ┃ ┗ 📂 img
 ┣ 📂 templates
 ┃ ┣ base.html
 ┃ ┣ index.html
 ┃ ┣ register.html
 ┃ ┣ tasks.html
 ┃ ┗ update.html
 ┣ app.py
 ┣ database.db
 ┣ .env.example
 ┗ README.md
```

## 🚀 Como Executar o Projeto

### 1️⃣ Clonar o Repositório
```sh
$ git clone https://github.com/bertucci/gerenciador-de-tarefas.git
$ cd gerenciador-de-tarefas
```

### 2️⃣ Criar e Ativar um Ambiente Virtual
```sh
$ python -m venv venv
$ source venv/bin/activate  # Linux/macOS
$ venv\Scripts\activate     # Windows
```

### 3️⃣ Instalar Dependências
```sh
$ pip install -r requirements.txt
```

### 4️⃣ Definir Variáveis de Ambiente
Crie um arquivo **.env** baseado no **.env.example** e defina a `SECRET_KEY`:
```sh
$ cp .env.example .env
$ nano .env  # Edite o arquivo e adicione sua SECRET_KEY
```

Ou defina manualmente no terminal:
```sh
$ export SECRET_KEY="sua_chave_super_secreta"  # Linux/macOS
$ set SECRET_KEY="sua_chave_super_secreta"    # Windows
```

### 5️⃣ Executar o Aplicativo
```sh
$ python app.py
```
Acesse no navegador: **http://127.0.0.1:5000** 🚀

## 🔥 Funcionalidades
- ✅ Cadastro/Login de usuários
- ✅ Adição/Edição/Exclusão de tarefas
- ✅ Status das tarefas (Pendente, Atrasada, Concluída)
- ✅ Interface responsiva com Bootstrap

## 📝 Licença
Este projeto está sob a licença **MIT**. Sinta-se à vontade para utilizá-lo e contribuir! 😊

