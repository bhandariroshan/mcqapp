import os
APP_ID = '238848396304709'
APP_SECRET='29f48b3a2d802cd26f4d1e487d1b6a71'

# For Django All Auth
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
SOCIALACCOUNT_AUTO_SIGNUP = True
LOGIN_REDIRECT_URL = "/test/"
# ACCOUNT_SIGNUP_FORM_CLASS = 'mainapp.forms.SignupForm'
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': [
        	"email",
            "public_profile", 
            "user_friends"
            ],
        #'AUTH_PARAMS': { 'auth_type': 'reauthenticate' },
        'AUTH_PARAMS': { },
        'METHOD': 'oauth2'
        },
    }


