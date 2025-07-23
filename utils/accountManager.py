import sqlite3
import pandas as pd
import streamlit as st

class CategoryManager:

    def __init__(self, username, db_name="category.db"):

        self.db_name = db_name
        self.username = username
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS category (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT,
                                category_type TEXT,
                                category TEXT)''')
        
        self.cursor.execute("SELECT * FROM category where username='admin'")

        if self.cursor.fetchone() is None:
            self.cursor.execute('''INSERT INTO category (username, category_type, category)
                        VALUES (?, ?, ?)''', 
                        ('admin', 'Cash In', 'Investment'))
        
            self.cursor.execute('''INSERT INTO category (username, category_type, category)
                                VALUES (?, ?, ?)''', 
                                ('admin', 'Cash In', 'Sales'))
            
            self.cursor.execute('''INSERT INTO category (username, category_type, category)
                                VALUES (?, ?, ?)''', 
                                ('admin', 'Cash Out', 'Rent'))
            
            self.cursor.execute('''INSERT INTO category (username, category_type, category)
                                VALUES (?, ?, ?)''', 
                                ('admin', 'Cash Out', 'Employee Salary'))        
            self.conn.commit()


    def addCategory(self, category_type, category): #WHAT IS THIS? :(
        self.cursor.execute('''INSERT INTO category (username, category_type, category)
                               VALUES (?, ?, ?)''', 
                               (self.username, category_type, category))
        self.conn.commit()

    def viewCategory(self,category_type='Cash In'):
        query = "SELECT username,category_type,category FROM category where username='{}' or username ='admin'".format(self.username,category_type)
        return pd.read_sql(query, self.conn)

class ProfileManager:

    def __init__(self, username, db_name="profile.db"):

        self.db_name = db_name
        self.username = username
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS profile (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE,
                                business_name TEXT,
                                business_type TEXT,
                                business_open_date DATE,
                                business_size INTEGER,
                                business_location TEXT)''')
        self.conn.commit()

    def addProfile(self, business_name, business_type,business_open_date,business_size,business_location): #WHAT IS THIS? :(
        self.cursor.execute('''INSERT INTO profile (username, business_name, business_type,business_open_date,business_size,business_location)
                               VALUES (?, ?, ?, ?, ?, ?)''', 
                               (self.username, business_name, business_type,business_open_date,business_size,business_location))
        self.conn.commit()

    def updateProfile(self, business_name, business_type,business_open_date,business_size,business_location):
        self.cursor.execute('''UPDATE profile SET business_name=?, business_type=?, business_open_date=?, business_size=?, business_location=? WHERE username=?''', 
                               (business_name, business_type,business_open_date,business_size,business_location, self.username))
        self.conn.commit()

    def viewProfile(self):
        query = "SELECT * FROM profile WHERE username='{}'".format(self.username)
        return pd.read_sql(query, self.conn)

class BudgetManager:

    def __init__(self, username, db_name="budget.db"):

        self.db_name = db_name
        self.username = username
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS budget (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE,
                                budget_str TEXT,
                                short_term_goal TEXT,
                                long_term_goal TEXT)''')
        self.conn.commit()

    def addBudget(self, budget_str, short_term_goal,long_term_goal): #WHAT IS THIS? :(
        self.cursor.execute('''INSERT INTO budget (username, budget_str, short_term_goal,long_term_goal)
                               VALUES (?, ?, ?, ?)''', 
                               (self.username, budget_str, short_term_goal,long_term_goal))
        self.conn.commit()

    def updateBudget(self, budget_str, short_term_goal,long_term_goal):
        self.cursor.execute('''UPDATE budget SET budget_str=?, short_term_goal=?, long_term_goal=? WHERE username=?''', 
                               (budget_str, short_term_goal,long_term_goal, self.username))
        self.conn.commit()  

    def viewBudget(self):
        query = "SELECT * FROM budget WHERE username='{}'".format(self.username)
        return pd.read_sql(query, self.conn)
    
#Expense manager class using db
class ExpenseManager:

    def __init__(self, username, db_name="expenses.db"):

        self.db_name = db_name
        self.username = username
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT,
                                category TEXT,
                                date DATE,
                                amount REAL,
                                description TEXT)''')
        self.conn.commit()

    def addExpense(self, category, date, amount, description): #WHAT IS THIS? :(
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               (self.username, category, date, amount, description))
        self.conn.commit()

    def viewExpenses(self):
        query = "SELECT category, date, amount, description FROM expenses where username='{}' order by date desc limit 10".format(self.username)
        return pd.read_sql(query, self.conn)

    # def deleteExpense(self, expense_id):
    #     self.cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    #     self.conn.commit()


class IncomeManager:
    def __init__(self, username, db_name="income.db"):
        self.db_name = db_name
        self.username = username
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS income (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT,
                                category TEXT,
                                date DATE,
                                amount REAL,
                                description TEXT)''')
        self.conn.commit()

    def addIncome(self, category, date, amount, description):
        self.cursor.execute('''INSERT INTO income (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               (self.username, category, date, amount, description))
        self.conn.commit()

    def viewIncome(self):
        query = "SELECT category, date, amount, description FROM income where username='{}' order by date desc limit 10".format(self.username)
        return pd.read_sql(query, self.conn)

    # def deleteIncome(self, income_id):
    #     self.cursor.execute("DELETE FROM income WHERE id=?", (income_id,))
    #     self.conn.commit()


class Account:
    def __init__(self, username):
        self.IncomeManager = IncomeManager(username)
        self.ExpenseManager = ExpenseManager(username)
        self.CategoryManager = CategoryManager(username)
        self.ProfileManager = ProfileManager(username)
        self.BudgetManager = BudgetManager(username)
        self.Balance = 0.0  

    def getBalance(self):
        total_income = self.IncomeManager.viewIncome()["amount"].sum()
        total_expense = self.ExpenseManager.viewExpenses()["amount"].sum()
        self.Balance = total_income - total_expense
        return self.Balance

    def addExpense(self, category, date, amount, description):
        self.ExpenseManager.addExpense(category, date, amount, description)
        self.Balance -= amount
        st.success(f"Expense added successfully!")

    def addIncome(self, category, date, amount, description):
        self.IncomeManager.addIncome(category, date, amount, description)
        self.Balance += amount
        st.success(f"Income added successfully!")

    def expenseList(self):
        return self.ExpenseManager.viewExpenses()

    def incomeList(self):
        return self.IncomeManager.viewIncome()
    
    def categoryList(self):
        return self.CategoryManager.viewCategory()

    def deleteExpense(self, expense_id):
        expenses = self.ExpenseManager.viewExpenses()
        if expenses.empty:
            st.warning("No expenses to delete.")
            return

        if expense_id in expenses["id"].values:
            amount = expenses.loc[expenses["id"] == expense_id, "amount"].iloc[0]
            self.ExpenseManager.deleteExpense(expense_id)
            self.Balance += amount
            st.success(f"Expense {expense_id} deleted successfully!")
        else:
            st.warning(f"Invalid Expense ID: {expense_id}")

    def deleteIncome(self, income_id):
        incomes = self.IncomeManager.viewIncome()
        if incomes.empty:
            st.warning("No income records to delete.")
            return

        if income_id in incomes["id"].values:
            amount = incomes.loc[incomes["id"] == income_id, "amount"].iloc[0]
            self.IncomeManager.deleteIncome(income_id)
            self.Balance -= amount
            st.success(f"Income {income_id} deleted successfully!")
        else:
            st.warning(f"Invalid Income ID: {income_id}")

# transactions list
    def format_transactions_for_ai(self):
        expenses = self.ExpenseManager.viewExpenses()
        income = self.IncomeManager.viewIncome()
        
       
        formatted_expenses = expenses[['name', 'date', 'amount', 'category', 'description']].to_dict(orient='records')
        formatted_income = income[['name', 'date', 'amount', 'source', 'description']].to_dict(orient='records')
        
        # final dictionary to be returned
        transactions = {
            'income': formatted_income,
            'expenses': formatted_expenses
        }
        
        return transactions