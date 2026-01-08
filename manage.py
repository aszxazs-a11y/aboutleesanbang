#!/usr/bin/env python
"""
===================================================================
manage.py - Django 프로젝트 관리 파일
===================================================================

이 파일은 Django 프로젝트를 관리하는 명령어를 실행하는 파일입니다.
터미널에서 다음과 같은 명령어를 실행할 때 사용됩니다:

- python manage.py runserver : 개발 서버 실행
- python manage.py migrate : 데이터베이스 테이블 생성
- python manage.py createsuperuser : 관리자 계정 생성
- python manage.py collectstatic : 정적 파일 수집

이 파일은 수정할 필요가 없습니다.
===================================================================
"""
import os
import sys


def main():
    """Django 관리 명령어를 실행하는 메인 함수"""
    # Django 설정 파일의 위치를 환경변수로 지정
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django를 불러올 수 없습니다. "
            "Django가 설치되어 있는지 확인하세요. "
            "가상환경이 활성화되어 있는지도 확인하세요."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
