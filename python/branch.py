from concurrent import futures
import grpc
import customer_pb2
import customer_pb2_grpc
import branch_pb2
import branch_pb2_grpc
import logging

logging.basicConfig(filename='bank.log', encoding='utf-8', level=logging.DEBUG, format='%(process)d %(asctime)s %(message)s')
PORT_BASE = 50050

# service related to branch-branch communications
class BranchService(branch_pb2_grpc.SyncAccountServicer):
    def __init__(self, account):
        self.account = account

    def PropogateDeposit(self, request, context):
        amount = request.amount
        self.account.deposit(amount)
        return branch_pb2.SyncAccountResponse(message="success")

    def PropogateWithdraw(self, request, context):
        amount = request.amount
        self.account.withdraw(amount)
        return branch_pb2.SyncAccountResponse(message="success")      

# service related to customer-branch communications
class AccountService(customer_pb2_grpc.AccountServicer):
    def __init__(self, branches, branchId, account):
        self.branches = branches
        self.branchId = branchId
        self.account = account

    def Query(self, request, context):
        logging.info("received request Query to: {}".format(self.branchId))
        balance = self.account.balance        
        return customer_pb2.AccountResponse(message="sucess", money=balance)

    def Deposit(self, request, context):
        logging.info("received request Deposit to: {}".format(self.branchId))
        amount = request.amount
        self.account.deposit(amount)
        balance = self.account.balance
        # propogate deposit
        for b in self.branches:
            if b['id'] != self.branchId:
                port = PORT_BASE + b['id']
                with grpc.insecure_channel("localhost:"+str(port)) as channel:
                    stub = branch_pb2_grpc.SyncAccountStub(channel)
                    response = stub.PropogateDeposit(branch_pb2.SyncAccountRequest(amount=amount))
                    logging.info('PropogateDeposit from: {} to: {} deposit:{} response: {}'.format(self.branchId, b['id'], amount, response.message))
                    channel.close()
        return customer_pb2.AccountResponse(message="success", money=balance)

    def Withdraw (self, request, context):
        logging.info("received request Withdraw to: {}".format(self.branchId))
        amount = request.amount
        self.account.withdraw(amount)
        balance = self.account.balance
        # propogate withdraw
        for b in self.branches:
            if b['id'] != self.branchId:
                port = PORT_BASE + b['id']
                with grpc.insecure_channel("localhost:"+str(port)) as channel:
                    stub = branch_pb2_grpc.SyncAccountStub(channel)
                    response = stub.PropogateWithdraw(branch_pb2.SyncAccountRequest(amount=amount))
                    logging.info('PropogateWithdraw from: {} to: {} deposit:{} response: {}'.format(self.branchId, b['id'], amount, response.message))
                    channel.close()
        return customer_pb2.AccountResponse(message="success", money=balance)

class Account:    
    def __init__(self, amount):
        self.balance = amount

    def setBalance(self, amount):
        self.balance = amount    

    def currentBalance(self):
        #logging.debug('current balance: ' + str(self.balance))
        return self.balance

    def deposit(self, amount):
        self.balance = self.balance + amount
        #logging.debug('Deposited amount: ' + str(amount) + ' current balance: ' + str(self.balance))

    def withdraw(self, amount):
        self.balance = self.balance - amount
        if(self.balance < 0):
            self.balance = 0
        #logging.debug('Withdrew amount: ' + str(amount) + ' current balance: ' + str(self.balance))       

def serve(branches, branchId, port, initial_amount):
    logging.info('**** starting branch ****' + str(branchId) + ' on port ' +  str(port))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    account = Account(initial_amount)
    aservice = AccountService(branches, branchId, account)
    bservice = BranchService(account)
    customer_pb2_grpc.add_AccountServicer_to_server(aservice, server)
    branch_pb2_grpc.add_SyncAccountServicer_to_server(bservice, server)
    server.add_insecure_port("[::]:"+str(port))
    server.start()
    logging.info('**** started branch ****'+ str(branchId) + ' on port '+ str(port))
    server.wait_for_termination()

#serve(1, 50051)       