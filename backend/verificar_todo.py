from app.database import get_supabase
supabase = get_supabase()

print("=== ESTUDIANTES ===")
students = supabase.table('users').select('id,username,hashed_password').eq('role', 'student').execute()
for s in students.data:
    print(s['id'], s['username'], s['hashed_password'])

print("\n=== CALIFICACIONES ===")
grades = supabase.table('grades').select('*').execute()
for g in grades.data:
    print(g)

print("\n=== BUSCANDO test_student ===")
test = supabase.table('users').select('*').eq('username', 'test_student').execute()
if test.data:
    print("test_student existe con ID:", test.data[0]['id'])
else:
    print("test_student NO existe")
