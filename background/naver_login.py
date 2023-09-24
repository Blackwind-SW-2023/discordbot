import re, poplib, email
from email.header import decode_header, make_header
# from background import _userid, _userpw

userid='dgistlogin'
userpw='komaruN12#$'

poplib._MAXLINE = 20480

def is_auth_mail(message):    
    fr = make_header(decode_header(message.get('From')))
    subject = make_header(decode_header(message.get('Subject')))

    return (fr == 'no-reply@dgist.ac.kr') and (subject == '2차 인증 코드')

def get_auth_pop3(userid, userpw):
    # access to email server
    server = poplib.POP3_SSL('pop.naver.com',995)
    server.user(userid)
    server.pass_(userpw)

    # server.stat() # access mailbox status
    # server.stat()[0] # num of total email
    
    recent_no = server.stat()[0] # get total num of emails
    
    # print(server.retr(recent_no)[1])
    
    # traverse from the most recent message and find auth email
    message = None
    for i in range(recent_no):
        raw_email = b'\n'.join(server.retr(recent_no-i)[1]) # retrieve the whole message, join as binary
        message = email.message_from_bytes(raw_email) # Return a message object structure from a bytes-like object.
        if is_auth_mail(message): break
    
    # find auth code in the email by parsing
    text = message.get_payload(decode=True).decode(message.get_content_charset())
    auth_reg = re.search('<span>[0-9][0-9][0-9][0-9][0-9][0-9]</span>', text)
    auth_num = auth_reg.group().rstrip('</span>').lstrip('<span>')
    
    return auth_num
