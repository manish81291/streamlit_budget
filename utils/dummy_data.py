import sqlite3
import pandas as pd
import streamlit as st


class InsertIncome:

    def __init__(self, db_name="income.db"):

        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def addIncome(self):

        self.cursor.execute('''INSERT INTO income (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Sales", "2024-07-01", "7845", "Income"))
        self.cursor.execute('''INSERT INTO income (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Sales", "2024-08-01", "8083.3", "Income"))
        self.cursor.execute('''INSERT INTO income (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Sales", "2024-09-01", "8105", "Income"))
        self.cursor.execute('''INSERT INTO income (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Sales", "2024-10-01", "8271.1", "Income"))
        self.cursor.execute('''INSERT INTO income (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Sales", "2024-11-01", "8290", "Income"))
        self.cursor.execute('''INSERT INTO income (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Sales", "2024-12-01", "8300", "Income"))
        self.cursor.execute('''INSERT INTO income (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Sales", "2025-01-01", "8457", "Income"))
        self.cursor.execute('''INSERT INTO income (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Sales", "2025-02-01", "8516", "Income"))
        self.cursor.execute('''INSERT INTO income (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Sales", "2025-03-01", "8599.5", "Income"))
        self.cursor.execute('''INSERT INTO income (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Sales", "2025-04-01", "8683", "Income"))
        self.cursor.execute('''INSERT INTO income (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Sales", "2025-05-01", "8766.5", "Income"))
        self.cursor.execute('''INSERT INTO income (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Sales", "2025-06-01", "8850", "Income"))


        self.conn.commit()


class InsertExpense:

    def __init__(self, db_name="expenses.db"):

        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def addExpense(self):

        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Rent", "2024-07-01", "900", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Rent", "2024-08-01", "900", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Rent", "2024-09-01", "900", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Rent", "2024-10-01", "900", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Rent", "2024-11-01", "900", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Rent", "2024-12-01", "900", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Rent", "2025-01-01", "900", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Rent", "2025-02-01", "900", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Rent", "2025-03-01", "900", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Rent", "2025-04-01", "950", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Rent", "2025-05-01", "950", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Rent", "2025-06-01", "950", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Employee", "2024-07-01", "2000", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Employee", "2024-08-01", "2300", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Employee", "2024-09-01", "2410", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Employee", "2024-10-01", "2646.66666666667", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Employee", "2024-11-01", "2851.66666666667", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Employee", "2024-12-01", "3056.66666666667", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Employee", "2025-01-01", "3261.66666666667", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Employee", "2025-02-01", "3466.66666666667", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Employee", "2025-03-01", "3571.66666666667", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Employee", "2025-04-01", "3776.66666666667", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Employee", "2025-05-01", "4081.66666666667", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Employee", "2025-06-01", "4186.66666666667", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Utilities", "2024-07-01", "180", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Utilities", "2024-08-01", "180", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Utilities", "2024-09-01", "210", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Utilities", "2024-10-01", "190", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Utilities", "2024-11-01", "220", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Utilities", "2024-12-01", "250", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Utilities", "2025-01-01", "250", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Utilities", "2025-02-01", "280", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Utilities", "2025-03-01", "270", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Utilities", "2025-04-01", "280", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Utilities", "2025-05-01", "290", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Utilities", "2025-06-01", "290", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Marketing", "2024-07-01", "2000", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Marketing", "2024-08-01", "2000", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Marketing", "2024-09-01", "2000", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Marketing", "2024-10-01", "2000", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Marketing", "2024-11-01", "1900", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Marketing", "2024-12-01", "1980", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Marketing", "2025-01-01", "1700", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Marketing", "2025-02-01", "1500", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Marketing", "2025-03-01", "1500", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Marketing", "2025-04-01", "1200", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Marketing", "2025-05-01", "1200", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Marketing", "2025-06-01", "1200", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Miscellaneous", "2024-07-01", "1100", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Miscellaneous", "2024-08-01", "1150", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Miscellaneous", "2024-09-01", "1090", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Miscellaneous", "2024-10-01", "1100", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Miscellaneous", "2024-11-01", "1080", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Miscellaneous", "2024-12-01", "1100", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Miscellaneous", "2025-01-01", "1100", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Miscellaneous", "2025-02-01", "1100", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Miscellaneous", "2025-03-01", "1100", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Miscellaneous", "2025-04-01", "1300", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Miscellaneous", "2025-05-01", "1500", "Expense"))
        self.cursor.execute('''INSERT INTO expenses (username, category, date, amount, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               ("john", "Miscellaneous", "2025-06-01", "1600", "Expense"))



        self.conn.commit()