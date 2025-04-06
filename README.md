# 🍲 Recipes App - Django

Uma aplicação web para cadastro e gerenciamento de receitas, desenvolvida com Django. Este projeto é focado em aprendizado e prática de conceitos como CRUD, organização de views, models e templates no Django.

---

## 🚀 Funcionalidades

- ✅ Cadastro, edição e remoção de receitas  
- ✅ Interface web com páginas dinâmicas  
- ✅ Organização de receitas por categorias  
- ✅ Upload de imagens para cada receita  
- ✅ Painel administrativo com Django Admin  

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- [Django 4.x](https://www.djangoproject.com/)
- SQLite (banco padrão do Django)
- HTML + CSS básico
- Django Templates

---

## 📦 Como rodar o projeto localmente

1. **Clone o repositório**
   ```bash
   git clone https://github.com/kevin-andrade/recipes-app-django.git
   cd recipes-app-django

2. **Criação de ambiente virtual**
   ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows

3. **Instale as depedências**
   ```bash
    pip install -r requirements.txt

4. **Aplique as migrações**
    ```bash
    python manage.py migrate

5. **Crie um Superusuário para acessar o Django admin**
    ```bash
     python manage.py createsuperuser
    
6. **Inicie no servidor**
   ```bash
     python manage.py runserver
