def check_your_privilege(subject, resource):
    """
    This function checks all the rules defined for our ABAC system.  
    """
    READ, WRITE, EXECUTE, OWN = False, False, False, False
    # A professor or a TA can read a gradebook if they are teaching/TA the course.
    READ = READ or (subject.role in {"professor", "student"} and resource.type == "gradebook" and resource.courses <= subject.courses_taught) 

    # A professor can write to a gradebook if they teach the course
    WRITE = WRITE or (subject.role in {"professor"} and resource.type == "gradebook" and resource.courses <= subject.courses_taught)

    # The Chancelor can read donor records.
    READ = READ or (subject.role in {"chancellor"} and resource.type == "donor_record")

    # A person in the finacial office can read a donor record if the departments that were donated to are in their subdepartments.
    READ = READ or ("fo" in subject.departments and resource.type == "donor_record" and subject.departments >= resource.subdepartments) 

    # A person can read their own transcript.  
    READ = READ or (subject.role in {"student"} and resource.type == "transcript" and subject.id == resource.subject) 

    # You can read and write any transcript if you work in the registrars office. (small office I guess)
    READ, WRITE = tuple(x or "reg" in subject.departments and resource.type == "transcript" for x in (READ, WRITE)) 

    # A student can read their own finacial_record
    READ = READ or (subject.role in {"student"} and resource.type == "finacial_record" and subject.id == resource.subject)

    # A person working in finacial office can read and write any finacial record.
    READ, WRITE = tuple(x or "fo" in subject.departments and resource.type == "finacial_record" for x in (READ, WRITE))

    # If you are the owner of a file, you can do anything with it. 
    READ, WRITE, EXECUTE, OWN = tuple(x or subject.id == resource.owner for x in (READ, WRITE, EXECUTE, OWN))

    # Admin can perform all actions on all resources
    READ, WRITE, EXECUTE, OWN = tuple(x or subject.role in {"admin"} for x in (READ, WRITE, EXECUTE, OWN))
    
    print(f'Subject ID = {subject.id} - {resource.id} - Read: {READ} - Write: {WRITE} - Execute: {EXECUTE} - Own: {OWN}')

    return READ, WRITE, EXECUTE, OWN

