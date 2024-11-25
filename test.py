from utils.ruleset import check_your_privilege
from utils.entities import Subject, Resource
from utils.utils import *
from db.db_interface import *
from utils.organization import SUBJECTS_LIST, RESOURCE_LIST

def run_privilege_check():
    """ Run test on objects without having to query the db. """
    # rename again to lower confusion
    admin = SUBJECTS_LIST[0]
    elliot = SUBJECTS_LIST[1]
    gary = SUBJECTS_LIST[2]
    matt =SUBJECTS_LIST[3]
    dipak =SUBJECTS_LIST[4]
    lucy = SUBJECTS_LIST[5]
    carl = SUBJECTS_LIST[6]

    transcript1 = RESOURCE_LIST[0]
    transcript2 = RESOURCE_LIST[1]
    gradebook1 = RESOURCE_LIST[2]
    gradebook2 = RESOURCE_LIST[3]
    d_record_1 = RESOURCE_LIST[4]
    finance1 = RESOURCE_LIST[5]
    READ, WRITE, EXECUTE, OWN = check_your_privilege(elliot, transcript1) # access my transcript
    READ, WRITE, EXECUTE, OWN = check_your_privilege(elliot, transcript2) # access someone elses transcript
    READ, WRITE, EXECUTE, OWN = check_your_privilege(elliot, gradebook1) # access gradebook for class I TA
    READ, WRITE, EXECUTE, OWN = check_your_privilege(elliot, gradebook2) # class I don't TA

    READ, WRITE, EXECUTE, OWN = check_your_privilege(admin, gradebook2) 
    READ, WRITE, EXECUTE, OWN = check_your_privilege(admin, transcript1)

    READ, WRITE, EXECUTE, OWN = check_your_privilege(lucy, transcript1) # registrar worker
    READ, WRITE, EXECUTE, OWN = check_your_privilege(carl, d_record_1) # finacial office. access donor record for
    READ, WRITE, EXECUTE, OWN = check_your_privilege(carl, finance1) # fo can read any finacial rec

    READ, WRITE, EXECUTE, OWN = check_your_privilege(admin, Resource()) # hand function a default object for execute actions like create_user

if __name__ == "__main__":
    run_privilege_check()

