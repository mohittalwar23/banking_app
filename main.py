# main.py

from flask import Flask, render_template, request, redirect, url_for
from bank import Bank

app = Flask(__name__, static_url_path='/static')
bank = Bank()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone_number = request.form['phone_number']
        gender = request.form['gender']
        address = request.form['address']
        email = request.form['email']
        bank.create_user(username, password, phone_number, gender, address, email)
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = bank.login_user(username, password)

        if user_id:
            return redirect(url_for('dashboard', user_id=user_id))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/dashboard/<int:user_id>', methods=['GET', 'POST'])
def dashboard(user_id):
    if request.method == 'POST':
        amount = float(request.form['amount'])

        if 'deposit' in request.form:
            bank.deposit(user_id, amount)
        elif 'withdraw' in request.form:
            bank.withdraw(user_id, amount)

    user_info = bank.get_statement(user_id)
    return render_template('dashboard.html', user_info=user_info)

@app.route('/deposit/<int:user_id>', methods=['POST'])
def deposit(user_id):
    if request.method == 'POST':
        amount = float(request.form['amount'])
        bank.deposit(user_id, amount)

    return redirect(url_for('dashboard', user_id=user_id))

@app.route('/withdraw/<int:user_id>', methods=['POST'])
def withdraw(user_id):
    if request.method == 'POST':
        amount = float(request.form['amount'])
        bank.withdraw(user_id, amount)

    return redirect(url_for('dashboard', user_id=user_id))

@app.route('/signout', methods=['POST'])
def signout():
    # Perform any signout logic if needed
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
