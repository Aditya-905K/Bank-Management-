import json
import random
import string
from pathlib import Path

import streamlit as st


# ------------------- File and Data Handling ------------------- #
class Bank:
    database = Path("data.json")

    @classmethod
    def load_data(cls):
        """Load accounts. Returns [] if the file is missing or empty.
        Raises json.JSONDecodeError if the file is corrupt."""
        if not cls.database.exists() or cls.database.stat().st_size == 0:
            return []
        with open(cls.database, "r", encoding="utf-8") as f:
            data = json.load(f)
        # PINs are stored as strings so leading zeros (e.g. 0123) survive.
        # Older files stored them as ints, so normalise them here.
        for user in data:
            user["pin"] = str(user["pin"]).zfill(4)
        return data

    @classmethod
    def save_data(cls, data):
        with open(cls.database, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def generate_account(cls, existing_numbers):
        """Generate an account number that is not already in use."""
        while True:
            alpha = random.choices(string.ascii_letters, k=3)
            num = random.choices(string.digits, k=3)
            spchar = random.choices("!@#$%&*^", k=1)
            acc_id = alpha + num + spchar
            random.shuffle(acc_id)
            acc_num = "".join(acc_id)
            if acc_num not in existing_numbers:
                return acc_num


def valid_pin(pin):
    return pin.isdigit() and len(pin) == 4


# ------------------- Streamlit UI ------------------- #
st.set_page_config(page_title="Banking App", layout="centered")
st.title("🏦 Welcome to Streamlit Bank")

menu = st.sidebar.radio("Choose an option:", [
    "Create Account", "Deposit Money", "Withdraw Money",
    "View Account Details", "Update Details", "Delete Account"
])

try:
    bank_data = Bank.load_data()
except json.JSONDecodeError:
    st.error("data.json is corrupted. Fix or delete the file and reload the app.")
    st.stop()


def find_user(account, pin):
    return next(
        (u for u in bank_data if u["accountNO."] == account and u["pin"] == pin),
        None,
    )


if menu == "Create Account":
    st.subheader("📝 Create New Account")
    name = st.text_input("Enter Name")
    age = st.number_input("Enter Age", min_value=0, step=1)
    email = st.text_input("Enter Email")
    pin = st.text_input("Enter 4-digit PIN", type="password")

    if st.button("Create Account"):
        if not name.strip():
            st.error("Name cannot be empty")
        elif age < 18:
            st.error("You must be 18 or older to create an account")
        elif not valid_pin(pin):
            st.error("PIN must be exactly 4 digits")
        else:
            acc_num = Bank.generate_account({u["accountNO."] for u in bank_data})
            user_info = {
                "name": name.strip(),
                "age": int(age),
                "email": email.strip(),
                "pin": pin,
                "accountNO.": acc_num,
                "balance": 0,
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
        user = find_user(acc, pin)
        if not user:
            st.error("No matching account found")
        elif amount > 10000:
            st.error("Amount exceeds deposit limit (10,000)")
        else:
            user["balance"] += int(amount)
            Bank.save_data(bank_data)
            st.success("Amount deposited successfully!")

elif menu == "Withdraw Money":
    st.subheader("🏧 Withdraw Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount to Withdraw", min_value=1, step=1)

    if st.button("Withdraw"):
        user = find_user(acc, pin)
        if not user:
            st.error("No matching account found")
        elif user["balance"] < amount:
            st.error("Insufficient balance")
        else:
            user["balance"] -= int(amount)
            Bank.save_data(bank_data)
            st.success("Amount withdrawn successfully!")

elif menu == "View Account Details":
    st.subheader("📋 Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Details"):
        user = find_user(acc, pin)
        if user:
            # Don't display the PIN on screen
            st.json({k: v for k, v in user.items() if k != "pin"})
        else:
            st.error("No matching account found")

elif menu == "Update Details":
    st.subheader("✏️ Update Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if acc and pin:
        user = find_user(acc, pin)
        if user:
            new_name = st.text_input("New Name", value=user["name"], key=f"name_{acc}")
            new_email = st.text_input("New Email", value=user["email"], key=f"email_{acc}")
            new_pin = st.text_input(
                "New 4-digit PIN (leave blank to keep current)",
                type="password",
                key=f"pin_{acc}",
            )

            if st.button("Update"):
                if new_pin and not valid_pin(new_pin):
                    st.error("PIN must be exactly 4 digits")
                elif not new_name.strip():
                    st.error("Name cannot be empty")
                else:
                    user["name"] = new_name.strip()
                    user["email"] = new_email.strip()
                    if new_pin:
                        user["pin"] = new_pin
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
        user = find_user(acc, pin)
        if not user:
            st.error("No matching account found")
        elif confirm:
            bank_data.remove(user)
            Bank.save_data(bank_data)
            st.success("Account deleted successfully!")
        else:
            st.warning("Please confirm deletion before proceeding")


# To run: streamlit run app.py
