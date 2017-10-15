import main
import txnProcess

#any special error handling necessary can be done within this class
class errorHandler:

    error_codess = {}               #dictionary of error codes

    def __init__(self):
        self.error_codess["ERR_GENERIC"] = "Generic Error encountered. Please try later."
        self.error_codess["ERR_LOGGEDIN"] = "Error logging in. User already logged into the system."
        self.error_codess["INVALID_SESSION"] = "Error invalid session type."
        self.error_codess["ERR_LOGGEDOUT"] = "Error already logged out of the system."
        self.error_codess["ERR_INVALIDACCOUNT"] = "Error Invalid account number"
        self.error_codess["ERR_INVALIDAMOUNT"] = "Error Invalid amount entered"

    def processError(self, errorCode):
        if(self.error_codess[errorCode] != None):
            print(self.error_codess[errorCode])
