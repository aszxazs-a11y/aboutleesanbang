"""
===================================================================
portfolio/admin.py - Django 관리자 페이지 설정
===================================================================

이 파일은 Django 관리자 페이지(/admin/)에서
데이터베이스의 데이터를 관리할 수 있도록 설정합니다.

[관리자 페이지 기능]
- 사이트 설정 편집 (히어로 제목, 설명, 소개글)
- 프로필 정보 편집 (이름, 소개, 이메일, 사진)
- SNS 링크 관리
- 카테고리 관리
- 작업/프로젝트 관리 (이미지 인라인 편집)
- 댓글 확인/삭제
- 좋아요 통계

[사용 방법]
1. 터미널에서 python manage.py createsuperuser 실행
2. 사용자명, 이메일, 비밀번호 입력
3. 웹브라우저에서 /admin/ 접속
4. 생성한 관리자 계정으로 로그인
===================================================================
"""

from django.contrib import admin
from .models import SiteSettings, Profile, SocialLink, Category, Work, WorkImage, Comment, Like


# ===================================================================
# 사이트 설정 관리
# ===================================================================

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    사이트 설정 관리자 클래스

    홈페이지의 히어로 섹션과 소개글을 관리합니다.
    하나의 설정만 필요하므로 추가 생성을 제한합니다.
    """
    # 목록 페이지에서 표시할 필드
    list_display = ['hero_title']

    # 필드 그룹화 (편집 페이지에서 보기 좋게 정리)
    fieldsets = (
        ('히어로 섹션', {
            'fields': ('hero_title', 'hero_description'),
            'description': '홈페이지 상단의 큰 영역에 표시됩니다.'
        }),
        ('소개', {
            'fields': ('short_intro',),
            'description': '홈페이지에 표시될 간략한 소개글입니다.'
        }),
    )

    def has_add_permission(self, request):
        """
        추가 권한 제한

        이미 설정이 존재하면 새로 추가하지 못하게 합니다.
        (하나의 사이트 설정만 필요)
        """
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)


# ===================================================================
# 프로필 관리
# ===================================================================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    프로필 관리자 클래스

    소개 페이지에 표시될 개인 정보를 관리합니다.
    """
    list_display = ['name', 'email']

    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'email', 'profile_image'),
        }),
        ('소개', {
            'fields': ('bio',),
        }),
    )

    def has_add_permission(self, request):
        """프로필은 하나만 필요하므로 추가 제한"""
        if Profile.objects.exists():
            return False
        return super().has_add_permission(request)


# ===================================================================
# SNS 링크 관리
# ===================================================================

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """
    SNS 링크 관리자 클래스

    소개 페이지에 표시될 SNS 링크를 관리합니다.
    드래그 앤 드롭으로 순서 변경이 가능합니다.
    """
    # 목록에서 표시할 필드
    list_display = ['platform', 'url', 'order']

    # 목록에서 직접 편집 가능한 필드
    list_editable = ['order']

    # 정렬 기준
    ordering = ['order']


# ===================================================================
# 카테고리 관리
# ===================================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    카테고리 관리자 클래스

    작업물을 분류하는 카테고리를 관리합니다.
    """
    list_display = ['name', 'order', 'work_count']
    list_editable = ['order']
    ordering = ['order']

    def work_count(self, obj):
        """해당 카테고리의 작업 수를 표시"""
        return obj.works.count()

    work_count.short_description = '작업 수'


# ===================================================================
# 작업 이미지 인라인
# ===================================================================

class WorkImageInline(admin.TabularInline):
    """
    작업 이미지 인라인 클래스

    작업 편집 페이지 내에서 이미지를 추가/수정/삭제할 수 있게 합니다.
    TabularInline: 테이블 형태로 표시
    """
    model = WorkImage
    extra = 1  # 기본으로 보여줄 빈 폼 개수
    fields = ['image', 'order']
    ordering = ['order']


# ===================================================================
# 작업 관리
# ===================================================================

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    """
    작업/프로젝트 관리자 클래스

    포트폴리오의 핵심인 작업물을 관리합니다.
    이미지는 인라인으로 함께 편집할 수 있습니다.
    """
    # 목록에서 표시할 필드
    list_display = ['title', 'category', 'created_at', 'like_count', 'comment_count']

    # 필터 사이드바
    list_filter = ['category', 'created_at']

    # 검색 가능 필드
    search_fields = ['title', 'description']

    # 날짜 기반 네비게이션
    date_hierarchy = 'created_at'

    # 인라인 (이미지 관리)
    inlines = [WorkImageInline]

    # 필드 그룹화
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'category', 'thumbnail'),
        }),
        ('상세 내용', {
            'fields': ('description', 'external_link'),
        }),
    )

    def like_count(self, obj):
        """좋아요 수 표시"""
        return obj.likes.count()

    like_count.short_description = '좋아요'

    def comment_count(self, obj):
        """댓글 수 표시"""
        return obj.comments.count()

    comment_count.short_description = '댓글'


# ===================================================================
# 댓글 관리
# ===================================================================

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    댓글 관리자 클래스

    작업물에 달린 댓글을 확인하고 관리합니다.
    """
    list_display = ['author_name', 'work', 'content_preview', 'created_at']
    list_filter = ['created_at', 'work']
    search_fields = ['author_name', 'content']
    date_hierarchy = 'created_at'

    # 읽기 전용 필드 (수정 불가)
    readonly_fields = ['work', 'author_name', 'content', 'created_at']

    def content_preview(self, obj):
        """댓글 내용 미리보기 (50자까지)"""
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content

    content_preview.short_description = '내용'

    def has_add_permission(self, request):
        """관리자 페이지에서 댓글 추가 불가 (사용자만 작성)"""
        return False


# ===================================================================
# 좋아요 관리
# ===================================================================

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """
    좋아요 관리자 클래스

    작업물의 좋아요 통계를 확인합니다.
    """
    list_display = ['work', 'created_at']
    list_filter = ['work', 'created_at']
    date_hierarchy = 'created_at'

    readonly_fields = ['work', 'created_at']

    def has_add_permission(self, request):
        """관리자 페이지에서 좋아요 추가 불가"""
        return False


# ===================================================================
# 관리자 페이지 커스터마이징
# ===================================================================

# 관리자 페이지 제목 변경
admin.site.site_header = '포트폴리오 관리'
admin.site.site_title = '포트폴리오 관리'
admin.site.index_title = '데이터 관리'
