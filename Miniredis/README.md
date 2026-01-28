# Mini Redis

CLI 기반 In-Memory Key-Value 저장소 - Redis 핵심 기능 직접 구현 프로젝트

## 📋 프로젝트 개요

이 프로젝트는 Redis의 핵심 기능을 직접 구현하며 자료구조의 내부 동작 원리를 학습하기 위한 교육용 프로젝트입니다.

### 학습 목표

- **해시맵**: 해시 함수와 충돌 해결 방식(체이닝) 이해
- **이중 연결 리스트**: O(1) 삽입/삭제/이동 연산 구현
- **LRU 캐시**: 이중 연결 리스트 + 해시맵 조합으로 O(1) 추적
- **힙**: TTL 만료 시간 관리에 최소 힙 활용
- **메모리 관리**: LRU 정책으로 데이터 자동 제거

## 🗂️ 프로젝트 구조

```
mini-redis/
├── data_structures/
│   ├── __init__.py
│   ├── doubly_linked_list.py  # 이중 연결 리스트
│   ├── hash_map.py            # 체이닝 방식 해시맵
│   └── heap.py                # 최소 힙
├── redis_core.py              # Mini Redis 핵심 로직
├── cli.py                     # CLI 인터페이스
├── main.py                    # 진입점
└── README.md
```

## 🚀 실행 방법

```bash
cd mini-redis
python main.py
```

## 📖 사용 가능한 명령어

### String 타입 기본 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `SET key value` | 키에 값 저장 | `SET user:1 "Alice"` |
| `GET key` | 키의 값 조회 | `GET user:1` |
| `DEL key` | 키 삭제 | `DEL user:1` |
| `EXISTS key` | 키 존재 여부 확인 | `EXISTS user:1` |
| `DBSIZE` | 전체 키 개수 | `DBSIZE` |

### 메모리 관리 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `CONFIG SET maxmemory <bytes>` | 최대 메모리 제한 설정 | `CONFIG SET maxmemory 100` |
| `CONFIG GET maxmemory` | 메모리 제한 조회 | `CONFIG GET maxmemory` |
| `INFO memory` | 메모리 사용량 정보 | `INFO memory` |

### TTL 관리 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `EXPIRE key seconds` | 만료 시간 설정 | `EXPIRE user:1 60` |
| `TTL key` | 남은 만료 시간 조회 | `TTL user:1` |

### 기타 명령어

| 명령어 | 설명 |
|--------|------|
| `KEYS *` | 모든 키 목록 출력 |
| `HELP` | 도움말 출력 |
| `EXIT` / `QUIT` | 프로그램 종료 |

## 💡 실행 예시

```bash
mini-redis> CONFIG SET maxmemory 100
OK
mini-redis> SET user:1 "Alice"
OK
mini-redis> SET user:2 "Bob"
OK
mini-redis> SET user:3 "Charlie"
OK
mini-redis> SET user:4 "David"
OK
# 메모리 100 바이트 초과로 가장 오래된 키(user:1) 자동 제거
mini-redis> GET user:1
(nil)
mini-redis> GET user:2
"Bob"
mini-redis> INFO memory
used_memory:85
maxmemory:100
evicted_keys:1
mini-redis> EXPIRE user:2 10
(integer) 1
mini-redis> TTL user:2
(integer) 8
mini-redis> exit
Bye!
```

## 🔧 기술 상세

### 1. 이중 연결 리스트 (Doubly Linked List)

LRU 캐시 추적에 사용됩니다.

- **노드 구조**: `prev`, `next`, `data` 필드
- **더미 노드**: head/tail 더미 노드로 경계 조건 단순화
- **시간 복잡도**: 모든 연산 O(1)

```
Head(더미) <-> Node1 <-> Node2 <-> ... <-> Tail(더미)
   ^                                          ^
   |                                          |
 최근 접근                                  오래된 접근
```

### 2. 해시맵 (HashMap) - 체이닝 방식

키-값 저장에 사용됩니다.

- **해시 함수**: 다항식 롤링 해시 (prime=31)
- **충돌 해결**: 체이닝 (각 버킷에 연결 리스트)
- **리사이징**: 로드 팩터 > 0.75 시 버킷 2배 확장

```
Bucket[0] -> [Entry] -> [Entry] -> None
Bucket[1] -> [Entry] -> None
Bucket[2] -> None
...
```

### 3. 최소 힙 (Min Heap)

TTL 만료 시간 관리에 사용됩니다.

- **구조**: 배열 기반 완전 이진 트리
- **저장 형식**: (만료시간, 키) 튜플
- **용도**: 가장 빨리 만료되는 키를 O(1)로 확인

```
        (10, "key1")         <- 루트 (가장 빠른 만료)
       /            \
  (20, "key2")    (30, "key3")
```

### 4. LRU 추적 시스템

이중 연결 리스트 + 해시맵 조합으로 O(1) LRU 추적:

1. **SET/GET 실행 시**: 해당 키의 노드를 리스트 맨 앞으로 이동
2. **메모리 초과 시**: 리스트 맨 뒤(가장 오래된) 키 제거

```
HashMap: key -> Entry(key, value, lru_node)
                                    |
                                    v
LRU List: Head <-> [key3] <-> [key1] <-> [key2] <-> Tail
                    ^                       ^
                  최근                    오래됨
```

## ⚠️ 제약 사항

- Python 내장 `list`, `dict`, `set`, `collections` 사용 금지
- 네트워크 통신 미구현 (CLI만 지원)
- 데이터 영속성 미구현 (메모리에만 저장)
- 복잡한 Redis 자료형(List, Set, Sorted Set) 미구현

## 📚 학습 키워드

- 해시 함수 (Hash Function)
- 충돌 해결 - 체이닝 (Chaining)
- 로드 팩터 (Load Factor)
- 이중 연결 리스트 (Doubly Linked List)
- LRU 캐시 (Least Recently Used Cache)
- 완전 이진 트리 (Complete Binary Tree)
- 힙 (Heap)
- 시간 복잡도 분석

## 📝 라이선스

이 프로젝트는 학습 목적으로 제작되었습니다.
