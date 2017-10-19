#!/usr/bin/env python3
import TxnProcess
import sys

"""This is the main program.
This program serves to meet the requirements of a Front End banking system.
Created as part of Software Quality Assurance course, CISC/CMPE 327 at Queen's University.

A user is able to login as either machine or agent, able to perform transactions such as 
deposit, withdraw, createacct, deleteacct, and transfers.
Valid accounts are verified by a valid accounts file provided by the back end software.
The back end processes daily transactions by a transaction summary file created by the front end (this application).

The program takes the following inputs:
    - stdIn, used for receiving user commands.
    - valid accounts file, file to use as a record of the valid accounts (provided by back end).
    - transaction summary file, file used after the "logout" command to write all valid 
      transactions processed throughout the session. Where a session is defined as login -> logout.

The program can be executed using the following usage example:
Usage Example: \"./Main.py validaccounts.txt transactionsummary.txt
"""
if __name__ == '__main__':

    txn = TxnProcess.TxnProcess()
    
    #Verify the correct number of input parameters are provided.
    if (len(sys.argv) != 3):
        print("Please provide a valid accounts file AND transaction summary file.")
        print("Usage Example: \"./Qbasic.py validaccounts.txt transactionsummary.txt\"")
        sys.exit()
    else:
        txn.valid_accounts_file = sys.argv[1]
        txn.transaction_summary_file = sys.argv[2]
    
    print("Welcome. Please enter appropriate transaction codes to use the system.")
    print("Valid transaction codes are login, logout, deposit, deposit, withdraw, createacct, deleteacct, and transfer.")
    user_input = input("Please begin by logging in: ").upper()

    #Check for a transaction code provided by the user.
    while(user_input != None):
        status = True
        
        if(user_input == "LOGIN"):
            if(txn.txn_login() == False):
                status = False

        elif(user_input == "LOGOUT"):
            if(txn.txn_logout() == False):
                status = False
            else:
                #If logout is successfull, exit the program (only one logout per session)
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
