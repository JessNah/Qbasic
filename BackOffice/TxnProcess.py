import Utility
import ErrorHandler
import Account
import sys
import re

"""All the global variables for the Qbasic Front end
"""

accounts_dic = {}

master_account_file = ""
transaction_summary_file = ""
output_master_account_file = ""
output_valid_account_file = ""

utl = Utility.Utility()
err = ErrorHandler.ErrorHandler()

class TxnProcess:
    """Class used for handling all transaction codes.

    All TxnProcess functions return booleans indiating transaction success or failure.
    Any errors encountered should be handled using processError() from the errorHandler class.
    Each transaction uses createTxnMsg() to cache messages to be written to transaction file.
    """

    def txn_new(self, items):
        """Function to process a user login transaction code.
        Sets user type (machine,agent) and reads the valid accounts file.
        """
        #create the new account object
        accountObj = Account.Account(int(items[1]), 000, items[4])
        #add new account to dictionary list of items
        accounts_dic[accountObj.getAccountNum] = accountObj

        #login successfully completed, return true
        return True
