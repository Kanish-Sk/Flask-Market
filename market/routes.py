from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':#To avoid resubmission we can use it instends of using validate_on_submit() both are same.
        # Purchse Item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'Congratulation! You purchased {p_item_object.name} for {p_item_object.price}₹', category="sucess")

            else:
                flash(f"Unfortunately, you don't have an enough money to purchase {p_item_object.name}", category="danger")

        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f'Congratulation! You sold {s_item_object.name} back to market!')

            else:
                flash(f"Somthing went wrong witn selling {s_item_object.name}",
                      category="danger")


        # After purchase it will redirect into the market page.
        return redirect(url_for('market_page'))

    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)#  We can id here because we relate two tables using id.
        return render_template("market.html", items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])  # route can handle post request.
def register_page():
    form = RegisterForm()
    if form.validate_on_submit(): #  All information are validate to store in the database then it will work.
        user_to_create = User(user_name=form.username.data,
                              emil_address=form.email_address.data,
                              password=form.password1.data)
        #  password goes to @password.setter and store the hashed password.
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.user_name}', category='success')
        return redirect(url_for("market_page"))

    # from.errors it is dictionary it stores value if validation fails.
    if form.errors != {}:  # If there is an error in the validation
        for err_msg in form.errors.values():
            flash(f'There was an error with creating user:{err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(user_name=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.user_name}', category='success')
            return redirect(url_for('market_page'))

        else:
            flash('Username and password are not match1 Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
