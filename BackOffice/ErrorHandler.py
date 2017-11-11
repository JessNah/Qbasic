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

    def process_error(self, errorCode):
        """Function to send error string to stdout."""
        if(self.error_codes[errorCode] != None):
            print(self.error_codes[errorCode])
