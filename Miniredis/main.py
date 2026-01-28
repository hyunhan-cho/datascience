#!/usr/bin/env python3
"""
Mini Redis - CLI 기반 In-Memory Key-Value 저장소

이 프로그램은 Redis의 핵심 기능을 직접 구현한 학습용 프로젝트입니다.

주요 기능:
- String 타입 기본 명령어 (SET, GET, DEL, EXISTS, DBSIZE)
- 메모리 관리 (CONFIG SET maxmemory, INFO memory)
- TTL 관리 (EXPIRE, TTL)
- LRU 추적 시스템

실행 방법:
    python main.py

사용 예시:
    mini-redis> SET user:1 "Alice"
    OK
    mini-redis> GET user:1
    "Alice"
    mini-redis> EXPIRE user:1 60
    (integer) 1
    mini-redis> TTL user:1
    (integer) 58
"""

import sys
import os

# 현재 디렉토리를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli import CLI


def main():
    """
    Mini Redis 메인 진입점
    
    CLI 인터페이스를 초기화하고 REPL 루프를 실행합니다.
    """
    try:
        cli = CLI()
        cli.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
