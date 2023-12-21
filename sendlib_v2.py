
#!/usr/bin/python3

# Module: sendlib_v2.py
# Copyright: University of Bordeaux, France (2023).

import sys
import socket
import base64
import ssl
import email

###############################################
###                DEFAULT                  ###
###############################################

DOMAIN = "pouet.com"
TIMEOUT = 2
MAXLINE = 1024

###############################################
###               SMTP/CLIENT               ###
###############################################

def smtp_connect(host, port, secure, verbose):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        if secure:
            context = ssl.create_default_context()
            s = context.wrap_socket(s, server_hostname=host)
        s.connect((host, port))
        if verbose:
            print(f"Connected to {host} on port {port}")
        return s
    except Exception as e:
        if verbose:
            print(f"Connection failed: {e}")
        return None

def smtp_hello(s, verbose):
    try:
        s.sendall(b'EHLO ' + DOMAIN.encode() +  b'\r\n')
        response = s.recv(MAXLINE).decode()
        if verbose:
            print(f"EHLO response: {response}")
        return '250' in response, response
    except Exception as e:
        if verbose:
            print(f"EHLO failed: {e}")
        return False, str(e)

def smtp_auth(s, login, password, verbose):
    try:
        auth_message = ' ' + login + ' ' + password
        encoded_auth = base64.b64encode(auth_message.encode()).decode()
        s.sendall(b'AUTH PLAIN ' + encoded_auth.encode() +  b'\r\n')
        response = s.recv(MAXLINE).decode()
        if verbose:
            print(f"AUTH response: {response}")
        return '235' in response, response
    except Exception as e:
        if verbose:
            print(f"AUTH failed: {e}")
        return False, str(e)

def smtp_noop(s, verbose):
    try:
        s.sendall(b'NOOP\r\n')
        response = s.recv(MAXLINE).decode()
        if verbose:
            print(f"NOOP response: {response}")
        return '250' in response, response
    except Exception as e:
        if verbose:
            print(f"NOOP failed: {e}")
        return False, str(e)

def smtp_send(s, msg, verbose):
    try:
        s.sendall(msg.as_bytes())
        response = s.recv(MAXLINE).decode()
        if verbose:
            print(f"SEND response: {response}")
        return '250' in response, response
    except Exception as e:
        if verbose:
            print(f"SEND failed: {e}")
        return False, str(e)

def smtp_quit(s, verbose):
    try:
        s.sendall(b'QUIT\r\n')
        response = s.recv(MAXLINE).decode()
        if verbose:
            print(f"QUIT response: {response}")
        s.close()
        return '221' in response, response
    except Exception as e:
        if verbose:
            print(f"QUIT failed: {e}")
        return False, str(e)

### EOF
