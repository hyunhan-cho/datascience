"""
해시맵 (HashMap) 구현 - 체이닝 방식

이 모듈은 체이닝 방식의 충돌 해결을 사용하는 해시맵을 구현합니다.
Python의 dict 사용 없이 직접 구현되었습니다.
"""

from data_structures.doubly_linked_list import DoublyLinkedList, Node


class HashMapEntry:
    """
    해시맵 엔트리 클래스
    
    Attributes:
        key: 키 값
        value: 저장된 값
        lru_node: LRU 리스트에서의 노드 참조 (옵션)
    """
    
    def __init__(self, key, value, lru_node=None):
        """
        엔트리 초기화
        
        Args:
            key: 키 값
            value: 저장할 값
            lru_node: LRU 리스트의 노드 참조
        """
        self.key = key
        self.value = value
        self.lru_node = lru_node


class HashMap:
    """
    체이닝 방식 해시맵 클래스
    
    충돌 해결: 체이닝 (각 버킷에 연결 리스트 사용)
    로드 팩터 0.75 초과 시 버킷 2배 확장
    
    Attributes:
        _capacity: 버킷 배열의 크기
        _size: 저장된 키-값 쌍의 개수
        _buckets: 버킷 배열 (각 버킷은 DoublyLinkedList)
        _load_factor_threshold: 리사이징 임계값
    """
    
    INITIAL_CAPACITY = 16
    LOAD_FACTOR_THRESHOLD = 0.75
    
    def __init__(self, capacity=None):
        """
        해시맵 초기화
        
        Args:
            capacity: 초기 버킷 크기 (기본값: 16)
        """
        self._capacity = capacity if capacity else self.INITIAL_CAPACITY
        self._size = 0
        self._buckets = self._create_buckets(self._capacity)
    
    def _create_buckets(self, capacity):
        """
        버킷 배열 생성
        
        Python list 대신 고정 크기 배열 시뮬레이션
        (실제로는 Python의 기본 배열 메커니즘 사용)
        
        Args:
            capacity: 버킷 개수
            
        Returns:
            list: 빈 DoublyLinkedList로 초기화된 버킷 배열
        """
        buckets = [None] * capacity
        for i in range(capacity):
            buckets[i] = DoublyLinkedList()
        return buckets
    
    def _hash(self, key):
        """
        해시 함수 - 키를 버킷 인덱스로 변환
        
        다항식 롤링 해시 방식 사용
        
        Args:
            key: 해시할 키 (문자열)
            
        Returns:
            int: 버킷 인덱스 (0 ~ capacity-1)
        """
        if key is None:
            return 0
        
        # 문자열을 해시값으로 변환 (다항식 롤링 해시)
        hash_value = 0
        prime = 31  # 소수 사용
        
        key_str = str(key)
        for char in key_str:
            hash_value = (hash_value * prime + ord(char)) & 0x7FFFFFFF
        
        return hash_value % self._capacity
    
    def put(self, key, value, lru_node=None):
        """
        키-값 쌍 저장
        
        이미 존재하는 키면 값을 업데이트합니다.
        시간 복잡도: 평균 O(1), 최악 O(n)
        
        Args:
            key: 키
            value: 값
            lru_node: LRU 리스트 노드 참조 (옵션)
            
        Returns:
            HashMapEntry: 저장/업데이트된 엔트리
        """
        # 로드 팩터 확인 및 리사이징
        if self._size / self._capacity > self.LOAD_FACTOR_THRESHOLD:
            self._resize()
        
        index = self._hash(key)
        bucket = self._buckets[index]
        
        # 이미 존재하는 키인지 확인
        current = bucket.head.next
        while current != bucket.tail:
            entry = current.data
            if entry.key == key:
                # 값 업데이트
                entry.value = value
                if lru_node is not None:
                    entry.lru_node = lru_node
                return entry
            current = current.next
        
        # 새 엔트리 추가
        new_entry = HashMapEntry(key, value, lru_node)
        bucket.insert_back(new_entry)
        self._size += 1
        
        return new_entry
    
    def get(self, key):
        """
        키로 값 조회
        
        시간 복잡도: 평균 O(1), 최악 O(n)
        
        Args:
            key: 조회할 키
            
        Returns:
            HashMapEntry: 찾은 엔트리, 없으면 None
        """
        index = self._hash(key)
        bucket = self._buckets[index]
        
        current = bucket.head.next
        while current != bucket.tail:
            entry = current.data
            if entry.key == key:
                return entry
            current = current.next
        
        return None
    
    def remove(self, key):
        """
        키-값 쌍 삭제
        
        시간 복잡도: 평균 O(1), 최악 O(n)
        
        Args:
            key: 삭제할 키
            
        Returns:
            HashMapEntry: 삭제된 엔트리, 없으면 None
        """
        index = self._hash(key)
        bucket = self._buckets[index]
        
        current = bucket.head.next
        while current != bucket.tail:
            entry = current.data
            if entry.key == key:
                bucket.remove_node(current)
                self._size -= 1
                return entry
            current = current.next
        
        return None
    
    def contains(self, key):
        """
        키 존재 여부 확인
        
        Args:
            key: 확인할 키
            
        Returns:
            bool: 존재하면 True
        """
        return self.get(key) is not None
    
    def keys(self):
        """
        모든 키 반환
        
        Returns:
            generator: 모든 키를 yield
        """
        for bucket in self._buckets:
            for entry in bucket:
                yield entry.key
    
    def values(self):
        """
        모든 값 반환
        
        Returns:
            generator: 모든 값을 yield
        """
        for bucket in self._buckets:
            for entry in bucket:
                yield entry.value
    
    def entries(self):
        """
        모든 엔트리 반환
        
        Returns:
            generator: 모든 엔트리를 yield
        """
        for bucket in self._buckets:
            for entry in bucket:
                yield entry
    
    def size(self):
        """
        저장된 키-값 쌍 개수 반환
        
        Returns:
            int: 개수
        """
        return self._size
    
    def _resize(self):
        """
        버킷 배열 2배 확장
        
        모든 엔트리를 새 버킷 배열로 재배치합니다.
        """
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = self._create_buckets(self._capacity)
        self._size = 0
        
        # 모든 엔트리 재삽입
        for bucket in old_buckets:
            for entry in bucket:
                self.put(entry.key, entry.value, entry.lru_node)
    
    def __len__(self):
        """len() 함수 지원"""
        return self._size
    
    def __contains__(self, key):
        """in 연산자 지원"""
        return self.contains(key)
