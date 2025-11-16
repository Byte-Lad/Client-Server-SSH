# Client-Server-SSH

This project implements a lightweight SSH server in Python using the Paramiko library.  
Its main purpose is to provide a controlled environment for experimenting with SSH,  
understanding authentication mechanisms, and testing remote command execution.

The server accepts incoming SSH connections, authenticates the user with a predefined  
username and password, and opens an interactive channel where commands can be sent  
from the server to the connected client. This makes it useful for learning how SSH  
transport, channels, and host keys work under the hood.

Key features:
- Custom SSH server built with Paramiko's low-level API
- Password-based authentication
- RSA host key support (PEM format)
- Interactive command execution over an SSH channel
- Graceful session management and connection handling

This code is primarily intended for educational and testing purposes, especially for  
those exploring offensive security concepts, protocol internals, or automation of  
remote command execution.

Feel free to modify or extend the server to suit your learning or research needs.
