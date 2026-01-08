"""
===================================================================
portfolio_project/urls.py - 메인 URL 설정 파일
===================================================================

이 파일은 웹사이트의 모든 URL 경로를 정의합니다.
사용자가 웹브라우저에서 특정 주소를 입력하면,
Django가 이 파일을 보고 어떤 페이지를 보여줄지 결정합니다.

[URL 구조]
- /admin/     : 관리자 페이지
- /           : 홈페이지
- /works/     : 작업 목록
- /about/     : 소개 페이지

이 파일은 portfolio 앱의 urls.py로 연결됩니다.
===================================================================
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 관리자 페이지 URL
    # 웹브라우저에서 /admin/ 으로 접속하면 관리자 페이지로 이동
    path('admin/', admin.site.urls),

    # portfolio 앱의 URL들을 포함
    # 빈 경로('')로 설정하여 메인 페이지가 portfolio 앱에서 처리됨
    path('', include('portfolio.urls')),
]

# 개발 환경에서 미디어 파일(업로드된 이미지) 서빙
# DEBUG가 True일 때만 동작합니다
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
