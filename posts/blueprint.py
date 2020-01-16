from flask import Blueprint, render_template, request, redirect, url_for
from flask_security import login_required

from models import Post, Tag, slugify
from .forms import PostForm, TagForm
from app import db


posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():

    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            print('Something wrong!')

        return redirect(url_for('posts.index'))

    else:
        form = PostForm()
        return render_template('posts/create_post.html', form=form)


@posts.route('/<slug>/update/', methods=['POST', 'GET'])
@login_required
def post_update(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    print(post)

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post) # Заполняет поля объекта post данными, введенными пользователем
        db.session.commit()

        return redirect(url_for('posts.post_detail', slug=post.slug))

    form = PostForm(obj=post)
    return render_template('posts/post_update.html', post=post, form=form)


@posts.route('/')
def index():
    q = request.args.get('q')
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=4)

    return render_template('posts/index.html', pages=pages)


# http://127.0.0.1:5000/blog/1
@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug==slug).first_or_404()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)


@posts.route('/tag/create', methods=['POST', 'GET'])
@login_required
def tag_create():

    if request.method == 'POST':
        name = request.form.get('name')

        try:
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.commit()
        except:
            print('Something wrong!')

        return redirect(url_for('posts.tag_detail', slug=tag.slug))

    else:
        form = TagForm()
        return render_template('posts/tag_create.html', form=form)


@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first()
    if tag:
        posts = tag.posts.all()
        return render_template('posts/tag_detail.html', tag=tag, posts=posts)
    return render_template('404.html'), 404
