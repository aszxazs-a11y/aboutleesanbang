"""
===================================================================
portfolio/views.py - 뷰(View) 정의 파일
===================================================================

이 파일은 웹페이지의 로직을 담당합니다.
사용자가 특정 URL에 접속하면, 해당하는 뷰 함수가 실행되어
데이터베이스에서 데이터를 가져오고, HTML 템플릿과 결합하여
웹페이지를 만들어 사용자에게 보여줍니다.

[뷰 함수 목록]
1. home       : 홈페이지 (/)
2. work_list  : 작업 목록 페이지 (/works/)
3. work_detail: 작업 상세 페이지 (/works/<id>/)
4. about      : 소개 페이지 (/about/)
5. add_comment: 댓글 작성 처리 (POST 요청)
6. delete_comment: 댓글 삭제 처리 (POST 요청)
7. add_like   : 좋아요 추가 처리 (POST 요청)

[뷰의 동작 방식]
1. 사용자가 URL에 접속
2. Django가 urls.py를 확인하여 해당 뷰 함수 호출
3. 뷰 함수가 데이터베이스에서 필요한 데이터 조회
4. 데이터와 템플릿을 결합하여 HTML 생성
5. 생성된 HTML을 사용자에게 응답
===================================================================
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import SiteSettings, Profile, SocialLink, Category, Work, Comment, Like


def home(request):
    """
    홈페이지 뷰

    홈페이지를 보여주는 함수입니다.
    사이트 설정(히어로 제목, 설명, 소개글)을 데이터베이스에서 가져와
    템플릿에 전달합니다.

    [매개변수]
    - request: 사용자의 HTTP 요청 정보

    [반환값]
    - 렌더링된 home.html 페이지

    [템플릿에 전달되는 데이터]
    - settings: 사이트 설정 데이터 (SiteSettings 모델)
    """
    # SiteSettings에서 첫 번째 설정을 가져옴 (없으면 None)
    settings = SiteSettings.objects.first()

    # home.html 템플릿에 settings 데이터를 전달하여 렌더링
    return render(request, 'home.html', {
        'settings': settings,
    })


def work_list(request):
    """
    작업 목록 뷰

    모든 작업물을 목록으로 보여주는 함수입니다.
    카테고리별 필터링 기능을 제공합니다.

    [매개변수]
    - request: 사용자의 HTTP 요청 정보
      - GET 파라미터 'category': 필터링할 카테고리 ID (선택사항)

    [반환값]
    - 렌더링된 works/list.html 페이지

    [템플릿에 전달되는 데이터]
    - works: 작업 목록 (Work 모델 쿼리셋)
    - categories: 모든 카테고리 목록
    - current_category: 현재 선택된 카테고리 ID
    """
    # 모든 작업을 가져옴 (최신순 정렬은 모델에서 설정됨)
    works = Work.objects.all()

    # 모든 카테고리 가져오기
    categories = Category.objects.all()

    # URL에서 카테고리 파라미터 확인 (?category=1 형태)
    category_id = request.GET.get('category')

    # 카테고리가 선택되었다면 해당 카테고리의 작업만 필터링
    if category_id:
        works = works.filter(category_id=category_id)

    return render(request, 'works/list.html', {
        'works': works,
        'categories': categories,
        'current_category': category_id,
    })


def work_detail(request, pk):
    """
    작업 상세 뷰

    특정 작업의 상세 정보를 보여주는 함수입니다.
    이미지 갤러리, 설명, 댓글, 좋아요, 이전/다음 작업 네비게이션을 제공합니다.

    [매개변수]
    - request: 사용자의 HTTP 요청 정보
    - pk: 작업의 고유 ID (Primary Key)

    [반환값]
    - 렌더링된 works/detail.html 페이지

    [템플릿에 전달되는 데이터]
    - work: 작업 데이터 (Work 모델)
    - images: 작업에 첨부된 이미지 목록
    - comments: 작업의 댓글 목록
    - like_count: 좋아요 수
    - prev_work: 이전 작업 (시간순)
    - next_work: 다음 작업 (시간순)
    """
    # pk에 해당하는 작업을 가져옴 (없으면 404 에러)
    work = get_object_or_404(Work, pk=pk)

    # 해당 작업의 이미지들 가져오기
    images = work.images.all()

    # 해당 작업의 댓글들 가져오기
    comments = work.comments.all()

    # 좋아요 수 계산
    like_count = work.likes.count()

    # 이전 작업 찾기 (현재 작업보다 이전에 생성된 것 중 가장 최근)
    prev_work = Work.objects.filter(created_at__lt=work.created_at).first()

    # 다음 작업 찾기 (현재 작업보다 이후에 생성된 것 중 가장 오래된)
    next_work = Work.objects.filter(created_at__gt=work.created_at).last()

    return render(request, 'works/detail.html', {
        'work': work,
        'images': images,
        'comments': comments,
        'like_count': like_count,
        'prev_work': prev_work,
        'next_work': next_work,
    })


def about(request):
    """
    소개 페이지 뷰

    프로필 정보와 SNS 링크를 보여주는 함수입니다.

    [매개변수]
    - request: 사용자의 HTTP 요청 정보

    [반환값]
    - 렌더링된 about.html 페이지

    [템플릿에 전달되는 데이터]
    - profile: 프로필 데이터 (Profile 모델)
    - social_links: SNS 링크 목록 (SocialLink 모델)
    """
    # 프로필 정보 가져오기 (첫 번째 것, 없으면 None)
    profile = Profile.objects.first()

    # SNS 링크 목록 가져오기 (순서대로)
    social_links = SocialLink.objects.all()

    return render(request, 'about.html', {
        'profile': profile,
        'social_links': social_links,
    })


def add_comment(request, pk):
    """
    댓글 작성 뷰

    작업에 새 댓글을 추가하는 함수입니다.
    POST 요청으로만 동작합니다.

    [매개변수]
    - request: 사용자의 HTTP 요청 정보
      - POST 데이터: author_name, password, content
    - pk: 댓글을 달 작업의 ID

    [반환값]
    - 작업 상세 페이지로 리다이렉트

    [동작 과정]
    1. POST 요청인지 확인
    2. 폼 데이터에서 닉네임, 비밀번호, 내용 추출
    3. 새 댓글 생성 및 저장
    4. 성공 메시지 표시
    5. 작업 상세 페이지로 이동
    """
    # POST 요청이 아니면 작업 상세 페이지로 리다이렉트
    if request.method != 'POST':
        return redirect('work_detail', pk=pk)

    # 해당 작업 가져오기
    work = get_object_or_404(Work, pk=pk)

    # POST 데이터에서 값 추출
    author_name = request.POST.get('author_name', '').strip()
    password = request.POST.get('password', '').strip()
    content = request.POST.get('content', '').strip()

    # 모든 필드가 입력되었는지 확인
    if author_name and password and content:
        # 새 댓글 생성
        Comment.objects.create(
            work=work,
            author_name=author_name,
            password=password,
            content=content
        )
        messages.success(request, '댓글이 작성되었습니다.')
    else:
        messages.error(request, '모든 필드를 입력해주세요.')

    # 작업 상세 페이지로 리다이렉트
    return redirect('work_detail', pk=pk)


def delete_comment(request, pk, comment_pk):
    """
    댓글 삭제 뷰

    댓글을 삭제하는 함수입니다.
    비밀번호 확인 후 삭제합니다.

    [매개변수]
    - request: 사용자의 HTTP 요청 정보
      - POST 데이터: password
    - pk: 작업의 ID
    - comment_pk: 삭제할 댓글의 ID

    [반환값]
    - 작업 상세 페이지로 리다이렉트

    [동작 과정]
    1. POST 요청인지 확인
    2. 입력된 비밀번호와 저장된 비밀번호 비교
    3. 일치하면 댓글 삭제
    4. 결과 메시지 표시
    5. 작업 상세 페이지로 이동
    """
    if request.method != 'POST':
        return redirect('work_detail', pk=pk)

    # 해당 댓글 가져오기
    comment = get_object_or_404(Comment, pk=comment_pk, work_id=pk)

    # 입력된 비밀번호
    password = request.POST.get('password', '').strip()

    # 비밀번호 확인
    if password == comment.password:
        comment.delete()
        messages.success(request, '댓글이 삭제되었습니다.')
    else:
        messages.error(request, '비밀번호가 일치하지 않습니다.')

    return redirect('work_detail', pk=pk)


def add_like(request, pk):
    """
    좋아요 추가 뷰

    작업에 좋아요를 추가하는 함수입니다.
    AJAX 요청을 처리하여 JSON으로 응답합니다.

    [매개변수]
    - request: 사용자의 HTTP 요청 정보
    - pk: 좋아요를 누를 작업의 ID

    [반환값]
    - JSON 응답: 새로운 좋아요 수

    [동작 과정]
    1. POST 요청인지 확인
    2. 새 좋아요 레코드 생성
    3. 현재 좋아요 수를 JSON으로 반환
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=400)

    # 해당 작업 가져오기
    work = get_object_or_404(Work, pk=pk)

    # 새 좋아요 생성
    Like.objects.create(work=work)

    # 현재 좋아요 수 계산
    like_count = work.likes.count()

    # JSON으로 응답
    return JsonResponse({
        'success': True,
        'like_count': like_count
    })
