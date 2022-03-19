import socket
import signal
import sys
import random

port = 8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    print("Using default port 8080")

username_dict = {}
secret_dict = {}
cookie_dict = {}
init = False

sock = socket.socket()
sock.bind(('', port))
sock.listen(2)

login_form = """
   <form action = "http://localhost:%d" method = "post">
   Name: <input type = "text" name = "username">  <br/>
   Password: <input type = "text" name = "password" /> <br/>
   <input type = "submit" value = "Submit" />
   </form>
""" % port
login_page = "<h1>Please login</h1>" + login_form
bad_creds_page = "<h1>Bad user/pass! Try again</h1>" + login_form
logout_page = "<h1>Logged out successfully</h1>" + login_form
success_page = """
   <h1>Welcome!</h1>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "action" value = "logout" />
   <input type = "submit" value = "Click here to logout" />
   </form>
   <br/><br/>
   <h1>Your secret data is here:</h1>
""" % port

def print_value(tag, value):
    print("Here is the ", tag)
    print("\"\"\"")
    print(value)
    print("\"\"\"")
    print("\n")


def sigint_handler(sig, frame):
    print('Finishing up by closing listening socket...')
    sock.close()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler) # CTRL+C

def check_header(header)
    split_header = header.split("\n")
    for string in split_header:
        split_string = string.split(": ")
        if string[0] == "Cookie":
            return True
        else:
            continue
    return False

def check_init(header)
    split_header = header.split("\n")
    if split_header[0] == "GET / HTTP/1.1":
        init = True

#def proc_body(body)
#    if body == '':
#        return
#    input = body.split("&")


# no cookie file, only valid while server runs
ufile = open("passwords.txt", "r")
for line in ufile:
    ustring = line.split(" ")
    username_dict[line[0]] = line[1]
sfile = open("secets.txt", "r")
for line in sfile:
    sstring = line.split(" ")
    secret_dict[line[0]] = line[1]

while True:
    client, addr = sock.accept()
    req = client.recv(1024)

    # Let's pick the headers and entity body apart
    header_body = req.split('\r\n\r\n') # header and body are split with this string
    headers = header_body[0]
    #has_cookie = check_header(headers)
    #check_init(headers)

    #if has_cookie and init:
    #    # authenticate off of cookie
    #    init = False
    #    rand_val = random.getrandbits(64)
    #    headers_to_send = "Set-Cookie: token=" + str(rand_val) + "\r\n"
    #else if init:
    #    # give cookie
    #    init = False

    body = '' if len(header_body) == 1 else header_body[1]
    print_value('headers', headers)
    print_value('entity body', body)

    html_content_to_send = login_page

    headers_to_send = ''

    response  = 'HTTP/1.1 200 OK\r\n'
    response += headers_to_send
    response += 'Content-Type: text/html\r\n\r\n'
    response += html_content_to_send
    print_value('response', response)
    client.send(response)
    client.close()

    print("Served one request/connection!")
    print("\n")

# We will never actually get here.
# Close the listening socket
sock.close()
