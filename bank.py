# bank.py

import mysql.connector
from datetime import datetime

class Bank:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="merit@me123",
            database="banking_system1"
        )
        self.cursor = self.db.cursor()

    def create_user(self, username, password, phone_number, gender, address, email):
        query = "INSERT INTO users (username, password, phone_number, gender, address, email, balance) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (username, password, phone_number, gender, address, email, 0.0)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            print("User created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def login_user(self, username, password):
        query = "SELECT user_id FROM users WHERE username = %s AND password = %s"
        values = (username, password)

        try:
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()

            if result:
                return result[0]  # Return user_id
            else:
                return None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def deposit(self, user_id, amount):
        query = "UPDATE users SET balance = balance + %s WHERE user_id = %s"
        values = (amount, user_id)

        try:
            self.cursor.execute(query, values)
            self.db.commit()

            # Record the transaction
            self.record_transaction(user_id, 'Deposit', amount)

            print("Deposit successful.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def withdraw(self, user_id, amount):
        query = "UPDATE users SET balance = balance - %s WHERE user_id = %s AND balance >= %s"
        values = (amount, user_id, amount)

        try:
            self.cursor.execute(query, values)

            if self.cursor.rowcount > 0:
                self.db.commit()

                # Record the transaction
                self.record_transaction(user_id, 'Withdrawal', amount)

                print("Withdrawal successful.")
            else:
                print("Insufficient funds.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def get_statement(self, user_id):
        user_query = "SELECT * FROM users WHERE user_id = %s"
        user_values = (user_id,)

        transactions_query = "SELECT * FROM transactions WHERE user_id = %s"
        transactions_values = (user_id,)

        try:
            self.cursor.execute(user_query, user_values)
            user_result = self.cursor.fetchone()

            self.cursor.execute(transactions_query, transactions_values)
            transactions_result = self.cursor.fetchall()

            if user_result:
                user_info = {'user_id': user_result[0], 'username': user_result[1], 'balance': user_result[3]}  # Adjust index for balance
                transaction_history = [{'date': transaction[4], 'type': transaction[2], 'amount': transaction[3]} for transaction in transactions_result]
                user_info['transactions'] = transaction_history
                return user_info
            else:
                print("User not found.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def record_transaction(self, user_id, transaction_type, amount):
        query = "INSERT INTO transactions (user_id, type, amount, date) VALUES (%s, %s, %s, %s)"
        values = (user_id, transaction_type, amount, datetime.now())

        try:
            self.cursor.execute(query, values)
            self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
