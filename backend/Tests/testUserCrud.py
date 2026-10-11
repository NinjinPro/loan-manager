from crud.user import UserCRUD
from database.main import db
from database.models import User
from config import ConfigInstance

db.init_app(ConfigInstance)

userCrud = UserCRUD()

def create_users(usersCount:int=10):
    # usersCount = 20
    # users = []
    print('Creating start ...')
    created = 0

    for i in range(1, usersCount+1):
        try:
            userCrud.create(
                username = f'user_tsyh_{i}',
                email = f'user{i}@example.com',
                password = 'Password@123',
            )

            created += 1
        except Exception as e:
            print(str(e))

    print(f'Created {created}/{usersCount} users')

def check_user_was_created(username:str, email:str):
    print('Assertion start ...')
    
    user = userCrud.get_by_username(username)
    
    assert isinstance(user, User)
    assert user.username == username
    assert user.email == email
    
    print('Assertion ended successfully')

print(f'Tests will always use database in memory')

create_users()
check_user_was_created('user_tsyh_10', 'user10@example.com')