import os
import requests
import urllib.parse
import calendar

from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def dateString(dashDate):
    """ Converts from YYYY-MM-DD to Month Day, Year format"""

    if dashDate != "N/A":
        dateString = calendar.month_name[int(dashDate.split("-")[1])] + " " + dashDate.split("-")[2].lstrip("0") + ", " + dashDate.split("-")[0].lstrip('0')
        return(dateString)
    else:
        return("N/A")