#from txnProcess import *
import txnProcess
import utility
import errorHandler

if __name__ == '__main__':

    txn = txnProcess.txnProcess()

    print("Welcome. Please enter appropriate transaction codes to use the system.")
    user_input = input("Please begin by logging in: ").upper()

    while(user_input != None):
        status = True
        if(user_input == "LOGIN"):
            if(txn.txnLogin() == False):
                status = False

        elif(user_input == "LOGOUT"):
            #user_input = None
            if(txn.txnLogout() == False):
                status = False

        elif(user_input == "DEPOSIT"):
            #user_input = None
            if(txn.txnDeposit() == False):
                status = False

        else:
            status = False

        #receive next user input
        if(status):
            user_input = input("Please enter the next transaction code to proceed: ").upper()
        else:
            user_input = input("Sorry we encountered an issue. Please try again: ").upper()
