import Utility
import ErrorHandler

"""All the global variables for the Qbasic Front end
"""

accounts_dic = {}

utl = Utility.Utility()
err = ErrorHandler.ErrorHandler()

class TxnProcess:
    """Class used for handling all transaction codes.

    All TxnProcess functions return booleans indiating transaction success or failure.
    Any errors encountered should be handled using processError() from the errorHandler class.
    Each transaction uses createTxnMsg() to cache messages to be written to transaction file.
    """

    def txn_new(self):
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
