"""
Mini Redis CLI 인터페이스

이 모듈은 사용자 입력을 받아 명령어를 파싱하고 실행 결과를 출력하는
REPL(Read-Eval-Print Loop) 환경을 제공합니다.
"""

import sys
import os

# 현재 디렉토리를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from redis_core import MiniRedis


class CLI:
    """
    Mini Redis CLI 클래스
    
    사용자 입력을 읽고 명령어를 파싱하여 MiniRedis 인스턴스에서 실행합니다.
    결과는 Redis 형식으로 출력됩니다.
    
    Attributes:
        redis: MiniRedis 인스턴스
    """
    
    def __init__(self):
        """
        CLI 초기화
        """
        self.redis = MiniRedis()
    
    def run(self):
        """
        REPL 메인 루프 실행
        
        사용자가 'exit' 또는 'quit'을 입력할 때까지 반복합니다.
        """
        print("=" * 50)
        print("   Mini Redis - In-Memory Key-Value Store")
        print("=" * 50)
        print("Type 'help' for available commands, 'exit' to quit.\n")
        
        while True:
            try:
                # 프롬프트 출력 및 입력 받기
                user_input = input("mini-redis> ").strip()
                
                if not user_input:
                    continue
                
                # 종료 명령어
                if user_input.lower() in ('exit', 'quit'):
                    print("Bye!")
                    break
                
                # 명령어 파싱 및 실행
                result = self._execute_command(user_input)
                
                # 결과 출력
                if result is not None:
                    print(result)
                    
            except KeyboardInterrupt:
                print("\nBye!")
                break
            except EOFError:
                print("\nBye!")
                break
            except Exception as e:
                print(f"(error) {str(e)}")
    
    def _parse_input(self, user_input):
        """
        사용자 입력 파싱
        
        따옴표로 묶인 문자열을 올바르게 처리합니다.
        
        Args:
            user_input: 사용자 입력 문자열
            
        Returns:
            list: 파싱된 토큰 리스트
        """
        tokens = []
        current_token = ""
        in_quotes = False
        quote_char = None
        
        i = 0
        while i < len(user_input):
            char = user_input[i]
            
            if char in ('"', "'") and not in_quotes:
                # 따옴표 시작
                in_quotes = True
                quote_char = char
            elif char == quote_char and in_quotes:
                # 따옴표 종료
                in_quotes = False
                quote_char = None
            elif char == ' ' and not in_quotes:
                # 공백 (토큰 구분)
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            else:
                current_token += char
            
            i += 1
        
        # 마지막 토큰 추가
        if current_token:
            tokens.append(current_token)
        
        return tokens
    
    def _execute_command(self, user_input):
        """
        명령어 실행
        
        Args:
            user_input: 사용자 입력
            
        Returns:
            str: 실행 결과
        """
        tokens = self._parse_input(user_input)
        
        if not tokens:
            return None
        
        command = tokens[0].upper()
        args = tokens[1:]
        
        # 명령어별 처리
        if command == "SET":
            return self._cmd_set(args)
        elif command == "GET":
            return self._cmd_get(args)
        elif command == "DEL":
            return self._cmd_del(args)
        elif command == "EXISTS":
            return self._cmd_exists(args)
        elif command == "DBSIZE":
            return self._cmd_dbsize(args)
        elif command == "CONFIG":
            return self._cmd_config(args)
        elif command == "INFO":
            return self._cmd_info(args)
        elif command == "EXPIRE":
            return self._cmd_expire(args)
        elif command == "TTL":
            return self._cmd_ttl(args)
        elif command == "HELP":
            return self._cmd_help()
        elif command == "KEYS":
            return self._cmd_keys(args)
        else:
            return f"(error) ERR unknown command '{command}'"
    
    # ==================== 명령어 핸들러 ====================
    
    def _cmd_set(self, args):
        """SET key value"""
        if len(args) < 2:
            return "(error) ERR wrong number of arguments for 'set' command"
        
        key = args[0]
        value = args[1]
        
        result = self.redis.set(key, value)
        return result
    
    def _cmd_get(self, args):
        """GET key"""
        if len(args) < 1:
            return "(error) ERR wrong number of arguments for 'get' command"
        
        key = args[0]
        result = self.redis.get(key)
        
        if result is None:
            return "(nil)"
        else:
            return f'"{result}"'
    
    def _cmd_del(self, args):
        """DEL key [key ...]"""
        if len(args) < 1:
            return "(error) ERR wrong number of arguments for 'del' command"
        
        deleted = 0
        for key in args:
            deleted += self.redis.delete(key)
        
        return f"(integer) {deleted}"
    
    def _cmd_exists(self, args):
        """EXISTS key"""
        if len(args) < 1:
            return "(error) ERR wrong number of arguments for 'exists' command"
        
        key = args[0]
        result = self.redis.exists(key)
        return f"(integer) {result}"
    
    def _cmd_dbsize(self, args):
        """DBSIZE"""
        result = self.redis.dbsize()
        return f"(integer) {result}"
    
    def _cmd_config(self, args):
        """CONFIG SET maxmemory <bytes>"""
        if len(args) < 3:
            return "(error) ERR wrong number of arguments for 'config' command"
        
        subcommand = args[0].upper()
        
        if subcommand == "SET":
            param = args[1].lower()
            value = args[2]
            
            if param == "maxmemory":
                try:
                    result = self.redis.config_set_maxmemory(int(value))
                    return result
                except ValueError:
                    return "(error) ERR value is not an integer"
            else:
                return f"(error) ERR unknown config parameter '{param}'"
        elif subcommand == "GET":
            param = args[1].lower()
            if param == "maxmemory":
                info = self.redis.info_memory()
                return f"1) \"maxmemory\"\n2) \"{info['maxmemory']}\""
            else:
                return f"(error) ERR unknown config parameter '{param}'"
        else:
            return f"(error) ERR unknown subcommand '{subcommand}'"
    
    def _cmd_info(self, args):
        """INFO memory"""
        if len(args) < 1:
            # 전체 정보 출력
            info = self.redis.info_memory()
            return self._format_info(info)
        
        section = args[0].lower()
        
        if section == "memory":
            info = self.redis.info_memory()
            return self._format_info(info)
        else:
            return f"(error) ERR unknown info section '{section}'"
    
    def _format_info(self, info):
        """INFO 출력 포맷팅"""
        lines = []
        for key, value in info.items():
            lines.append(f"{key}:{value}")
        return "\n".join(lines)
    
    def _cmd_expire(self, args):
        """EXPIRE key seconds"""
        if len(args) < 2:
            return "(error) ERR wrong number of arguments for 'expire' command"
        
        key = args[0]
        try:
            seconds = int(args[1])
        except ValueError:
            return "(error) ERR value is not an integer"
        
        result = self.redis.expire(key, seconds)
        return f"(integer) {result}"
    
    def _cmd_ttl(self, args):
        """TTL key"""
        if len(args) < 1:
            return "(error) ERR wrong number of arguments for 'ttl' command"
        
        key = args[0]
        result = self.redis.ttl(key)
        return f"(integer) {result}"
    
    def _cmd_keys(self, args):
        """KEYS pattern (간단 구현: 모든 키 출력)"""
        keys = []
        idx = 1
        for key in self.redis._store.keys():
            keys.append(f"{idx}) \"{key}\"")
            idx += 1
        
        if not keys:
            return "(empty list or set)"
        return "\n".join(keys)
    
    def _cmd_help(self):
        """HELP - 사용 가능한 명령어 출력"""
        help_text = """
Available commands:
  SET key value         - Set key to hold the string value
  GET key               - Get the value of key
  DEL key [key ...]     - Delete a key
  EXISTS key            - Check if key exists
  DBSIZE                - Return the number of keys in the database
  
  CONFIG SET maxmemory <bytes>  - Set maximum memory limit
  CONFIG GET maxmemory          - Get maximum memory limit
  INFO memory                   - Get memory usage information
  
  EXPIRE key seconds    - Set a timeout on key
  TTL key               - Get the time to live for a key
  
  KEYS *                - List all keys
  HELP                  - Show this help message
  EXIT / QUIT           - Exit the program
"""
        return help_text.strip()


def main():
    """메인 함수"""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
