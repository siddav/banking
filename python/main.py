from collections import defaultdict
from branch import serve
from customer import processEvents
import multiprocessing
import os
import json
import time
import logging

logging.basicConfig(filename='bank.log', encoding='utf-8', level=logging.DEBUG, format='%(process)d %(asctime)s %(message)s', filemode='w')

if __name__ == "__main__":
    logging.info('**** start *****')
    data = defaultdict()
    consistency_to_show = ['monotonic_writes','read_your_writes']    
    i = 0
    for consistency in consistency_to_show:
        # port base that branch process will start from
        port_base = 50050 + (i * 10010)
        i = i + 1
        # input file format to show case corresponding consistency: <consistency>_input.son
        inputFile = consistency+'_input.json'
        with open(inputFile) as f:
            data = json.load(f)

        logging.info('**** Processing file ***** ' + inputFile)

        customers = [x for x in data if x['type'] == 'customer']
        branches = [x for x in data if x['type'] == 'branch']

        logging.info('total branches ' + str(len(branches)))
        
        branch_process = {}    
        try:
            for branch in branches:
                bId = branch['id']
                initial_amount = branch['balance']
                #Spawn branch process                   
                p = multiprocessing.Process(target=serve, args=(branches, bId, port_base, initial_amount,))        
                p.start()
                branch_process[bId] = p
            logging.info('processing customer events')
            time.sleep(3)        
            customer_process = {}
            # Process Customer events
            for c in customers:
                customerId = c['id']
                events = c['events']
                if customerId not in customer_process:
                    # Spawn the customer process
                    # output file format fileName_output_customerId.json
                    output_file = consistency + "_output_" + str(customerId) + ".json"  
                    p = multiprocessing.Process(target=processEvents, args=(customerId, events, port_base,output_file,))
                    p.start()
                    customer_process[customerId] = p
                    logging.info('Customer Process started (customerId:processId) {}:{}'.format(customerId, p.pid))

            # Wait for the completion of customer process events
            for c, v in customer_process.items():
                v.join()
            logging.info('processed all customer events')  
        finally:
            for k, v in branch_process.items():
                # teminate all the branch processes
                v.terminate()
                logging.info('**** terminating branch process {} ****'.format(k))
                time.sleep(2)
                if(p.is_alive()):                
                    logging.info('**** killing branch process {} ****'.format(k))
                    v.kill()         
    logging.info('**** end *****')