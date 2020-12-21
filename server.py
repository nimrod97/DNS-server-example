
import socket
import sys
import time, threading

# creating a socket with the parent's server to get the details from there
def fetch_new_record(dns_name: str):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    server_socket.sendto(dns_name, (parentIP, parentPort))
    data, addr = server_socket.recvfrom(1024)

    return data

myPort = int(sys.argv[1])
parentIP = (sys.argv[2])
parentPort = int(sys.argv[3])
ipsFileName = sys.argv[4]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
s.bind(('', myPort))

while True:
    data, addr = s.recvfrom(1024)
    clientaddr=addr
    f = open(ipsFileName, 'r')
    str_records = f.readlines()
    f.close()
    records = dict()

    for rec in str_records:
        splitted = rec.split(',')
        # differentiating between static and dynamic lines in the file and saving them accordingly in the dict
        if len(splitted) == 3:
            records[splitted[0]] = (splitted[1], splitted[2].split('\n')[0])
        elif len(splitted) == 4:
            if float(splitted[3]) + float(splitted[2]) > time.time():
                records[splitted[0]] = (splitted[1], splitted[2], splitted[3].split('\n')[0])

    if data.decode() in records:
        rec = records[data.decode()]
        s.sendto(','.join([data.decode()] + list(rec)).encode(), clientaddr)
    else:
        # Need to fetch the new record
        result = fetch_new_record(data).decode().split(',')
        #saving the details in the dict
        records[data.decode()] = (str(result[1]), str(result[2]), str(time.time()))
        #sending the data to the client
        s.sendto(','.join([data.decode()] + list(records[data.decode()])).encode(), clientaddr)
        
    #updating the file
    f = open(ipsFileName, 'w')
    for record in records:
        str_val = ','.join([record] + list(records[record]))
        f.write(str_val + '\n')
    f.close()

s.close()			

				
			
			
	
			
