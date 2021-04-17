from google.protobuf.empty_pb2 import Empty
from clock import Clock
import grpc
import customer_pb2
import customer_pb2_grpc
import logging

logging.basicConfig(filename='bank.log', encoding='utf-8', level=logging.DEBUG, format='%(process)d %(asctime)s %(message)s')

def run(customerId, eventId, port, command, money, clock):    
    with grpc.insecure_channel("localhost:"+str(port)) as channel:
        stub = customer_pb2_grpc.AccountStub(channel)
        # Query Request
        if(command.lower() == 'query'):
            response = stub.Query(Empty())
            logging.info("Customer: {} received: {}".format(customerId, response.message))
            channel.close()
            return response
        # Deposit Request
        if(command.lower() == 'deposit'):
            response = stub.Deposit(customer_pb2.AccountRequest(amount=money, clock=clock.getClock(), eventId=eventId))
            logging.info("Customer: {} deposited: {}".format(customerId, response.message))
            channel.close()
            return response
        # Withdraw Request
        if(command.lower() == 'withdraw'):
            response = stub.Withdraw(customer_pb2.AccountRequest(amount=money, clock=clock.getClock(), eventId=eventId))
            logging.info("Customer: {} withdrew: {}".format(customerId, response.message))
            channel.close()
            return response

def processEvents(customerId, events, branch_base_port):
    clock = Clock(1)
    # process all the events for this customer
    for e in events:
                eId = e['id']
                command = e['interface']
                money = e['money']                
                port = branch_base_port + customerId
                logging.info("Processing event id: {} for customer {}:".format(customerId, eId))    
                result = run(customerId, eId, port, command, money, clock)
                logging.info("Processed event id: {} for customer {} response {}:".format(customerId, eId, result.message))
                