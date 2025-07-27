import json
from logging import exception
import random
import string
from pathlib import Path


class Bank :
    database = 'data.json'
    data = []
    try :
        if Path(database).exists() :

         with open(database) as fs :
            data = json.loads(fs.read())
        else :
            print('No file exist')

    except Exception as err :
        print(f'Exception aoccured as {err}')
    
    @classmethod
    def __update(cls) :
        with open(Bank.database, 'w') as fs :
            fs.write(json.dumps(Bank.data))    

    @classmethod
    def __accountgenerate(cls) :
        alpha = random.choices(string.ascii_letters, k = 3)
        num = random.choices(string.digits, k = 3)
        spchar = random.choices('!@#$%&*^', k = 1 )
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)

    
    def Createaccount(self) :
        info = {
            "name" : input(' enter name   -> '),
            "age" : int(input("Enter age  -> ")),
            "email" : input('enter email  -> '),
            "pin" : int(input("Enter pin  ONLY NUMBERS  -> ")),
            "accountNO." : Bank.__accountgenerate(),
            "balance" : 0
        }

        if info['age'] < 18 or len(str(info['pin'])) != 4 :
            print("Sorry you cannot create your account")

        else :
            print("account has been created successfully")
            for i in info :
                print(f'{i} : {info[i]}')
            print("<---------------- Please! Note your account number ------------------>")
            print("")
            
            Bank.data.append(info)

            Bank.__update()

    def depositemoney(self) :
          accnumber = input("please tell your account number -> ")
          pin = int(input("please tell your pin as well -> "))

          userdata = [i for i in Bank.data if i['accountNO.'] == accnumber and i['pin'] == pin]

          if userdata == False:
                print("sorry no data found")
            
          else:
                amount = int(input("how much you want to depoit "))
                if amount  > 10000 or amount < 0:
                    print("sorry the amount is too much you can deposit below 10000 and above 0")

                else:
                    userdata[0][''] += amount
                    Bank.__update()
                    
                    print("Amount deposited successfully ")

    def withdrawmoney(self):
          accnumber = input("please tell your account number -> ")
          pin = int(input("please tell your pin as well -> "))

          userdata = [i for i in Bank.data if i['accountNO.'] == accnumber and i['pin'] == pin]

          if userdata == False:
                print("sorry no data found")
            
          else:
                amount = int(input("how much you want to withdraw "))
                if userdata[0]['balance'] < amount:
                    print("sorry the amount entered is more than your deposited money in your account")

                else:
                    userdata[0]['balance'] -= amount
                    Bank.__update()
                    
                    print("Amount withdrew successfully ")

    def showdetails(self):
          accnumber = input("please tell your account number -> ")
          pin = int(input("please tell your pin as well -> "))

          userdata = [i for i in Bank.data if i['accountNO.'] == accnumber and i['pin'] == pin]
          print('Your informations ')
          for h in userdata[0] :
              print(f"{h} : {userdata[0][h]}")
    
    def detailupdate(self):
          accnumber = input("please tell your account number -> ")
          pin = int(input("please tell your pin as well -> "))

          userdata = [i for i in Bank.data if i['accountNO.'] == accnumber and i['pin'] == pin]

          if userdata == False :
               print("sorry no data found")
        
          else :
              print("you can't change age,account number,balance")
              print('Fill the details  for change or leave it blank if not to change')

              newdata = {
                  "name" : input("enter your name or enter to skip -> "),
                  "email" : input("Enetr new email or enter to skip -> "),
                  "pin" : input("Enter new pin or enter to skip ->")
               }              
              
              if newdata["name"] == '':
                  newdata["name"] = userdata[0]['name']
              if newdata["pin"] == '':
                  newdata["pin"] = userdata[0]['pin']
              if newdata["email"] == '':
                  newdata["email"] = userdata[0]['email']
              
              newdata['age'] = userdata[0]['age']
              newdata['accountNO.'] = userdata[0]['accountNO.']
              newdata['balance'] = userdata[0]['balance']
              if type(newdata['pin']) == str :
                  newdata["pin"] = int(newdata['pin'])
              
              for i in newdata :
                  if newdata[i] == userdata[0][i]:
                      continue
                  else :
                      userdata[0][i] = newdata[i]
              
              Bank.__update()
              print("Detail updated successfully")
    

    def deleteall(self):    
          accnumber = input("please tell your account number -> ")
          pin = int(input("please tell your pin as well -> "))

          userdata = [i for i in Bank.data if i['accountNO.'] == accnumber and i['pin'] == pin]
          
          if userdata == False :
               print("sorry no data found")
            
          else :
              check = input('Press  y  if you want to delete the account or press  n -> ')
              if check == 'n' or check == "N" :
                  print("Bypassed")
              

              else : 
                  index = Bank.data.index(userdata[0])
                  Bank.data.pop(index)
                  print('Account deleted successfully')
                  Bank.__update()


user = Bank()
print('1.For create account')
print('2.For deposition the money in the account')
print('3.For withdrawing money')
print('4.For for details')
print('5.For updating details')
print('6.To delete account')

response = int(input("Enter your respons  ==> "))

if response == 1 :
    user.Createaccount()

elif response == 2 :
    user.depositemoney()

elif response == 3:
    user.withdrawmoney()

elif response == 4:
    user.showdetails()

elif response == 5 :
    user.detailupdate() #name,email,pin

elif response == 6 :
    user.deleteall()