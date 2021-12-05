"""
    USER: {userId, username, password, userType}
"""


class UsersList:
    ID_COUNT = 7
    USERS = [{'userId': 1, 'username': 'Andre', 'password': 'password', 'userType': 'seller'},
             {'userId': 2, 'username': 'Julia', 'password': 'password', 'userType': 'seller'},
             {'userId': 3, 'username': 'Robson', 'password': 'password', 'userType': 'seller'},
             {'userId': 4, 'username': 'Monica', 'password': 'password', 'userType': 'seller'},
             {'userId': 5, 'username': 'Ricardo', 'password': 'password', 'userType': 'seller'},
             {'userId': 6, 'username': 'Manager', 'password': 'password', 'userType': 'admin'}]

    # FUNCTIONS
    def get_users(self):
        return self.USERS.copy()

    def get_users_by_user_type(self, user_type):
        users = []
        for user in self.USERS:
            if user['userType'] == user_type:
                users.append(user)
        return users

    def get_user_by_id(self, user_id):
        for i in range(len(self.USERS)):
            if self.USERS[i]['userId'] == user_id:
                return self.USERS[i]

        return False

    def get_user_by_username(self, username):
        for i in range(len(self.USERS)):
            if self.USERS[i]['username'] == username:
                return self.USERS[i]

        return False

    def verify_login(self, username, password):
        user = self.get_user_by_username(username)
        if not user or user['password'] != password:
            return False

        return user
