def check_rules(subject, obj):
     # A professor can read a gradebook if they are teaching the course.
    READ = True if subject.role in {"Professor"} and obj.type == "gradebook" and obj.course in subject.courses_taught else False

    # The Chancelor can read donor records."
    READ = True if subject.role in {"Chancellor"} and obj.type == "donor_record" else False

    # A person in the finacial office can read a donor record if the departments that were donated to are in their departments.
    READ = True if {"fo"} in subject.departments and obj.type == "donor_record" and obj.departments in subject.departments else False

    # A person can read a transcript if they work in the registrar's office, or it is their own transcript.  
    READ = True if subject.role in {"Student"} or {"reg"} in subject.departments and obj.type == "transcript" and subject.id == obj.student else False
