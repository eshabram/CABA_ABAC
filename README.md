# CABA_ABAC
The Cool and Absolutely Bad Ass Attribute Based Access Control policy simulator. This project is an implementation of ABAC within a shell program. 

TODO: 
- Define organization with roles, subjects, resources, and attributes.
- Establish subject, resource, and ruleset db tables. Subjects and resources will have unique IDs and various attributes in the form of dictionaries or lists. These tables are non-relational.
- Define the ruleset. A rule consists of 4 items: a subject condition, a resource condition, a constraint, and an action.

### Rules:
#### Conditions
The two types of conditions can both be a series of ANDed atomic conditions, such as: 
```python
type(sub1) in {Professor} and isTenured == True
```
The comparisons are made as: Single contained in Multiple, which is the reason for the brackets around {Professor}. This also means that type(sub1) is a singular attribute. The two allowed scenarios are single in multi and single = single, which is covered by: contains (a python ```in```).

#### Constraints 
Constraints can be empty as access does not always require it. Example: 
```python
type(sub1) in {Professor}
``` 
This would work for any resource that only requires you to be a professor. The addition of a constraint might look like this: 
```python
READ = True if type(sub1) in {Professor} and departments in departments_taught
```
NOTE: departments_taught is the subject attribute and departments is a resource attribute. They are reversed here because typically you want to check whether the subject attibute of the constraint is a *superset* of the resource attribute. 

#### Actions
Actions are what you would expect, and usually consist of the typical options: read, write, and execute.