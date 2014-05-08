

#..................Server Settings............................
REMOTE_SERVER_LITE = 'foodtradelite.cloudapp.net' 
LOCAL_SERVER = 'localhost' 
REMOTE_SERVER_STAGING = 'ftstaging.cloudapp.net' 
REMOTE_MONGO_DBNAME = 'foodtrade'
REMOTE_MONGO_USERNAME = 'ftroot'
REMOTE_MONGO_PASSWORD = 'ftroot'
#..................Server Settings............................




import os


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


