from app.database import get_supabase
supabase = get_supabase()

student = supabase.table('users').select('id').eq('username', 'test_student').execute()
if student.data:
    student_id = student.data[0]['id']
    print('? Estudiante ID:', student_id)
    
    grades = [
        {'student_id': student_id, 'teacher_id': 2, 'period_id': 1, 'subject': 'Matematicas', 'grade_value': 85.5},
        {'student_id': student_id, 'teacher_id': 2, 'period_id': 1, 'subject': 'Espanol', 'grade_value': 92.0},
        {'student_id': student_id, 'teacher_id': 2, 'period_id': 1, 'subject': 'Ciencias', 'grade_value': 78.0},
    ]
    
    for g in grades:
        supabase.table('grades').insert(g).execute()
        print('? Creada:', g['subject'], '-', g['grade_value'])
    
    print('')
    print('? Listo! Inicia sesion con test_student / test123')
else:
    print('? Estudiante no encontrado')
