import curses
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
    
    def display_cache(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0, "Cache (Most recently used at the bottom):")
        i = 0
        for i, (key, value) in enumerate(self.cache.items(), 1):
            stdscr.addstr(i, 0, f"{key}: {value}")
        stdscr.addstr(i + 2, 0, "Enter operation (put <key> <value> or get <key>):")
        stdscr.refresh()

def main(stdscr):
    # Set up the screen
    stdscr.clear()

    # Initialize the cache with a capacity of 2
    cache = LRUCache(10)

    while True:
        cache.display_cache(stdscr)
        
        # Get input from the user
        stdscr.addstr(10, 0, "> ")
        stdscr.refresh()
        user_input = stdscr.getstr(10, 2, 20).decode('utf-8')

        # Process user input
        if user_input.startswith("put"):
            try:
                _, key, value = user_input.split()
                key, value = int(key), int(value)
                cache.put(key, value)
            except ValueError:
                stdscr.addstr(12, 0, "Invalid input! Use format: put <key> <value>")
                stdscr.refresh()
                stdscr.getch()  # Wait for key press to continue
        elif user_input.startswith("get"):
            try:
                _, key = user_input.split()
                key = int(key)
                result = cache.get(key)
                if result == -1:
                    stdscr.addstr(12, 0, f"Key {key} not found!")
                else:
                    stdscr.addstr(12, 0, f"Value for key {key}: {result}")
                stdscr.refresh()
                stdscr.getch()  # Wait for key press to continue
            except ValueError:
                stdscr.addstr(12, 0, "Invalid input! Use format: get <key>")
                stdscr.refresh()
                stdscr.getch()  # Wait for key press to continue
        else:
            stdscr.addstr(12, 0, "Invalid command! Use 'put' or 'get'.")
            stdscr.refresh()
            stdscr.getch()  # Wait for key press to continue

# Run the curses application
curses.wrapper(main)
