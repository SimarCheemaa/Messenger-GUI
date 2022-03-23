# Simar Cheema
# simarc@uci.edu
# 31075859

import unittest
import ds_protocol as dsp

t = 'user_token'
entry = 'Hello World!'
user = 'ohhimark'
pwd = 'password123'
# Send a directmessage to another DS user
send_msg = '{"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}'
# Request unread message from the DS server
req_new = '{"token":"user_token", "directmessage": "new"}'
# Request all messages from the DS server
req_all = '{"token":"user_token", "directmessage": "all"}'
# join as existing or new user
join = '{"join": {"username": "ohhimark","password": "password123", "token":""}}'

class test_dsc(unittest.TestCase):

    def test_join_Test(self):
        self.assertEqual(dsp.join(user, pwd), join)

    def test_send_msg_Test(self):
        self.assertEqual(dsp.send_msg(t, entry, user, "1603167689.3928561"), send_msg)

    def test_req_all_Test(self):
        self.assertEqual(dsp.req_all(t), req_all)

    def test_req_new_Test(self):
        self.assertEqual(dsp.req_new(t), req_new)

if __name__ == '__main__':
    unittest.main()