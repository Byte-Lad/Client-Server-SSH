import socket
import paramiko
import threading
import sys


"""
This program is a SSH server, that our SSH client
Where we want to run commands. This could be a Linux or Windows,
that has python and Paramiko installed.
"""



# Using the key from the Paramiko demo files
# Used for authentication as a server or to sign SSH conections
host_key = paramiko.RSAKey(filename='<YourKeyName.key>', password='<YourPassphrase>')

class Server(paramiko.server.ServerInterface):
	def __init__(self):
		self.event = threading.Event()

	def check_channel_request(self, kind, chanid):
		if kind == 'session':
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

	def check_auth_password(self, username, password):
		if (username == '<SSHuser>') and (password == "<YourPassword>"):
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED



server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((server, ssh_port))
	sock.listen(100)

	print("[+] Listen for connection...")

	client, addr = sock.accept()
except Exception as e:
	print(f"[-] Listen failed: {e}")
	sys.exit(1)
print("[+] Got a connection!")

try:
	bhSession = paramiko.Transport(client)
	bhSession.add_server_key(host_key)
	server = Server()
	try:
		bhSession.start_server(server=server)
	except paramiko.SSHException as x:
		print(f"[-] SSH negotiation failed ==> {x}")

	chan = bhSession.accept(20)

	if chan is None:
		raise Exception("No channel request received :(")

	print("[+] Authenticated!")
	print(chan.recv(1024))
	chan.sendall(b'Welcome to bh_sshserver')

	while True:
		try:
			command = input("Enter command: ").strip('\n')
			if command != 'exit':
				chan.sendall(command)
				print(chan.recv(1024).decode() + '\n')
			else:
				# Closing session without leaving open execution paths
				chan.sendall(b'exit')
				print("Exiting")
				bhSession.close()
				raise Exception ('exit')
		except KeyboardInterrupt:
			bhSession.close()
except Exception as e:
	print('[-] Caught exception: ' + str(e))
	try:
		bhSession.close()
	except:
		pass
	sys.exit(1)