from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key : int) -> int:
        if key not in self.cache:
            print(f"GET {key}: Key not found.")
            return -1
        else:
            self.cache.move_to_end(key)
            print(f"GET {key}: Key found, moved to recent.")
            return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        print(f"PUT {key}: Inserted/Updated (key={key}, value={value}).")
        if len(self.cache) > self.capacity:
            removed = self.cache.popitem(last=False)
            print(f"Cache exceeded capacity. Removed least recently used item: {removed}")
    
    def display_cache(self):
        print(f"Current Cache: {self.cache}\n")
            
cache = LRUCache(2)

cache.put(1, 1)    # Cache is {1=1}
cache.display_cache()

cache.put(2, 2)    # Cache is {1=1, 2=2}
cache.display_cache()

cache.get(1)       # Returns 1, Cache is {2=2, 1=1} (1 is moved to most recent)
cache.display_cache()

cache.put(3, 3)    # Evicts key 2, Cache is {1=1, 3=3}
cache.display_cache()

cache.get(2)       # Returns -1 (not found), Cache is unchanged
cache.display_cache()

cache.put(4, 4)    # Evicts key 1, Cache is {3=3, 4=4}
cache.display_cache()

cache.get(1)       # Returns -1 (not found), Cache is unchanged
cache.display_cache()

cache.get(3)       # Returns 3, Cache is {4=4, 3=3}
cache.display_cache()

cache.get(4)       # Returns 4, Cache is {3=3, 4=4}
cache.display_cache()