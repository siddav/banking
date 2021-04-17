from collections import defaultdict
from customer import processEvents
from branch import serve
from multiprocessing import Queue, JoinableQueue
import multiprocessing
import os
import json
import time
import logging

logging.basicConfig(filename='bank.log', encoding='utf-8', level=logging.DEBUG, format='%(process)d %(asctime)s %(message)s', filemode='w')

if __name__ == "__main__":
    logging.info('**** start *****')
    data = defaultdict()
    # Read the inputs from input.json file
    with open('input.json') as f:
        data = json.load(f)

    customers = [x for x in data if x['type'] == 'customer']
    branches = [x for x in data if x['type'] == 'branch']

    logging.info('total branches ' + str(len(branches)))
    logging.info('total customers with events ' + str(len(customers)))
    branch_port_base = 50050
    branch_process = {}    
    # queue to save events from multi branch processes
    queue = Queue()
    try:
        for branch in branches:
            bId = branch['id']
            port = branch_port_base + bId  
            initial_amount = branch['balance'] 
            # Spawn the branch process
            p = multiprocessing.Process(target=serve, args=(branches,bId,port,initial_amount,queue,))        
            p.start()
            branch_process[bId] = p
            logging.info('Branch Process started (branchId:port:processId) {}:{}:{}'.format(bId,port,p.pid))

        logging.info('processing customer events')
        time.sleep(3)
        customer_process = {}
        # Process Customer events
        for c in customers:
            customerId = c['id']
            events = c['events']
            if customerId not in customer_process:
                # Spawn the customer process
                p = multiprocessing.Process(target=processEvents, args=(customerId, events, branch_port_base,))
                p.start()
                customer_process[customerId] = p
                logging.info('Customer Process started (customerId:processId) {}:{}'.format(customerId, p.pid))

        # Wait for the completion of customer process events
        for c, v in customer_process.items():
            v.join()
        logging.info('processed all customer events')
        queue.put(None) 
        branch_events = {}
        all_events = {}
        # Process the Queue for events per branch and all Events        
        for item in iter(queue.get, None):
            if item['type'] == 'branch':
                processId = item['processId']
                entry = {}
                entry['id'] = item['eventId']
                entry['name'] = item['name']
                entry['clock'] = item['clock']
                branch_events.setdefault(processId,[]).append(entry)
            else:
                eventId = item['eventId']
                entry = {}
                entry['clock'] = item['clock']
                entry['name'] = item['name']
                all_events.setdefault(eventId,[]).append(entry)

        # Save the results in output.json
        writeResultJsons = []
        for b, v in branch_events.items():
            resultJson = {}
            resultJson['pid'] = b
            resultJson['data'] = v
            writeResultJsons.append(resultJson)

        for e, v in all_events.items():
            resultJson = {}
            resultJson['eventid'] = e
            resultJson['data'] = v
            writeResultJsons.append(resultJson)

        with open("output.json", "w") as outfile: 
            json.dump(writeResultJsons, outfile)

    finally:
        # Terminate all the branch processes
        for k, v in branch_process.items():
            v.terminate()
            logging.info('**** terminating branch process {} ****'.format(k))
            time.sleep(2)
            if(p.is_alive()):                
                logging.info('**** killing branch process {} ****'.format(k))
                v.kill()
        logging.info('completed writing to output.json')       
    logging.info('**** end *****') 
