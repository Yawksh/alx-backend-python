
MIDDLEWARE = [
'django.middleware.security.SecurityMiddleware', # Security enhancements
'django.contrib.sessions.middleware.SessionMiddleware', # Sessionmanagement
'django.middleware.common.CommonMiddleware', # Common request handling
'django.middleware.csrf.CsrfViewMiddleware', # CSRF protection
'django.contrib.auth.middleware.AuthenticationMiddleware', # Userauthentication
'django.contrib.messages.middleware.MessageMiddleware', # User messages
'django.middleware.clickjacking.XFrameOptionsMiddleware', # Clickjackingprotection
'chats.middleware.RequestLoggingMiddleware', # Custom middleware for logging

]