import os
APP_ID = '238848396304709'
APP_SECRET='29f48b3a2d802cd26f4d1e487d1b6a71'

# For Django All Auth
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
# ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
SOCIALACCOUNT_AUTO_SIGNUP = True
LOGIN_REDIRECT_URL = "/"
# ACCOUNT_SIGNUP_FORM_CLASS = 'apps.mainapp.forms.SignupForm'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_USERNAME_BLACKLIST =[]
ACCOUNT_USERNAME_REQUIRED =False
APPEND_SLASH = False
SERVER_EMAIL= 'info@meroanswer.com'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = 'MeroAnswer <info@meroanswer.com>'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': [
        	"email",
            # "public_profile", 
            "user_friends"
            ],
        #'AUTH_PARAMS': { 'auth_type': 'reauthenticate' },
        'AUTH_PARAMS': { },
        'METHOD': 'oauth2'
        },
    }


