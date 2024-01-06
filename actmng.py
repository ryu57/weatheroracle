import os
import pickle

class AccountManager:
    def __init__(self):
        if os.path.isfile('acts/accounts.pkl'):
            file = open('acts/accounts.pkl', 'wb')
            self.accounts = pickle.load(file)

        else:
            file = open('acts/accounts.pkl', 'wb')
            pickle.dump({}, file)
            file.close()
            self.accounts = {}
