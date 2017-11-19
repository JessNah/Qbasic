class ErrorHandler:
    """Class used for error handling by QBasic backend program.
    Uses dictionary to map error codes to error strings.
    """

    #Dictionary of error codes
    error_codes = {}

    def __init__(self):
        """Initialize error code to error string mapping."""
        self.error_codes["ERR_GENERIC"]             = "Generic Error encountered."
        self.error_codes["ERR_MASTERACCOUNT"]       = "Error processing master accounts file."
        self.error_codes["ERR_BADACCOUNTNUM"]       = "Error the account number already exists."
        self.error_codes["ERR_BADACCOUNTNAME"]      = "Error the account name does not match the associated account name."
        self.error_codes["ERR_BADBALANCEDEL"]       = "Error the balance of the account to be deleted is not zero."
        self.error_codes["ERR_BADBALANCEWDR"]       = "Error the balance of the account would be below zero after withdraw transaction."
        self.error_codes["ERR_BADBALANCEDEP"]       = "Error the balance of the account would be above $999999.99 after deposit transaction."
        self.error_codes["ERR_BADBALANCEFRMACCXFR"] = "Error the balance of the FROM account would be below zero after transfer transaction."
        self.error_codes["ERR_BADBALANCETOACCXFR"]  = "Error the balance of the TO account would be above $999999.99 after transfer transaction."
        self.error_codes["ERR_INVALIDTXNSUM"]       = "Error transaction summary file provided not in correct format."
        self.error_codes["ERR_INVALIDACCOUNTNUM"]   = "Error the account number is not in a valid format."
        self.error_codes["ERR_ACCOUNTNOTFOUND"]   = "Error the account number entered does not exist in the system."
        self.error_codes["ERR_INVALIDAMOUNT"]       = "Error the monetary amount entered is not in a valid format."

    def process_error(self, errorCode):
        """Function to send error string to stdout."""
        if(self.error_codes[errorCode] != None):
            print(self.error_codes[errorCode])
