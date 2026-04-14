from app.database import get_supabase
supabase = get_supabase()

existing = supabase.table('users').select('*').eq('username', 'test_student').execute()
if not existing.data:
    new_student = {
        'email': 'test@test.com',
        'username': 'test_student',
        'full_name': 'Estudiante de Prueba',
        'hashed_password': 'test123',
        'role': 'student',
        'is_active': True
    }
    result = supabase.table('users').insert(new_student).execute()
    print('? Estudiante creado con ID:', result.data[0]['id'])
else:
    print('?? Estudiante ya existe con ID:', existing.data[0]['id'])
    supabase.table('users').update({'hashed_password': 'test123'}).eq('id', existing.data[0]['id']).execute()
    print('? Contrase?a actualizada')

print('')
print('? Usuario: test_student / Contrase?a: test123')
