from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required

from form.Host import HostAddForm


class HostController:

    def hostAddForm(self):
        form = HostAddForm()
        return render_template('host.html', form=form)
