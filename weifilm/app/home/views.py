#coding:utf8
from . import home
from flask import render_template, redirect, url_for, flash, session, request, jsonify, json
from .forms import RegisterForm,LoginForm,UserdetailForm,PwdForm,CommentForm
from app.models import User,Userlog,Preview,Tag,Comment,Moviecol,Movie
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from app import db,app
from uuid import uuid4
from functools import wraps
import datetime
import os

#登录装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if 'user' not in session:
            return redirect(url_for('home.login',next=request.url))
        return  f(*args,**kwargs)
    return decorated_function

# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + uuid4().hex + fileinfo[-1]
    return filename


@home.route('/<int:page>/',methods=['GET','POST'])#基础页面
def index(page=None):
    tags = Tag.query.all()
    page_data = Movie.query
    #标签
    tid = request.args.get('tid',0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id = int(tid))
    #星级
    star = request.args.get('star',0)
    if int(star) != 0:
        page_data = page_data.filter_by(star = int(star))
    #时间
    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1 :
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
    #播放量
    pm = request.args.get('pm', 0)
    if int(pm) != 0:
        if int(pm) == 1:
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )
    #评论量
    cm = request.args.get('cm', 0)
    if int(cm) != 0:
        if int(pm) == 1:
            page_data = page_data.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.commentnum.asc()
            )
    if page==None:
        page=1
    page_data = page_data.paginate(page=page,per_page=10)
    p = dict(
        tid=tid,
        star=star,
        pm=pm,
        cm=cm,
        time=time
    )
    return render_template('home/index.html',tag=tags,p=p,page_data=page_data)

@home.route('/login/',methods=['GET','POST'])#登录页面
def login():
    form = LoginForm()
    if request.method=='GET':
        form.name.data = request.args.get('name')

    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name = data['name']).first()
        user_count = User.query.filter_by(name=data['name']).count()
        if user_count == 0:
            flash('用户名不存在！', 'err')
            return redirect(url_for('home.login'))
        if not user.check_pwd(data['pwd']):
            flash('密码错误！','err')
            return redirect(url_for('home.login',name=user.name))
        session['user'] = user.name
        session['user_id'] = user.id
        userlog = Userlog(
            user_id=user.id,
            ip = request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for('home.user'))
    return render_template('home/login.html',form=form)

@home.route('/logout/')#退出页面
@user_login_req
def logout():
    session.pop('user_id',None)
    session.pop('user',None)
    return redirect(url_for('home.login'))

@home.route('/register/',methods=['GET','POST'])#注册页面
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name = data['name'],
            email=data['email'],
            phone=data['phone'],
            pwd=generate_password_hash(data['pwd']),
            uuid=uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功！','ok')
    return render_template('home/register.html',form=form)

@home.route('/user/',methods=['GET','POST'])#会员中心
@user_login_req
def user():
    form = UserdetailForm()
    user = User.query.get(session['user_id'])
    form.face.validators=[]
    form.info.validators = []
    if request.method=='GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        if not os.path.exists(app.config['FC_DIR']):
            os.makedirs(app.config['FC_DIR'])
            os.chmod(app.config['FC_DIR'], "rw")
        if form.face.data.filename!='':
            if user.face:
                file_face = secure_filename(form.face.data.filename)
                os.remove(app.config['FC_DIR'] + user.face + '.png')
                user.face = change_filename(file_face)
                user.face.data.save(app.config['FC_DIR'] + user.face + '.png')
            else:
                user.face = change_filename(form.face.data.filename)
                form.face.data.save(app.config['FC_DIR'] + user.face + '.png')
        email_count = User.query.filter_by(email=data['email']).count()
        if email_count == 1 and user.email != data['email']:
            flash("邮箱已被注册！", 'err')
            return redirect(url_for("home.user"))

        phone_count = User.query.filter_by(phone=data['phone']).count()
        if phone_count == 1 and user.phone != data['phone']:
            flash("手机号码已被注册！", 'err')
            return redirect(url_for("home.user"))

        name_count = User.query.filter_by(name=data['name']).count()
        if name_count == 1 and user.name != data['name']:
            flash("昵称已存在！", 'err')
            return redirect(url_for("home.user"))

        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']
        print( user.uuid )

        db.session.add(user)
        db.session.commit()
        flash('修改成功！','ok')
        return redirect(url_for('home.user'))
    return render_template('home/user.html',form=form,user=user)

@home.route('/pwd/',methods=['GET','POST'])#修改密码
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session['user']).first()
        from werkzeug.security import generate_password_hash
        user.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(user)
        db.session.commit()
        flash("修改密码成功，请重新登录！", 'ok')
        return redirect(url_for("home.logout"))
    return render_template("home/pwd.html", form=form)


@home.route('/comments/<int:page>')#评论记录
@user_login_req
def comments(page=None):
    if page is None:
        page=1
    id = session['user_id']
    page_data = Comment.query.join(User).filter(
        User.id==id,
        User.id==Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page,per_page=10)
    return render_template('home/comments.html',page_data=page_data)

@home.route('/loginlog/<int:page>/',methods=['GET','POST'])#登录日志
@user_login_req
def loginlog(page):
    if page is None:
        page = 1
    page_data = Userlog.query.join(
        User
    ).filter(
        User.id==session['user_id'],
        User.id==Userlog.user_id,
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page,per_page=10)
    return render_template("home/loginlog.html",page_data=page_data)

@home.route('/moviecol/<int:page>/')#收藏电影
@user_login_req
def moviecol(page=None):
    if page is None:
        page=1
    id = session['user_id']
    page_data = Moviecol.query.join(User).join(Movie).filter(
        Movie.id == Moviecol.movie_id,
        User.id == id,
        User.id == Moviecol.user_id
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page,per_page=10)
    return render_template('home/moviecol_list.html',page_data=page_data)

@home.route('/moviecoladd/',methods=['POST'])#添加收藏电影
def moviecoladd():
    if request.method=='POST':
        data = json.loads(request.form.get('data'))
        name = str(data['username'])
        movie_id = int(data['movie_id'])
        movie = Movie.query.get(movie_id)

        moveicol_count = Moviecol.query.join(User).join(Movie).filter(
            User.id==Moviecol.user_id,
            Movie.id==Moviecol.movie_id,
            Movie.id==movie_id,
            User.name==name
        ).count()
        if moveicol_count == 0 :
            user = User.query.filter(User.name==name).first()
            moviecol = Moviecol(
                user_id=user.id,
                movie_id=movie_id,
                addtime=datetime.datetime.now()
            )
            db.session.add(moviecol)
            db.session.commit()
            return jsonify({'msg': '添加收藏成功！'})
        else:
            return jsonify({'msg': '添加收藏失败，《'+movie.title+'》已被收藏！'})




@home.route('/animation/')
def animation():
    data = Preview.query.all()
    count=0
    return render_template('home/animation.html',data=data,count=count)

@home.route('/search/<int:page>')
def search(page=None):
    if page==None:
        page=1
    key = request.args.get('key','')
    page_data = Movie.query.filter(
        Movie.title.like('%'+key+'%')
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page,per_page=10)
    count = Movie.query.filter(
        Movie.title.like('%'+key+'%')
    ).count()
    return render_template('home/search.html',key=key,page_data=page_data,count=count)

@home.route('/play/<int:id>/<int:page>',methods=['GET','POST'])
def play(id=None,page=None):
    movie = Movie.query.join(Tag).filter(Tag.id == Movie.tag_id, Movie.id == id).first()
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        User.id == Comment.user_id,
        Movie.id == movie.id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    movie.playnum += 1
    form = CommentForm()
    if "user" in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content = data['content'],
            movie_id= movie.id,
            user_id=session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        movie.commentnum += 1
        db.session.add(movie)
        db.session.commit()
        flash('添加评论成功', 'ok')
        return redirect(url_for('home.play', id=movie.id, page=1))
    db.session.add(movie)
    db.session.commit()
    if "user" in session:
        name = session['user']
    else:
        name = 'none'
    return render_template('home/play.html',movie=movie,form=form,page_data=page_data,name=name)


@home.route('/login/<int:id>/',methods=['GET','POST'])#登录页面
def login_cm(id):
    form = LoginForm()
    if request.method=='GET':
        form.name.data = request.args.get('name')
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name = data['name']).first()
        user_count = User.query.filter_by(name=data['name']).count()
        if user_count == 0:
            flash('用户名不存在！', 'err')
            return redirect(url_for('home.login'))
        if not user.check_pwd(data['pwd']):
            flash('密码错误！','err')
            return redirect(url_for('home.login',name=user.name))
        session['user'] = user.name
        session['user_id'] = user.id
        userlog = Userlog(
            user_id=user.id,
            ip = request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for('home.play',id=id,page=1))
    return render_template('home/login.html',form=form)

@home.route('/user/see/<int:id>/')#会员中心
def see_user(id):

    form = UserdetailForm()
    user = User.query.filter(
        User.id == id
    ).first()
    form.face.validators = []
    form.info.validators = []
    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if user.id == session['user_id']:
        return render_template('home/user.html',form=form,user=user)
    return render_template('home/see_user.html',user=user)


@home.route('/comments/see/<int:id>/<int:page>/')#评论记录
def see_comments(id,page=None):
    user = User.query.get(int(id))
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id,
        User.id == id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/see_comments.html',page_data=page_data,user=user)

@home.route('/moviecol/see/<int:id>/<int:page>/')#收藏电影
def see_moviecol(id,page=None):
    user = User.query.get(int(id))
    if page is None:
        page=1
    id = user.id
    page_data = Moviecol.query.join(User).join(Movie).filter(
        Movie.id == Moviecol.movie_id,
        User.id == id,
        User.id == Moviecol.user_id
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page,per_page=10)
    return render_template('home/see_moviecol.html',page_data=page_data,user=user)