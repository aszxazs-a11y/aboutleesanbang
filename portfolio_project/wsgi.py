"""
===================================================================
portfolio_project/wsgi.py - WSGI 설정 파일
===================================================================

WSGI (Web Server Gateway Interface)는 웹 서버와 Django를 연결하는
표준 인터페이스입니다.

Render나 다른 서버에서 배포할 때 이 파일을 사용합니다.
gunicorn 명령어로 서버를 실행할 때:
    gunicorn portfolio_project.wsgi

이 파일은 수정할 필요가 없습니다.
===================================================================
"""

import os

from django.core.wsgi import get_wsgi_application

# Django 설정 파일 위치 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')

# WSGI 애플리케이션 객체 생성
# 이 객체가 웹 서버와 Django 사이의 통신을 담당합니다
application = get_wsgi_application()
