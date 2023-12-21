#!/usr/bin/env python3

# Program: sendmail.py
# Copyright: University of Bordeaux, France (2023).

import sys
import argparse
import sendlib as sendlib
import email.utils
import email.message

###############################################
###                DEFAULT                  ###
###############################################

## server config
DOMAIN = "pouet.com"
SMTP_HOST = "localhost"
SMTP_PORT = 10025          # unsecure
SMTP_PORT_SECURE = 10465   # secure over SSL/TLS

## mail config
LOGIN="toto"
PASSWORD="toto"
SENDER = "toto@pouet.com"
RECIPIENT = "tutu@pouet.com"
SUBJECT = "Test"
BODY = "Hello World!"

###############################################
###                ERROR                    ###
###############################################

def error(cmd, ans):
    print(f"[Error {cmd}] {ans.strip()}")
    sys.exit(1) # exit failure

###############################################
###                MAIN                     ###
###############################################

if __name__ == "__main__":

    ## parse arguments
    parser = argparse.ArgumentParser(prog='sendmail.py', description='SMTP client')
    parser.add_argument('-H', '--host', type=str, default=SMTP_HOST, help='server host')
    parser.add_argument('-P', '--port', type=int, default=0, help='server port')
    parser.add_argument('-S', '--secure', action='store_true', default=False, help='secure mode')
    parser.add_argument('-A', '--auth', action='store_true', default=False, help='auth mode')
    parser.add_argument('-l', '--login', type=str, default=LOGIN, help='user login')
    parser.add_argument('-p', '--password', type=str, default=PASSWORD, help='user password')
    parser.add_argument('-f', '--from', type=str, dest="sender", default=SENDER, help='mail sender')
    parser.add_argument('-t', '--to', type=str, dest="recipient", default=RECIPIENT, help='mail recipient')
    parser.add_argument('-s', '--subject', type=str, default=SUBJECT, help='mail subject')
    parser.add_argument('-b', '--body', type=str, default=BODY, help='mail body')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    args = parser.parse_args()

    ## set default port
    if args.port == 0: args.port = SMTP_PORT_SECURE if args.secure else SMTP_PORT

    ## print arguments
    if args.verbose: print("args:", args.__dict__)

    ## start smtp client
    s = sendlib.smtp_connect(args.host, args.port, args.secure, args.verbose)
    if not s: error("connect", "")

    ## hello
    ok, ans = sendlib.smtp_hello(s, args.verbose)
    if not ok: error("hello", ans)

    ## auth (optional)
    if args.auth:
        ok, ans = sendlib.smtp_auth(s, args.login, args.password, args.verbose)
        if not ok: error("auth", ans)

    ## prepare mail
    date = email.utils.formatdate(localtime=True)  # current date (RFC 5322)
    msg = email.message.EmailMessage()
    msg['From'] = args.sender
    msg['To'] = args.recipient
    msg['Subject'] = args.subject
    msg['Date'] = date
    msg.set_payload(args.body)

    ## send mail
    print(msg)
    ok, ans = sendlib.smtp_send(s, msg, args.verbose)
    if not ok: error("send", ans)

    # quit
    ok, ans = sendlib.smtp_quit(s, args.verbose)
    if not ok: error("quit", ans)
    s.close()
    print("[Success]")

### EOF
