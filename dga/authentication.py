from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    flash,
    session,
    Blueprint,
)
from dga import auth
from .rtdatabase import db

authentication = Blueprint("authentication", __name__)


@authentication.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        session.pop("_flashes", None)  # clear flash messages

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            # print(auth.get_account_info(user['idToken']))
            # print(auth.current_user)
            session["idToken"] = user["idToken"]
            return redirect(url_for("rtdatabase.home"))
        except:
            flash("Invalid username/password combination.", "danger")
            return redirect(url_for("authentication.index"))
    else:
        return render_template("index.html")


@authentication.route("/logout")
def logout():
    auth.current_user = None
    session.pop("idToken", None)
    print("User logged out")
    return redirect(url_for("authentication.index"))


@authentication.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        # we can use request.form.get() to avoid getting errors if the form field is empty
        # with this we will get None instead
        # email = request.form.get('email')
        # password = request.form.get('password')
        # confirm_password = request.form.get('cpassword')
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["cpassword"]
        session.pop("_flashes", None)  # clear flash messages

        try:
            # Password must be looooooooong
            # You have to meet google's password complexity standards
            # if len(password) < 7:
            #     flash('Password must be at least 7 characters long', 'error')
            #     return redirect(url_for('registration'))

            if password != confirm_password:
                flash("Passwords do not match", "error")
                return redirect(url_for("authentication.registration"))

            auth.create_user_with_email_and_password(email, password)

            flash("Registration successful. You can login now.", "msg")
            return redirect(url_for("authentication.index"))
        except Exception as e:
            print(e)
            flash("Email already exists", "error")
            return redirect(url_for("authentication.registration"))
    else:
        return render_template("registration.html")


# def get_user_id_by_email(email):
#     user = auth.get_account_info(auth.current_user['idToken'])['localId']

#     return user
