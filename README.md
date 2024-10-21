# CABA_ABAC
The Cool and Absolutely Bad Ass Attribute Based Access Control Policy Simulator. This project is a shell implementation of ABAC policy using a university system as the organizational body. It is meant to demonstrate how an ABAC policy can work in a shell environment, as well as to demonstrate the power and efficiency that ABAC policies can provide. 

### Getting Started:
To run the program from the main directory of the repository simply start the ```abac-shell.py``` script like so:
```
python abac-shell.py
```
To print a help menu of commands that can be run, simply type in ```help``` or ```?```.

TODO: 
- [x] Define organization with roles, subjects, resources, and attributes.
- [] Establish subject, resource, and ruleset db tables. Subjects and resources will have unique IDs and various attributes in the form of dictionaries or lists. These tables are non-relational.
- [] Define the ruleset. A rule consists of 4 items: a subject condition, a resource condition, a constraint, and an action.

## Our Organization: University
### Subjects:
- Subject roles: admin, chancellor, staff, professor, student
- departments: "ecs", "eec", "fo" (Finacial Office), "reg" (registrar)
- subdepartments: "ecs", "eec", "fo", "reg"
- is_chair: Boolean
- courses_taught: "ecs_235a", "ecs_235b", "ecs_236", "ecs_252", "ecs_253", "ecs_255", "ecs_257", "eec_201", "eec_244"
- courses_taken: "ecs_235a", "ecs_235b", "ecs_236", "ecs_252", "ecs_253", "ecs_255", "ecs_257", "eec_201", "eec_244"

Example1 subject:
```python
subject.id = "Gary_S_May" # has to be unique
subject.role = "chancellor"
subject.departments = {"ecs", "eec"}
subject.is_chair = False
subject.courses_taught = {}
```

Example2 subject: 
```python
subject.id = "Matt_Bishop" # has to be unique
subject.role = "professor"
subject.departments = {"ecs"}
subject.is_chair = False
subject.courses_taught = {"ecs_235a", "ecs_235b", "ecs_236"}
```

Example3 subject: 
```python
subject.id = "Dipak_Ghosal" # has to be unique
subject.role = "professor"
subject.departments = {"ecs"}
subject.is_chair = True # note that Dipak is the chair of the cs department
subject.courses_taught = {"ecs_252", "ecs_253", "ecs_255", "ecs_257"}
```

Example4 subject: 
```python
subject.id = "Elliot_Shabram" # has to be unique
subject.role = "student"
subject.departments = {"ecs"}
subject.is_chair = False
subject.courses_taught = {"ecs_252"} # lets pretend that I am the TA for the computer networks course
subject.courses_taken = {"ecs_235a", "ecs_252"} # note the added section courses_taken for students only. For a professor, it is implied.
```

### Resources: 
- Resource types: gradebook, transcript, finacial_record, donor_record, create_user, edit_user, delete_user
- Resource student: Unique ID of associated studet for some of the types
- Resource Departments: "ecs", "eec", "fo", "reg"
- Resource Courses: "ecs_235a", "ecs_235b", "ecs_236", "ecs_252", "ecs_253", "ecs_255", "ecs_257", "eec_201", "eec_244"

Example 1 Resource:
```python
resource.id = "gradebook_1"
resource.type = "gradebook"
resource.departments = {"ecs"}
resource.courses = {"ecs_252"}
```
Example 2 Resource:
```python
resource.id = "transcript_1"
resource.type = "transcript"
resource.student = "Elliot_Shabram"
resource.departments = {"ecs"}
resource.courses = {"ecs_235a", "ecs_252"}
```

Example 2 Resource:
```python
resource.id = "donor_record_1"
resource.type = "donor_record"
resource.departments = {"ecs", "eec"} # donated to all departments. Could be one department
```

### Rules:
#### Conditions
The two types of conditions can both be a series of ANDed atomic conditions, such as: 
```python 
subject.type in {Professor} and subject.isTenured == True
```
The comparisons are made as: Single contained in Multiple, which is the reason for the brackets around {Professor}. This also means that type(sub1) is a singular attribute. The two allowed scenarios are single in multi and single = single, which is covered by: contains (a python ```in```).

#### Constraints 
Constraints can be empty as access does not always require it. Example: 
```python
subject.role in {"professor"} # Subject condition only
``` 
This would work for any resource that only requires you to be a professor. The addition of a constraint might look like this: 
```python
subject.role in {"professor"} and subject.courses_taught >= resource.courses
```
Here is a full rule with all 4 components, subject condition, resource condition, constraint, and action.

Example 1 Rule:
```python
READ = READ or (subject.role in {"professor"} and resource.type == "gradebook" and subject.courses_taught >=  resource.courses)
```
In English: "A professor can read a gradebook if they are teaching the course."

Example 2 Rule: 
```python
READ = READ or (subject.role in {"chancellor"} and resource.type == "donor_record")
```
In English: "The Chancelor can read donor records."

NOTE: the above rule does not need a constraint. 

The above rule does not mean that subjects who are not the Chancellor cannot read donor_records. There may be multiple rules for reading the same resource. Sometimes these rules can be combined for efficiency, but they become more complicated to implement. Here is an example of another rule that grants reads on the same documents:
```python
READ = READ or ({"fo"} in subject.departments and resource.type == "donor_record" and subject.departments >= resource.departments)
```
In English: "A person in the finacial office can read a donor record if the departments that were donated to are in their departments."

#### Actions
Actions are what you would expect, and usually consist of the typical options: read, write, and execute. 
