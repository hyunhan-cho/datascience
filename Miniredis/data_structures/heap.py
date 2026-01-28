"""
최소 힙 (Min Heap) 구현 - 배열 기반

이 모듈은 TTL 만료 시간 관리를 위한 최소 힙을 구현합니다.
완전 이진 트리를 배열로 표현하며, 가장 작은 값(가장 빠른 만료 시간)이 항상 루트에 위치합니다.
"""


class MinHeap:
    """
    최소 힙 클래스 (배열 기반)
    
    TTL 만료 시간 관리에 사용됩니다.
    튜플 (expire_time, key) 형태로 저장하여 만료 시간 기준 정렬합니다.
    
    Attributes:
        _data: 힙 데이터를 저장하는 배열
        _size: 현재 힙에 저장된 요소 개수
        _capacity: 배열의 현재 용량
    """
    
    INITIAL_CAPACITY = 16
    
    def __init__(self):
        """
        최소 힙 초기화
        """
        self._capacity = self.INITIAL_CAPACITY
        self._data = [None] * self._capacity
        self._size = 0
    
    def _parent(self, index):
        """
        부모 노드 인덱스 계산
        
        Args:
            index: 현재 노드 인덱스
            
        Returns:
            int: 부모 노드 인덱스
        """
        return (index - 1) // 2
    
    def _left_child(self, index):
        """
        왼쪽 자식 노드 인덱스 계산
        
        Args:
            index: 현재 노드 인덱스
            
        Returns:
            int: 왼쪽 자식 노드 인덱스
        """
        return 2 * index + 1
    
    def _right_child(self, index):
        """
        오른쪽 자식 노드 인덱스 계산
        
        Args:
            index: 현재 노드 인덱스
            
        Returns:
            int: 오른쪽 자식 노드 인덱스
        """
        return 2 * index + 2
    
    def _swap(self, i, j):
        """
        두 인덱스의 요소 교환
        
        Args:
            i: 첫 번째 인덱스
            j: 두 번째 인덱스
        """
        self._data[i], self._data[j] = self._data[j], self._data[i]
    
    def _resize(self):
        """
        배열 용량 2배 확장
        """
        self._capacity *= 2
        new_data = [None] * self._capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
    
    def _heapify_up(self, index):
        """
        상향 힙화 (Bubble Up)
        
        삽입된 노드를 올바른 위치로 올립니다.
        시간 복잡도: O(log n)
        
        Args:
            index: 시작 인덱스
        """
        while index > 0:
            parent_idx = self._parent(index)
            # 부모보다 현재 노드가 작으면 교환
            if self._compare(self._data[index], self._data[parent_idx]) < 0:
                self._swap(index, parent_idx)
                index = parent_idx
            else:
                break
    
    def _heapify_down(self, index):
        """
        하향 힙화 (Bubble Down)
        
        제거된 위치의 노드를 올바른 위치로 내립니다.
        시간 복잡도: O(log n)
        
        Args:
            index: 시작 인덱스
        """
        while True:
            smallest = index
            left = self._left_child(index)
            right = self._right_child(index)
            
            # 왼쪽 자식과 비교
            if left < self._size and self._compare(self._data[left], self._data[smallest]) < 0:
                smallest = left
            
            # 오른쪽 자식과 비교
            if right < self._size and self._compare(self._data[right], self._data[smallest]) < 0:
                smallest = right
            
            # 현재 노드가 가장 작으면 종료
            if smallest == index:
                break
            
            self._swap(index, smallest)
            index = smallest
    
    def _compare(self, a, b):
        """
        두 요소 비교
        
        튜플의 경우 첫 번째 요소(만료 시간)를 기준으로 비교합니다.
        
        Args:
            a: 첫 번째 요소
            b: 두 번째 요소
            
        Returns:
            int: a < b이면 음수, a == b이면 0, a > b이면 양수
        """
        # 튜플인 경우 첫 번째 요소로 비교 (만료 시간)
        if isinstance(a, tuple) and isinstance(b, tuple):
            if a[0] < b[0]:
                return -1
            elif a[0] > b[0]:
                return 1
            else:
                return 0
        
        # 일반 값 비교
        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0
    
    def push(self, item):
        """
        힙에 요소 삽입
        
        시간 복잡도: O(log n)
        
        Args:
            item: 삽입할 요소 (보통 (expire_time, key) 튜플)
        """
        # 용량 확인 및 확장
        if self._size >= self._capacity:
            self._resize()
        
        # 마지막에 삽입 후 상향 힙화
        self._data[self._size] = item
        self._size += 1
        self._heapify_up(self._size - 1)
    
    def pop(self):
        """
        최소값 제거 및 반환
        
        시간 복잡도: O(log n)
        
        Returns:
            최소값, 힙이 비어있으면 None
        """
        if self._size == 0:
            return None
        
        # 루트 저장
        min_item = self._data[0]
        
        # 마지막 요소를 루트로 이동
        self._size -= 1
        if self._size > 0:
            self._data[0] = self._data[self._size]
            self._heapify_down(0)
        
        self._data[self._size] = None  # 참조 해제
        
        return min_item
    
    def peek(self):
        """
        최소값 조회 (제거하지 않음)
        
        시간 복잡도: O(1)
        
        Returns:
            최소값, 힙이 비어있으면 None
        """
        if self._size == 0:
            return None
        return self._data[0]
    
    def size(self):
        """
        힙의 요소 개수 반환
        
        Returns:
            int: 요소 개수
        """
        return self._size
    
    def is_empty(self):
        """
        힙이 비어있는지 확인
        
        Returns:
            bool: 비어있으면 True
        """
        return self._size == 0
    
    def __len__(self):
        """len() 함수 지원"""
        return self._size
