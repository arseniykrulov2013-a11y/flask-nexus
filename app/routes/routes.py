from app.app import app, nexusdb, LoginManager, Admin
from app.models.users import Users
from app.models.posts import Posts
from app.models.comments import Comments
from flask import render_template, url_for, redirect, abort, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import uuid

admin = Admin(app, name="Админ-панель")
app.secret_key = secret_key = uuid.uuid4()

lm = LoginManager(app)

@lm.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route("/")
def homeRedirect():
    return redirect("/home")

@app.route("/home")
def home():
    l = current_user.is_authenticated
    p = Posts.query.limit(3).all()
    return render_template("home.html", loginned=l, posts = p)

@app.route("/boards")
def boards():
    l = current_user.is_authenticated
    return render_template("boards.html", loginned=l)

@app.route("/boards/random", methods=['GET', 'POST'])
@login_required
def boards_random():

    if request.method == "POST":
        postname = request.form.get("RandomPostName")
        posttext = request.form.get("RandomPostText")

        if not postname or not posttext:
            print("ERROR: Имя или текст поста неправельны!")
        
        post = Posts(name = postname, text = posttext, board = "random", user_name = current_user.login)

        nexusdb.session.add(post)
        nexusdb.session.commit()
        return redirect("/boards/random")
    
    else:
        posts = Posts.query.filter_by(board = "random").order_by(Posts.name).all()
        return render_template("random-b.html", posts = posts)

@app.route("/boards/clean", methods=['GET', 'POST'])
@login_required
def boards_clean():
    if request.method == "POST":
        postname = request.form.get("CleanPostName")
        posttext = request.form.get("CleanPostText")

        if not postname or not posttext:
            print("ERROR: Имя или текст поста неправельны!")
        
        post = Posts(name = postname, text = posttext, board = "clean", user_name = current_user.login)

        nexusdb.session.add(post)
        nexusdb.session.commit()
        return redirect("/boards/clean")
    
    else:
        posts = Posts.query.filter_by(board = "clean").order_by(Posts.name).all()
        return render_template("clean-b.html", posts = posts)

@app.route("/boards/creative", methods=['GET', 'POST'])
@login_required
def boards_creative():
    if request.method == "POST":
        postname = request.form.get("CreativePostName")
        posttext = request.form.get("CreativePostText")

        if not postname or not posttext:
            print("ERROR: Имя или текст поста неправельны!")
        
        post = Posts(name = postname, text = posttext, board = "creative", user_name = current_user.login)

        nexusdb.session.add(post)
        nexusdb.session.commit()
        return redirect("/boards/creative")
    
    else:
        posts = Posts.query.filter_by(board = "creative").order_by(Posts.name).all()
        return render_template("creative-b.html", posts = posts)

@app.route("/user", methods=['GET', 'POST'])
@login_required
def user():
    user = current_user
    
    if request.method == 'POST':
        newlogin = request.form.get("userName")
        newdes = request.form.get("userDes")

        user.login = newlogin
        user.description = newdes

        nexusdb.session.commit()

        newuser = current_user
        return render_template("user.html", u=newuser)

    return render_template("user.html", u=user)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login = request.form.get("loginName")
    password = request.form.get("loginPassword")

    if request.method == "POST":
        if login and password:
            user = Users.query.filter_by(login=login).first()

            if user and check_password_hash(user.password, password):
                login_user(user)

                return redirect("/home")
            else:
                print("ERROR: Логин или пароль неправельны!")
        else:
            print("ERROR: Логин и пароль неправельны!")

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get("regName")
    password = request.form.get("regPassword")
    password_retype = request.form.get("passRepeat")

    if request.method == "POST":
        if not (login or password or password_retype):
            print("ERROR: Логин, пароль или его повторение неправельны!")
        elif password != password_retype:
            print("ERROR: Пароль и его повторение должны быть одинаковы!")
        else:
            hash_pwd = generate_password_hash(password)
            new_user = Users(login = login, password = hash_pwd)
            nexusdb.session.add(new_user)
            nexusdb.session.commit()

            return redirect(url_for('login')) # В url_for имя функции

    return render_template("register.html")

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/boards/post/<int:postid>', methods=['GET', 'POST'])
@login_required
def post_detail(postid):
    if request.method == "POST":
        text = request.form.get("CommentText")
        user = current_user.login

        if text and user:
            comment = Comments(user_name = user, text=text, post_id = postid)

            nexusdb.session.add(comment)
            nexusdb.session.commit()
            return redirect(f"/boards/post/{postid}")

    post = Posts.query.filter_by(id = postid).one()
    comments = Comments.query.filter_by(post_id = post.id).all()
    return render_template("post-detail.html", post = post, coms = comments)

@app.errorhandler(401)
def login_regirect(p):
    return redirect("/login")

@app.before_request
def before_request():
    if request.full_path.startswith('/admin/'):
        if current_user.is_admin == "FALSE":
            abort(400, 'Отказанно в доступе...')


