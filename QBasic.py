#!/usr/bin/env python3

import TxnProcess
import sys

"""This is the main function
This is used to call out for user input transaction codes
"""
if __name__ == '__main__':

    txn = TxnProcess.TxnProcess()
    
    if (len(sys.argv) != 3):
        print("Please provide a valid accounts file AND transaction summary file.")
        print("Usage Example: \"./Main.py validaccounts.txt transactionsummary.txt\"")
        sys.exit()
    else:
        txn.valid_accounts_file = sys.argv[1]
        txn.transaction_summary_file = sys.argv[2]
    
    print("Welcome. Please enter appropriate transaction codes to use the system.")
    print("Valid transaction codes are login, logout, deposit, deposit, withdraw, createacct, deleteacct, and transfer.")
    user_input = input("Please begin by logging in: ").upper()

    while(user_input != None):
        status = True
        
        if(user_input == "LOGIN"):
            if(txn.txn_login() == False):
                status = False

        elif(user_input == "LOGOUT"):
            if(txn.txn_logout() == False):
                status = False
            else:
                sys.exit()    

        elif(user_input == "DEPOSIT"):
            if(txn.txn_deposit() == False):
                status = False

        elif(user_input == "CREATEACCT"):
            if(txn.txn_createacct() == False):
                status = False

        elif(user_input == "DELETEACCT"):
            if(txn.txn_deleteacct() == False):
                status = False
                
        elif(user_input == "WITHDRAW"):
            if(txn.txn_withdraw() == False):
                status = False

        elif(user_input == "TRANSFER"):
            if(txn.txn_transfer() == False):
                status = False
            
        else:
            status = False

        #receive next user input
        if(status):
            user_input = input("Please enter the next transaction code to proceed (example: deposit): ").upper()
        else:
            user_input = input("Sorry we encountered an issue. Please try another transaction code: ").upper()
