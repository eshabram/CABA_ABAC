# Subject attributes
ROLES = ["admin", "chancellor", "staff", "professor", "student", "guest"]
DEPARTMENTS = ["ecs", "eec", "fo", "reg"]
COURSES_TAUGHT = ["ecs_235a", "ecs_235b", "ecs_236", "ecs_252", "ecs_253", "ecs_255", "ecs_257", "eec_201", "eec_244"]
COURSES_TAKEN = ["ecs_235a", "ecs_235b", "ecs_236", "ecs_252", "ecs_253", "ecs_255", "ecs_257", "eec_201", "eec_244"]

# Resource attributes. Courses and departments are the same.
RESOURCE_TYPES = ["gradebook", "transcript", "finacial_record", "donor_record", "user_file", "create_user", "edit_user", "delete_user"]
FILE_TYPES = ["gradebook", "transcript", "finacial_record", "donor_record", "user_file"]

class Subject():
    def __init__(self, id="", name="", role="", departments=set(), subdepartments=set(), is_chair=False, courses_taught=set(), courses_taken=set()):
        self.id = id
        self.name = name
        self.role = role
        self.departments = departments
        self.subdepartments = subdepartments
        self.is_chair = is_chair
        self.courses_taught = courses_taught
        self.courses_taken = courses_taken

    def __str__(self):
        return (f"Subject(\n"
                f"  id='{self.id}',\n"
                f"  name='{self.name},\n"
                f"  role='{self.role}',\n"
                f"  departments={self.departments if self.departments else '{}'},\n"
                f"  subdepatrments={self.subdepartments},\n"
                f"  is_chair={self.is_chair},\n"
                f"  courses_taught={self.courses_taught if self.courses_taught else '{}'},\n"
                f"  courses_taken={self.courses_taken if self.courses_taken else '{}'}\n"
                f")\n")

class Resource():
    def __init__(self, id=-1, name="", owner="", type="", subject="", departments=set(), courses=set()):
        self.id = id
        self.name = name
        self.owner = owner
        self.type = type
        self.subject = subject
        self.departments = departments
        self.courses = courses

    def __str__(self):
        return (f"Resource(\n"
                f"  id='{self.id}',\n"
                f"  owner='{self.owner}',\n"
                f"  type='{self.type}',\n"
                f"  subject='{self.subject}',\n"
                f"  departments={self.departments if self.departments else '{}'},\n"
                f"  courses={self.courses if self.courses else '{}'}\n"
                f")\n")
        