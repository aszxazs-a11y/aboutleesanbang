"""
===================================================================
portfolio_project/settings.py - Django 프로젝트 설정 파일
===================================================================

이 파일은 Django 프로젝트의 모든 설정을 담고 있습니다.
데이터베이스, 보안, 앱 목록, 템플릿 경로 등을 설정합니다.

[중요 설정 항목]
- SECRET_KEY: 보안 키 (배포 시 반드시 변경)
- DEBUG: 개발 모드 (배포 시 False로 변경)
- ALLOWED_HOSTS: 접속 허용 도메인
- INSTALLED_APPS: 사용할 앱 목록
- DATABASES: 데이터베이스 설정
===================================================================
"""

import os
from pathlib import Path
import dj_database_url

# ===================================================================
# 기본 경로 설정
# ===================================================================
# BASE_DIR: 프로젝트의 최상위 폴더 경로
# 모든 파일 경로의 기준이 됩니다
BASE_DIR = Path(__file__).resolve().parent.parent


# ===================================================================
# 보안 설정
# ===================================================================
# SECRET_KEY: Django가 암호화에 사용하는 비밀 키
# [중요] 배포 시 반드시 환경변수로 변경하세요!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-this-in-production')

# DEBUG: 개발 모드 설정
# True: 상세한 에러 메시지 표시 (개발용)
# False: 에러 메시지 숨김 (배포용)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS: 이 서버에 접속할 수 있는 도메인 목록
# 배포 시 실제 도메인을 추가해야 합니다
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']


# ===================================================================
# 앱 설정
# ===================================================================
# INSTALLED_APPS: Django 프로젝트에서 사용할 앱 목록
# Django 기본 앱 + 우리가 만든 앱(portfolio)을 포함합니다
INSTALLED_APPS = [
    # Django 기본 앱들
    'django.contrib.admin',         # 관리자 페이지
    'django.contrib.auth',          # 사용자 인증
    'django.contrib.contenttypes',  # 콘텐츠 타입
    'django.contrib.sessions',      # 세션 관리
    'django.contrib.messages',      # 메시지 프레임워크
    'django.contrib.staticfiles',   # 정적 파일 관리

    # 클라우드 스토리지
    'cloudinary_storage',           # Cloudinary 스토리지
    'cloudinary',                   # Cloudinary

    # 우리가 만든 앱
    'portfolio',                    # 포트폴리오 앱
]


# ===================================================================
# 미들웨어 설정
# ===================================================================
# 미들웨어: 요청과 응답 사이에서 동작하는 처리 계층
# 보안, 세션, 인증 등을 처리합니다
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',      # 보안 미들웨어
    'whitenoise.middleware.WhiteNoiseMiddleware',         # 정적 파일 서빙 (배포용)
    'django.contrib.sessions.middleware.SessionMiddleware',  # 세션 처리
    'django.middleware.common.CommonMiddleware',          # 공통 처리
    'django.middleware.csrf.CsrfViewMiddleware',          # CSRF 보안
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 인증 처리
    'django.contrib.messages.middleware.MessageMiddleware',     # 메시지 처리
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # 클릭재킹 방지
]


# ===================================================================
# URL 설정
# ===================================================================
# ROOT_URLCONF: URL 설정 파일의 위치
ROOT_URLCONF = 'portfolio_project.urls'


# ===================================================================
# 템플릿 설정
# ===================================================================
# TEMPLATES: HTML 템플릿 파일 설정
# 템플릿은 웹페이지의 구조(HTML)를 정의합니다
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 템플릿 파일을 찾을 폴더 목록
        'DIRS': [BASE_DIR / 'templates'],
        # 앱 폴더 내의 templates 폴더도 자동으로 찾음
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ===================================================================
# WSGI 설정
# ===================================================================
# WSGI: 웹 서버와 Django를 연결하는 인터페이스
WSGI_APPLICATION = 'portfolio_project.wsgi.application'


# ===================================================================
# 데이터베이스 설정
# ===================================================================
# DATABASES: 데이터베이스 연결 정보
# DATABASE_URL 환경변수가 있으면 PostgreSQL 사용 (배포용)
# 없으면 SQLite 사용 (로컬 개발용)
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
    )
}


# ===================================================================
# 비밀번호 검증 설정
# ===================================================================
# 사용자 비밀번호의 보안 수준을 검증하는 설정
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ===================================================================
# 국제화 설정
# ===================================================================
# 언어 및 시간대 설정
LANGUAGE_CODE = 'ko-kr'  # 한국어
TIME_ZONE = 'Asia/Seoul'  # 서울 시간대
USE_I18N = True           # 국제화 사용
USE_TZ = True             # 시간대 사용


# ===================================================================
# 정적 파일 설정 (CSS, JavaScript, 이미지 등)
# ===================================================================
# STATIC_URL: 정적 파일에 접근하는 URL 경로
STATIC_URL = '/static/'

# STATICFILES_DIRS: 정적 파일이 있는 폴더 목록 (개발용)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# STATIC_ROOT: 정적 파일을 모으는 폴더 (배포용)
# python manage.py collectstatic 명령어로 모든 정적 파일을 이 폴더로 복사
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise 설정: 정적 파일 압축 및 캐싱
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ===================================================================
# 미디어 파일 설정 (사용자 업로드 파일)
# ===================================================================
# MEDIA_URL: 업로드된 파일에 접근하는 URL 경로
MEDIA_URL = '/media/'

# MEDIA_ROOT: 업로드된 파일이 저장되는 폴더 (로컬 개발용)
MEDIA_ROOT = BASE_DIR / 'media'


# ===================================================================
# Cloudinary 설정 (이미지 클라우드 스토리지)
# ===================================================================
# CLOUDINARY_URL 환경변수가 있으면 Cloudinary 사용 (배포용)
if os.environ.get('CLOUDINARY_URL'):
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# ===================================================================
# 기본 자동 필드 설정
# ===================================================================
# 모델의 기본 키(Primary Key) 타입 설정
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
