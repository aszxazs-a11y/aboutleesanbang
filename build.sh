#!/usr/bin/env bash
# ===================================================================
# build.sh - Render 배포 빌드 스크립트
# ===================================================================
#
# 이 파일은 Render에서 배포할 때 자동으로 실행됩니다.
# 필요한 패키지 설치, 데이터베이스 마이그레이션, 정적 파일 수집을 수행합니다.
#
# [실행 순서]
# 1. pip 업그레이드
# 2. requirements.txt의 패키지들 설치
# 3. 정적 파일 수집 (CSS, JS 등)
# 4. 데이터베이스 마이그레이션
# ===================================================================

set -o errexit  # 오류 발생 시 스크립트 중단

# pip 업그레이드
pip install --upgrade pip

# 의존성 설치
pip install -r requirements.txt

# 정적 파일 수집
python manage.py collectstatic --no-input

# 데이터베이스 마이그레이션
python manage.py migrate
