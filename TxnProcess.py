import Utility
import ErrorHandler

"""All the global variables for the Qbasic Front end
"""
login_status = False           #False == Not logged
login_user_agent = False       #False == Machine
valid_acc_list = []            #valid account list
new_acc_list = []              #Accounts created within the processing day
txn_message_list = []          #List of messages to be written in transaction summary file
withdraw_limits = {}           #Dictionary of how much has been withdrawn from each account in the current processing day.
valid_accounts_file = ""       #Relative path to valid accounts file
transaction_summary_file = ""  #Relative path to transaction summary file

utl = Utility.Utility()
err = ErrorHandler.ErrorHandler()

class TxnProcess:
    """Class used for handling all transaction codes.
    
    All TxnProcess functions return booleans indiating transaction success or failure.
    Any errors encountered should be handled using processError() from the errorHandler class.
    Each transaction uses createTxnMsg() to cache messages to be written to transaction file.
    """

    def txn_login(self):
        """Function to process a user login transaction code.
        Sets user type (machine,agent) and reads the valid accounts file.
        """
        global login_status
        global login_user_agent
        
        if(login_status == False):
            login_status = True
        else:
            #if already logged in, do not proceed. return false
            err.process_error("ERR_LOGGEDIN")
            return False

        #prompt user for the session type
        sessType = utl.get_input("Please enter the desired session type (Machine/Agent): ")
        if(sessType != "MACHINE" and sessType != "AGENT"):
            err.process_error("INVALID_SESSION")
            return False

        if(sessType == "MACHINE"):
            login_user_agent = False
        else:
            login_user_agent = True

        #read the valid accounts list file
        utl.process_account_file(self.valid_accounts_file)
        
        #Intiliaze withdraw totals
        utl.intiliaze_withdraw_totals()

        #login successfully completed, return true
        return True


    #logout transaction
    def txn_logout(self):
        """Function to process a user logout transaction code.
        Logs out the current user and creates transaction summary file.
        """
        global login_status
        if(login_status == True):
            print("Successfully Logged out of the system.")
            login_status = False
        else:
            #if already logged out, do not proceed. return false
            err.process_error("ERR_LOGGEDOUT")
            return False

        #Add EOS tag to transaction summary buffer
        txn_message_list.append(utl.create_txn_msg("EOS", None, None, None, None))

        #create the transaction summary file
        utl.create_txn_summary_file(self.transaction_summary_file, txn_message_list)

        return True

    def txn_deposit(self):
        """Function to process a user deposit transaction code.
        Checks if account number and deposit amount are valid.
        """
        if(login_status == False):
            err.process_error("ERR_LOGGEDOUT")
            return False
        
        try:
            accNum = int(utl.get_input("Please enter the account number you wish to deposit in: "))
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNT")
            return False
        
        #Check if account number provided is valid.
        if(not utl.is_account_valid(accNum)):
            err.process_error("ERR_INVALIDACCOUNT")
            return False
            
        try:
            amount = int(utl.get_input("Please enter the amount you wish to deposit: "))
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDAMOUNT")
            return False
        
        #Check if deposit amount provided is valid.        
        if(not utl.is_amount_valid(amount)):
            err.process_error("ERR_INVALIDAMOUNT")
            return False

        #Add DEP line to transaction summary buffer
        txn_message_list.append(utl.create_txn_msg("DEP", accNum, amount, None, None))

        return True

    def txn_createacct(self):
        """Function to process a user createacct transaction code.
        Checks if account number and account name are valid before creating account.
        """
        
        #Verify user logged in has the proper priveledges.
        if(login_status == False):
            err.process_error("ERR_LOGGEDOUT")
            return False
        if(login_user_agent == False):
            err.process_error("ERR_UNPRIVILEGED")
            return False
            
        try:
            accNum = int(utl.get_input("Please enter the new account number: "))
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNT")
            return False
        
        #Check if account number provided is unique.
        if(not utl.is_account_unique(accNum)):
            err.process_error("ERR_INVALIDACCOUNT")
            return False
            
        accName = utl.get_input("Please enter the name of account owner: ")
        
        #Check if account name provided is valid.
        if(not utl.is_name_valid(accName)):
            err.process_error("ERR_INVALIDNAME")
            return False
        
        #Append new valid account to a list containing all new accounts created.
        new_acc_list.append(accNum)
        
        #Add NEW line to transaction summary buffer
        txn_message_list.append(utl.create_txn_msg("NEW", accNum, None, None, accName))

        return True

    def txn_deleteacct(self):
        """Function to process a user deleteacct transaction code.
        Checks if account number and account name are valid before deleting account.
        """
        
        #Verify user logged in has the proper priveledges.
        if(login_status == False):
            err.process_error("ERR_LOGGEDOUT")
            return False
        if(login_user_agent == False):
            err.process_error("ERR_UNPRIVILEGED")
            return False
        
        try:
            accNum = int(utl.get_input("Please enter the account number you wish to delete: "))
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNT")
            return False
        
        #Check if account number provided is valid.
        if(not utl.is_account_valid(accNum)):
            err.process_error("ERR_INVALIDACCOUNT")
            return False
            
        accName = input("Please enter the name of account owner: ").upper()
        if(not utl.is_name_valid(accName)):
            err.process_error("ERR_INVALIDNAME")
            return False

        #remove account from the accounts list so that it will not be used in further transactions
        valid_acc_list.remove(accNum)

        #Add DEL line to transaction summary buffer
        txn_message_list.append(utl.create_txn_msg("DEL", accNum, None, None, accName))

        return True
        
    def txn_withdraw(self):
        """Function to process a user withdraw transaction code.
        Checks if account number and withdraw amount are valid before processing withdrawal.
        """
        if(login_status == False):
            err.process_error("ERR_LOGGEDOUT")
            return False
            
        try:
            accNum = int(utl.get_input("Please enter the account number you wish to withdraw from: "))
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNT")
            return False    
        
        #Check if account number provided is valid.    
        if(not utl.is_account_valid(accNum)):
            err.process_error("ERR_INVALIDACCOUNT")
            return False
        
        try:    
            amount = int(utl.get_input("Please enter the amount you wish to withdraw: "))
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDAMOUNT")
            return False
        
        #Check if withdraw amount provided is valid.    
        if(not utl.is_amount_valid(amount)):
            err.process_error("ERR_INVALIDAMOUNT")
            return False
        
        #Check if this account will hit it's withdraw it's withdraw limit during this session.
        if(not utl.is_within_withdraw_limit(accNum, amount)):
            err.process_error("ERR_WITHDRAWLIMIT")
            return False    

        #Update withdraw total for account
        withdraw_limits[accNum]+=amount

        #Add WDR line to transaction summary buffer
        txn_message_list.append(utl.create_txn_msg("WDR", None, amount, accNum, None))

        return True
    
    def txn_transfer(self):
        """Function to process a user transfer transaction code.
        Checks if \"From\" and \"To\" account number and transfer amount are valid before processing transfer.
        """
        if(login_status == False):
            err.process_error("ERR_LOGGEDOUT")
            return False
            
        try:
            fromAccNum = int(utl.get_input("Please enter the \"From\" account number: "))
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNT")
            return False
        
        #Check if FROM account number provided is valid.
        if(not utl.is_account_valid(fromAccNum)):
            err.process_error("ERR_INVALIDACCOUNT")
            return False
            
        try:    
            toAccNum = int(utl.get_input("Please enter the \"To\" account number: "))
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNT")
            return False    
        
        #Check if TO account number provided is valid.    
        if(not utl.is_account_valid(toAccNum)):
            err.process_error("ERR_INVALIDACCOUNT")
            return False    
        
        #Assuming you can't transfer between the same account
        if(fromAccNum == toAccNum):
            err.process_error("ERR_SAMEACCOUNT")
            return False
            
        try:    
            amount = int(utl.get_input("Please enter the amount you wish to transfer: "))
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDAMOUNT")
            return False
        
        #Check if transfer amount provided is valid.
        if(not utl.is_amount_valid(amount)):
            err.process_error("ERR_INVALIDAMOUNT")
            return False

        #Add XFR line to transaction summary buffer
        txn_message_list.append(utl.create_txn_msg("XFR", toAccNum, amount, fromAccNum, None))

        return True
