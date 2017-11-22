import TxnProcess
import ErrorHandler
import sys
import re
import Account
import collections

err = ErrorHandler.ErrorHandler()

class Utility:
    """Class used for utility functions for QBasic application.
    Utility functions are by TxnProcess for routine operations.
    """

    def process_master_account(self, fileName):
        """Function to create a dictionary of account objects from the master accounts file.
        This allows for a cached version of the master accounts file for any future transactions.
        """
        with open(fileName) as file:
            for line in file:
                #Remove leading and trailing spaces.
                line = line.strip()
                
                try:
                    #Split line into list, use items in master account line to create Account object.
                    #Store Account objects in dictionary using account number for easy access.
                    items = line.split(" ")
                    accountObj = Account.Account(int(items[0]), int(items[1]), items[2])
                    TxnProcess.accounts_dic[accountObj.get_account_num()] = accountObj
                except ValueError:
                    err.process_error("ERR_MASTERACCOUNT")
                    sys.exit()

    def create_master_valid_account_files(self, dic, masterAccountFile, validAccountFile):
        """Function to write all cached dictionary items (account objects) to master account file and valid account file."""
        masterF = open(masterAccountFile, 'w')
        validF = open(validAccountFile, 'w')

        for item in sorted(dic.keys()):
            #Write lines for master accounts file and valid accounts file.
            #Ensure account balances are between 3 and 8 digits (pad with leading zeros if necessary)
            masterF.writelines(str(dic[item].get_account_num()) + " " + str(dic[item].get_account_balance()).zfill(3)  + " " + dic[item].get_account_name() + "\n")
            validF.writelines(str(dic[item].get_account_num()) + "\n")
        masterF.close()
        
        #Add invalid account number to end of valid accounts file
        validF.writelines("0000000")
        validF.close()
        
    def account_name_exists(self, accountName):
        """Function to check if an account name already exists in the dictionary of accounts."""
        for account in TxnProcess.accounts_dic:
            if (accountName == TxnProcess.accounts_dic[account].get_account_name()):
                return True
        return False
