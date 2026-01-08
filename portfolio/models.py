"""
===================================================================
portfolio/models.py - 데이터베이스 모델 정의 파일
===================================================================

이 파일은 데이터베이스의 테이블 구조를 정의합니다.
각 클래스가 하나의 테이블이 되고, 클래스의 속성이 테이블의 열(컬럼)이 됩니다.

[모델 목록]
1. SiteSettings : 사이트 전역 설정 (히어로 제목, 설명, 소개글)
2. Profile      : 프로필 정보 (이름, 소개, 이메일, 사진)
3. SocialLink   : SNS 링크 (플랫폼명, URL, 순서)
4. Category     : 작업 카테고리 (이름, 순서)
5. Work         : 작업/프로젝트 (제목, 설명, 썸네일, 외부링크, 카테고리)
6. WorkImage    : 작업 이미지 (작업에 여러 이미지 첨부)
7. Comment      : 댓글 (닉네임, 비밀번호, 내용)
8. Like         : 좋아요 (작업별 좋아요 수 집계용)

[모델 관계]
- Category → Work (1:N) : 하나의 카테고리에 여러 작업
- Work → WorkImage (1:N) : 하나의 작업에 여러 이미지
- Work → Comment (1:N) : 하나의 작업에 여러 댓글
- Work → Like (1:N) : 하나의 작업에 여러 좋아요
===================================================================
"""

from django.db import models


class SiteSettings(models.Model):
    """
    사이트 전역 설정 모델

    홈페이지의 히어로 섹션에 표시될 제목, 설명, 간략 소개를 저장합니다.
    이 모델은 하나의 레코드만 사용합니다 (싱글톤 패턴).

    [필드 설명]
    - hero_title: 히어로 섹션의 메인 제목
    - hero_description: 히어로 섹션의 설명 텍스트
    - short_intro: 홈페이지에 표시될 간략한 소개글
    """
    hero_title = models.CharField(
        max_length=200,
        verbose_name='히어로 제목',
        help_text='홈페이지 상단에 크게 표시될 제목입니다.'
    )
    hero_description = models.TextField(
        verbose_name='히어로 설명',
        help_text='히어로 제목 아래에 표시될 설명글입니다.'
    )
    short_intro = models.TextField(
        verbose_name='간략 소개',
        help_text='홈페이지에 표시될 짧은 소개글입니다.'
    )

    class Meta:
        # 관리자 페이지에서 표시될 이름
        verbose_name = '사이트 설정'
        verbose_name_plural = '사이트 설정'

    def __str__(self):
        """관리자 페이지에서 객체를 표시할 때 사용"""
        return '사이트 설정'


class Profile(models.Model):
    """
    프로필 정보 모델

    소개 페이지에 표시될 개인 정보를 저장합니다.
    이 모델도 하나의 레코드만 사용합니다.

    [필드 설명]
    - name: 표시할 이름
    - bio: 자기소개 글
    - email: 연락받을 이메일 주소
    - profile_image: 프로필 사진
    """
    name = models.CharField(
        max_length=100,
        verbose_name='이름',
        help_text='소개 페이지에 표시될 이름입니다.'
    )
    bio = models.TextField(
        verbose_name='자기소개',
        help_text='자신에 대한 소개글입니다.'
    )
    email = models.EmailField(
        verbose_name='이메일',
        help_text='연락받을 이메일 주소입니다.'
    )
    profile_image = models.ImageField(
        upload_to='profile/',
        verbose_name='프로필 사진',
        help_text='소개 페이지에 표시될 프로필 사진입니다.',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = '프로필'
        verbose_name_plural = '프로필'

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    """
    SNS 링크 모델

    소개 페이지에 표시될 소셜 미디어 링크를 저장합니다.
    여러 개의 SNS 링크를 추가할 수 있습니다.

    [필드 설명]
    - platform: SNS 플랫폼 이름 (예: Instagram, Twitter, GitHub)
    - url: 해당 SNS 프로필 주소
    - order: 표시 순서 (숫자가 작을수록 먼저 표시)
    """
    platform = models.CharField(
        max_length=50,
        verbose_name='플랫폼',
        help_text='SNS 이름입니다. (예: Instagram, Twitter, GitHub)'
    )
    url = models.URLField(
        verbose_name='URL',
        help_text='SNS 프로필 주소입니다.'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='순서',
        help_text='표시 순서입니다. 숫자가 작을수록 먼저 표시됩니다.'
    )

    class Meta:
        verbose_name = 'SNS 링크'
        verbose_name_plural = 'SNS 링크'
        ordering = ['order']  # order 필드 기준으로 정렬

    def __str__(self):
        return self.platform


class Category(models.Model):
    """
    작업 카테고리 모델

    작업물을 분류하는 카테고리를 저장합니다.
    예: 웹 디자인, 일러스트, 사진 등

    [필드 설명]
    - name: 카테고리 이름
    - order: 표시 순서
    """
    name = models.CharField(
        max_length=50,
        verbose_name='카테고리명',
        help_text='카테고리 이름입니다. (예: 웹 디자인, 일러스트)'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='순서',
        help_text='표시 순서입니다.'
    )

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'
        ordering = ['order']

    def __str__(self):
        return self.name


class Work(models.Model):
    """
    작업/프로젝트 모델

    포트폴리오의 핵심인 작업물 정보를 저장합니다.
    각 작업은 하나의 카테고리에 속합니다.

    [필드 설명]
    - title: 작업 제목
    - description: 작업에 대한 상세 설명
    - thumbnail: 작업 목록에 표시될 대표 이미지
    - external_link: 외부 링크 (선택사항)
    - category: 이 작업이 속한 카테고리 (외래키)
    - created_at: 작업 등록 날짜

    [관계]
    - Category와 N:1 관계 (여러 작업이 하나의 카테고리에 속함)
    - WorkImage와 1:N 관계 (하나의 작업에 여러 이미지)
    - Comment와 1:N 관계 (하나의 작업에 여러 댓글)
    - Like와 1:N 관계 (하나의 작업에 여러 좋아요)
    """
    title = models.CharField(
        max_length=200,
        verbose_name='제목',
        help_text='작업물의 제목입니다.'
    )
    description = models.TextField(
        verbose_name='설명',
        help_text='작업물에 대한 상세 설명입니다.'
    )
    thumbnail = models.ImageField(
        upload_to='works/thumbnails/',
        verbose_name='썸네일',
        help_text='작업 목록에 표시될 대표 이미지입니다.'
    )
    external_link = models.URLField(
        blank=True,
        null=True,
        verbose_name='외부 링크',
        help_text='작업물과 관련된 외부 사이트 링크입니다. (선택사항)'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='works',
        verbose_name='카테고리',
        help_text='이 작업물의 카테고리를 선택하세요.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='등록일',
        help_text='작업물이 등록된 날짜입니다. 자동으로 설정됩니다.'
    )

    class Meta:
        verbose_name = '작업'
        verbose_name_plural = '작업'
        ordering = ['-created_at']  # 최신순 정렬

    def __str__(self):
        return self.title

    def like_count(self):
        """좋아요 수를 반환하는 메서드"""
        return self.likes.count()


class WorkImage(models.Model):
    """
    작업 이미지 모델

    하나의 작업에 여러 이미지를 첨부할 수 있도록 합니다.
    상세 페이지의 이미지 갤러리에 사용됩니다.

    [필드 설명]
    - work: 이 이미지가 속한 작업 (외래키)
    - image: 이미지 파일
    - order: 이미지 표시 순서

    [관계]
    - Work와 N:1 관계 (여러 이미지가 하나의 작업에 속함)
    """
    work = models.ForeignKey(
        Work,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='작업',
        help_text='이 이미지가 속한 작업입니다.'
    )
    image = models.ImageField(
        upload_to='works/images/',
        verbose_name='이미지',
        help_text='작업 상세 페이지에 표시될 이미지입니다.'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='순서',
        help_text='이미지 표시 순서입니다.'
    )

    class Meta:
        verbose_name = '작업 이미지'
        verbose_name_plural = '작업 이미지'
        ordering = ['order']

    def __str__(self):
        return f'{self.work.title} - 이미지 {self.order}'


class Comment(models.Model):
    """
    댓글 모델

    작업에 달린 댓글을 저장합니다.
    댓글 작성 시 닉네임과 비밀번호를 입력받아,
    비밀번호로 본인 확인 후 삭제할 수 있습니다.

    [필드 설명]
    - work: 댓글이 달린 작업 (외래키)
    - author_name: 댓글 작성자 닉네임
    - password: 댓글 삭제용 비밀번호
    - content: 댓글 내용
    - created_at: 댓글 작성 시간

    [관계]
    - Work와 N:1 관계 (여러 댓글이 하나의 작업에 속함)
    """
    work = models.ForeignKey(
        Work,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='작업',
        help_text='이 댓글이 달린 작업입니다.'
    )
    author_name = models.CharField(
        max_length=50,
        verbose_name='닉네임',
        help_text='댓글 작성자의 닉네임입니다.'
    )
    password = models.CharField(
        max_length=128,
        verbose_name='비밀번호',
        help_text='댓글 삭제 시 필요한 비밀번호입니다.'
    )
    content = models.TextField(
        verbose_name='내용',
        help_text='댓글 내용입니다.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='작성일',
        help_text='댓글 작성 시간입니다. 자동으로 설정됩니다.'
    )

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
        ordering = ['-created_at']  # 최신순 정렬

    def __str__(self):
        return f'{self.author_name}의 댓글 - {self.work.title}'


class Like(models.Model):
    """
    좋아요 모델

    작업에 대한 좋아요를 저장합니다.
    좋아요 버튼을 누를 때마다 새로운 레코드가 생성됩니다.

    [필드 설명]
    - work: 좋아요가 눌린 작업 (외래키)
    - created_at: 좋아요 시간

    [관계]
    - Work와 N:1 관계 (여러 좋아요가 하나의 작업에 속함)
    """
    work = models.ForeignKey(
        Work,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='작업',
        help_text='좋아요가 눌린 작업입니다.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='좋아요 시간',
        help_text='좋아요를 누른 시간입니다. 자동으로 설정됩니다.'
    )

    class Meta:
        verbose_name = '좋아요'
        verbose_name_plural = '좋아요'

    def __str__(self):
        return f'{self.work.title}의 좋아요'
