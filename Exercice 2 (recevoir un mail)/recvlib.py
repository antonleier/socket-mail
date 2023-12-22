#!/usr/bin/python3

# Module: recvlib.py
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
###               POP3/CLIENT               ###
###############################################

def pop3_connect(host, port, secure, verbose):
    """
    Connects to the POP3 server.

    Parameters:
        - host (str): The address of the POP3 server.
        - port (int): The port of the POP3 server.
        - secure (bool): Indicates whether the connection should be secure.
        - verbose (bool): Indicates whether debug messages should be displayed.

    Returns:
        - s (socket): The socket connected to the POP3 server.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ...
    return s

###############################################

def pop3_auth(s, login, password, verbose):
    """
    Authenticates the client with the POP3 server using the provided login information.

    Parameters:
        - s (socket): The socket connected to the POP3 server.
        - login (str): The username for authentication.
        - password (str): The password for authentication.
        - verbose (bool): Indicates whether debug messages should be displayed.

    Returns:
        - ok (bool): Server status (True if authentication is successful, False otherwise).
        - ans (str): Server response.
    """
    ok = False
    ans = ""
    # ...
    return ok, ans

###############################################

def pop3_noop(s, verbose):
    """
    Sends the NOOP command to the POP3 server.

    Parameters:
        - s (socket): The socket connected to the POP3 server.
        - verbose (bool): Indicates whether debug messages should be displayed.

    Returns:
        - ok (bool): Server status (True if the command is successful, False otherwise).
        - ans (str): Server response.
    """
    ok = False
    ans = ""
    # ...
    return ok, ans

###############################################

def pop3_stat(s, verbose):
    """
    Sends the STAT command to the POP3 server.

    Parameters:
        - s (socket): The socket connected to the POP3 server.
        - verbose (bool): Indicates whether debug messages should be displayed.

    Returns:
        - ok (bool): Server status (True if the command is successful, False otherwise).
        - ans (str): Server response.
    """
    ok = False
    ans = ""
    # ...
    return ok, ans

###############################################

def pop3_list(s, verbose):
    """
    Sends the LIST command to the POP3 server.

    Parameters:
        - s (socket): The socket connected to the POP3 server.
        - verbose (bool): Indicates whether debug messages should be displayed.

    Returns:
        - ok (bool): Server status (True if the command is successful, False otherwise).
        - ans (str): Server response.
        - info (str): List information.
    """
    ok = False
    ans = ""
    info = ""
    # ...
    return ok, ans, info

###############################################

def pop3_retr(s, rank, verbose):
    """
    Sends the RETR command to the POP3 server to retrieve a message.

    Parameters:
        - s (socket): The socket connected to the POP3 server.
        - rank (int): The rank of the message to retrieve.
        - verbose (bool): Indicates whether debug messages should be displayed.

    Returns:
        - ok (bool): Server status (True if the command is successful, False otherwise).
        - ans (str): Server response.
        - msg (email.message.Message): Retrieved message.
    """
    ok = False
    ans = ""
    msg = None
    # ...
    return ok, ans, msg

###############################################

def pop3_dele(s, rank, verbose):
    """
    Sends the DELE command to the POP3 server to delete a message.

    Parameters:
        - s (socket): The socket connected to the POP3 server.
        - rank (int): The rank of the message to delete.
        - verbose (bool): Indicates whether debug messages should be displayed.

    Returns:
        - ok (bool): Server status (True if the command is successful, False otherwise).
        - ans (str): Server response.
    """
    ok = False
    ans = ""
    # ...
    return ok, ans

###############################################

def pop3_quit(s, verbose):
    """
    Sends the QUIT command to the POP3 server to terminate the connection.

    Parameters:
        - s (socket): The socket connected to the POP3 server.
        - verbose (bool): Indicates whether debug messages should be displayed.

    Returns:
        - ok (bool): Server status (True if the command is successful, False otherwise).
        - ans (str): Server response.
    """
    ok = False
    ans = ""
    # ...
    return ok, ans

### EOF
