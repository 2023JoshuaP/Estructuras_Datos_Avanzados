import curses
from collections import defaultdict

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # Almacena los pares clave-valor
        self.freq = defaultdict(int)  # Almacena la frecuencia de cada clave
        self.min_freq = 0  # Frecuencia mínima actual en la cache
        self.freq_list = defaultdict(list)  # Listas de claves ordenadas por frecuencia

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        else:
            # Incrementar la frecuencia de la clave
            self._update_freq(key)
            return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return

        if key in self.cache:
            # Si la clave ya existe, actualizamos el valor y la frecuencia
            self.cache[key] = value
            self._update_freq(key)
        else:
            if len(self.cache) >= self.capacity:
                # Si la cache está llena, eliminamos el elemento menos frecuentado
                self._evict()

            # Insertamos el nuevo par clave-valor y lo asignamos a la frecuencia 1
            self.cache[key] = value
            self.freq[key] = 1
            self.freq_list[1].append(key)
            self.min_freq = 1  # Al ser una nueva clave, la frecuencia mínima es 1

    def _evict(self):
        # Eliminamos la clave menos frecuentada
        key_to_evict = self.freq_list[self.min_freq].pop(0)  # Clave menos frecuentada
        if not self.freq_list[self.min_freq]:
            del self.freq_list[self.min_freq]
        del self.cache[key_to_evict]
        del self.freq[key_to_evict]

    def _update_freq(self, key: int):
        freq = self.freq[key]
        self.freq_list[freq].remove(key)
        if not self.freq_list[freq]:
            del self.freq_list[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        # Incrementamos la frecuencia de la clave
        self.freq[key] += 1
        self.freq_list[self.freq[key]].append(key)

    def display_cache(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0, "Cache (Least Frequently Used):")
        row = 1
        for freq in sorted(self.freq_list):
            for key in self.freq_list[freq]:
                stdscr.addstr(row, 0, f"Key: {key}, Value: {self.cache[key]}, Frequency: {self.freq[key]}")
                row += 1
        stdscr.addstr(row + 1, 0, "Enter operation (put <key> <value> or get <key>):")
        stdscr.refresh()

def main(stdscr):
    stdscr.clear()
    
    # Initialize the cache with a capacity of 2
    cache = LFUCache(5)

    while True:
        cache.display_cache(stdscr)
        
        stdscr.addstr(10, 0, "> ")
        stdscr.refresh()
        user_input = stdscr.getstr(10, 2, 20).decode('utf-8')

        if user_input.startswith("put"):
            try:
                _, key, value = user_input.split()
                key, value = int(key), int(value)
                cache.put(key, value)
            except ValueError:
                stdscr.addstr(12, 0, "Invalid input! Use format: put <key> <value>")
                stdscr.refresh()
                stdscr.getch()
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
                stdscr.getch()
            except ValueError:
                stdscr.addstr(12, 0, "Invalid input! Use format: get <key>")
                stdscr.refresh()
                stdscr.getch()
        else:
            stdscr.addstr(12, 0, "Invalid command! Use 'put' or 'get'.")
            stdscr.refresh()
            stdscr.getch()

# Run the curses application
curses.wrapper(main)
