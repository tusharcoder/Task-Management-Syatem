# @Author: Tushar Agarwal(tusharcoder) <tushar>
# @Date:   2017-06-13T10:05:51+05:30
# @Email:  tamyworld@gmail.com
# @Filename: settings.py
# @Last modified by:   tushar
# @Last modified time: 2017-06-13T10:50:05+05:30



"""
Django settings for taskmgt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import environ
root = environ.Path(__file__) - 0 # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False),) # set default values and casting
environ.Env.read_env()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
            'django.contrib.admin',
                'django.contrib.auth',
                    'django.contrib.contenttypes',
                        'django.contrib.sessions',
                            'django.contrib.messages',
                                'django.contrib.staticfiles',
                                    'core.apps.CoreConfig',
                                        'github_hook'

                                        )

MIDDLEWARE_CLASSES = (
            'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.common.CommonMiddleware',
                    'django.middleware.csrf.CsrfViewMiddleware',
                        'django.contrib.auth.middleware.AuthenticationMiddleware',
                            'django.contrib.messages.middleware.MessageMiddleware',
                                'django.middleware.clickjacking.XFrameOptionsMiddleware',
                                )

#templates settings
TEMPLATES = [
            {
                        'BACKEND': 'django.template.backends.django.DjangoTemplates',
                                'DIRS': ['templates'],
                                        'APP_DIRS': True,
                                                'OPTIONS': {
                                                                'context_processors': [
                                                                                    'django.template.context_processors.debug',
                                                                                                    'django.template.context_processors.request',
                                                                                                                    'django.contrib.auth.context_processors.auth',
                                                                                                                                    'django.contrib.messages.context_processors.messages',
                                                                                                                                                ],
                                                                        },
                                                    }
            ]
ROOT_URLCONF = 'taskmgt.urls'

WSGI_APPLICATION = 'taskmgt.wsgi.application'


DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
     }
    }

#DATABASES = {
 #    'default': env.db(),
  #   }                                

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/


STATIC_ROOT=os.path.join(BASE_DIR,'static/')
STATIC_URL = '/static/'
STATICFILES_DIRS=['static_files',]
MEDIA_ROOT=os.path.join(BASE_DIR,'/Task-Managment-System/static_files/assets/media/')
MEDIA_URL='/media/'
