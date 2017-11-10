#!/usr/bin/env python
import TxnProcess
import Utility
import sys
import Account

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
Usage Example: \"./QBasic.py validaccounts.txt transactionsummary.txt
"""
if __name__ == '__main__':

    txnProcess.TxnProcess()
    utl = Utility.Utility()

    #Verify the correct number of input parameters are provided.
    if (len(sys.argv) != 3):
        print("Please provide a valid accounts file AND transaction summary file.")
        print("Usage Example: \"./QBasic.py validaccounts.txt transactionsummary.txt\"")
        sys.exit()
    else:
            txn.master_account_file = sys.argv[1]
            txn.transaction_summary_file = sys.argv[2]
            txn.output_master_account_file = sys.arg[3]
            txn.output_valid_account_file = sys.arg[4]


    #READ MASTER ACCOUNTS file AND MAKE THE ACCOUNTS OBJECTS TO A LIST
    utl.process_masterAccount(txn.master_account_file)

    #Check for a transaction code provided by the user.
            with open(txn.transaction_summary_file) as file:
                for line in file:
                    #remove leading and trailing spaces.
                    line = line.strip()

                    items = line.split(" ")

                    if (items[0] == "NEW"):
                        txnProcess.txn_new(items)
