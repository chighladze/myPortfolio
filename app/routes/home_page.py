# myPortfolio/app/routes/home_page.py
from flask import Blueprint, render_template

home_page = Blueprint('home_page', __name__)

@home_page.route('/', methods=['GET'])
def index():
    return render_template('home_page.html')
