#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint
from backend import models


app_views = Blueprint("app_views", __name__, url_prefix="/byteschool")


users = models.storage.all("User")

from api.v1.views.users import *
from api.v1.views.index import *
from api.v1.views.projects import *