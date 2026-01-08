"""
===================================================================
portfolio_project/asgi.py - ASGI 설정 파일
===================================================================

ASGI (Asynchronous Server Gateway Interface)는 비동기 웹 서버와
Django를 연결하는 인터페이스입니다.

실시간 기능(웹소켓 등)이 필요할 때 사용합니다.
현재 프로젝트에서는 사용하지 않지만, Django 표준 구조로 포함합니다.

이 파일은 수정할 필요가 없습니다.
===================================================================
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')

application = get_asgi_application()
