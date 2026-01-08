"""
===================================================================
portfolio/apps.py - 앱 설정 파일
===================================================================

이 파일은 Django 앱의 설정 정보를 담고 있습니다.
앱의 이름과 기본 설정을 정의합니다.

이 파일은 수정할 필요가 없습니다.
===================================================================
"""

from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    """
    Portfolio 앱의 설정 클래스

    - default_auto_field: 모델의 자동 생성 ID 필드 타입
    - name: 앱의 이름 (settings.py의 INSTALLED_APPS와 일치해야 함)
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio'
