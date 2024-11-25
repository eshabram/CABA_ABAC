from utils.entities import Subject, Resource


###################### Subjects #################################
admin = Subject()
admin.id = "admin1"
admin.role = "admin"

guest = Subject()
guest.id = "guest" # has to be unique
guest.role = "guest"

elliot = Subject()
elliot.id = 'eshabram'
elliot.name = "Elliot Shabram" 
elliot.role = "student"
elliot.departments = {"ecs"}
elliot.courses_taught = {"ecs_252"} # lets pretend that I am the TA for the computer networks course
elliot.courses_taken = {"ecs_235a", "ecs_252"} 

gary = Subject()
gary.id = "gmay"
gary.name = "Gary S. May" 
gary.role = "chancellor"
gary.departments = {"ecs", "eec"}

# Matt Bishop
matt = Subject()
matt.id = "mbishop" 
matt.name = "Matt Bishop"
matt.role = "professor"
matt.departments = {"ecs"}
matt.courses_taught = {"ecs_235a", "ecs_235b", "ecs_236"}

dipak = Subject()
dipak.id = "dghosal"
dipak.name = "Dipak Ghosal" 
dipak.role = "professor"
dipak.departments = {"ecs"}
dipak.is_chair = True # note that Dipak is the chair of the cs department
dipak.courses_taught = {"ecs_252", "ecs_253", "ecs_255", "ecs_257"}

lucy = Subject()
lucy.id =  "llu"
lucy.name = "lucy lu"
lucy.role = "staff"
lucy.departments = {"reg"}

carl = Subject()
carl.id = "carl"
carl.name = "carl"
carl.role = "staff"
carl.departments = {"fo"}
carl.subdepartments = {"ecs", "eec"}

SUBJECTS_LIST = [admin, guest, elliot, gary, matt, dipak, lucy, carl]
PASSWORD_LIST = ['password', 'password', '1234', 'chancellor!!', 'supersecret!', 'lakjsdhffdsa$', 'kkajsdf&&&&', 'iamc4rl']

###################### Resources #################################
transcript1 = Resource()
transcript1.name = "transcript_eshabram"
transcript1.type = "transcript"
transcript1.subject = "eshabram"
transcript1.departments = {"ecs"}
transcript1.courses = {"ecs_235a", "ecs_252"}

transcript2 = Resource()
transcript2.name = "transcript_bmcshitty"
transcript2.type = "transcript"
transcript2.subject = "Bob_McShitty"
transcript2.departments = {"ecs"}
transcript2.courses = {"ecs_235a", "ecs_252"}

gradebook1 = Resource()
gradebook1.name = "gb-ecs252"
gradebook1.type = "gradebook"
gradebook1.departments = {"ecs"}
gradebook1.courses = {"ecs_252"}

gradebook2 = Resource()
gradebook2.name = "gb-ecs235a"
gradebook2.type = "gradebook"
gradebook2.departments = {"ecs"}
gradebook2.courses = {"ecs_235a"}

d_record_1 = Resource()
d_record_1.name = "donor_record_1"
d_record_1.type = "donor_record"
d_record_1.departments = {"ecs", "eec"}

finance1 = Resource()
finance1.name = "fin1"
finance1.type = "finacial_record"
finance1.departments = {"eec"}

RESOURCE_LIST = [transcript1, transcript2, gradebook1, gradebook2,  d_record_1, finance1]
