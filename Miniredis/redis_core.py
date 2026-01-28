"""
Mini Redis 핵심 로직 구현

이 모듈은 Redis의 핵심 기능을 구현합니다:
- String 타입 기본 명령어 (SET, GET, DEL, EXISTS, DBSIZE)
- 메모리 관리 (CONFIG SET maxmemory, INFO memory)
- TTL 관리 (EXPIRE, TTL)
- LRU 추적 시스템
"""

import time
import sys
import os

# 현재 디렉토리를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_structures.doubly_linked_list import DoublyLinkedList
from data_structures.hash_map import HashMap
from data_structures.heap import MinHeap


class MiniRedis:
    """
    Mini Redis 메인 클래스
    
    LRU 캐시와 TTL 관리 기능을 갖춘 In-Memory Key-Value 저장소입니다.
    
    Attributes:
        _store: 키-값 저장을 위한 해시맵
        _lru_list: LRU 추적을 위한 이중 연결 리스트
        _ttl_heap: TTL 관리를 위한 최소 힙
        _ttl_map: 키별 만료 시간 저장 해시맵
        _maxmemory: 최대 메모리 제한 (바이트)
        _evicted_keys: 제거된 키 개수
    """
    
    def __init__(self):
        """
        Mini Redis 초기화
        """
        # 키-값 저장소 (HashMap)
        # key -> HashMapEntry(key, value, lru_node)
        self._store = HashMap()
        
        # LRU 추적용 이중 연결 리스트
        # head 쪽: 최근 접근, tail 쪽: 오래된 접근
        self._lru_list = DoublyLinkedList()
        
        # TTL 관리용 최소 힙
        # (만료시간, key) 튜플 저장
        self._ttl_heap = MinHeap()
        
        # 키별 만료 시간 저장
        # key -> expire_timestamp
        self._ttl_map = HashMap()
        
        # 메모리 제한 (0 = 무제한)
        self._maxmemory = 0
        
        # 제거된 키 개수
        self._evicted_keys = 0
    
    # ==================== String 타입 기본 명령어 ====================
    
    def set(self, key, value):
        """
        SET key value - 키에 값 저장
        
        1. 메모리 초과 시 LRU 정책으로 가장 오래된 키 제거
        2. 키가 이미 존재하면 값 업데이트
        3. LRU 리스트에서 해당 키를 최신으로 갱신
        
        Args:
            key: 저장할 키
            value: 저장할 값
            
        Returns:
            str: "OK"
        """
        # 만료된 키 정리
        self._cleanup_expired()
        
        # 기존 키 존재 여부 확인
        existing_entry = self._store.get(key)
        
        if existing_entry:
            # 기존 키 업데이트
            existing_entry.value = value
            # LRU 순서 갱신
            if existing_entry.lru_node:
                self._lru_list.move_to_front(existing_entry.lru_node)
        else:
            # 메모리 초과 확인 및 LRU 제거
            self._enforce_memory_limit(key, value)
            
            # 새 키 추가
            # LRU 리스트에 추가 (맨 앞 = 최근)
            lru_node = self._lru_list.insert_front(key)
            
            # 해시맵에 저장
            self._store.put(key, value, lru_node)
        
        return "OK"
    
    def get(self, key):
        """
        GET key - 키의 값 조회
        
        1. TTL 만료 확인 (만료되었으면 삭제)
        2. LRU 순서 갱신
        
        Args:
            key: 조회할 키
            
        Returns:
            str: 값 또는 None (키가 없거나 만료됨)
        """
        # 만료된 키 정리
        self._cleanup_expired()
        
        # TTL 확인
        if self._is_expired(key):
            self._delete_key_internal(key)
            return None
        
        entry = self._store.get(key)
        if entry is None:
            return None
        
        # LRU 순서 갱신 (최신으로)
        if entry.lru_node:
            self._lru_list.move_to_front(entry.lru_node)
        
        return entry.value
    
    def delete(self, key):
        """
        DEL key - 키 삭제
        
        Args:
            key: 삭제할 키
            
        Returns:
            int: 삭제된 키 개수 (0 또는 1)
        """
        return self._delete_key_internal(key)
    
    def exists(self, key):
        """
        EXISTS key - 키 존재 여부 확인
        
        Args:
            key: 확인할 키
            
        Returns:
            int: 1 (존재) 또는 0 (없음)
        """
        # 만료 확인
        if self._is_expired(key):
            self._delete_key_internal(key)
            return 0
        
        return 1 if self._store.contains(key) else 0
    
    def dbsize(self):
        """
        DBSIZE - 전체 키 개수 반환
        
        Returns:
            int: 키 개수
        """
        # 만료된 키 정리
        self._cleanup_expired()
        return self._store.size()
    
    # ==================== 메모리 관리 명령어 ====================
    
    def config_set_maxmemory(self, bytes_limit):
        """
        CONFIG SET maxmemory - 최대 메모리 제한 설정
        
        Args:
            bytes_limit: 바이트 단위 메모리 제한 (0 = 무제한)
            
        Returns:
            str: "OK"
        """
        self._maxmemory = int(bytes_limit)
        
        # 현재 메모리가 제한을 초과하면 제거
        while self._maxmemory > 0 and self._get_memory_usage() > self._maxmemory:
            if not self._evict_lru():
                break
        
        return "OK"
    
    def info_memory(self):
        """
        INFO memory - 메모리 정보 반환
        
        Returns:
            dict: 메모리 사용 정보
        """
        return {
            'used_memory': self._get_memory_usage(),
            'maxmemory': self._maxmemory,
            'evicted_keys': self._evicted_keys
        }
    
    # ==================== TTL 관리 명령어 ====================
    
    def expire(self, key, seconds):
        """
        EXPIRE key seconds - 키의 만료 시간 설정
        
        Args:
            key: 대상 키
            seconds: 만료 시간 (초)
            
        Returns:
            int: 1 (성공) 또는 0 (키 없음)
        """
        if not self._store.contains(key):
            return 0
        
        expire_time = time.time() + int(seconds)
        
        # TTL 맵에 저장
        self._ttl_map.put(key, expire_time)
        
        # TTL 힙에 추가
        self._ttl_heap.push((expire_time, key))
        
        return 1
    
    def ttl(self, key):
        """
        TTL key - 키의 남은 만료 시간 조회
        
        Args:
            key: 대상 키
            
        Returns:
            int: 남은 시간(초), -1(만료 없음), -2(키 없음)
        """
        # 키 존재 확인
        if not self._store.contains(key):
            return -2
        
        # TTL 확인
        ttl_entry = self._ttl_map.get(key)
        if ttl_entry is None:
            return -1  # 만료 시간 설정 안됨
        
        remaining = int(ttl_entry.value - time.time())
        
        if remaining <= 0:
            # 만료됨
            self._delete_key_internal(key)
            return -2
        
        return remaining
    
    # ==================== 내부 메서드 ====================
    
    def _delete_key_internal(self, key):
        """
        내부 키 삭제 로직
        
        해시맵, LRU 리스트, TTL 맵에서 모두 제거합니다.
        
        Args:
            key: 삭제할 키
            
        Returns:
            int: 삭제된 키 개수
        """
        entry = self._store.get(key)
        if entry is None:
            return 0
        
        # LRU 리스트에서 제거
        if entry.lru_node:
            self._lru_list.remove_node(entry.lru_node)
        
        # 해시맵에서 제거
        self._store.remove(key)
        
        # TTL 맵에서 제거
        self._ttl_map.remove(key)
        
        return 1
    
    def _is_expired(self, key):
        """
        키의 만료 여부 확인
        
        Args:
            key: 확인할 키
            
        Returns:
            bool: 만료되었으면 True
        """
        ttl_entry = self._ttl_map.get(key)
        if ttl_entry is None:
            return False
        
        return time.time() > ttl_entry.value
    
    def _cleanup_expired(self):
        """
        만료된 키 정리 (Lazy Expiration)
        
        TTL 힙에서 만료된 키들을 확인하고 삭제합니다.
        """
        current_time = time.time()
        
        while not self._ttl_heap.is_empty():
            top = self._ttl_heap.peek()
            if top is None:
                break
            
            expire_time, key = top
            
            if expire_time > current_time:
                # 아직 만료 안됨
                break
            
            # 힙에서 제거
            self._ttl_heap.pop()
            
            # 실제로 이 키가 아직 유효한지 확인
            # (이미 삭제되었거나 TTL이 갱신되었을 수 있음)
            ttl_entry = self._ttl_map.get(key)
            if ttl_entry and ttl_entry.value <= current_time:
                self._delete_key_internal(key)
    
    def _get_memory_usage(self):
        """
        현재 메모리 사용량 계산
        
        간소화된 계산: 각 키-값 쌍의 문자열 길이 합
        
        Returns:
            int: 예상 메모리 사용량 (바이트)
        """
        total = 0
        for entry in self._store.entries():
            # 키와 값의 문자열 길이를 바이트로 계산
            total += len(str(entry.key))
            total += len(str(entry.value))
        return total
    
    def _enforce_memory_limit(self, new_key, new_value):
        """
        메모리 제한 적용
        
        새 키-값을 추가해도 메모리 제한을 초과하지 않도록
        필요한 만큼 LRU 정책으로 오래된 키를 제거합니다.
        
        Args:
            new_key: 추가할 키
            new_value: 추가할 값
        """
        if self._maxmemory == 0:
            return  # 무제한
        
        new_size = len(str(new_key)) + len(str(new_value))
        
        while self._get_memory_usage() + new_size > self._maxmemory:
            if not self._evict_lru():
                break  # 더 이상 제거할 키 없음
    
    def _evict_lru(self):
        """
        LRU 정책으로 가장 오래된 키 제거
        
        Returns:
            bool: 제거 성공 여부
        """
        # LRU 리스트에서 가장 오래된 키 (tail 쪽)
        oldest_node = self._lru_list.get_back_node()
        if oldest_node is None:
            return False
        
        key = oldest_node.data
        self._delete_key_internal(key)
        self._evicted_keys += 1
        
        return True
