from app import application, classes, db
from app import model, tokenizer
from app.model import predict_statement
from app.model import bigram_explain, monogram_explain

from flask import flash, render_template, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField

import os


class UploadFileForm(FlaskForm):
    """Class for uploading file when submitted"""
    file_selector = FileField('File', validators=[FileRequired()])
    submit = SubmitField('Submit')


# @application.route('/index')
# def index():
#     """Index Page : Renders index.html with author name."""
#     return ("<h1> File uploaded. Thanks for using Deep Depeception! </h1>")
#     # return (render_template('index.html', author='Deep Deception'))


@application.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    prediction_form = classes.PredictionForm()
    if prediction_form.validate_on_submit():
        statement = prediction_form.statement.data

        soft_preds, hard_preds = predict_statement(str(statement), model=model, tokenizer=tokenizer)

#       # dummy dics
#        dic1 = {'"said': 4.814517498016357, 'AIG': 3.624594211578369, 'were': 3.196007013320923}
#        dictionary2 = {'being': -0.0250399112701416, 'payments)': -0.04054903984069824, 'giving': -1.5874862670898438}

        dic1, dictionary2 = monogram_explain(str(statement), model, tokenizer)

        word1 = list(dic1.keys())[0]
        word2 = list(dic1.keys())[1]
        word3 = list(dic1.keys())[2]
        
        word4 = list(dictionary2.keys())[0]
        word5 = list(dictionary2.keys())[1]
        word6 = list(dictionary2.keys())[2]
        
        proba1 = list(dic1.values())[0]
        proba2 = list(dic1.values())[1]
        proba3 = list(dic1.values())[2]
        
        proba4 = list(dictionary2.values())[0]
        proba5 = list(dictionary2.values())[1]
        proba6 = list(dictionary2.values())[2]

        if hard_preds[0] == 1:
            veracity = "The statement is true."
        else:
            veracity = "The statement is false." 
        if True:
            return render_template('predict.html', form=prediction_form, 
                            word1=word1, word2=word2, word3=word3, 
                            word4=word4, word5=word5, word6=word6, 
                            proba1=proba1, proba2=proba2, proba3=proba3, 
                            proba4=proba4, proba5=proba5, proba6=proba6,
                            soft_preds= soft_preds[0], hard_preds = hard_preds[0],
                            veracity=veracity)

    return render_template('predict.html', form=prediction_form)
        
    # prediction_form = classes.PredictionForm()
    # if prediction_form.validate_on_submit():
    #     statement = prediction_form.statement.data
    #     soft_preds, hard_preds = predict_statement(str(statement), model=model, tokenizer=tokenizer)
    #     dic1 = {'"said': 4.814517498016357, 'AIG': 3.624594211578369, 'were': 3.196007013320923}
    #     dictionary2 = {'being': -0.0250399112701416, 'payments)': -0.04054903984069824, 'giving': -1.5874862670898438}

    #     word1 = list(dic1.keys())[0]
    #     word2 = list(dic1.keys())[1]
    #     word3 = list(dic1.keys())[2]
        
    #     word4 = list(dictionary2.keys())[0]
    #     word5 = list(dictionary2.keys())[1]
    #     word6 = list(dictionary2.keys())[2]
        
    #     proba1 = list(dic1.values())[0]
    #     proba2 = list(dic1.values())[1]
    #     proba3 = list(dic1.values())[2]
        
    #     proba4 = list(dictionary2.values())[0]
    #     proba5 = list(dictionary2.values())[1]
    #     proba6 = list(dictionary2.values())[2]

    #     if hard_preds:
    #     # if hard_preds[0] == 1:
    #     #     return "The statement is True."
    #     # else:
    #     #     return "The statement is False."
    #         return render_template('predict.html', word1=word1, word2=word2,
    #                             word3=word3, word4=word4, word5=word5,
    #                             word6=word6, proba1=proba1, proba2=proba2,
    #                             proba3=proba3, proba4=proba4, proba5=proba5,
    #                             proba6=proba6)

    # # return render_template('predict.html', form=prediction_form)


#@application.route('/upload', methods=['GET', 'POST'])
#@login_required
#def upload():
#    """
#    upload and process a csv file to check for deception.
#    Note: This is still a WIP
#    """
#    file = UploadFileForm()  # file : UploadFileForm class instance
#    if file.validate_on_submit():  # Check if it is a POST request and if it is valid.
#        f = file.file_selector.data  # f : Data of FileField
#        filename = f.filename
#        # filename : filename of FileField
#
#        file_dir_path = os.path.join(application.instance_path, 'files')
#        file_path = os.path.join(file_dir_path, filename)
#        # f.save(file_path)  # Save file to file_path (instance/ + 'files’ + filename)
#
#        return redirect(url_for('upload'))  # Redirect to / (/index) page.
#    return render_template('upload.html', form=file)


@application.route('/register', methods=('GET', 'POST'))
def register():
    registration_form = classes.RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = classes.User.query.filter_by(username=username).count() \
                     + classes.User.query.filter_by(email=email).count()
        if user_count > 0:
            flash('Error - Existing user : ' + username + ' OR ' + email)
        else:
            user = classes.User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', form=registration_form)


@application.route('/index')
@application.route('/')
def main():
    return render_template('index.html')

@application.route('/plotly')
def plotly():
    return render_template('plotly.html')

@application.route('/google')
def google():
    dic1 = {'"said': 4.814517498016357, 'AIG': 3.624594211578369, 'were': 3.196007013320923}
    dictionary2 = {'being': -0.0250399112701416, 'payments)': -0.04054903984069824, 'giving': -1.5874862670898438}

    word1 = list(dic1.keys())[0]
    word2 = list(dic1.keys())[1]
    word3 = list(dic1.keys())[2]
    
    word4 = list(dictionary2.keys())[0]
    word5 = list(dictionary2.keys())[1]
    word6 = list(dictionary2.keys())[2]
    
    proba1 = list(dic1.values())[0]
    proba2 = list(dic1.values())[1]
    proba3 = list(dic1.values())[2]
    
    proba4 = list(dictionary2.values())[0]
    proba5 = list(dictionary2.values())[1]
    proba6 = list(dictionary2.values())[2]
    
    return render_template('google.html', word1=word1, word2=word2,
                            word3=word3, word4=word4, word5=word5,
                            word6=word6, proba1=proba1, proba2=proba2,
                            proba3=proba3, proba4=proba4, proba5=proba5,
                            proba6=proba6)

@application.route('/login', methods=['GET', 'POST'])
def login():
    login_form = classes.LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Look for it in the database.
        user = classes.User.query.filter_by(username=username).first()

        # Login and validate the user.
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('predict'))
        else:
            flash('Invalid username and password combination!')

    return render_template('login.html', form=login_form)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@application.errorhandler(401)
def re_route(e):
    return redirect(url_for('login'))


# @application.route('/team')
# def team():
#     """Index Page : Renders index.html with author name."""
#     return (render_template('our-team.html', author='Deception Perception'))
