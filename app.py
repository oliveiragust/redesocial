import logging

from flask import Flask, redirect, render_template, request, url_for, flash, abort, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.testing.pickleable import User
from werkzeug.security import check_password_hash
from forms import RegistrationForm, LoginForm, PostForm, CommentForm
from models import Users, Posts, Comments, db
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://socialnetdb_user:GNVlzNmKOEF3ZLrXHGHaKHKZ9FGXl69B@dpg-cnog73md3nmc73dkrt3g-a/socialnetdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'sua_chave_secreta'

db.init_app(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return None

    return Users.query.get(user_id)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data).decode('utf-8')
        new_user = Users(username=form.username.data, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            session['username'] = user.username

            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('home', username=user.username))
        else:
            flash('Credenciais inválidas. Por favor, tente novamente.', 'danger')

    return render_template('login.html', form=form)



@app.route('/', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))  # Redireciona usuários não autenticados para a página de login

    user = current_user
    posts = Posts.query.all()


    form = PostForm()
    comment_form = CommentForm()

    if form.validate_on_submit():
        new_post = Posts(content=form.content.data, created_at=datetime.utcnow(), user_id=current_user.id)
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Post criado com sucesso!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('Erro ao criar post. Tente novamente.', 'danger')
            db.session.rollback()

    for post in posts:
        post.content = "\n".join([post.content[i:i + 70] for i in range(0, len(post.content), 70)])

    # Consulta os comentários para cada postagem
    for post in posts:
        post.comments = Comments.query.filter_by(post_id=post.id).join(Users).all()

    return render_template('home.html', form=form, comment_form=comment_form, user=user, allow_posting=True, posts=posts)


from flask import request, jsonify


@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment(post_id):
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        try:
            new_comment = Comments(content=comment_form.content.data, created_at=datetime.utcnow(),
                                   user_id=current_user.id, post_id=post_id)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comentário adicionado com sucesso!', 'success')
        except IntegrityError:
            flash(
                'Erro: Comentário não pôde ser adicionado devido a um problema com o banco de dados. Tente novamente.',
                'danger')
        except Exception as e:
            flash('Erro ao adicionar comentário. Tente novamente.', 'danger')
            logging.error(f"Error adding comment: {e}")


    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        post = Posts.query.get_or_404(post_id)
        comments_html = render_template('content/comments.html', post=post)
        return jsonify({'comments_html': comments_html})
    else:
        return redirect(url_for('home'))


@app.route('/create_post', methods=['POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            # Print user ID for verification
            print(f"Current user ID: {current_user.id}")

            # Create new post object
            new_post = Posts(content=form.content.data, created_at=datetime.utcnow(), user_id=current_user.id)

            # Print post object contents for debugging
            print(f"New post object: {new_post}")

            # Database operations
            db.session.add(new_post)
            db.session.commit()

            flash('Post criado com sucesso!', 'success')
            return redirect(url_for('home', username=current_user.username))

        except IntegrityError as e:
            flash(f'Erro ao criar post: {str(e)}', 'danger')
            return render_template('home.html', form=form, user=user, allow_posting=True)

        except Exception as e:
            flash('Erro ao criar post. Tente novamente.', 'danger')
            return render_template('home.html', form=form, user=user, allow_posting=True)

    return redirect(url_for('home', username=current_user.username))


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404





@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
