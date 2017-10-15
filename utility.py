import main
import txnProcess
import errorHandler


class utility:
    def __init__(self):
        self.variable = 0

    def processAccountFile(self, fileName): #creating valid account list array
        with open(fileName) as file:
            for line in file:
                line = line.strip() #or some other preprocessing
                #TODO remove all trailing spaces and leading spaces from each line before converting to int
                line = int(line)
                txnProcess.valid_acc_list.append(line) #storing everything in memory!
        print(txnProcess.valid_acc_list[0])

    #forms the transaction msg to be added into the transaction summary file
    def createTxnMsg(self, txnCode, toAcc, amount, fromAcc, accName):
        msg = ""

        if(txnCode == None):
            return None

        msg += txnCode

        if(toAcc == None):
            msg += " 0000000"
        else:
            msg += " " + str(toAcc)

        if(amount == None):
            msg += " 000"
        else:
            msg += " " + str(amount)

        if(fromAcc == None):
            msg += " 0000000"
        else:
            msg += " " + str(fromAcc)

        if(accName == None):
            msg += " ***"
        else:
            msg += " " + accName

        return msg

    #create the transaction summary file
    def createTxnSummaryFile(self, listTxnMsgs):
        myfile = open('txn_summary_file.txt', 'w')
        for line in listTxnMsgs:
                #var1, var2 = line.split(",");
                myfile.writelines(line + "\n")
        myfile.close()

    def isAccountValid(self, accNum):
        if(accNum in txnProcess.valid_acc_list):
            return True
        else:
            return False

    def isAmountValid(self, amount):
        #TODO handle agent mode amounts
        if(amount < 0 or amount > 1000):
            return False
        return True
