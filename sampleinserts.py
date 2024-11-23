import sqlite3

conn = sqlite3.connect('attributes.db')
cur = conn.cursor()


# List of tables to truncate
tables = ['Subjects', 'Resources', 'Passwords']

# Truncate each table (delete all rows)
for table in tables:
    cur.execute(f"DELETE FROM {table};")
    print(f"All rows from table {table} have been deleted.")

# Commit the changes
conn.commit()

subject_insert = "INSERT INTO Subjects (uid, name, role, department, sub-department, is_chair, courses_taught, courses_taken) VALUES"
# Generated sample inserts
# ecs department
cur.execute(f"{subject_insert} ('BSmith', 'Bob Smith', 'student', 'ecs', NULL, 0, NULL, 'ecs_201, math_120');")
cur.execute(f"{subject_insert} ('DKim', 'David Kim', 'student', 'ecs', NULL, 0, NULL, 'ecs_235a, eec_201, ecs_236, ecs_252, ecs_255, eec_244, ecs_257, ecs_253, ecs_235b');")
cur.execute(f"{subject_insert} ('CRosenbaum', 'Carl Rosenbaum', 'student', 'ecs', NULL, 0, NULL, 'cs_101, ecs_201');")
cur.execute(f"{subject_insert} ('EFostwich', 'Edgar Fostwich', 'student', 'ecs', NULL, 0, NULL, 'cs_101, ecs_201');")
cur.execute(f"{subject_insert} ('OWhite', 'Olivia White', 'student', 'ecs', NULL, 0, NULL, 'ecs_255, ecs_257, ecs_235b');")
cur.execute(f"{subject_insert} ('CLee', 'Carol Lee', 'professor', 'ecs', NULL, 0, 'cs_420', NULL);")
cur.execute(f"{subject_insert} ('FWhite', 'Frank White', 'professor', 'ecs', 'networks', 0, 'ecs_235', NULL);")
cur.execute(f"{subject_insert} ('AJohnson', 'Alice Johnson', 'professor', 'ecs', NULL, 0, 'ecs_201, ecs_235', NULL);")
cur.execute(f"{subject_insert} ('EBrown', 'Eva Brown', 'chair', 'ecs', 'ecs', 1, 'math_101, math_201', NULL);")

# eec department
cur.execute(f"{subject_insert} ('LTurner', 'Leo Turner', 'student', 'eec', NULL, 0, NULL, 'ecs_235');")
cur.execute(f"{subject_insert} ('MLee', 'Maria Lee', 'student', 'eec', NULL, 0, NULL, 'cs_520');")
cur.execute(f"{subject_insert} ('GGreen', 'Grace Green', 'student', 'eec', NULL, 0, NULL, 'math_101, math_102');")
cur.execute(f"{subject_insert} ('IScott', 'Ivy Scott', 'student', 'eec', NULL, 0, NULL, 'ecs_235b, ecs_257, ecs_252, ecs_255');")
cur.execute(f"{subject_insert} ('JBlack', 'Jack Black', 'professor', 'eec', NULL, 0, 'cs_520', NULL);")
cur.execute(f"{subject_insert} ('NYoung', 'Nick Young', 'professor', 'eec', NULL, 0, 'math_120', NULL);")
cur.execute(f"{subject_insert} ('HYoung', 'Henry Young', 'professor', 'eec', NULL, 0, 'cs_101', NULL);")
cur.execute(f"{subject_insert} ('KMiller', 'Karen Miller', 'chair', 'eec', 'eec', 1, 'cs_420', NULL);")

# fo
cur.execute(f"{subject_insert} ('PAdams', 'Paul Adams', 'staff', 'fo', 'fo, reg', NULL, NULL, NULL);")
cur.execute(f"{subject_insert} ('QJones', 'Quincy Jones', 'staff', 'fo', 'eec, ecs, fo, reg', NULL, NULL, NULL);")
cur.execute(f"{subject_insert} ('RGrey', 'Rachel Grey', 'staff', 'fo', 'fo', NULL, NULL, NULL);")
cur.execute(f"{subject_insert} ('TKing', 'Tina King', 'staff', 'fo', 'eec', NULL, NULL, NULL);")
cur.execute(f"{subject_insert} ('SHill', 'Sam Hill', 'staff', 'fo', 'eec, ecs, reg', NULL, NULL, NULL);")

# reg office
cur.execute(f"{subject_insert} ('LAcampo', 'Luis Acampo', 'staff', 'reg', 'ecs', NULL, NULL, NULL);")
cur.execute(f"{subject_insert} ('PKing', 'Patrice King', 'staff', 'reg', 'eec', NULL, NULL, NULL);")
cur.execute(f"{subject_insert} ('SHart', 'Samantha Hart', 'staff', 'reg', 'eec, ecs', NULL, NULL, NULL);")

# Chancellor
cur.execute(f"{subject_insert} ('GMay', 'Gary S. May', 'chancellor', NULL, 'eec, ecs, fo, reg', NULL, NULL, NULL);")
# Admin
cur.execute(f"{subject_insert} ('admin1','Admin Joe', 'admin', NULL, NULL, NULL, NULL, NULL);")

print("Samples inserted into Subjects")

# Sample resource inserts
resource_insert = "INSERT INTO Resources (uid, owner, type, subject, departments, courses) VALUES"
# gradebooks
cur.execute(f"{resource_insert} ('gb_ecs_255a', NULL, 'gradebook', NULL, 'ecs', 'ecs_235a');")
cur.execute(f"{resource_insert} ('gb_ecs_235b', NULL, 'gradebook', NULL, 'ecs', 'ecs_235b');")
cur.execute(f"{resource_insert} ('gb_ecs_252', NULL, 'gradebook', NULL, 'ecs', 'ecs_252');")
cur.execute(f"{resource_insert} ('gb_eec_201', NULL, 'gradebook', NULL, 'eec', 'eec_201');")
cur.execute(f"{resource_insert} ('gb_eec_224', NULL, 'gradebook', NULL, 'eec', 'eec_225');")

# transcripts
cur.execute(f"{resource_insert} ('trans_ISott', NULL, 'transcript', 'IScott', 'cs', 'ecs_235b, ecs_257, ecs_252, ecs_255');")
cur.execute(f"{resource_insert} ('trans_DKim', NULL, 'transcript', 'DKim', 'cs', 'ecs_235a, eec_201, ecs_236, ecs_252, ecs_255, eec_244, ecs_257, ecs_253, ecs_235b');")
cur.execute(f"{resource_insert} ('trans_OWhite', NULL, 'transcript', 'OWhite', 'cs', 'ecs_255, ecs_257, ecs_235b');")
cur.execute(f"{resource_insert} ('trans_RGrey', NULL, 'transcript', 'RGrey', 'ecs', 'ecs_201');")

# finacial records
cur.execute(f"{resource_insert} ('fo_1', NULL, 'finacial_record', 'Grace Green', 'math', 'math_102');")
cur.execute(f"{resource_insert} ('fo_2', NULL, 'finacial_record', 'Carol Lee', 'cs', 'cs_420');")
cur.execute(f"{resource_insert} ('fo_3', NULL, 'finacial_record', 'Maria Lee', 'cs', 'cs_520');")
cur.execute(f"{resource_insert} ('fo_4, NULL, 'finacial_record', 'Quincy Jones', 'cs', 'cs_101');")
cur.execute(f"{resource_insert} ('fo_5', NULL, 'finacial_record', 'Tina King', 'cs', 'cs_420');")

# user files
cur.execute(f"{resource_insert} ('user_file', 'Frank White', 'ecs', 'ecs_235');")
cur.execute(f"{resource_insert} ('user_file', 'Jack Black', 'cs', 'cs_520');")
cur.execute(f"{resource_insert} ('user_file', 'Leo Turner', 'ecs', 'ecs_235');")
cur.execute(f"{resource_insert} ('user_file', 'Sam Hill', 'math', 'math_102');")

# donor record
cur.execute(f"{resource_insert} ('donor_record', 'admin1', 'math', 'math_120');")
cur.execute(f"{resource_insert} ('donor_record', 'Henry Young', 'cs', 'cs_101');")

print("Samples inserted into Resources")
conn.commit()