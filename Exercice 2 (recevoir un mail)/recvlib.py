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
    try:
        if secure:
            # Create a secure socket using SSL/TLS
            s = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((host, port))

        if verbose:
            print(f"Connected to {host}:{port}{' securely' if secure else ''}")

        return s
    except Exception as e:
        if verbose:
            print(f"Connection failed: {str(e)}")
        return None

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

    try:
        # Send the username
        s.send(f"USER {login}\r\n".encode())
        response = s.recv(MAXLINE).decode()

        if verbose:
            print(response)

        if response.startswith("+OK"):
            # Send the password
            s.send(f"PASS {password}\r\n".encode())
            response = s.recv(MAXLINE).decode()

            if verbose:
                print(response)

            if response.startswith("+OK"):
                ok = True
                ans = response
    except Exception as e:
        if verbose:
            print(f"Authentication failed: {str(e)}")

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

    try:
        # Send the NOOP command
        s.send(b"NOOP\r\n")
        response = s.recv(MAXLINE).decode()

        if verbose:
            print(response)

        if response.startswith("+OK"):
            ok = True
            ans = response
    except Exception as e:
        if verbose:
            print(f"NOOP command failed: {str(e)}")

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

    try:
        # Send the STAT command
        s.send(b"STAT\r\n")
        response = s.recv(MAXLINE).decode()

        if verbose:
            print(response)

        if response.startswith("+OK"):
            ok = True
            ans = response
    except Exception as e:
        if verbose:
            print(f"STAT command failed: {str(e)}")

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

    try:
        # Send the LIST command
        s.send(b"LIST\r\n")
        response = s.recv(MAXLINE).decode()

        if verbose:
            print(response)

        if response.startswith("+OK"):
            ok = True
            ans = response
            info = response

            # Receive and parse the list of message information
            '''
            response = s.recv(MAXLINE).decode()
                if response == ".":
                    break
                message_info.append(response)

            info = "\n".join(message_info)
            '''
    except Exception as e:
        if verbose:
            print(f"LIST command failed: {str(e)}")

    return ok, ans, info

###############################################

def get_from(lines):
    return_path = None
    # Iterate through the lines to find the "Return-path:" line
    for line in lines:
        if line.startswith('Return-path:'):
            # Extract the email address from the line
            parts = line.split('<')
            if len(parts) > 1:
                return_path = parts[1].strip('>')
            break

    return return_path

def get_to(lines):
    envelope_to = None
    # Iterate through the lines to find the "Envelope-to:" line
    for line in lines:
        if line.startswith('Envelope-to:'):
            # Extract the email address from the line
            parts = line.split(':')
            if len(parts) > 1:
                envelope_to = parts[1].strip()
            break

    return envelope_to

def get_subject(lines):
    subject = None

    # Iterate through the lines to find the "Subject:" line
    for line in lines:
        if line.startswith('Subject:'):
            # Extract the text that follows "Subject:"
            subject = line[len('Subject:'):].strip()
            break
    return subject


def get_date(lines):
    delivery_date = None

    # Iterate through the lines to find the "Delivery-date:" line
    for line in lines:
        if line.startswith('Delivery-date:'):
            # Extract the date that follows "Delivery-date:"
            delivery_date = line[len('Delivery-date:'):].strip()
            break

    return delivery_date

def get_payload(lines):
    # Find the index of the line that contains "Hello World!"
    hello_world_index = None
    for i, line in enumerate(lines):
        if "Hello World!" in line:
            hello_world_index = i
            break

    # Extract the text from "Hello World!" up to and including the dot
    if hello_world_index is not None:
        text_start = hello_world_index
        while text_start > 0 and lines[text_start - 1] != '.':
            text_start -= 1
        extracted_text = '\r\n'.join(lines[text_start:hello_world_index + 2])

        # Print the extracted text
        #print(extracted_text)

    return extracted_text

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

    try:
        # Send the RETR command to the server
        s.send(f"RETR {rank}\r\n".encode())

        # Receive the server's response
        ans = s.recv(MAXLINE).decode()

        # Check if the response starts with "+OK"
        if ans.startswith("+OK"):
            # Split the response into lines
            lines = ans.split('\r\n')

            # Create a new email.message.Message object
            email_object = email.message.Message()
            email_object['From'] = get_from(lines)
            email_object['To'] = get_to(lines)
            email_object['Subject'] = get_subject(lines)
            email_object['Date'] = get_subject(lines)
            email_object.set_payload(get_payload(lines))

            ok = True
            msg = email_object

    except Exception as e:
        if verbose:
            print(f"Error: {e}")

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

    try:
        # Send the DELE command to mark a message for deletion
        s.send(f"DELE {rank}\r\n".encode())
        response = s.recv(MAXLINE).decode()

        if verbose:
            print(response)

        if response.startswith("+OK"):
            ok = True
            ans = response
    except Exception as e:
        if verbose:
            print(f"DELE command failed: {str(e)}")

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

    try:
        # Send the QUIT command to terminate the connection
        s.send(b"QUIT\r\n")
        response = s.recv(MAXLINE).decode()

        if verbose:
            print(response)

        if response.startswith("+OK"):
            ok = True
            ans = response
    except Exception as e:
        if verbose:
            print(f"QUIT command failed: {str(e)}")

    return ok, ans
### EOF
