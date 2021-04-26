from concurrent import futures
from collections import defaultdict
from account import Account
from IdGenerator import IdGenerator
import grpc
import customer_pb2
import customer_pb2_grpc
import branch_pb2
import branch_pb2_grpc
import time
import multiprocessing
import threading
import logging

logging.basicConfig(filename='bank.log', encoding='utf-8', level=logging.DEBUG, format='%(process)d %(asctime)s %(message)s')

class Branch:
    def __init__(self, branches, branchId, balance, port_base):        
        self.account = Account(balance)
        self.port_base = port_base
        self.branches = branches
        self.branchId = branchId
        self.port = self.port_base + branchId
        self.idGenerator = IdGenerator(branchId * 100)
        # writeset to maintain write operations per customer
        self.writesets = defaultdict()
    
    def Query(self, request, context):
        customerId = request.customerId
        logging.info("received request Query to: {} from customer {} ".format(self.branchId, customerId))
        #customerId = request.customerId
        customerWriteSet = request.writeset

        status = self.waitForWriteSetPropogation(customerId, customerWriteSet)
        balance = self.account.balance

        # if write is not propogated with retry mechanism returning fail to customer for closure
        if not status:
            return customer_pb2.AccountResponse(message="fail", money=balance)
        
        return customer_pb2.AccountResponse(message="sucess", money=balance)

    def Deposit(self, request, context):
        logging.info("received request Deposit to: {} from customer {} ".format(self.branchId, request.customerId))        
        amount = request.amount
        customerId = request.customerId
        customerWriteSet = request.writeset        

        writeOperationId = self.idGenerator.nextNumber()
        status = self.waitForWriteSetPropogation(customerId, customerWriteSet)

        # if write is not propogated with retry mechanism returning fail to customer for closure
        if not status:
            return customer_pb2.AccountResponse(message="fail", write_operation_id=writeOperationId)

        self.account.deposit(amount)        
        self.addCustomerWriteSet(customerId, writeOperationId)

        balance = self.account.balance        
        # propogate deposit
        for b in self.branches:
            if b['id'] != self.branchId:
                port = self.port_base + b['id']                
                # async propogate deposit to return response to the customer immediately
                thread = threading.Thread(target=self.AsyncPropogateDeposit, args=(port,customerId,amount, writeOperationId))
                thread.start()                
        return customer_pb2.AccountResponse(message="success", money=balance, write_operation_id=writeOperationId)

    def AsyncPropogateDeposit(self, port, customerId, amount, writeOperationId):
        with grpc.insecure_channel("localhost:"+str(port)) as channel:
                stub = branch_pb2_grpc.SyncAccountStub(channel)
                stub.PropogateDeposit(branch_pb2.SyncAccountRequest(amount=amount,customerId=customerId, write_operation_id=writeOperationId))
                channel.close()

    def Withdraw (self, request, context):
        logging.info("received request Withdraw to: {} from customer {} ".format(self.branchId, request.customerId))
        amount = request.amount
        customerId = request.customerId
        customerWriteSet = request.writeset    

        writeOperationId = self.idGenerator.nextNumber()
        status = self.waitForWriteSetPropogation(customerId, customerWriteSet)

        if not status:
            return customer_pb2.AccountResponse(message="fail", money=0, write_operation_id=writeOperationId)

        self.account.withdraw(amount)        
        self.addCustomerWriteSet(customerId, writeOperationId)

        balance = self.account.balance
        # propogate withdraw
        for b in self.branches:
            if b['id'] != self.branchId:
                port = self.port_base + b['id']
                # async propogate deposit to return response to the customer immediately
                thread = threading.Thread(target=self.AsyncPropogateWithdraw, args=(port,customerId,amount, writeOperationId))
                thread.start()                
        return customer_pb2.AccountResponse(message="success", money=balance)
    
    def AsyncPropogateWithdraw(self,port,customerId, amount,writeOperationId ):
        with grpc.insecure_channel("localhost:"+str(port)) as channel:
            stub = branch_pb2_grpc.SyncAccountStub(channel)
            stub.PropogateWithdraw(branch_pb2.SyncAccountRequest(amount=amount,customerId=customerId, write_operation_id=writeOperationId))            
            channel.close()
        
    def PropogateDeposit(self, request, context):
        amount = request.amount
        customerId = request.customerId
        writeOperationId = request.write_operation_id                
        self.addCustomerWriteSet(customerId, writeOperationId)
        self.account.deposit(amount)
        return branch_pb2.SyncAccountResponse(message="success")

    def PropogateWithdraw(self, request, context):
        amount = request.amount
        self.addCustomerWriteSet(request.customerId, request.write_operation_id)
        self.account.withdraw(amount)
        return branch_pb2.SyncAccountResponse(message="success")
    
    # maintain customer write set
    def addCustomerWriteSet(self, customerId, write_operation_id):
        if customerId not in self.writesets:
            self.writesets[customerId] = []            
        self.writesets[customerId].append(write_operation_id)

    def getCustomerWriteSet(self, customerId):
        if customerId not in self.writesets:
            self.writesets[customerId] = []
        return self.writesets[customerId]       

    # This method waits for the write to propogate if in case the write is not present in customerWriteSet
    def waitForWriteSetPropogation(self, customerId, customerWriteSet):
        exists = False 
        for write in customerWriteSet.write_operation_ids:
            exists = write in self.getCustomerWriteSet(customerId)
            if exists:
                return True    
            max_retries = 4
            sleep_time = 1        
            while not exists and max_retries != 0:
                # exponential sleep time 1, 2, 4 and max of 4 retries
                sleep_time = sleep_time * 2
                time.sleep(sleep_time)            
                exists = write in self.getCustomerWriteSet(customerId)
                if exists:
                    return True
                max_retries = max_retries - 1
                logging.info("retrying.... for {} for write {}".format(max_retries, write))

            if max_retries <= 0:
                return False
        return True

    def startBranchServer(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
        customer_pb2_grpc.add_AccountServicer_to_server(self, server)
        branch_pb2_grpc.add_SyncAccountServicer_to_server(self, server)
        server.add_insecure_port("[::]:"+str(self.port))
        logging.info('**** starting branch ****' + str(self.branchId) + ' on port ' +  str(self.port))            
        server.start()
        logging.info('**** started branch ****'+ str(self.branchId) + ' on port '+ str(self.port))
        server.wait_for_termination()

def serve(branches, branchId, port_base, balance):
    branch = Branch(branches, branchId, balance, port_base)
    branch.startBranchServer()    

#serve(1, 50051)       