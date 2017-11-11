class ErrorHandler:
    """Class used for error handling by QBasic program.
    Uses dictionary to map error codes to error strings.
    """

    #dictionary of error codes
    error_codes = {}

    def __init__(self):
        """Initialize error code to error string mapping."""
        self.error_codes["ERR_GENERIC"] = "Generic Error encountered."
        self.error_codes["ERR_MASTERACCOUNT"] = "Error processing master accounts file."
        self.error_codes["ERR_BADACCOUNTNUM"] = "Error the account number already exists."
        self.error_codes["ERR_BADACCOUNTNAME"] = "Error the account name does not match the associated account name."
        self.error_codes["ERR_BADBALANCE"] = "Error the balance of the account to be deleted is not zero."

    def process_error(self, errorCode):
        """Function to send error string to stdout."""
        if(self.error_codes[errorCode] != None):
            print(self.error_codes[errorCode])
