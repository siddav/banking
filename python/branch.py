from concurrent import futures
from clock import Clock
import grpc
import customer_pb2
import customer_pb2_grpc
import branch_pb2
import branch_pb2_grpc
import logging

logging.basicConfig(filename='bank.log', encoding='utf-8', level=logging.DEBUG, format='%(process)d %(asctime)s %(message)s')
PORT_BASE = 50050                        

# Method to track every event request received by the branch
def Event_Request(branchId, eventId, eventName, clock, remoteClock, queue):
    localClock = clock.getClock()
    clock.setClock(max(localClock, remoteClock) + 1)
    logBranchEvent(branchId, eventId, eventName, clock.getClock(), queue)

# Method to track every event execute by the branch
def Event_Execute(branchId, eventId, eventName, clock, queue):
    clock.incrementClock(1)
    logBranchEvent(branchId, eventId, eventName, clock.getClock(), queue)

# Method to track every propogate request received by the branch
def Propogate_Request(branchId, eventId, eventName, clock, remoteClock, queue):
    localClock = clock.getClock()
    clock.setClock(max(localClock, remoteClock) + 1)
    logBranchEvent(branchId, eventId, eventName, clock.getClock(), queue)

# Method to track propogate execute received by the branch
def Propogate_Execute(branchId, eventId, eventName, clock, queue):    
    clock.incrementClock(1) 
    logBranchEvent(branchId, eventId, eventName, clock.getClock(), queue)

# Method to track propogate response received by each branch
def Propogate_Response(branchId, eventId, eventName, clock, remoteClock, queue):
    localClock = clock.getClock()
    clock.setClock(max(localClock, remoteClock) + 1)
    logBranchEvent(branchId, eventId, eventName, clock.getClock(), queue)

# Method to track event response to the customer
def Event_Response(branchId, eventId, eventName, clock, queue):    
    clock.incrementClock(1) 
    logBranchEvent(branchId, eventId, eventName, clock.getClock(), queue)

# Log the event to the queue
def logEvent(eventId, eventName, clock, queue):
    entry = {}
    entry["type"] = 'event'
    entry["eventId"] = eventId
    entry["name"] = eventName
    entry["clock"] = clock
    queue.put(entry)    

# Log the branch event to the queue
def logBranchEvent(processId, eventId, eventName, clock, queue):
    entry = {}
    entry["type"] = 'branch'
    entry["processId"] = processId
    entry["eventId"] = eventId
    entry["name"] = eventName
    entry["clock"] = clock
    queue.put(entry)
    logEvent(eventId, eventName, clock, queue)    

# service related to branch-branch communications
class BranchService(branch_pb2_grpc.SyncAccountServicer):
    def __init__(self, branchId, account, clock, queue):
        self.account = account
        self.clock = clock
        self.branchId = branchId
        self.queue = queue

    def PropogateDeposit(self, request, context):
        amount = request.amount
        remoteClock = request.clock        
        eventId = request.eventId
        #Propogate Request        
        Propogate_Request(self.branchId, eventId, 'deposit_broadcast_request', self.clock, remoteClock, self.queue)        
        self.account.deposit(amount)
        #Propogate Execute        
        Propogate_Execute(self.branchId, eventId, 'deposit_broadcast_execute', self.clock, self.queue)
        return branch_pb2.SyncAccountResponse(message="success", clock=self.clock.getClock(),eventId=eventId)

    def PropogateWithdraw(self, request, context):
        amount = request.amount
        remoteClock = request.clock        
        eventId = request.eventId
        #Propogate Request        
        Propogate_Request(self.branchId, eventId, 'withdraw_broadcast_request', self.clock, remoteClock, self.queue)        
        self.account.withdraw(amount)        
        #Propogate Execute
        Propogate_Execute(self.branchId, eventId, 'withdraw_broadcast_execute', self.clock, self.queue)
        return branch_pb2.SyncAccountResponse(message="success", clock=self.clock.getClock(), eventId=eventId)      

# service related to customer-branch communications
class AccountService(customer_pb2_grpc.AccountServicer):
    def __init__(self, branches, branchId, account, clock, queue):
        self.branches = branches
        self.branchId = branchId
        self.account = account
        self.clock = clock
        self.queue = queue                

    # Method to return the balance of the customer
    def Query(self, request, context):
        logging.info("received request Query to: {}".format(self.branchId))
        balance = self.account.balance        
        return customer_pb2.AccountResponse(message="sucess", money=balance)

    # Method to deposit the balance to the customer account
    def Deposit(self, request, context):
        # get the deposit amount
        amount = request.amount
        remoteClock = request.clock
        eventId = request.eventId
        logging.info("received request Deposit to: {} clock: {} ".format(self.branchId, remoteClock))
        # Event Request        
        Event_Request(self.branchId, eventId, 'deposit_request', self.clock, remoteClock, self.queue)        
        # Event Execute
        self.account.deposit(amount)                
        Event_Execute(self.branchId, eventId,'deposit_execute', self.clock, self.queue)

        balance = self.account.balance
        # propogate deposit
        for b in self.branches:
            if b['id'] != self.branchId:
                port = PORT_BASE + b['id']
                with grpc.insecure_channel("localhost:"+str(port)) as channel:
                    stub = branch_pb2_grpc.SyncAccountStub(channel)
                    response = stub.PropogateDeposit(branch_pb2.SyncAccountRequest(amount=amount, clock=self.clock.getClock(),eventId=eventId))                    
                    remoteClock = response.clock                                                            
                    # Propogate Response
                    Propogate_Response(self.branchId, response.eventId, 'deposit_broadcast_response', self.clock, remoteClock, self.queue)
                    logging.info('PropogateDeposit from: {} to: {} deposit:{} response: {}'.format(self.branchId, b['id'], amount, response.message))
                    channel.close()
        #Event response                    
        Event_Response(self.branchId, eventId, 'deposit_response',self.clock, self.queue)            
        return customer_pb2.AccountResponse(message="success", money=balance, clock=self.clock.getClock(),eventId=eventId)

    # Method to withdraw the balance from the customer account
    def Withdraw (self, request, context):
        amount = request.amount
        remoteClock = request.clock
        eventId = request.eventId
        logging.info("received request Withdraw to: {}".format(self.branchId))        
        # Event Request        
        Event_Request(self.branchId, eventId, 'withdraw_request', self.clock, remoteClock, self.queue)        
        # Event Execute
        self.account.withdraw(amount)                
        Event_Execute(self.branchId, eventId,'withdraw_execute', self.clock, self.queue)

        balance = self.account.balance
        # propogate withdraw
        for b in self.branches:
            if b['id'] != self.branchId:
                port = PORT_BASE + b['id']
                with grpc.insecure_channel("localhost:"+str(port)) as channel:
                    stub = branch_pb2_grpc.SyncAccountStub(channel)
                    response = stub.PropogateWithdraw(branch_pb2.SyncAccountRequest(amount=amount,clock=self.clock.getClock(),eventId=eventId))                    
                    remoteClock = response.clock                    
                    # Propogate Response
                    Propogate_Response(self.branchId, response.eventId, 'withdraw_broadcast_response', self.clock, remoteClock, self.queue)
                    logging.info('PropogateWithdraw from: {} to: {} deposit:{} response: {}'.format(self.branchId, b['id'], amount, response.message))
                    channel.close()
        #Event response                    
        Event_Response(self.branchId, eventId, 'withdraw_response',self.clock, self.queue)            
        return customer_pb2.AccountResponse(message="success", money=balance, clock=self.clock.getClock(), eventId=eventId)

# Account abstraction for real bank account of a customer
class Account:    
    def __init__(self, amount):
        self.balance = amount

    def setBalance(self, amount):
        self.balance = amount    

    def currentBalance(self):        
        return self.balance

    def deposit(self, amount):
        self.balance = self.balance + amount        

    def withdraw(self, amount):
        self.balance = self.balance - amount
        if(self.balance < 0):
            self.balance = 0        

def serve(branches, branchId, port, initial_amount, queue):
    logging.info('**** starting branch ****' + str(branchId) + ' on port ' +  str(port))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    account = Account(initial_amount)
    # intialize clock per branch
    clock = Clock(1)
    # account service to handle customer requests
    aservice = AccountService(branches, branchId, account, clock, queue)        
    # branch service to handle branch-branch requests
    bservice = BranchService(branchId, account, clock, queue)
    customer_pb2_grpc.add_AccountServicer_to_server(aservice, server)
    branch_pb2_grpc.add_SyncAccountServicer_to_server(bservice, server)
    server.add_insecure_port("[::]:"+str(port))
    # start the server
    server.start()
    logging.info('**** started branch ****'+ str(branchId) + ' on port '+ str(port))
    server.wait_for_termination()

#serve(1, 50051)       