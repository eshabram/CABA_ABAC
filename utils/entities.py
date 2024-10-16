class Subject():
    def __init__(self):
        self.id = ""
        self.role = ""
        self.departments = set()
        self.is_chair = False
        self.courses_taught = set()
        self.courses_taken = set()

class Resource():
    def __init__(self):
        self.id = ""
        self.type = ""
        self.student = ""
        self.departments = set()
        self.subdepartments = set()
        self.courses = set()
        