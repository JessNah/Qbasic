class ErrorHandler:
    """Class used for error handling by QBasic program.
    Uses dictionary to map error codes to error strings.
    """

    #dictionary of error codes
    error_codes = {}

    def __init__(self):
        """Initialize error code to error string mapping."""
        self.error_codes["ERR_GENERIC"] = "Generic Error encountered. Please try later."
        self.error_codes["ERR_LOGGEDIN"] = "Error logging in. User already logged into the system."
        self.error_codes["INVALID_SESSION"] = "Error invalid session type."
        self.error_codes["ERR_LOGGEDOUT"] = "Error already logged out of the system."
        self.error_codes["ERR_INVALIDACCOUNT"] = "Error Invalid account number"
        self.error_codes["ERR_INVALIDAMOUNT"] = "Error Invalid amount entered"
        self.error_codes["ERR_INVALIDNAME"] = "Error Invalid name entered"
        self.error_codes["ERR_UNPRIVILEGED"] = "Error Invalid User Type, increased priviledges required."
        self.error_codes["ERR_WITHDRAWLIMIT"] = "Error Withdraw Limit reached for \"From\" account."
        self.error_codes["ERR_SAMEACCOUNT"] = "Error \"From\" and \"To\" account are the same."
        self.error_codes["ERR_INVALIDACCFILE"] = "Error Invalid account number in valid accounts file!"
        self.error_codes["ERR_TXNFILE"] = "Error Creating Transaction Summary File. Invalid Data."

    def process_error(self, errorCode):
        """Function to send error string to stdout."""
        if(self.error_codes[errorCode] != None):
            print(self.error_codes[errorCode])
