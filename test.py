from utils.entities import Subject, Resource
from utils.ruleset import check_rules

###################### Subjects #################################
elliot = Subject()
elliot.id = "Elliot_Shabram" # has to be unique
elliot.role = "student"
elliot.departments = {"ecs"}
elliot.courses_taught = {"ecs_252"} # lets pretend that I am the TA for the computer networks course
elliot.courses_taken = {"ecs_235a", "ecs_252"} 

gary = Subject()
gary.id = "Gary_S_May" # has to be unique
gary.role = "chancellor"
gary.departments = {"ecs", "eec"}

matt = Subject()
matt.id = "Matt_Bishop" # has to be unique
matt.role = "professor"
matt.departments = {"ecs"}
matt.courses_taught = {"ecs_235a", "ecs_235b", "ecs_236"}

dipak = Subject()
dipak.id = "Dipak_Ghosal" # has to be unique
dipak.role = "professor"
dipak.departments = {"ecs"}
dipak.is_chair = True # note that Dipak is the chair of the cs department
dipak.courses_taught = {"ecs_252", "ecs_253", "ecs_255", "ecs_257"}

lucy = Subject()
lucy.id = "lucy_lu"
lucy.role = "staff"
lucy.departments = {"reg"}

carl = Subject()
carl.id = "carl"
carl.role = "staff"
carl.departments = {"fo", "ecs", "eec"}

admin = Subject()
admin.id = "admin1"
admin.role = "admin"

###################### Resources #################################
transcript1 = Resource()
transcript1.id = "transcript_1"
transcript1.type = "transcript"
transcript1.student = "Elliot_Shabram"
transcript1.departments = {"ecs"}
transcript1.courses = {"ecs_235a", "ecs_252"}

transcript2 = Resource()
transcript2.id = "transcript_1"
transcript2.type = "transcript"
transcript2.student = "Bob_McShitty"
transcript2.departments = {"ecs"}
transcript2.courses = {"ecs_235a", "ecs_252"}

gradebook1 = Resource()
gradebook1.id = "gradebook_1"
gradebook1.type = "gradebook"
gradebook1.departments = {"ecs"}
gradebook1.courses = {"ecs_252"}

gradebook2 = Resource()
gradebook2.id = "gradebook_2"
gradebook2.type = "gradebook"
gradebook2.departments = {"ecs"}
gradebook2.courses = {"ecs_235a"}

d_record_1 = Resource()
d_record_1.id = "donor_record_1"
d_record_1.type = "donor_record"
d_record_1.departments = {"ecs", "eec"}

finance1 = Resource()
finance1.id = "fin1"
finance1.type = "finacial_record"
finance1.departments = {"eec"}


READ, WRITE, EXECUTE = check_rules(elliot, transcript1) # access my transcript
READ, WRITE, EXECUTE = check_rules(elliot, transcript2) # access someone elses transcript
READ, WRITE, EXECUTE = check_rules(elliot, gradebook1) # access gradebook for class I TA
READ, WRITE, EXECUTE = check_rules(elliot, gradebook2) # class I don't TA

READ, WRITE, EXECUTE = check_rules(admin, gradebook2) 
READ, WRITE, EXECUTE = check_rules(admin, transcript1)

READ, WRITE, EXECUTE = check_rules(lucy, transcript1) # registrar worker
READ, WRITE, EXECUTE = check_rules(carl, d_record_1) # finacial office. access donor record for
READ, WRITE, EXECUTE = check_rules(carl, finance1) # fo can read any finacial rec

READ, WRITE, EXECUTE = check_rules(admin, Resource()) # hand function a default object for execute actions like create_user








