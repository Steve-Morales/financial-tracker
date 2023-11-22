from flask import Flask, render_template, url_for, request, redirect, jsonify
import utils
from database import db as db
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.app_context().push()
db.init_app(app)
utils.app = app


from models.user import User
from models.expense import Expense
from models.category import Category
with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Hash the password before storing it
        hashed_password = utils.hash_password(password=password)

        # Create a new user with the hashed password
        new_user = User(email=email, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and utils.password_match(password):
            # login_user(user)
            return redirect(url_for('index'))  # Redirect after successful login

    return render_template('login.html')


# Endpoint to retrieve categories
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    formatted_categories = []
    for category in categories:
        formatted_categories.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
        })
    return jsonify({'categories': formatted_categories})


# Endpoint to create a new category
@app.route('/create_category', methods=['POST'])
def create_category():
    category_name = request.form['category_name']
    category_description = request.form['category_description']

    new_category = Category(name=category_name, description=category_description)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({'message': 'Category created successfully'})


# Endpoint to add an expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    expense_title = request.form['expense_title']
    expense_description = request.form['expense_description']
    expense_balance = request.form['expense_balance']
    category_id = request.form['category_id']

    new_expense = Expense(
        title=expense_title,
        description=expense_description,
        balance=expense_balance,
        category_id=category_id,
        date_created=datetime.utcnow()
    )
    db.session.add(new_expense)
    db.session.commit()

    return jsonify({'message': 'Expense added successfully'})


# Endpoint to retrieve expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    formatted_expenses = []
    for expense in expenses:
        formatted_expenses.append({
            'id': expense.id,
            'title': expense.title,
            'description': expense.description,
            'balance': expense.balance,
            'category': expense.category.name,
            'date_created': expense.date_created.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify({'expenses': formatted_expenses})

# Endpoint to update an expense
@app.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    # Get expense details from request data
    # Update the expense in the database using expense_id
    # Return appropriate response
    expense = Expense.query.get(expense_id)

    if not expense:
        return jsonify({'message': 'Expense not found'}), 404

    # Get updated details from request data
    title = request.json.get('title')
    description = request.json.get('description')
    balance = request.json.get('balance')
    category_id = request.json.get('category_id')

    # Update expense fields if provided in request
    if title:
        expense.title = title
    if description:
        expense.description = description
    if balance:
        expense.balance = balance
    if category_id:
        expense.category_id = category_id

    db.session.commit()
    return jsonify({'message': 'Expense updated successfully'})


# Endpoint to delete an expense
@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    # Delete the expense from the database using expense_id
    # Return appropriate response
    expense = Expense.query.get(expense_id)

    if not expense:
        return jsonify({'message': 'Expense not found'}), 404

    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted successfully'})

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
