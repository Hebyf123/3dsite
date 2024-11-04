from authlib.integrations.django_client import OAuth
from django.shortcuts import redirect
from django.conf import settings

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.AUTHLIB_OAUTH_CLIENTS['google']['client_id'],
    client_secret=settings.AUTHLIB_OAUTH_CLIENTS['google']['client_secret'],
    authorize_url=settings.AUTHLIB_OAUTH_CLIENTS['google']['authorize_url'],
    authorize_params=None,
    access_token_url=settings.AUTHLIB_OAUTH_CLIENTS['google']['token_url'],
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:8000/auth/callback/',  
    client_kwargs={'scope': 'openid profile email'}
)

def google_login(request):
    redirect_uri = 'http://localhost:8000/auth/callback/' 
    return oauth.google.authorize_redirect(request, redirect_uri)

def auth_callback(request):
    token = oauth.google.authorize_access_token(request)
    user_info = oauth.google.parse_id_token(request, token)
    
    user, created = CustomUser.objects.get_or_create(
        oauth_provider='google',
        oauth_uid=user_info['sub'],  # 'sub' это уникальный идентификатор пользователя
        defaults={
            'username': user_info['email'],
            'email': user_info['email'],
            'first_name': user_info.get('given_name', ''),
            'last_name': user_info.get('family_name', ''),
            'avatar_url': user_info.get('picture', ''),
        }
    )

    login(request, user)

    return redirect('/dashboard/')