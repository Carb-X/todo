from app import app, db
from flask import request, render_template, redirect, url_for
from app.models import Category, Item


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        body = request.form.get('item')
        category_id = request.form.get('category')
        category = Category.query.get_or_404(category_id)
        item = Item(body=body, category=category)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('category', id=category_id))
    return redirect(url_for('category', id=1))


@app.route('/category/<int:id>')
def category(id):
    category = Category.query.get_or_404(id)
    categories = Category.query.all()
    items = category.items
    return render_template('index.html', items=items,
                           categories=categories, category_now=category)


@app.route('/new-category', methods=['GET', 'POST'])
def new_category():
    name = request.form.get('name')
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('category', id=category.id))


@app.route('/edit-item/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    category = item.category
    item.body = request.form.get('body')
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('category', id=category.id))


@app.route('/edit-category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    category.name = request.form.get('name')
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('category', id=category.id))


@app.route('/done/<int:id>', methods=['GET', 'POST'])
def done(id):
    item = Item.query.get_or_404(id)
    category = item.category
    done_category = Category.query.get_or_404(2)
    done_item = Item(body=item.body, category=done_category)
    db.session.add(done_item)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('category', id=category.id))


@app.route('/delete-item/<int:id>')
def del_item(id):
    item = Item.query.get_or_404(id)
    category = item.category
    if item is None:
        return redirect(url_for('category', id=1))
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('category', id=category.id))


@app.route('/delete-category/<int:id>')
def del_category(id):
    category = Category.query.get_or_404(id)
    if category is None or id in [1, 2]:
        return redirect(url_for('category', id=1))
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('category', id=1))