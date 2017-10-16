import Main
import Utility
import ErrorHandler

login_status = False        #False == Not logged
login_user_agent = False    #False == Machine
valid_acc_list = []         #valid account list
new_acc_list = []           #Accounts created within the processing day
txn_message_list = []       #List of messages to be written in transaction summary file
withdrawLimits = {}    #Dictionary of how much has been withdrawn from each account in the current processing day.

utl = Utility.Utility()
err = ErrorHandler.ErrorHandler()

#all functions in txProcess are to return booleans indiating transaction success
#any errors encountered should be handled by calling the processError() from the errorHandler
#at the end of each transaction, call createTxnMsg() to form the appropriate string for the summary file

class TxnProcess:

    #login transaction
    def txn_login(self):
        global login_status
        global login_user_agent
        if(login_status == False):
            login_status = True
        else:
            #if already logged in, do not proceed. return false
            err.process_error("ERR_LOGGEDIN")
            return False

        #prompt user for the session type
        sessType = input("Please enter the desired session type (Machine/Agent): ").upper()
        if(sessType != "MACHINE" and sessType != "AGENT"):
            err.process_error("INVALID_SESSION")
            return False

        if(sessType == "MACHINE"):
            login_user_agent = False
        else:
            login_user_agent = True

        #read the valid accounts list file
        utl.process_account_file("valid_accounts_list_file.txt")
        
        #Intiliaze withdraw totals
        utl.intiliazeWithdrawTotals()

        #login successfully completed, return true
        return True


    #logout transaction
    def txn_logout(self):
        global login_status
        if(login_status == True):
            print("Successfully Logged out of the system.")
            login_status = False
        else:
            #if already logged out, do not proceed. return false
            err.process_error("ERR_LOGGEDOUT")
            return False

        #create the transaction summary file
        utl.create_txn_summary_file(txn_message_list)

        return True

    def txn_deposit(self):
        if(login_status == False):
            err.process_error("ERR_LOGGEDOUT")
            return False
        
        try:
            accNum = int(input("Please enter the account number you wish to deposit in: ").upper())
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNT")
            return False
        
        if(not utl.is_account_valid(accNum)):
            err.process_error("ERR_INVALIDACCOUNT")
            return False
            
        try:
            amount = int(input("Please enter the amount you wish to deposit: ").upper())
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDAMOUNT")
            return False
                
        if(not utl.is_amount_valid(amount)):
            err.process_error("ERR_INVALIDAMOUNT")
            return False

        txn_message_list.append(utl.create_txn_msg("DEP", accNum, amount, None, None))

        return True

    def txn_createacct(self):
        if(login_status == False):
            err.process_error("ERR_LOGGEDOUT")
            return False
        if(login_user_agent == False):
            err.process_error("ERR_UNPRIVILEGED")
            return False
            
        try:
            accNum = int(input("Please enter the new account number: ").upper())
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNT")
            return False
        
        if(not utl.is_account_unique(accNum)):
            err.process_error("ERR_INVALIDACCOUNT")
            return False
            
        accName = input("Please enter the name of account owner: ").upper()
        if(not utl.is_name_valid(accName)):
            err.process_error("ERR_INVALIDNAME")
            return False
        new_acc_list.append(accNum)
        txn_message_list.append(utl.create_txn_msg("NEW", accNum, None, None, accName))

        return True

    def txn_deleteacct(self):
        if(login_status == False):
            err.process_error("ERR_LOGGEDOUT")
            return False
        if(login_user_agent == False):
            err.process_error("ERR_UNPRIVILEGED")
            return False
        
        try:
            accNum = int(input("Please enter the account number you wish to delete: ").upper())
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNT")
            return False
        
        if(not utl.is_account_valid(accNum)):
            err.process_error("ERR_INVALIDACCOUNT")
            return False
            
        accName = input("Please enter the name of account owner: ").upper()
        if(not utl.is_name_valid(accName)):
            err.process_error("ERR_INVALIDNAME")
            return False

        #remove account from the list so that it will not be used in further transactions
        valid_acc_list.remove(accNum)

        txn_message_list.append(utl.create_txn_msg("DEL", accNum, None, None, accName))

        return True
        
    def txn_withdraw(self):
        if(login_status == False):
            err.process_error("ERR_LOGGEDOUT")
            return False
            
        try:
            accNum = int(input("Please enter the account number you wish to withdraw from: ").upper())
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNT")
            return False    
            
        if(not utl.is_account_valid(accNum)):
            err.process_error("ERR_INVALIDACCOUNT")
            return False
        
        try:    
            amount = int(input("Please enter the amount you wish to withdraw: ").upper())
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDAMOUNT")
            return False
            
        if(not utl.is_amount_valid(amount)):
            err.process_error("ERR_INVALIDAMOUNT")
            return False
        if(not utl.is_within_withdraw_limit(accNum, amount)):
            err.process_error("ERR_WITHDRAWLIMIT")
            return False    

        #Update withdraw total for account
        withdrawLimits[accNum]+=amount

        txn_message_list.append(utl.create_txn_msg("WDR", None, amount, accNum, None))

        return True
    
    def txn_transfer(self):
        if(login_status == False):
            err.process_error("ERR_LOGGEDOUT")
            return False
            
        try:
            fromAccNum = int(input("Please enter the \"From\" account number: ").upper())
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNT")
            return False
        
        if(not utl.is_account_valid(fromAccNum)):
            err.process_error("ERR_INVALIDACCOUNT")
            return False
            
        try:    
            toAccNum = int(input("Please enter the \"To\" account number: ").upper())
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDACCOUNT")
            return False    
            
        if(not utl.is_account_valid(toAccNum)):
            err.process_error("ERR_INVALIDACCOUNT")
            return False    
        
        #Assuming you can't transfer between the same account
        if(fromAccNum == toAccNum):
            err.process_error("ERR_SAMEACCOUNT")
            return False
            
        try:    
            amount = int(input("Please enter the amount you wish to transfer: ").upper())
        except ValueError:
            #Handle the exception if user did not enter an integer
            err.process_error("ERR_INVALIDAMOUNT")
            return False
        
        if(not utl.is_amount_valid(amount)):
            err.process_error("ERR_INVALIDAMOUNT")
            return False

        txn_message_list.append(utl.create_txn_msg("XFR", toAccNum, amount, fromAccNum, None))

        return True
