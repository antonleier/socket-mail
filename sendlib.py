#!/usr/bin/python3

# Module: sendlib.py
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
MAXLINE= 1024

###############################################
###               SMTP/CLIENT               ###
###############################################

def smtp_connect(host, port, secure, verbose):
    """
    Connects the socket to the specified SMTP server.

    Parameters:
        - host (str): The address of the SMTP server.
        - port (int): The port of the SMTP server.
        - secure (bool): Indicates whether the connection should be secure.
        - verbose (bool): Indicates whether debug messages should be displayed.

    Returns:
        - s (socket): The socket connected to the SMTP server.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ...
    return s

###############################################

def smtp_hello(s, verbose):
    """
    Sends the EHLO command to the SMTP server.

    Parameters:
        - s (socket): The socket connected to the SMTP server.
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

def smtp_auth(s, login, password, verbose):
    """
    Authenticates the client with the SMTP server using AUTH PLAIN method.

    Parameters:
        - s (socket): The socket connected to the SMTP server.
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

def smtp_noop(s, verbose):
    """
    Sends the NOOP command to the SMTP server.

    Parameters:
        - s (socket): The socket connected to the SMTP server.
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

def smtp_send(s, msg, verbose):
    """
    Sends the specified message to the SMTP server.

    Parameters:
        - s (socket): The socket connected to the SMTP server.
        - msg (email.message.EmailMessage): The message to send.
        - verbose (bool): Indicates whether debug messages should be displayed.

    Returns:
        - ok (bool): Server status (True if the send is successful, False otherwise).
        - ans (str): Server response.
    """
    ok = False
    ans = ""
    # ...
    return ok, ans

###############################################


def smtp_quit(s, verbose):
    """
    Sends the QUIT command to the SMTP server to terminate the connection.

    Parameters:
        - s (socket): The socket connected to the SMTP server.
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
