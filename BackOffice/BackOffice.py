#!/usr/bin/env python
import TxnProcess
import Utility
import sys
import Account

"""This is the main back office program.
This program serves to meet the requirements of a Back End banking system.
Created as part of Software Quality Assurance course, CISC/CMPE 327 at Queen's University.

Daily, the backend reads the master accounts file and the transaction summary file and processes
the various transactions:
deposit, withdraw, createacct, deleteacct, and transfers.
The backend then creates the new updated master accounts file and produces the new valid accounts file.

The program takes the following inputs:
    - master accounts file, used for receiving user commands.
    - transaction summary file, file used after the "logout" command on the front end to write all valid
      transactions processed throughout the session. Where a session is defined as login -> logout.


The program can be executed using the following usage example:
Usage Example: \"./BackOffice.py masteraccount.txt transactionsummary.txt
"""
if __name__ == '__main__':

    txn = TxnProcess.TxnProcess()
    utl = Utility.Utility()

    #Verify the correct number of input parameters are provided.
    if (len(sys.argv) != 5):
        print("Please provide a valid master accounts file AND transaction summary file.")
        print("Usage Example: \"./BackOffice.py masteraccount.txt transactionsummary.txt\"")
        sys.exit()
    else:
        txn.master_account_file = sys.argv[1]
        txn.transaction_summary_file = sys.argv[2]
        txn.output_master_account_file = sys.argv[3]
        txn.output_valid_account_file = sys.argv[4]


    #READ MASTER ACCOUNTS file AND MAKE THE ACCOUNTS OBJECTS TO A LIST
    utl.process_masterAccount(txn.master_account_file)

    #Check for a transaction code provided by the user.
    with open(txn.transaction_summary_file) as file:
        for line in file:
            #remove leading and trailing spaces.
            line = line.strip()
            items = line.split(" ")

            if (items[0] == "NEW"):
                txn.txn_new(items)

    #Create new master and valid account file
    utl.create_master_valid_account_files(TxnProcess.accounts_dic, txn.output_master_account_file, txn.output_valid_account_file)
