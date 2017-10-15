import Main
import Utility
import ErrorHandler

login_status = False        #False == Not logged
login_user_agent = False    #False == Machine
valid_acc_list = []         #valid account list
new_acc_list = []           #Accounts created within the processing day
txn_message_list = []       #List of messages to be written in transaction summary file

utl = Utility.Utility()
err = ErrorHandler.ErrorHandler()

#all functions in txProcess are to return booleans indiating transaction success
#any errors encountered should be handled by calling the processError() from the errorHandler
#at the end of each transaction, call createTxnMsg() to form the appropriate string for the summary file

class TxnProcess:
    def __init__(self):
        self.variable = 0

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
        #TODO handle non numeric entries and data types
        accNum = int(input("Please enter the account number you wish to deposit in: ").upper())
        if(not utl.is_account_valid(accNum)):
            err.process_error("ERR_INVALIDACCOUNT")
            return False
        amount = int(input("Please enter the amount you wish to deposit: ").upper())
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
        #TODO handle non numeric entries and data types
        accNum = int(input("Please enter the new account number: ").upper())
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
        #TODO handle non numeric entries and data types
        accNum = int(input("Please enter the account number you wish to delete: ").upper())
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
