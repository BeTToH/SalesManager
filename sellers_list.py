"""
    SELLER: {sellerId, username, password}
"""


class SellersList:
    ID_COUNT = 1
    SELLERS = [{'sellerId': 1, 'username': 'Andre', 'password': 'password'},
               {'sellerId': 2, 'username': 'Julia', 'password': 'password'},
               {'sellerId': 3, 'username': 'Robson', 'password': 'password'},
               {'sellerId': 4, 'username': 'Monica', 'password': 'password'},
               {'sellerId': 5, 'username': 'Ricardo', 'password': 'password'}]

    # FUNCTIONS
    def get_sellers(self):
        return self.SELLERS.copy()

    def get_seller_by_id(self, seller_id):
        for i in range(len(self.SELLERS)):
            if self.SELLERS[i]['sellerId'] == seller_id:
                return self.SELLERS[i]

        return False

    def get_seller_by_username(self, username):
        for i in range(len(self.SELLERS)):
            if self.SELLERS[i]['username'] == username:
                return self.SELLERS[i]

        return False

    def verify_login(self, username, password):
        user = self.get_seller_by_username(username)
        if not user or user['password'] != password:
            return False

        return user

    def insert_new_seller(self, username, password):
        new_seller = {'sellerId': self.ID_COUNT, 'username': username, 'password': password}

        self.SELLERS.append(new_seller)
        self.ID_COUNT += 1
