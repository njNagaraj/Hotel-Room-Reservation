from flask import Blueprint, render_template

main_page = Blueprint('main_page', __name__)

@main_page.route('/', methods=['GET', 'POST'])
@main_page.route('/main', methods=['GET', 'POST'])
def main():
    return render_template('main.html')