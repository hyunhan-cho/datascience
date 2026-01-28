"""
이중 연결 리스트 (Doubly Linked List) 구현

이 모듈은 LRU 캐시 추적을 위한 이중 연결 리스트를 구현합니다.
모든 삽입, 삭제, 이동 연산은 O(1) 시간 복잡도를 가집니다.
"""


class Node:
    """
    이중 연결 리스트의 노드 클래스
    
    Attributes:
        data: 노드에 저장된 데이터 (key, value 튜플)
        prev: 이전 노드에 대한 참조
        next: 다음 노드에 대한 참조
    """
    
    def __init__(self, data=None):
        """
        노드 초기화
        
        Args:
            data: 노드에 저장할 데이터 (기본값: None)
        """
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """
    이중 연결 리스트 클래스
    
    LRU 캐시 구현을 위해 head는 가장 최근에 접근한 항목,
    tail은 가장 오래된 항목을 가리킵니다.
    
    Attributes:
        head: 리스트의 첫 번째 노드 (더미 노드)
        tail: 리스트의 마지막 노드 (더미 노드)
        _size: 리스트에 저장된 실제 노드 개수
    """
    
    def __init__(self):
        """
        이중 연결 리스트 초기화
        
        더미 head와 tail 노드를 생성하여 경계 조건 처리를 단순화합니다.
        """
        # 더미 노드 생성 (경계 조건 처리 단순화)
        self.head = Node()  # 더미 head
        self.tail = Node()  # 더미 tail
        self.head.next = self.tail
        self.tail.prev = self.head
        self._size = 0
    
    def insert_front(self, data):
        """
        리스트의 맨 앞에 새 노드 삽입 (head 바로 뒤)
        
        시간 복잡도: O(1)
        
        Args:
            data: 삽입할 데이터
            
        Returns:
            Node: 새로 생성된 노드
        """
        new_node = Node(data)
        
        # head와 head.next 사이에 삽입
        new_node.next = self.head.next
        new_node.prev = self.head
        self.head.next.prev = new_node
        self.head.next = new_node
        
        self._size += 1
        return new_node
    
    def insert_back(self, data):
        """
        리스트의 맨 뒤에 새 노드 삽입 (tail 바로 앞)
        
        시간 복잡도: O(1)
        
        Args:
            data: 삽입할 데이터
            
        Returns:
            Node: 새로 생성된 노드
        """
        new_node = Node(data)
        
        # tail.prev와 tail 사이에 삽입
        new_node.prev = self.tail.prev
        new_node.next = self.tail
        self.tail.prev.next = new_node
        self.tail.prev = new_node
        
        self._size += 1
        return new_node
    
    def remove_front(self):
        """
        리스트의 맨 앞 노드 제거 (head 바로 뒤)
        
        시간 복잡도: O(1)
        
        Returns:
            data: 제거된 노드의 데이터, 리스트가 비어있으면 None
        """
        if self.is_empty():
            return None
        
        node_to_remove = self.head.next
        data = node_to_remove.data
        
        self.head.next = node_to_remove.next
        node_to_remove.next.prev = self.head
        
        # 참조 해제
        node_to_remove.prev = None
        node_to_remove.next = None
        
        self._size -= 1
        return data
    
    def remove_back(self):
        """
        리스트의 맨 뒤 노드 제거 (tail 바로 앞)
        
        시간 복잡도: O(1)
        LRU에서 가장 오래된 항목을 제거할 때 사용합니다.
        
        Returns:
            data: 제거된 노드의 데이터, 리스트가 비어있으면 None
        """
        if self.is_empty():
            return None
        
        node_to_remove = self.tail.prev
        data = node_to_remove.data
        
        self.tail.prev = node_to_remove.prev
        node_to_remove.prev.next = self.tail
        
        # 참조 해제
        node_to_remove.prev = None
        node_to_remove.next = None
        
        self._size -= 1
        return data
    
    def remove_node(self, node):
        """
        특정 노드를 리스트에서 제거
        
        시간 복잡도: O(1)
        
        Args:
            node: 제거할 노드
            
        Returns:
            data: 제거된 노드의 데이터
        """
        if node is None or node == self.head or node == self.tail:
            return None
        
        data = node.data
        
        # 이전 노드와 다음 노드를 연결
        node.prev.next = node.next
        node.next.prev = node.prev
        
        # 참조 해제
        node.prev = None
        node.next = None
        
        self._size -= 1
        return data
    
    def move_to_front(self, node):
        """
        특정 노드를 리스트의 맨 앞으로 이동
        
        시간 복잡도: O(1)
        LRU에서 접근된 항목을 최신으로 갱신할 때 사용합니다.
        
        Args:
            node: 이동할 노드
        """
        if node is None or node == self.head or node == self.tail:
            return
        
        # 이미 맨 앞에 있는 경우
        if node == self.head.next:
            return
        
        # 기존 위치에서 제거
        node.prev.next = node.next
        node.next.prev = node.prev
        
        # head 바로 뒤로 이동
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def get_back_node(self):
        """
        리스트의 맨 뒤 노드 반환 (제거하지 않음)
        
        시간 복잡도: O(1)
        
        Returns:
            Node: 맨 뒤 노드, 리스트가 비어있으면 None
        """
        if self.is_empty():
            return None
        return self.tail.prev
    
    def is_empty(self):
        """
        리스트가 비어있는지 확인
        
        Returns:
            bool: 비어있으면 True
        """
        return self._size == 0
    
    def size(self):
        """
        리스트의 노드 개수 반환
        
        Returns:
            int: 노드 개수
        """
        return self._size
    
    def __len__(self):
        """len() 함수 지원"""
        return self._size
    
    def __iter__(self):
        """
        이터레이터 지원 (head에서 tail 방향)
        
        Yields:
            data: 각 노드의 데이터
        """
        current = self.head.next
        while current != self.tail:
            yield current.data
            current = current.next
