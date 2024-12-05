from .User import User

# from action.classroom_management.ManageClassroom import ManageClassroom
# from action.course_management.ManageCourse import ManageCourse
# from action.ListUserInfo import ListUserInfo
# from action.event.SearchEvent import SearchEve

class Admin(User):
    def __init__(self, userid, username, pwd, gender, bdate):
        super().__init__(self, userid, username, pwd, gender, bdate)
        self.user_action =  super().get_available_action() + [
                                # ManageClassroom("Add/Remove/Modify/Search Classroom"),
                                # ManageCourse("Add/Upload/Remove/Modify/Search Course"),
                                # ListUserInfo("List User Information"),
                                # SearchEvent("Search Study Event")
                            ]


    def isAdmin(self):
        return True