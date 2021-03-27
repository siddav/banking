from google.protobuf.empty_pb2 import Empty
import grpc
import customer_pb2
import customer_pb2_grpc
import logging

logging.basicConfig(filename='bank.log', encoding='utf-8', level=logging.DEBUG, format='%(process)d %(asctime)s %(message)s')

def run(port, command, money):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel("localhost:"+str(port)) as channel:
        stub = customer_pb2_grpc.AccountStub(channel)
        # Query
        if(command.lower() == 'query'):
            response = stub.Query(Empty())
            logging.info("Customer received: {}".format(response.message))
            channel.close()
            return response
        # Deposit
        if(command.lower() == 'deposit'):
            response = stub.Deposit(customer_pb2.AccountRequest(amount=money))
            logging.info("Customer deposited: {}".format(response.message))
            channel.close()
            return response
        # Withdraw
        if(command.lower() == 'withdraw'):
            response = stub.Withdraw(customer_pb2.AccountRequest(amount=money))
            logging.info("Customer withdrew: {}".format(response.message))
            channel.close()
            return response