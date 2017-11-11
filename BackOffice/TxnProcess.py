import Utility
import ErrorHandler
import Account
import sys
import re

"""All the global variables for the Qbasic Back end
"""

accounts_dic = {}

master_account_file = ""
transaction_summary_file = ""
output_master_account_file = ""
output_valid_account_file = ""

utl = Utility.Utility()
err = ErrorHandler.ErrorHandler()

class TxnProcess:
    """Class used for handling all transaction processing.

    All TxnProcess functions return booleans indicating transaction success or failure.
    Any errors encountered should be handled using processError() from the errorHandler class.
    Each transaction manipulates the accounts dictionary used to later create the new master
    account and valid account files.
    """

    def txn_new(self, items):
        """Function to process a new transaction code.
        Creates a new account
        """
        #create the new account object
        accountObj = Account.Account(int(items[1]), 000, items[4])
        #add new account to dictionary list of items
        accounts_dic[accountObj.getAccountNum] = accountObj

        #new account creation successfully completed, return true
        return True

    def txn_del(self, items):
        """Function to process a del transaction code.
        Deletes an account
        """
        #delete the account object
        key = int(items[1])
        accounts_dic.pop(key)

        #delete successfully completed, return true
        return True

    def txn_dep(self, items):
        """Function to process a dep transaction code.
        Deposits money into an account
        """
        #get the account and update its balanace
        key = int(items[1])
        balance = accounts_dic[key].getAccountBalance() + int(items[2])
        (accounts_dic[key]).setAccountBalance(balance)

        #deposit successfully completed, return true
        return True
