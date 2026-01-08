/*
===================================================================
static/js/main.js - 메인 JavaScript 파일
===================================================================

이 파일은 웹사이트의 모든 인터랙티브 기능을 담당합니다.

[기능 목록]
1. 커스텀 커서 : 마우스를 따라다니는 커스텀 커서
2. 다크/라이트 모드 토글 : 테마 전환 기능
3. 페이지 로딩 애니메이션 : 페이지 로드 시 로더 숨김
4. 스크롤 애니메이션 : 요소가 뷰포트에 들어오면 애니메이션
5. 네비게이션 스크롤 효과 : 스크롤 시 헤더 스타일 변경
6. 모바일 메뉴 토글 : 햄버거 메뉴 열기/닫기
7. 메시지 자동 닫기 : Django 메시지 자동 숨김

[사용된 기술]
- DOM 조작 : document.querySelector, addEventListener
- CSS 클래스 토글 : classList.add, remove, toggle
- 로컬 스토리지 : 테마 설정 저장
- Intersection Observer : 스크롤 애니메이션
===================================================================
*/


/* ===================================================================
   1. 커스텀 커서
   =================================================================== */

/**
 * 커스텀 커서 기능
 *
 * 마우스 포인터를 커스텀 디자인으로 대체합니다.
 * - cursor: 작은 원 (마우스 위치에 정확히 위치)
 * - cursor-follower: 큰 원 (약간의 딜레이를 두고 따라옴)
 */

// 커서 요소 선택
const cursor = document.querySelector('.cursor');
const cursorFollower = document.querySelector('.cursor-follower');

// 마우스 위치 저장 변수
let mouseX = 0;
let mouseY = 0;
let followerX = 0;
let followerY = 0;

// 마우스 이동 이벤트 리스너
document.addEventListener('mousemove', (e) => {
    // 현재 마우스 위치 저장
    mouseX = e.clientX;
    mouseY = e.clientY;

    // 작은 커서는 즉시 이동
    if (cursor) {
        cursor.style.left = mouseX + 'px';
        cursor.style.top = mouseY + 'px';
    }
});

/**
 * 커서 팔로워 애니메이션
 *
 * requestAnimationFrame을 사용하여 부드러운 애니메이션 구현
 * 팔로워가 마우스 위치를 약간의 딜레이를 두고 따라갑니다.
 */
function animateCursor() {
    // 현재 위치에서 목표 위치까지 10%씩 이동 (부드러운 움직임)
    followerX += (mouseX - followerX) * 0.1;
    followerY += (mouseY - followerY) * 0.1;

    if (cursorFollower) {
        cursorFollower.style.left = followerX + 'px';
        cursorFollower.style.top = followerY + 'px';
    }

    // 다음 프레임에서 다시 실행
    requestAnimationFrame(animateCursor);
}

// 커서 애니메이션 시작
animateCursor();

/**
 * 호버 효과
 *
 * 링크나 버튼에 마우스를 올리면 커서가 확대됩니다.
 */
const hoverElements = document.querySelectorAll('a, button, .work-card');

hoverElements.forEach(element => {
    element.addEventListener('mouseenter', () => {
        if (cursor) cursor.classList.add('hover');
        if (cursorFollower) cursorFollower.classList.add('hover');
    });

    element.addEventListener('mouseleave', () => {
        if (cursor) cursor.classList.remove('hover');
        if (cursorFollower) cursorFollower.classList.remove('hover');
    });
});


/* ===================================================================
   2. 다크/라이트 모드 토글
   =================================================================== */

/**
 * 테마 토글 기능
 *
 * - 버튼 클릭 시 다크/라이트 모드 전환
 * - 설정을 로컬 스토리지에 저장하여 재방문 시 유지
 * - 시스템 테마 설정을 기본값으로 사용
 */

const themeToggle = document.querySelector('.theme-toggle');
const html = document.documentElement;

// 저장된 테마 또는 시스템 테마 적용
function initializeTheme() {
    // 로컬 스토리지에서 저장된 테마 확인
    const savedTheme = localStorage.getItem('theme');

    if (savedTheme) {
        // 저장된 테마가 있으면 적용
        html.setAttribute('data-theme', savedTheme);
    } else {
        // 없으면 시스템 테마 확인
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        html.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    }
}

// 테마 토글 함수
function toggleTheme() {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    // 테마 변경
    html.setAttribute('data-theme', newTheme);

    // 로컬 스토리지에 저장
    localStorage.setItem('theme', newTheme);
}

// 초기 테마 설정
initializeTheme();

// 토글 버튼 클릭 이벤트
if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme);
}


/* ===================================================================
   3. 페이지 로딩 애니메이션
   =================================================================== */

/**
 * 페이지 로더
 *
 * 페이지가 완전히 로드되면 로더를 숨깁니다.
 */

const pageLoader = document.querySelector('.page-loader');

window.addEventListener('load', () => {
    // 약간의 딜레이 후 로더 숨김 (더 자연스러운 효과)
    setTimeout(() => {
        if (pageLoader) {
            pageLoader.classList.add('hidden');
        }
    }, 500);
});


/* ===================================================================
   4. 스크롤 애니메이션 (Intersection Observer)
   =================================================================== */

/**
 * 스크롤 시 요소 애니메이션
 *
 * Intersection Observer API를 사용하여
 * 요소가 뷰포트에 들어오면 애니메이션을 트리거합니다.
 *
 * [사용법]
 * HTML에서 data-animate 속성을 가진 요소에 자동 적용
 * 예: <div data-animate="fade">...</div>
 */

const animateElements = document.querySelectorAll('[data-animate]');

// Intersection Observer 생성
const animateObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        // 요소가 뷰포트에 들어오면
        if (entry.isIntersecting) {
            // animated 클래스 추가 (CSS에서 애니메이션 정의)
            entry.target.classList.add('animated');

            // 한 번 애니메이션 후 관찰 중단
            animateObserver.unobserve(entry.target);
        }
    });
}, {
    // 요소의 20%가 보이면 트리거
    threshold: 0.2,
    // 뷰포트 하단에서 50px 전에 트리거
    rootMargin: '0px 0px -50px 0px'
});

// 모든 애니메이션 요소 관찰 시작
animateElements.forEach(element => {
    animateObserver.observe(element);
});


/* ===================================================================
   5. 네비게이션 스크롤 효과
   =================================================================== */

/**
 * 스크롤 시 헤더 스타일 변경
 *
 * 페이지를 아래로 스크롤하면 헤더에 배경색과 그림자가 추가됩니다.
 */

const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    if (header) {
        // 스크롤 위치가 50px 이상이면 scrolled 클래스 추가
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
});


/* ===================================================================
   6. 모바일 메뉴 토글
   =================================================================== */

/**
 * 모바일 햄버거 메뉴
 *
 * 모바일에서 햄버거 아이콘 클릭 시 메뉴를 열고 닫습니다.
 */

const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
        // 토글 버튼과 메뉴에 active 클래스 토글
        navToggle.classList.toggle('active');
        navMenu.classList.toggle('active');

        // 메뉴가 열리면 스크롤 방지
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    });

    // 메뉴 링크 클릭 시 메뉴 닫기
    const navLinks = navMenu.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.style.overflow = '';
        });
    });
}


/* ===================================================================
   7. 메시지 자동 닫기
   =================================================================== */

/**
 * Django 메시지 자동 숨김
 *
 * 성공/에러 메시지를 5초 후에 자동으로 숨깁니다.
 * 닫기 버튼 클릭으로도 즉시 닫을 수 있습니다.
 */

const messages = document.querySelectorAll('.message');

messages.forEach(message => {
    // 5초 후 자동 숨김
    setTimeout(() => {
        message.style.opacity = '0';
        message.style.transform = 'translateX(100%)';

        // 애니메이션 후 DOM에서 제거
        setTimeout(() => {
            message.remove();
        }, 300);
    }, 5000);

    // 닫기 버튼 클릭 이벤트
    const closeBtn = message.querySelector('.message-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            setTimeout(() => {
                message.remove();
            }, 300);
        });
    }
});


/* ===================================================================
   8. 페이지 전환 효과 (선택적)
   =================================================================== */

/**
 * 페이지 전환 애니메이션
 *
 * 내부 링크 클릭 시 페이지 전환 효과를 보여줍니다.
 * 주석 처리되어 있으며, 필요시 활성화할 수 있습니다.
 */

/*
const pageTransition = document.querySelector('.page-transition');
const internalLinks = document.querySelectorAll('a[href^="/"]');

internalLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        // 새 탭에서 열리는 링크는 제외
        if (link.target === '_blank') return;

        e.preventDefault();
        const href = link.getAttribute('href');

        // 전환 애니메이션 시작
        if (pageTransition) {
            pageTransition.classList.add('active');
        }

        // 애니메이션 후 페이지 이동
        setTimeout(() => {
            window.location.href = href;
        }, 500);
    });
});
*/


/* ===================================================================
   9. 히어로 섹션 인터랙티브 효과 (선택적)
   =================================================================== */

/**
 * 히어로 배경 마우스 추적
 *
 * 마우스 위치에 따라 배경 도형이 약간씩 움직입니다.
 */

const heroShapes = document.querySelector('.hero-shapes');

if (heroShapes) {
    document.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 20;
        const y = (e.clientY / window.innerHeight - 0.5) * 20;

        heroShapes.style.transform = `translate(${x}px, ${y}px)`;
    });
}
