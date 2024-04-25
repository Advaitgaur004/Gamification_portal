from service import get_enrolled_students
rows = get_enrolled_students(sheet_name="Testing_GP", worksheet_name="Sheet1")
print(rows)