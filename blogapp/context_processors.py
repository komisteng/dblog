from .models import User

def login_user(request):
    try:
        user_id = request.session.get('user_id')
        if user_id:
            login_user = User.objects.get(id=user_id)
        else:
            login_user = {}
    except User.DoesNotExist:
        login_user = {}

    return {'login_user': login_user}