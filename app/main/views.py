from flask import render_template, session, redirect, url_for, current_app
from .forms import ContainerName, ItemName, NameForm
from . import main



@main.route('/', methods=['GET', 'POST'])
def index():
    # form = NameForm()
    # session['name'] = form.name.data
    # return render_template('index.html', form=form, name=session.get('name'))

    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['CLEANING-ZEN_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))


@main.route('/items', methods=['GET', 'POST'])
def form_add_item():
    itemform = ItemName()
    session['item'] = itemform.name.data
    return render_template('form_add_item.html', form=itemform, name=session.get('item'))


@main.route('/container', methods=['GET', 'POST'])
def form_add_container():
    containerform = ContainerName()
    session['container'] = containerform.name.data
    return render_template('form_add_container.html', form=containerform, name=session.get('container'))


@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)