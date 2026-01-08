"""
===================================================================
portfolio/urls.py - 앱 URL 설정 파일
===================================================================

이 파일은 portfolio 앱의 URL 경로를 정의합니다.
각 URL 경로가 어떤 뷰 함수와 연결되는지 설정합니다.

[URL 패턴]
경로              | 뷰 함수      | 이름          | 설명
------------------|--------------|---------------|------------------
/                 | home         | home          | 홈페이지
/works/           | work_list    | work_list     | 작업 목록
/works/<id>/      | work_detail  | work_detail   | 작업 상세
/works/<id>/comment/    | add_comment  | add_comment   | 댓글 작성
/works/<id>/comment/<cid>/delete/ | delete_comment | delete_comment | 댓글 삭제
/works/<id>/like/ | add_like     | add_like      | 좋아요 추가
/about/           | about        | about         | 소개 페이지

[URL 이름 사용법]
템플릿에서 URL을 하드코딩하지 않고 이름으로 참조할 수 있습니다.
예: <a href="{% url 'work_list' %}">작업 목록</a>
예: <a href="{% url 'work_detail' pk=work.id %}">상세 보기</a>
===================================================================
"""

from django.urls import path
from . import views

# URL 패턴 목록
urlpatterns = [
    # 홈페이지
    # 경로: / (사이트 메인)
    # 뷰: views.home 함수
    # 이름: 'home' (템플릿에서 {% url 'home' %}으로 사용)
    path('', views.home, name='home'),

    # 작업 목록 페이지
    # 경로: /works/
    # 뷰: views.work_list 함수
    # 이름: 'work_list'
    path('works/', views.work_list, name='work_list'),

    # 작업 상세 페이지
    # 경로: /works/1/, /works/2/ 등 (숫자는 작업의 ID)
    # 뷰: views.work_detail 함수
    # <int:pk>: URL에서 정수 값을 추출하여 pk 변수로 뷰에 전달
    path('works/<int:pk>/', views.work_detail, name='work_detail'),

    # 댓글 작성 처리
    # 경로: /works/1/comment/ (POST 요청)
    # 뷰: views.add_comment 함수
    path('works/<int:pk>/comment/', views.add_comment, name='add_comment'),

    # 댓글 삭제 처리
    # 경로: /works/1/comment/5/delete/ (POST 요청)
    # <int:comment_pk>: 삭제할 댓글의 ID
    path('works/<int:pk>/comment/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),

    # 좋아요 추가 처리
    # 경로: /works/1/like/ (POST 요청, AJAX)
    # 뷰: views.add_like 함수
    path('works/<int:pk>/like/', views.add_like, name='add_like'),

    # 소개 페이지
    # 경로: /about/
    # 뷰: views.about 함수
    path('about/', views.about, name='about'),
]
