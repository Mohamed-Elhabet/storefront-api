from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2(2np&4%fj3^me=z=3hvfvcpa+wt-0+4wrd(3w#i9x^0%imm6*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront7',
        # 'HOST': 'localhost',
        'HOST': 'mysql',
        'USER': 'root',
        'PASSWORD': 'MyPassword'
    }
}
