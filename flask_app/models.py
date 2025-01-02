from flask_app import db
from datetime import datetime
from flask_login import UserMixin

import pytz

def pstnow():
    return datetime.now(pytz.timezone('US/Pacific'))

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    total = db.Column(db.Float, nullable=False, default=0.0)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=pstnow)
    updated_at = db.Column(db.DateTime, default=pstnow, onupdate=pstnow)
    
    categorys = db.relationship("Category", back_populates="user", lazy="dynamic")
    projects = db.relationship("Project", back_populates="user", lazy="dynamic")

class Project(db.Model):
    __tablename__="projects"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default=pstnow)
    updated_at = db.Column(db.DateTime, default=pstnow, onupdate=pstnow)
    
    items = db.relationship("Item", secondary="projectItems", back_populates="projects", lazy="dynamic")
    
class ProjectItems(db.Model):
    __tablename__="projectItems"
    id = db.Column(db.Integer, primary_key = True)
    project_id = db.Column(db.Integer, db.ForeignKey('categorys.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    
class Item(db.Model):
    __tablename__="items"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=pstnow)
    updated_at = db.Column(db.DateTime, default=pstnow, onupdate=pstnow)
    
    categorys = db.relationship("Category", secondary="categoryItems", back_populates="items", lazy="dynamic")
    projects = db.relationship("Item", secondary="projectItems", back_populates="items", lazy="dynamic")

class CategoryItems(db.Model):
    __tablename__="categoryItems"
    id = db.Column(db.Integer, primary_key = True)
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

class Category(db.Model):
    __tablename__="categorys"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    created_at = db.Column(db.DateTime, default=pstnow)
    updated_at = db.Column(db.DateTime, default=pstnow, onupdate=pstnow)

    user = db.relationship("User", back_populates="categorys")
    items = db.relationship("Item", secondary="categoryItems", back_populates="categorys", lazy="dynamic")