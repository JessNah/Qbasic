class Account:
    """Class used for creating Account objects.

    Each account's details including account name, account number, and account balance are stored in each account object.
    When the Master Accounts File is read through the backend application, a dictionary of account number's and corresponding
    Account objects is created. This allows all future transactions (parsed from the transaction summary file) to easily
    interact with each Account object. At the end of the banking session the backend uses the dictionary of Account files
    to create the new Master Accounts File.
    """

    def __init__(self, num, balance, name):
        """Constructor for Account object, populating accountName, accountNum and balance attributes."""
        self.accountName = name
        self.accountNum = num
        self.balance = balance

    def get_account_num(self):
        """Accessor to return an account's account number."""
        return self.accountNum

    def get_account_name(self):
        """Accessor to return an account's account name."""
        return self.accountName

    def get_account_balance(self):
        """Accessor to return an account's account balance."""
        return self.balance

    def set_account_balance(self, val):
        """Mutator function to set a new account balance for an Account object."""
        self.balance = val
