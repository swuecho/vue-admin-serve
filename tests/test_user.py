from django.contrib.auth import get_user_model
import pytest

# Assuming the User model has been created as shown above,
# this example assumes its structure for demonstration purposes.

User = get_user_model()  # Get a reference to the user model (replace with your actual user model).

@pytest.mark.django_db
def test_user_creation():
    """Test if creating a new User instance is successful."""
    
    # Create a new user and save it to the database
    new_user = User.objects.create(email='test@example.com', first_name='Test', last_name='User')
    
    assert new_user is not None  # Assert that an instance of User was created successfully.
