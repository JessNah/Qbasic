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
        try:
            accountNum = int(items[1])
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNTNUM")
            #Since the back end should only get valid input, exit the back end on any value error.
            sys.exit()

        #Make sure new account number is unused/unique
        if(accountNum in accounts_dic):
            err.process_error("ERR_BADACCOUNTNUM")
            return

        accountName = items[4]
        if(utl.account_name_exists(accountName)):
            err.process_error("ERR_USEDACCOUNTNAME")
            return

        #Create the new account object
        accountObj = Account.Account(accountNum, 000, accountName)
        #Add new account to dictionary list of items
        accounts_dic[accountObj.get_account_num()] = accountObj

        #new account creation successfully completed.
        return

    def txn_del(self, items):
        """Function to process a del transaction code.
        Deletes an account
        """

        try:
            accountNum = int(items[1])
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNTNUM")
            #Since the back end should only get valid input, exit the back end on any value error.
            sys.exit()

        #Make sure the name provided matches the account to be deleted's name
        if(accounts_dic[accountNum].get_account_name() != items[4]):
            err.process_error("ERR_BADACCOUNTNAME")
            return

        #Check that the account has 0 balance, only then delete
        if(accounts_dic[accountNum].get_account_balance() is not 0):
            err.process_error("ERR_BADBALANCEDEL")
            return

        #Delete the account object
        accounts_dic.pop(accountNum)

        #Delete transaction successfully completed
        return

    def txn_dep(self, items):
        """Function to process a dep transaction code.
        Deposits money into an account
        """
        try:
            #Get the account and update its balance
            accountNum = int(items[1])
        except ValueError:
            #Handle the exception if user did not enter an integer.
            err.process_error("ERR_INVALIDACCOUNTNUM")
            #Since the back end should only get valid input, exit the back end on any value error.
            sys.exit()

        try:
            #Get the deposit amount
            depAmount = int(items[2])
        except ValueError:
            #Handle the exception if user did not enter an integer.
            err.process_error("ERR_INVALIDAMOUNT")
            #Since the back end should only get valid input, exit the back end on any value error.
            sys.exit()

        #Check that the account balance of the account will not exceed $999999.99 after deposit
        if((accounts_dic[accountNum].get_account_balance() + depAmount) > 99999999):
            err.process_error("ERR_BADBALANCEDEP")
            return

        balance = accounts_dic[accountNum].get_account_balance() + depAmount
        (accounts_dic[accountNum]).set_account_balance(balance)

        #Deposit transaction successfully completed
        return

    def txn_wdr(self, items):
        """Function to process a wdr transaction code.
        Withdraw money from an account
        """
        try:
            accountNum = int(items[1])
        except ValueError:
            #Handle the exception if user did not enter an integer.
            err.process_error("ERR_INVALIDACCOUNTNUM")
            #Since the back end should only get valid input, exit the back end on any value error.
            sys.exit()

        try:
            withdrawAmount = int(items[2])
        except ValueError:
            #Handle the exception if user did not enter an integer.
            err.process_error("ERR_INVALIDAMOUNT")
            #Since the back end should only get valid input, exit the back end on any value error.
            sys.exit()

        #Check if account number to withdraw from exists in system's accounts dictionary
        if(accountNum not in accounts_dic):
            err.process_error("ERR_ACCOUNTNOTFOUND")
            return
        else:
            #Check that the account balance will not go below 0 after withdraw
            if((accounts_dic[accountNum].get_account_balance() - withdrawAmount) < 0):
                err.process_error("ERR_BADBALANCEWDR")
                return
            else:
                #Get the account and update its balanace
                balance = accounts_dic[accountNum].get_account_balance() - withdrawAmount
                (accounts_dic[accountNum]).set_account_balance(balance)

        #Withdraw transaction successfully completed
        return

    def txn_xfr(self, items):
        """Function to process a xfr transaction code.
        Transfer money from FROM account to TO account.
        """
        try:
            #Get the TO account
            toAccountNum = int(items[1])

            #Get the FROM account
            fromAccountNum = int(items[3])
        except ValueError:
            #Handle the exception if user did not enter an integer.
            err.process_error("ERR_INVALIDACCOUNTNUM")
            #Since the back end should only get valid input, exit the back end on any value error.
            sys.exit()

        try:
            transferAmount = int(items[2])
        except ValueError:
            #Handle the exception if user did not enter an integer.
            err.process_error("ERR_INVALIDAMOUNT")
            #Since the back end should only get valid input, exit the back end on any value error.
            sys.exit()

        #Check that the account balance of FROM account will not go below 0 after transfer
        if((accounts_dic[fromAccountNum].get_account_balance() - transferAmount) < 0):
            err.process_error("ERR_BADBALANCEFRMACCXFR")
            return

        #Check that the account balance of TO account will not exceed $999999.99 after transfer
        if((accounts_dic[toAccountNum].get_account_balance() + transferAmount) > 99999999):
            err.process_error("ERR_BADBALANCETOACCXFR")
            return

        #Subtract transfer amount from FROM account's balance.
        balance = accounts_dic[fromAccountNum].get_account_balance() - transferAmount
        (accounts_dic[fromAccountNum]).set_account_balance(balance)

        #Add transfer amount to TO account's balance.
        balance = accounts_dic[toAccountNum].get_account_balance() + transferAmount
        (accounts_dic[toAccountNum]).set_account_balance(balance)

        #Transfer transaction successfully completed
        return

    def txn_eos(self, items):
        """Function to process the EOS line from transaction file to ensure validity.
        """

        #If NOT all items in EOS line match those expected then set validity flag.
        if (not((items[1] == "0000000") and (items[2] == "000") and (items[3] == "0000000") and (items[4] == "***"))):
            err.process_error("ERR_INVALIDTXNSUM")
            return
        else:
            print("End of merged transaction summary file successfully reached.")

        #EOS validity successfully verified
        return
