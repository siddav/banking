from customer_pb2 import WriteSet
import grpc
import customer_pb2
import customer_pb2_grpc
import logging
import json

logging.basicConfig(filename='bank.log', encoding='utf-8', level=logging.DEBUG, format='%(process)d %(asctime)s %(message)s')

class Customer:
    def __init__(self, customerId):        
        self.writeset = []   

    def getWriteSet(self):
        ws = customer_pb2.WriteSet()
        ws.write_operation_ids.extend(self.writeset)        
        return ws

    def run(self, customerId, port, command, money):    
        with grpc.insecure_channel("localhost:"+str(port)) as channel:
            stub = customer_pb2_grpc.AccountStub(channel)
            # Query
            if(command.lower() == 'query'):
                ws = self.getWriteSet()
                response = stub.Query(customer_pb2.AccountRequest(customerId=str(customerId), writeset=ws))
                logging.info("Customer {} received: {}".format(customerId, response.message))
                channel.close()
                return response
            # Deposit
            if(command.lower() == 'deposit'):
                ws = self.getWriteSet()                
                response = stub.Deposit(customer_pb2.AccountRequest(customerId=str(customerId), amount=money, writeset=ws))
                logging.info("Customer {} deposited: {}".format(customerId, response.message))
                channel.close()
                woi = response.write_operation_id
                # save the write opeearation Id to send in subsequent requests
                if woi:
                    self.writeset.append(woi)
                return response
            # Withdraw
            if(command.lower() == 'withdraw'):
                ws = self.getWriteSet()
                response = stub.Withdraw(customer_pb2.AccountRequest(customerId=str(customerId), amount=money, writeset=ws))
                logging.info("Customer {} withdrew: {}".format(customerId, response.message))
                channel.close()
                woi = response.write_operation_id
                # if write is not propogated with retry mechanism returning fail to customer for closure
                if woi:
                    self.writeset.append(woi)
                return response

def processEvents(customerId, events, branch_base_port, output_file):
    # create a customer to process events
    c = Customer(customerId)
    # process all the events for this customer
    writeResultJsons = []
    for e in events:
        command = e['interface']
        money = 0
        if(command.lower() != "query"):        
            money = e['money'] 
        dest = e['dest']        
        # the destination port of branch process to connect to       
        port = branch_base_port + dest
        logging.info("Processing event: {} for customer {}:".format(command, customerId))    
        result = c.run(customerId, port, command, money)
        logging.info("Processed event id: {} for customer {} response {}:".format(command, customerId, result.message))
        if(command.lower() == 'query'):
            resultJson = {}
            resultJson['id'] = customerId
            resultJson['balance'] = result.money
            writeResultJsons.append(resultJson)  
    # saving the file to output file                          
    with open(output_file, "w") as outfile: 
            json.dump(writeResultJsons, outfile)