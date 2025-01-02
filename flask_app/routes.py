from flask import Blueprint, current_app, jsonify, Response, request, render_template, redirect, url_for, flash
from flask_app import db, bcrypt
from flask_app.models import User, Project, Category, Item
from flask_login import login_user, logout_user, login_required, current_user
from flask_app.forms import RegistrationForm, LoginForm
from dotenv import load_dotenv
import io, csv, re
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def home():
    return render_template('home.html', RForm = RegistrationForm(), LForm = LoginForm())

