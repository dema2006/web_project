from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime

from forms.news import NewsForm, LessonForm
from forms.user import RegisterForm, LoginForm
from data.news import Course
from data.users import User
from data import db_session
from data.lesson import Lesson
from forms.add_user_to_course import InviteForm


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        # to_add = form.add_users.data
        # try:
        #     a = map(int, to_add.split())
        # except:
        #     return render_template('news.html', title='Добавление новости', form=form,
        #                            message="Неправильно введены id для добавления")
        db_sess = db_session.create_session()
        course = Course()
        course.title = form.title.data
        course.content = form.content.data
        course.is_private = form.is_private.data
        course.included_users = f"{current_user.id} "
        course.create_link(current_user.id, datetime.datetime.now())
        current_user.course.append(course)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости', form=form, inv=0)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Course).filter(Course.id == id, Course.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        course = db_sess.query(Course).filter(Course.id == id, Course.user == current_user).first()
        if Course:
            form.title.data = course.title
            form.content.data = course.content
            # form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        # to_add = form.add_users.data
        # try:
        #     a = map(int, to_add.split())
        # except:
        #     return render_template('news.html', title='Добавление новости', form=form,
        #                            message="Неправильно введены id для добавления")
        db_sess = db_session.create_session()
        course = db_sess.query(Course).filter(Course.id == id, Course.user == current_user).first()
        if course:
            course.title = form.title.data
            course.content = form.content.data
            course.included_users = course.included_users
            # news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    db_sess = db_session.create_session()
    course = db_sess.query(Course).filter(Course.id == id, Course.user == current_user).first()
    if course:
        inv = course.invite_code
    else:
        inv = 0
    print(inv)
    db_sess.commit()

    return render_template('news.html', title='Редактирование курса', form=form, inv=inv)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        all = db_sess.query(Course)
        course = list()
        for i in all:
            if current_user.id in list(map(int, i.included_users.split())):
                course.append(i)
        # news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))

    else:
        course = []
    return render_template("index.html", news=course)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        if form.type.data.lower() not in ["student", "teacher", "owner"]:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="неверно указан тип акаунта")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            type=form.type.data.lower()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/course_info/<int:id>', methods=['GET', 'POST'])
@login_required
def info(id):
    db_sess = db_session.create_session()
    name = db_sess.query(Course)
    creator = None
    for i in name:
        if i.id == id:
            name = i.title
            creator = i.user_id
            break
    if current_user.is_authenticated:
        all = db_sess.query(Lesson)
        course = list()
        for i in all:
            if id == i.course:
                course.append(i)
        # news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    else:
        course = []
    print(course)
    return render_template("course_info.html", lessons=course, name=name, id=id, creator=creator)


@app.route('/add_lesson/<int:id>', methods=['GET', 'POST'])
@login_required
def add_lesson(id):
    form = LessonForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        lesson = Lesson()
        lesson.title = form.title.data
        lesson.content = form.content.data
        lesson.course = id
        db_sess.add(lesson)
        db_sess.commit()
        return redirect(f'/course_info/{id}')
    return render_template(f'add_lesson.html', title='Добавление урока', form=form)


@app.route('/invite_code', methods=['GET', 'POST'])
@login_required
def invite_people():
    form = InviteForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        course = db_sess.query(Course).filter(Course.invite_code == form.title.data).first()
        print(course)
        if course:
            course.included_users = course.included_users + f" {current_user.id}"
            db_sess.commit()

        return redirect("/")
    return render_template("invite.html", title="Добавление к курсу", form=form)


if __name__ == '__main__':
    main()
