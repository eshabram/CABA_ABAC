
class Subject():
    def __init__(self, id="", role="", departments=set(), is_chair=False, courses_taught=set(), courses_taken=set()):
        self.id = id
        self.role = role
        self.departments = departments
        self.is_chair = is_chair
        self.courses_taught = courses_taught
        self.courses_taken = courses_taken

    def __str__(self):
        return (f"Subject(\n"
                f"  id='{self.id}',\n"
                f"  role='{self.role}',\n"
                f"  departments={self.departments if self.departments else '{}'},\n"
                f"  is_chair={self.is_chair},\n"
                f"  courses_taught={self.courses_taught if self.courses_taught else '{}'},\n"
                f"  courses_taken={self.courses_taken if self.courses_taken else '{}'}\n"
                f")")

class Resource():
    def __init__(self, id="", owner="", type="", subject="", departments=set(), courses=set()):
        self.id = id
        self.owner = owner
        self.type = type
        self.subject = subject
        self.departments = departments
        self.subdepartments = set()
        self.courses = courses

    def __str__(self):
        return (f"Resource(\n"
                f"  id='{self.id}',\n"
                f"  owner='{self.owner}',\n"
                f"  type='{self.type}',\n"
                f"  subject='{self.subject}',\n"
                f"  departments={self.departments if self.departments else '{}'},\n"
                f"  subdepartments={self.subdepartments if self.subdepartments else '{}'},\n"
                f"  courses={self.courses if self.courses else '{}'}\n"
                f")")
        