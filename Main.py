import TxnProcess
import Utility
import ErrorHandler

if __name__ == '__main__':

    txn = TxnProcess.TxnProcess()
    print("Welcome. Please enter appropriate transaction codes to use the system.")
    user_input = input("Please begin by logging in: ").upper()

    while(user_input != None):
        status = True
        if(user_input == "LOGIN"):
            if(txn.txn_login() == False):
                status = False

        elif(user_input == "LOGOUT"):
            #user_input = None
            if(txn.txn_logout() == False):
                status = False

        elif(user_input == "DEPOSIT"):
            #user_input = None
            if(txn.txn_deposit() == False):
                status = False

        elif(user_input == "CREATEACCT"):
            #user_input = None
            if(txn.txn_createacct() == False):
                status = False

        else:
            status = False

        #receive next user input
        if(status):
            user_input = input("Please enter the next transaction code to proceed: ").upper()
        else:
            user_input = input("Sorry we encountered an issue. Please try again: ").upper()
