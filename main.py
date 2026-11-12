import json
import random
import string
from pathlib import Path


def ask_int(prompt):
    """Keep asking until the user enters a whole number."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter numbers only.")


def valid_pin(pin):
    return pin.isdigit() and len(pin) == 4


class Bank:
    database = "data.json"
    data = []

    # ---------- Load data once when the program starts ---------- #
    path = Path(database)
    if path.exists() and path.stat().st_size > 0:
        try:
            with open(database, "r", encoding="utf-8") as fs:
                data = json.load(fs)
            # PINs are stored as strings so leading zeros survive.
            # Older files stored them as ints, so normalise them here.
            for _user in data:
                _user["pin"] = str(_user["pin"]).zfill(4)
        except json.JSONDecodeError as err:
            raise SystemExit(f"data.json is corrupted ({err}). Fix or delete it and try again.")
    else:
        print("No data file found yet. It will be created with your first account.")

    # ---------- Helpers ---------- #
    @classmethod
    def __update(cls):
        with open(cls.database, "w", encoding="utf-8") as fs:
            json.dump(cls.data, fs, indent=4)

    @classmethod
    def __accountgenerate(cls):
        existing = {u["accountNO."] for u in cls.data}
        while True:
            alpha = random.choices(string.ascii_letters, k=3)
            num = random.choices(string.digits, k=3)
            spchar = random.choices("!@#$%&*^", k=1)
            acc_id = alpha + num + spchar
            random.shuffle(acc_id)
            acc_num = "".join(acc_id)
            if acc_num not in existing:
                return acc_num

    @classmethod
    def __login(cls):
        """Ask for account number + PIN. Returns the user dict or None."""
        accnumber = input("please tell your account number -> ")
        pin = input("please tell your pin as well -> ").strip()
        user = next(
            (u for u in cls.data if u["accountNO."] == accnumber and u["pin"] == pin),
            None,
        )
        if user is None:
            print("sorry no data found")
        return user

    # ---------- Features ---------- #
    def Createaccount(self):
        name = input(" enter name   -> ").strip()
        age = ask_int("Enter age  -> ")
        email = input("enter email  -> ").strip()
        pin = input("Enter 4 digit pin  ONLY NUMBERS  -> ").strip()

        if not name:
            print("Sorry, name cannot be empty")
        elif age < 18:
            print("Sorry you cannot create your account (must be 18 or older)")
        elif not valid_pin(pin):
            print("Sorry you cannot create your account (PIN must be exactly 4 digits)")
        else:
            info = {
                "name": name,
                "age": age,
                "email": email,
                "pin": pin,
                "accountNO.": Bank.__accountgenerate(),
                "balance": 0,
            }
            Bank.data.append(info)
            Bank.__update()

            print("account has been created successfully")
            for key, value in info.items():
                if key != "pin":
                    print(f"{key} : {value}")
            print("<---------------- Please! Note your account number ------------------>")
            print("")

    def depositemoney(self):
        user = Bank.__login()
        if not user:
            return

        amount = ask_int("how much you want to deposit -> ")
        if amount > 10000 or amount <= 0:
            print("sorry, you can deposit an amount above 0 and up to 10000")
        else:
            user["balance"] += amount
            Bank.__update()
            print("Amount deposited successfully")

    def withdrawmoney(self):
        user = Bank.__login()
        if not user:
            return

        amount = ask_int("how much you want to withdraw -> ")
        if amount <= 0:
            print("sorry, the amount must be above 0")
        elif user["balance"] < amount:
            print("sorry the amount entered is more than your deposited money in your account")
        else:
            user["balance"] -= amount
            Bank.__update()
            print("Amount withdrawn successfully")

    def showdetails(self):
        user = Bank.__login()
        if not user:
            return

        print("Your informations ")
        for key, value in user.items():
            if key != "pin":
                print(f"{key} : {value}")

    def detailupdate(self):
        user = Bank.__login()
        if not user:
            return

        print("you can't change age, account number, balance")
        print("Fill the details for change or leave it blank if not to change")

        new_name = input("enter your name or enter to skip -> ").strip()
        new_email = input("Enter new email or enter to skip -> ").strip()
        new_pin = input("Enter new 4 digit pin or enter to skip -> ").strip()

        if new_pin and not valid_pin(new_pin):
            print("PIN must be exactly 4 digits. Nothing was changed.")
            return

        if new_name:
            user["name"] = new_name
        if new_email:
            user["email"] = new_email
        if new_pin:
            user["pin"] = new_pin

        Bank.__update()
        print("Detail updated successfully")

    def deleteall(self):
        user = Bank.__login()
        if not user:
            return

        check = input("Press  y  if you want to delete the account or press  n -> ")
        if check.strip().lower() == "y":
            Bank.data.remove(user)
            Bank.__update()
            print("Account deleted successfully")
        else:
            print("Bypassed")


if __name__ == "__main__":
    user = Bank()
    print("1.For create account")
    print("2.For deposition the money in the account")
    print("3.For withdrawing money")
    print("4.For details")
    print("5.For updating details")
    print("6.To delete account")

    response = ask_int("Enter your response ==> ")

    if response == 1:
        user.Createaccount()
    elif response == 2:
        user.depositemoney()
    elif response == 3:
        user.withdrawmoney()
    elif response == 4:
        user.showdetails()
    elif response == 5:
        user.detailupdate()  # name, email, pin
    elif response == 6:
        user.deleteall()
    else:
        print("Invalid option. Please choose a number from 1 to 6.")
