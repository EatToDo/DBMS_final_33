class Role():
    def __init__(self, userid, username, pwd, gender, bdate):
        self.userid = userid
        self.username = username
        self.pwd = pwd
        self.gender = gender
        self.bdate = bdate
        self.user_action = []

    def get_available_action(self):
        pass
    def get_username(self):
        return self.username
    def get_userid(self):
        return self.userid
    def get_gender(self):
        return self.gender
    def get_bdate(self):
        return self.bdate
    def get_available_action(self):
        return self.user_action
    def get_info_msg_no_pwd(self):
        return f'userid: {self.userid}, username: {self.username}, gender: {self.gender}, birthday: {self.bdate}, role: {type(self).__name__}'
    def get_info_msg(self):
        return f'userid: {self.userid}, username: {self.username}, pwd: {self.pwd}, gender: {self.gender}, birthday: {self.bdate}, role: {type(self).__name__}'
    def isAdmin(self):
        return False