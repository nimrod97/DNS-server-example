import socket
import sys

serverIP= sys.argv[1]
serverPort= int(sys.argv[2])


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
	webSiteAddr= input()
	s.sendto(webSiteAddr.encode(), (serverIP, serverPort))
	data, addr = s.recvfrom(1024)
	print(data.decode().split(',')[1])
s.close()
