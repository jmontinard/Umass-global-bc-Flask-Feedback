from flask import Flask, render_template, redirect, session, flash, Response
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)



@app.route('/')
def show_home():
    """Homepage of site, redirect to register."""
    return redirect("/register")



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/unauthorized")
def unauthorized():
    return Response(response="Unauthorized", status=401)

@app.route('/register', methods=['GET', 'POST'])
def show_register():
    """handles register action for form"""
    # user = User.query.get_or_404(session['username'])
    if "username" in session:
         flash(f"{session['username']} Aleady logged in!", "danger")
         return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data 
        
        # new_user = User(username = username, password = password, email = email, first_name = first_name, last_name=last_name)
        new_user = User.register(username, password, first_name, last_name, email)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:

            form.username.errors.append('Username taken. Please pick another')
            return render_template('register.html', form=form)
        
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f"/users/{new_user.username}")

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """handles login action for form"""
    
    if "username" in session:
         flash(f"{user.username} Aleady logged in!", "danger")
         return redirect(f"/users/{session['username']}")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username/password.']
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    """Log out User"""
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/login')


@app.route('/users/<username>')
def show_secret(username):
    """show our oh so secret secret"""
    user = User.query.get_or_404(username)
    form = DeleteForm()
    if "username" not in session or username != session['username']:
         flash("Please login first!", "danger")
         return redirect('/unauthorized')
    
    return render_template("userDetails.html",form=form, user=user)


@app.route('/users/<username>/delete', methods= ["POST"])
def delete_user(username):
    """deletes selected user"""
    user = User.query.get_or_404(username)
    if "username" not in session or username != session['username']:
         flash("Please login first!", "danger")
         return redirect('/unauthorized')
    db.session.delete(user)
    db.session.commit() 
    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def new_feedback(username):
    """handles add feedback action for form"""

    if "username" not in session or username != session['username']:
         flash("Please login first!", "danger")
         return redirect('/unauthorized')

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=username)
        
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    else:
        return render_template('addFeedback.html', form=form)



@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    """handles edit feedback action for form"""
    # user = User.get_or_404(username)
    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.user.username != session['username']:
        flash("{feedback.user.username} does not have access to this feedback post", "danger")
        return redirect('/unauthorized')

    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template('editFeedback.html', form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """deletes selected user""" 
    feedback = Feedback.query.get_or_404(feedback_id)
    if "username" not in session or feedback.username != session['username']:
         flash("Please login first!", "danger")
         return redirect('/unauthorized')

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
