#!/usr/bin/env python3

# Program: recvmail.py
# Copyright: University of Bordeaux, France (2023).

import sys
import argparse
import recvlib
import email.message

###############################################
###                DEFAULT                  ###
###############################################

## server config
DOMAIN = "pouet.com"
POP3_HOST = "localhost"
POP3_PORT = 10110          # unsecure
POP3_PORT_SECURE = 10995   # secure over SSL/TLS

## mail config
LOGIN="tutu"
PASSWORD="tutu"

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
    parser = argparse.ArgumentParser(prog='recvmail.py', description='POP3 client')
    parser.add_argument('-H', '--host', type=str, default=POP3_HOST, help='server host')
    parser.add_argument('-P', '--port', type=int, default=0, help='server port')
    parser.add_argument('-S', '--secure', action='store_true', default=False, help='secure mode')
    parser.add_argument('-l', '--login', type=str, default=LOGIN, help='user login')
    parser.add_argument('-p', '--password', type=str, default=PASSWORD, help='user password')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('cmd', type=str, choices=['noop', 'stat', 'list', 'retr', 'dele'], help='command')
    parser.add_argument('rank', type=int, nargs='?', default=1, help='mail rank')
    args = parser.parse_args()

    ## set default port
    if args.port == 0: args.port = POP3_PORT_SECURE if args.secure else POP3_PORT

    ## print arguments
    if args.verbose: print("args:", args.__dict__)

    ## start pop3 client
    s = recvlib.pop3_connect(args.host, args.port, args.secure, args.verbose)
    if not s: error("connect", "")

    ## auth (required)
    ok, ans = recvlib.pop3_auth(s, args.login, args.password, args.verbose)
    if not ok: error("auth", ans)

    # run command
    if(args.cmd == 'noop'):
        ok, ans = recvlib.pop3_noop(s, args.verbose)
    if(args.cmd == 'stat'):
        ok, ans = recvlib.pop3_stat(s, args.verbose)
    if(args.cmd == 'list'):
        ok, ans, info = recvlib.pop3_list(s, args.verbose)
        print(info)
    if(args.cmd == 'retr'):
        ok, ans, msg = recvlib.pop3_retr(s, args.rank, args.verbose)
        print(msg)
    if(args.cmd == 'dele'):
        ok, ans = recvlib.pop3_dele(s, args.rank, args.verbose)
    if not ok: error(args.cmd, ans)

    # print result
    print(ans)


    # quit
    ok, ans = recvlib.pop3_quit(s, args.verbose)
    if not ok: error("quit", ans)
    s.close()
    print("[Success]")

### EOF
