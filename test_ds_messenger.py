# Simar Cheema
# simarc@uci.edu
# 31075859

import unittest
import ds_messenger

usr = 'herr'
usr2 = 'herr2'
pwd = 'password123'
HOST = '168.235.86.101'
PORT = 3021
token = '3199cde1-b404-40eb-a9a9-22426d202f5e'
msg = 'hi'
send_message = '{"response": {"type": "ok", "message": "Direct message sent"}}\n'
dsm = ds_messenger.DirectMessenger(HOST, usr, pwd)

class test_dsm(unittest.TestCase):

    def test_connect_Test(self):
        self.assertEqual(dsm.token, token)

    def test_send_Test(self):
        self.assertEqual(dsm.send('hello', usr2), True)
        self.assertEqual(dsm.send(12, usr2), False)

    def test_retrieve_Test(self):
        self.assertEqual(dsm.retrieve_new(), [])

if __name__ == '__main__':
    unittest.main()