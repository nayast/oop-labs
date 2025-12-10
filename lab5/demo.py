from user import User
from user_repository import UserRepository
from auth_service import AuthService

# Create repositories
user_repo = UserRepository('users.pkl')
auth_service = AuthService(user_repo,'session.pkl')

# Add a new user
user1 = User(id=1, name='Anastasiia', login='nayast', password='pass1', email='alice@example.com')
user_repo.add(user1)
print("Added user:", user1)

# Add another user
user2 = User(id=2, name='Sonic', login='sonic', password='pass2')
user_repo.add(user2)
print("Added user:", user2)

# Edit user properties
user1.email = 'nayast@example.com'
user_repo.update(user1)
print("Updated user:", user_repo.get_by_id(1))

# Demonstrate sorting by name
all_users = user_repo.get_all()
sorted_users = sorted(all_users)
print("All users sorted by name:", sorted_users)

# Sign in a user
auth_service.sign_in(user1)
print("Signed in user:", auth_service.current_user)
print("Is authorized:", auth_service.is_authorized)

# Switch the current user
auth_service.sign_in(user2)
print("Switched to user:", auth_service.current_user)

# Simulate application relaunch by creating new AuthService
print("\nSimulating application relaunch...")
auth_service2 = AuthService(user_repo, 'session.pkl')
print("Restored session, current user:", auth_service2.current_user)
print("Is authorized:", auth_service2.is_authorized)

# All users
print("All users:", user_repo.get_all())
