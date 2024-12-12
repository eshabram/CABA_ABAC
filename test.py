from utils.ruleset import check_your_privilege
from utils.entities import Subject, Resource
from utils.utils import *
from db.db_interface import *
from utils.organization import SUBJECTS_LIST, RESOURCE_LIST
priv_check = []
priv_correct = [8, 0, 8, 0, 12, 0, 14, 0, 14, 8, 0, 0, 14, 0, 8, 0, 2, 0, 0, 0, 0, 0, 0, 15, 0, 15]

def run_privilege_check():
    """ Run test on objects without having to query the db. """
    # rename again to lower confusion
    admin = SUBJECTS_LIST[0]
    guest = SUBJECTS_LIST[1]
    elliot = SUBJECTS_LIST[2]
    gary = SUBJECTS_LIST[3]
    matt =SUBJECTS_LIST[4]
    dipak =SUBJECTS_LIST[5]
    lucy = SUBJECTS_LIST[6]
    carl = SUBJECTS_LIST[7]
    jimbo = SUBJECTS_LIST[8]
    bob = SUBJECTS_LIST[9]

    transcript1 = RESOURCE_LIST[0]
    transcript2 = RESOURCE_LIST[1]
    gradebook1 = RESOURCE_LIST[2]
    gradebook2 = RESOURCE_LIST[3]
    d_record_1 = RESOURCE_LIST[4]
    d_record_2 = RESOURCE_LIST[5]
    finance1 = RESOURCE_LIST[6]
    finance2 = RESOURCE_LIST[7]
    user_file = RESOURCE_LIST[8]
    user_file1 = RESOURCE_LIST[9]
    edit_course = RESOURCE_LIST[10]

    READ, WRITE, EXECUTE, OWN = check_your_privilege(elliot, transcript1, test=True) # access my transcript 1000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(elliot, transcript2, test=True) # access someone elses transcript 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)

    READ, WRITE, EXECUTE, OWN = check_your_privilege(elliot, gradebook1, test=True) # access gradebook for class I TA 1000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)

    READ, WRITE, EXECUTE, OWN = check_your_privilege(elliot, gradebook2, test=True) # class I don't TA 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)


    READ, WRITE, EXECUTE, OWN = check_your_privilege(matt, gradebook2, test=True) # access grade book for course a professor teaches 1100
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)

    READ, WRITE, EXECUTE, OWN = check_your_privilege(matt, gradebook1, test=True) # access grade book for course a professor doesn't teach 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)

    READ, WRITE, EXECUTE, OWN = check_your_privilege(lucy, transcript1, test=True) # registrar worker 1110
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)

    READ, WRITE, EXECUTE, OWN = check_your_privilege(gary, transcript1, test=True) # not a registrar worker 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)

    READ, WRITE, EXECUTE, OWN = check_your_privilege(carl, d_record_1, test=True) # finacial office. access donor record in subdepartment 1110
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(gary, d_record_1, test=True) # Chancellor access donor record 1000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(jimbo, d_record_2, test=True) # finacial office. access donor record not in subdepartment 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(lucy, d_record_1, test=True) # not finacial office. access donor record 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)


    READ, WRITE, EXECUTE, OWN = check_your_privilege(carl, finance1, test=True) # fo can read, write, and execute any finacial rec 1110 
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(lucy, finance1, test=True) # not fo cannot read fin rec 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(elliot, finance1, test=True) # student can read their own finacial record 1000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(elliot, finance2, test=True) # student cannot read someone else's finacial record 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)

    READ, WRITE, EXECUTE, OWN = check_your_privilege(dipak, edit_course, test=True) # department chair can edit courses 0010
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(matt, d_record_1, test=True) # not department chair cannot edit courses 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN) 
        
    # Guest rule checks
    READ, WRITE, EXECUTE, OWN = check_your_privilege(guest, d_record_1, test=True) # 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(guest, finance1, test=True) # 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(guest, transcript1, test=True) # 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(guest, edit_course, test=True) # 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(guest, gradebook1, test=True) # 0000
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(guest, user_file, test=True) # can do anything to a userfile that they owns 1111
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    READ, WRITE, EXECUTE, OWN = check_your_privilege(guest, user_file1, test=True) # cannot access userfile that they do not own
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)

    READ, WRITE, EXECUTE, OWN = check_your_privilege(admin, Resource(), test=True) # hand function a default object for execute actions like create_user 1111
    priv_check.append(READ << 3 | WRITE << 2 | EXECUTE << 1| OWN)
    print(priv_check)

    # Compute element-wise difference
    diff = [a - b for a, b in zip(priv_correct, priv_check)]
    result = True if priv_correct == priv_check else False
    print(f'Test diff: {diff} - Success: {result}')

if __name__ == "__main__":
    run_privilege_check()

