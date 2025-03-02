import textwrap
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
import os
from openai import OpenAI

class PythonCompressor:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    @staticmethod
    def create_compression_prompt(source_code: str) -> str:
        """Creates a prompt for compressing Python code via LLM."""
        return textwrap.dedent(f'''
        You are a specialized compressor for Python programs. Your task is to create an extremely compact yet unambiguous representation of the following Python program. Follow these rules:

        1. Focus on semantic meaning over syntax
        2. Use these abbreviations:
           - fn for function
           - cls for class
           - ret for return
           - arg for argument
           - imp for import
        3. Describe algorithms using high-level patterns rather than implementation details
        4. Reference standard library functions by their full paths
        5. Use => to indicate function signatures
        6. Use :: to separate class methods
        7. Use ... to indicate standard implementation patterns
        8. Preserve type hints in their original form

        Original program:
        ```python
        {source_code}
        ```

        Create a compressed representation using the format:
        IMP: <imports>
        TYPES: <custom type definitions>
        FN: <function signatures and core algorithms>
        FLOW: <key control flow patterns>
        DEPS: <critical dependencies>

        Your compression should be deterministic and reversible. Be precise about function signatures and type information.
        ''')

    def compress_with_openai(self, source_code: str) -> str:
        """Compress code using OpenAI's API"""
        prompt = self.create_compression_prompt(source_code)
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return response.choices[0].message.content

    def decompress_with_openai(self, compressed: str) -> str:
        """Decompress code using OpenAI's API"""
        prompt = self.create_decompression_prompt(compressed)
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return response.choices[0].message.content

    @staticmethod
    def create_decompression_prompt(compressed: str) -> str:
        """Creates a prompt for decompressing Python code via LLM."""
        return textwrap.dedent(f'''
        You are a specialized decompressor for Python programs. Your task is to reconstruct a complete, working Python program from this compressed representation. Follow these rules:

        1. Generate complete, working Python code
        2. Maintain exact function signatures and type hints
        3. Implement all described algorithms and patterns
        4. Use idiomatic Python style (PEP 8)
        5. Include docstrings for all functions and classes
        6. Expand abbreviated keywords:
           - fn => function
           - cls => class
           - ret => return
           - arg => argument
           - imp => import
        7. Interpret => as function signatures
        8. Interpret :: as class method separators
        9. Interpret ... as standard implementation patterns

        Compressed representation:
        {compressed}

        Generate a complete Python program that implements this specification. The code should be production-ready, well-documented, and maintain all type information.
        ''')

def test_compression_system():
    """Test the compression system with a sample Python program."""
    compressor = PythonCompressor()
    
    # Sample program to compress
    sample_program = '''
    from typing import List, Optional, Dict
    from dataclasses import dataclass
    import heapq

    @dataclass
    class TaskItem:
        priority: int
        description: str
        completed: bool = False

    class PriorityTaskManager:
        def __init__(self):
            self.tasks: List[TaskItem] = []
            self.task_index: Dict[str, int] = {}
        
        def add_task(self, priority: int, description: str) -> None:
            task = TaskItem(priority, description)
            heapq.heappush(self.tasks, (-priority, task))
            self.task_index[description] = len(self.tasks) - 1
        
        def get_highest_priority(self) -> Optional[TaskItem]:
            if not self.tasks:
                return None
            return self.tasks[0][1]
        
        def mark_completed(self, description: str) -> bool:
            if description not in self.task_index:
                return False
            idx = self.task_index[description]
            self.tasks[idx][1].completed = True
            return True
    '''

    # Test OpenAI compression/decompression
    print("=== Testing OpenAI Compression ===")
    compressed = compressor.compress_with_openai(sample_program)
    print(compressed)
    
    print("\n=== Testing OpenAI Decompression ===")
    decompressed = compressor.decompress_with_openai(compressed)
    print(decompressed)

def main():
    import sys
    
    def print_help():
        print("Python Code Compressor/Decompressor")
        print("\nUsage:")
        print("  python test3-claude.py test                        # Run test case")
        print("  python test3-claude.py compress <file>             # Compress a Python file")
        print("  python test3-claude.py decompress <file>           # Decompress a file")
        print("\nExamples:")
        print("  python test3-claude.py compress example.py         # Creates example.py.compressed")
        print("  python test3-claude.py decompress example.compressed  # Creates example.compressed.decompressed.py")
    
    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)
        
    command = sys.argv[1]
    
    if command == "test":
        test_compression_system()
    elif command in ["compress", "decompress"]:
        if len(sys.argv) < 3:
            print(f"Error: No file specified for {command}")
            print_help()
            sys.exit(1)
        process_file(sys.argv[2], command)
    else:
        print(f"Error: Unknown command '{command}'")
        print_help()
        sys.exit(1)
    
if __name__ == "__main__":
    main()