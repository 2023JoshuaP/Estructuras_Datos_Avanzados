import pygame
import random
import sys

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def draw(self, screen, radius):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), radius)
        
class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.points = []
    
    def contains(self, point):
        return self.x <= point.x <= self.x + self.w and self.y <= point.y <= self.y + self.h

class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.divided = False
        self.no = None
        self.ne = None
        self.so = None
        self.se = None
    
    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
        no = Rectangle(x, y, w//2, h//2)
        ne = Rectangle(x + w//2, y, w//2, h//2)
        so = Rectangle(x, y + h//2, w//2, h//2)
        se = Rectangle(x + w//2, y + h//2, w//2, h//2)
        self.no = QuadTree(no, self.capacity)
        self.ne = QuadTree(ne, self.capacity)
        self.so = QuadTree(so, self.capacity)
        self.se = QuadTree(se, self.capacity)
        self.divided = True
        
        for point in self.boundary.points:
            if not self.insert(point):
                print("No se pudo insertar el punto")
        
        self.boundary.points.clear()
    
    def insert(self, point):
        if not self.boundary.contains(point):
            return False
        
        if len(self.boundary.points) <= self.capacity - 1 and self.divided == False:
            self.boundary.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
            if self.no.insert(point):
                return True
            if self.ne.insert(point):
                return True
            if self.so.insert(point):
                return True
            if self.se.insert(point):
                return True
    
    def count_elements(self):
        if not self.divided:
            return len(self.boundary.points)
        else:
            return (self.no.count_elements() + self.ne.count_elements() + 
                    self.so.count_elements() + self.se.count_elements())
    
    def delete(self, point):
        if not self.boundary.contains(point):
            return False
        
        if not self.divided:
            try:
                self.boundary.points.remove(point)
            except ValueError:
                print("El punto no se encuentra en el QuadTree")
                return False
            else:
                self.optimize()
                return True
        else:
            if self.no.delete(point):
                self.optimize()
                return True
            if self.ne.delete(point):
                self.optimize()
                return True
            if self.so.delete(point):
                self.optimize()
                return True
            if self.se.delete(point):
                self.optimize()
                return True
    
    def search(self, point):
        if not self.boundary.contains(point):
            return False
        
        if not self.divided:
            return self.boundary.points.count(point)
        else:
            return (self.no.search(point) or self.ne.search(point) or 
                    self.so.search(point) or self.se.search(point))
    
    def merge(self):
        self.boundary.points = (
            self.no.boundary.points + self.ne.boundary.points +
            self.so.boundary.points + self.se.boundary.points
        )
        self.no = None
        self.ne = None
        self.so = None
        self.se = None
        self.divided = False
    
    def optimize(self):
        if self.divided and self.count_elements() <= self.capacity:
            self.merge()
    
    def repr_helper(self, string):
        if not self.divided:
            for point in self.boundary.points:
                string += repr(point) + ", "
            return string
        else:
            string = self.no.repr_helper(string)
            string = self.ne.repr_helper(string)
            string = self.so.repr_helper(string)
            string = self.se.repr_helper(string)
            return string
    
    def __repr__(self):
        string = self.repr_helper("")
        return "[" + string[:-2] + "]"

    def draw(self, screen, scroke_weight):
        pygame.draw.rect(screen, (255, 255, 255), (self.boundary.x, self.boundary.y, self.boundary.w, self.boundary.h), scroke_weight)
        if self.divided:
            self.no.draw(screen, scroke_weight)
            self.ne.draw(screen, scroke_weight)
            self.so.draw(screen, scroke_weight)
            self.se.draw(screen, scroke_weight)
            
if __name__ == "__main__":
    pygame.init()
    
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("QuadTree")
    
    background = (0, 0, 0)
    screen.fill(background)
    
    points = []
    point_radius = 5
    stroke_weight = 3
    
    rect = Rectangle(0, 0, WIDTH, HEIGHT)
    qtree = QuadTree(rect, 4)
    
    for _ in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        point = Point(x, y)
        points.append(point)
        qtree.insert(point)
    
    def draw_points():
        for point in points:
            point.draw(screen, point_radius)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(background)
        draw_points()
        qtree.draw(screen, stroke_weight)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()