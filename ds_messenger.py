#Simar Cheema
#simarc@uci.edu
#31075859

import socket
import ds_protocol as dsp
from Profile import Profile
from Profile import Post

HOST = '168.235.86.101'
PORT = 3021
profile = Profile()

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None

class DirectMessenger:

  """Creates or loads a user profile with new or pre-existing user info and connects it to the DS server."""

  def __init__(self, dsuserver=None, username=None, password=None, p=None):
    """Sets DirectMessenger class attributes with username, password, and dsuserver if new profile. If not, sets class attributes to data found in "p"."""
    self.dsuserver = dsuserver
    self.username = username
    self.password = password
    if p != None:
      try:
        profile.load_profile(p)
        profile.username = self.username
        profile.password = self.password
        profile.dsuserver = self.dsuserver
        profile.save_profile(p)
      except:
        profile.username = self.username
        profile.password = self.password
        profile.dsuserver = self.dsuserver
        profile.save_profile(p)

    token = self.get_token()
    self.token = token
  
  def connect(self, func):

    """Connects user to DS server and if successful, returns a response from the server signalling a successful connection."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      try:
        client.settimeout(4)
        client.connect(('168.235.86.101', 3021))
        self._send = client.makefile('w')
        self.recv = client.makefile('r')
        self._send.write(func + '\r\n')
        self._send.flush()
        srv_msg = self.recv.readline()
        return srv_msg
      except:
        print('Unable to connect to server. Please try again')

  def get_token(self):

    """Connects to DS server with a username and password and attempts to retrieve a token."""

    join_msg = dsp.join(self.username, self.password)
    srv_msg = self.connect(join_msg)
    try:
      x = dsp.extract_token(srv_msg)
      token = x.token
      return token
    except:
      print('Invalid username or password')
      exit()

  def send(self, message:str, recipient:str, p=None) -> bool:

    """Returns True if message successfully sent to recipient or False failed."""
    # returns true if message successfully sent, false if send failed

    try:
      post = Post()
      post.set_entry(message)
      msg = post._entry
      self.time = str(post._timestamp)
      req = dsp.send_msg(self.token, msg, recipient, self.time)
      srv_msg = self.connect(req)
      i = {'message': ['*sent:' + msg], 'timestamp': [self.time]}
      if recipient in profile.sent:
        profile.sent[recipient]['message'].append('*sent:' + msg)
        profile.sent[recipient]['timestamp'].append(self.time)
      else:
        profile.sent[recipient] = i
      if p != None:
        profile.save_profile(p)

      if srv_msg[23:28] == 'error':
        return False
      else:
        return True
    except:
      return False

  def retrieve_new(self, p=None) -> list:

    """Returns a list of DirectMessage objects containing all new messages."""

    # returns a list of DirectMessage objects containing all new messages
    #Need token of User trying to read new messages they have gotten
    req = dsp.req_new(self.token)
    srv_msg = self.connect(req)
    srv_msg = dsp.extract_json(srv_msg)
    lst = srv_msg[1]
    k = []
    for l in lst:
      user = l['from']
      msg = l['message']
      time = l['timestamp']
      directmessage = DirectMessage()
      directmessage.message = msg
      directmessage.recipient = user
      directmessage.timestamp = time
      k.append(directmessage)
      if p != None:
        i = {'message': [msg], 'timestamp': [time]}
        if user in profile.sent:
          profile.sent[user]['message'].append(msg)
          profile.sent[user]['timestamp'].append(time)
        else:
          profile.sent[user] = i
        profile.save_profile(p)

    return k

  def retrieve_all(self, p=None) -> list:

    """Returns a list of DirectMessage objects containing all messages."""
    
    # returns a list of DirectMessage objects containing all messages
    #Need token of User trying to read all messages they have gotten
    req = dsp.req_all(self.token)
    srv_msg = self.connect(req)
    srv_msg = dsp.extract_json(srv_msg)
    lst = srv_msg[1]
    profile.sent = {}
    k = []
    for l in lst:
      user = l['from']
      msg = l['message']
      time = l['timestamp']
      directmessage = DirectMessage()
      directmessage.message = msg
      directmessage.recipient = user
      directmessage.timestamp = time
      k.append(directmessage)
      i = {'message': [msg], 'timestamp': [time]}
      if user in profile.sent:
        profile.sent[user]['message'].append(msg)
        profile.sent[user]['timestamp'].append(time)
      else:
        profile.sent[user] = i
      try:
        profile.save_profile(p)
      except:
        pass
    return k
