import Main
import TxnProcess

#any special error handling necessary can be done within this class
class ErrorHandler:

    error_codes = {}               #dictionary of error codes

    def __init__(self):
        self.error_codes["ERR_GENERIC"] = "Generic Error encountered. Please try later."
        self.error_codes["ERR_LOGGEDIN"] = "Error logging in. User already logged into the system."
        self.error_codes["INVALID_SESSION"] = "Error invalid session type."
        self.error_codes["ERR_LOGGEDOUT"] = "Error already logged out of the system."
        self.error_codes["ERR_INVALIDACCOUNT"] = "Error Invalid account number"
        self.error_codes["ERR_INVALIDAMOUNT"] = "Error Invalid amount entered"
        self.error_codes["ERR_INVALIDNAME"] = "Error Invalid name entered"
        self.error_codes["ERR_UNPRIVILEGED"] = "Error Invalid Mode"
        self.error_codes["ERR_WITHDRAWLIMIT"] = "Error Withdraw Limit reached for \"From\" account."
        self.error_codes["ERR_SAMEACCOUNT"] = "Error \"From\" and \"To\" account are the same."

    def process_error(self, errorCode):
        if(self.error_codes[errorCode] != None):
            print(self.error_codes[errorCode])
