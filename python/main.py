from collections import defaultdict
from customer import run
from branch import serve
import multiprocessing
import os
import json
import time
import logging

logging.basicConfig(filename='bank.log', encoding='utf-8', level=logging.DEBUG, format='%(process)d %(asctime)s %(message)s', filemode='w')

if __name__ == "__main__":
    logging.info('**** start *****')
    data = defaultdict()
    with open('input.json') as f:
        data = json.load(f)

    customers = [x for x in data if x['type'] == 'customer']
    branches = [x for x in data if x['type'] == 'branch']

    initial_amount = 500
    logging.info('total branches ' + str(len(branches)))
    logging.info('total customers with events ' + str(len(customers)))
    port_base = 50050
    branch_process = {}    
    try:
        for branch in branches:
            bId = branch['id']
            port = port_base + bId    
            p = multiprocessing.Process(target=serve, args=(branches,bId,port,initial_amount,))        
            p.start()
            branch_process[bId] = p
            logging.info('Branch Process started {}:{}:{}'.format(bId,port,p.pid))

        logging.info('processing customer events')
        time.sleep(3)

        writeResultJsons = []
        for c in customers:
            resultJson = {}
            customerId = c['id']        
            resultJson['id'] = customerId                
            events = c['events']
            resultJson['recv'] = []
            logging.info('processing events for customer {}'.format(customerId))
            for e in events:
                interfaceOperation = {}
                eId = e['id']
                command = e['interface']
                interfaceOperation['interface'] = command            
                money = e['money']                
                port = port_base + customerId    
                result = run(port,command, money)
                interfaceOperation['result'] = result.message
                if hasattr(result, 'money') and command.lower() == 'query':
                    interfaceOperation['money'] = result.money
                # add operatioon result to resultJson    
                resultJson['recv'].append(interfaceOperation)    
            writeResultJsons.append(resultJson)        
            
        logging.info('completed processing customer events')    
        with open("output.json", "w") as outfile: 
            json.dump(writeResultJsons, outfile)

        logging.info('completed writing to output.json')    
    finally:
        for k, v in branch_process.items():
            v.terminate()
            logging.info('**** terminating branch process {} ****'.format(k))
            time.sleep(2)
            if(p.is_alive()):                
                logging.info('**** killing branch process {} ****'.format(k))
                v.kill()         
    logging.info('**** end *****') 
