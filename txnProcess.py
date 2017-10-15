import main
import utility
import errorHandler

login_status = False        #False == Not logged
login_user_agent = False    #False == Machine
valid_acc_list = []         #valid account list
new_acc_list = []           #Accounts created within the processing day
txn_message_list = []       #List of messages to be written in transaction summary file

utl = utility.utility()
err = errorHandler.errorHandler()

#all functions in txProcess are to return booleans indiating transaction success
#any errors encountered should be handled by calling the processError() from the errorHandler
#at the end of each transaction, call createTxnMsg() to form the appropriate string for the summary file

class txnProcess:
    def __init__(self):
        self.variable = 0

    #login transaction
    def txnLogin(self):
        global login_status
        if(login_status == False):
            login_status = True
        else:
            #if already logged in, do not proceed. return false
            err.processError("ERR_LOGGEDIN")
            return False

        #prompt user for the session type
        sessType = input("Please enter the desired session type (Machine/Agent): ").upper()
        while(sessType != "MACHINE" and sessType != "AGENT"):
            err.processError("INVALID_SESSION")
            sessType = input("Please enter the desired session type (Machine/Agent): ").upper()
            #TODO set agent vari

        #read the valid accounts list file
        utl.processAccountFile("test.txt")

        print(login_status)

        #test
        txn_message_list.append(utl.createTxnMsg("LOG", valid_acc_list[0], None, valid_acc_list[1], None))
        txn_message_list.append(utl.createTxnMsg("DEP", valid_acc_list[1], 9999999, valid_acc_list[2], None))

        #login successfully completed, return true
        return True


    #logout transaction
    def txnLogout(self):
        global login_status
        if(login_status == True):
            print("Successfully Logged out of the system.")
            login_status = False
        else:
            #if already logged out, do not proceed. return false
            err.processError("ERR_LOGGEDOUT")
            return False

        #create the transaction summary file
        utl.createTxnSummaryFile(txn_message_list)

        return True

    def txnDeposit(self):
        if(login_status == False):
            err.processError("ERR_LOGGEDOUT")
            return False
        #TODO handle non numeric entries and data types
        accNum = int(input("Please enter the account number you wish to deposit in: ").upper())
        if(not utl.isAccountValid(accNum)):
            err.processError("ERR_INVALIDACCOUNT")
            return False
        amount = int(input("Please enter the amount you wish to deposit: ").upper())
        if(not utl.isAmountValid(amount)):
            err.processError("ERR_INVALIDAMOUNT")
            return False

        txn_message_list.append(utl.createTxnMsg("DEP", accNum, amount, None, None))

        return True
