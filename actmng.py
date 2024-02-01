import os
import pickle
from account import Account

class AccountManager:
    def __init__(self):
        if os.path.isfile('acts/accounts.pkl'):
            file = open('acts/accounts.pkl', 'rb')
            self.accounts = pickle.load(file)
            file.close()

        else:
            self.accounts = {"accounts": {} }
            self.accounts["accounts"]["default"] = Account("default")
            self.accounts["current_profile"] = "default"
            file = open('acts/accounts.pkl', 'wb')
            pickle.dump(self.accounts, file)
            file.close()

    def add_account(self, id, location):
        self.accounts["accounts"][id] = Account(id)
        self.accounts["accounts"][id].change_location(location)

    def remove_account(self, id):
        if id in self.accounts["accounts"] and id != "default":
            del self.accounts["accounts"][id]
            if id == self.accounts["current_profile"]:
                self.accounts["current_profile"] = "default"
            return True
        else:
            return False

    def change_location(self, id, location):
        self.accounts["accounts"][id].change_location(location)

    def get_profiles(self):
        return list(self.accounts["accounts"].keys())



    def set_current_profile(self, id):
        self.accounts["current_profile"] = id

    def get_current_profile(self):
        return self.accounts["current_profile"]

    def write_to_file(self):
        file = open('acts/accounts.pkl', 'wb')
        pickle.dump(self.accounts, file)
        file.close()
