import customer_pb2
import customer_pb2_grpc
import logging
import grpc
import branch_pb2_grpc
import branch_pb2

PORT_BASE = 50050
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