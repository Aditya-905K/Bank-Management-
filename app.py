import json
import random
import string
from pathlib import Path
import streamlit as st
import os

if os.path.exists('data.json') and os.path.getsize('data.json') == 0:
    print("The file is empty.")



# ------------------- File and Data Handling ------------------- #
class Bank:
    database = 'data.json'

    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            with open(cls.database, 'r') as f:
                return json.load(f)
        return []

    @classmethod
    def save_data(cls, data):
        with open(cls.database, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def generate_account(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices('!@#$%&*^', k=1)
        acc_id = alpha + num + spchar
        random.shuffle(acc_id)
        return "".join(acc_id)

# ------------------- Streamlit UI ------------------- #
st.set_page_config(page_title="Banking App", layout="centered")
st.title("🏦 Welcome to Streamlit Bank")

menu = st.sidebar.radio("Choose an option:", [
    "Create Account", "Deposit Money", "Withdraw Money",
    "View Account Details", "Update Details", "Delete Account"
])

bank_data = Bank.load_data()

def find_user(account, pin):
    return next((user for user in bank_data if user['accountNO.'] == account and user['pin'] == pin), None)

if menu == "Create Account":
    st.subheader("📝 Create New Account")
    name = st.text_input("Enter Name")
    age = st.number_input("Enter Age", min_value=0, step=1)
    email = st.text_input("Enter Email")
    pin = st.text_input("Enter 4-digit PIN", type="password")

    if st.button("Create Account"):
        if age < 18 or not pin.isdigit() or len(pin) != 4:
            st.error("Invalid Age or PIN (Must be 4 digits and age >= 18)")
        else:
            acc_num = Bank.generate_account()
            user_info = {
                "name": name,
                "age": age,
                "email": email,
                "pin": int(pin),
                "accountNO.": acc_num,
                "balance": 0
            }
            bank_data.append(user_info)
            Bank.save_data(bank_data)
            st.success("Account created successfully!")
            st.info(f"Your Account Number: {acc_num}")

elif menu == "Deposit Money":
    st.subheader("💰 Deposit Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount to Deposit", min_value=1, step=1)

    if st.button("Deposit"):
        user = find_user(acc, int(pin)) if pin.isdigit() else None
        if not user:
            st.error("No matching account found")
        elif amount > 10000:
            st.error("Amount exceeds deposit limit (10,000)")
        else:
            user['balance'] += amount
            Bank.save_data(bank_data)
            st.success("Amount deposited successfully!")

elif menu == "Withdraw Money":
    st.subheader("🏧 Withdraw Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount to Withdraw", min_value=1, step=1)

    if st.button("Withdraw"):
        user = find_user(acc, int(pin)) if pin.isdigit() else None
        if not user:
            st.error("No matching account found")
        elif user['balance'] < amount:
            st.error("Insufficient balance")
        else:
            user['balance'] -= amount
            Bank.save_data(bank_data)
            st.success("Amount withdrawn successfully!")

elif menu == "View Account Details":
    st.subheader("📋 Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Details"):
        user = find_user(acc, int(pin)) if pin.isdigit() else None
        if user:
            st.json(user)
        else:
            st.error("No matching account found")

elif menu == "Update Details":
    st.subheader("✏️ Update Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if acc and pin and pin.isdigit():
        user = find_user(acc, int(pin))
        if user:
            new_name = st.text_input("New Name", value=user['name'])
            new_email = st.text_input("New Email", value=user['email'])
            new_pin = st.text_input("New 4-digit PIN", value=str(user['pin']), type="password")

            if st.button("Update"):
                if not new_pin.isdigit() or len(new_pin) != 4:
                    st.error("PIN must be 4 digits")
                else:
                    user['name'] = new_name
                    user['email'] = new_email
                    user['pin'] = int(new_pin)
                    Bank.save_data(bank_data)
                    st.success("Details updated successfully!")
        else:
            st.error("Account not found")

elif menu == "Delete Account":
    st.subheader("🗑️ Delete Account")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    confirm = st.checkbox("Yes, I want to delete my account")

    if st.button("Delete"):
        user = find_user(acc, int(pin)) if pin.isdigit() else None
        if not user:
            st.error("No matching account found")
        elif confirm:
            bank_data.remove(user)
            Bank.save_data(bank_data)
            st.success("Account deleted successfully!")
        else:
            st.warning("Please confirm deletion before proceeding")


# streamlit run app.py