from app.database import get_supabase
supabase = get_supabase()

student = supabase.table('users').select('id').eq('username', 'test_student').execute()
if student.data:
    student_id = student.data[0]['id']
    result = supabase.table('grades').select('*').eq('student_id', student_id).execute()
    print('?? Calificaciones para estudiante:')
    for g in result.data:
        print('  ', g['subject'], ':', g['grade_value'])
else:
    print('? Estudiante no encontrado')
