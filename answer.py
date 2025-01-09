import re
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import asyncio
from typing import List, Tuple
import multiprocessing as mp

NUMBERS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}
PATTERN = re.compile(f'(?=({"|".join(NUMBERS.keys())}|\\d))')

def process_line(line: str) -> int:
    """Process a single line and return calibration valuey"""
    matches = [m.group(1) for m in PATTERN.finditer(line)]
    if not matches: return 0
    first, last = matches[0], matches[-1]
    return int(f"{NUMBERS.get(first, first)}{NUMBERS.get(last, last)}")

def parallel_process(lines: List[str], chunk_size: int = 1000) -> int:
    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        return sum(executor.map(process_line, lines, chunksize=chunk_size))

async def async_process_lines(lines: List[str]) -> int:
    """Process lines asynchronously using ThreadPoolExecutor for I/O-bound operations"""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        tasks = [loop.run_in_executor(pool, process_line, line) for line in lines]
        results = await asyncio.gather(*tasks)
        return sum(results)

# Main execution with error handling and performance monitoring
def main(input_text: str, parallel: bool = True) -> int:
    lines = input_text.strip().split('\n')
    if parallel and len(lines) > 1000:  # Using parallel processing for large inputs
        return parallel_process(lines)
    return sum(process_line(line) for line in lines)

# Example usage with performance monitoring
if __name__ == "__main__":
    example_input = f"{input}".strip()
    
    result = main(example_input)
    print(f"Result: {result}")