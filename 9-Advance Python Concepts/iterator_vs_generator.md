# Iterator vs Generator in Python


**can iterate both!** But there are important differences:

> **All generators ARE iterators, but not all iterators are generators!**


---

## The Relationship

```
┌─────────────────────────────────────┐
│         ITERATORS                   │
│  (Objects with __iter__ & __next__) │
│                                     │
│  ┌───────────────────────────┐     │
│  │     GENERATORS             │     │
│  │  (Created with yield)      │     │
│  │                            │     │
│  └───────────────────────────┘     │
│                                     │
│  - Built-in iterators (iter(list)) │
│  - Custom iterator classes         │
│  - File objects                    │
└─────────────────────────────────────┘
```

---

## Comparison Table

| Feature | Iterator | Generator |
|---------|----------|-----------|
| **Definition** | Any object with `__iter__()` and `__next__()` | Special type of iterator using `yield` |
| **How to create** | Define class with `__iter__` & `__next__` | Use `yield` in a function or `()` expression |
| **Complexity** | More code (class, methods) | Simple (just a function with yield) |
| **State management** | Manual (you track position) | Automatic (Python tracks it) |
| **Example** | `iter([1,2,3])`, custom class | `(x for x in range(5))`, generator function |
| **Memory** | Depends on implementation | Always memory efficient (lazy) |
| **Can iterate?** | ✅ Yes | ✅ Yes |

---

## 1. Iterator (General Concept)

An iterator is **any object** that implements:
- `__iter__()` - returns the iterator object
- `__next__()` - returns the next value or raises `StopIteration`

### Example: Built-in Iterator

```python
# Create an iterator from a list
my_list = [1, 2, 3, 4, 5]
iterator = iter(my_list)  # This is an iterator

print(type(iterator))  # <class 'list_iterator'>

# Can iterate
print(next(iterator))  # 1
print(next(iterator))  # 2

# Or use in loop
for item in iterator:
    print(item)  # 3, 4, 5
```

### Example: Custom Iterator Class

```python
class MyIterator:
    """Custom iterator - more verbose"""
    def __init__(self, max_num):
        self.max_num = max_num
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.max_num:
            raise StopIteration
        self.current += 1
        return self.current ** 2

# Use it
my_iter = MyIterator(5)
print(type(my_iter))  # <class '__main__.MyIterator'>

for num in my_iter:
    print(num)  # 1, 4, 9, 16, 25
```

---

## 2. Generator (Special Iterator)

A generator is a **simpler way** to create an iterator using:
- `yield` keyword in a function
- Generator expression with `()`

### Example: Generator Function

```python
def my_generator(max_num):
    """Generator - much simpler!"""
    current = 0
    while current < max_num:
        current += 1
        yield current ** 2

# Use it
my_gen = my_generator(5)
print(type(my_gen))  # <class 'generator'>

for num in my_gen:
    print(num)  # 1, 4, 9, 16, 25
```

### Example: Generator Expression

```python
# Generator expression (even simpler!)
my_gen = (x**2 for x in range(1, 6))
print(type(my_gen))  # <class 'generator'>

for num in my_gen:
    print(num)  # 1, 4, 9, 16, 25
```

---

## Side-by-Side: Same Result, Different Implementation

```python
print("=" * 60)
print("ITERATOR (Class-based)")
print("=" * 60)

class SquareIterator:
    def __init__(self, n):
        self.n = n
        self.i = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.i < self.n:
            result = self.i ** 2
            self.i += 1
            return result
        raise StopIteration

# Use iterator
iterator = SquareIterator(5)
print(f"Type: {type(iterator)}")
for num in iterator:
    print(num, end=' ')  # 0 1 4 9 16

print("\n\n" + "=" * 60)
print("GENERATOR (Function-based)")
print("=" * 60)

def square_generator(n):
    for i in range(n):
        yield i ** 2

# Use generator
generator = square_generator(5)
print(f"Type: {type(generator)}")
for num in generator:
    print(num, end=' ')  # 0 1 4 9 16

print("\n\n" + "=" * 60)
print("GENERATOR EXPRESSION")
print("=" * 60)

gen_expr = (i**2 for i in range(5))
print(f"Type: {type(gen_expr)}")
for num in gen_expr:
    print(num, end=' ')  # 0 1 4 9 16
```

**Output:**
```
============================================================
ITERATOR (Class-based)
============================================================
Type: <class '__main__.SquareIterator'>
0 1 4 9 16 

============================================================
GENERATOR (Function-based)
============================================================
Type: <class 'generator'>
0 1 4 9 16 

============================================================
GENERATOR EXPRESSION
============================================================
Type: <class 'generator'>
0 1 4 9 16
```

---

## Why Use Generators Over Custom Iterators?

### 1. Much Less Code

```python
# Iterator: ~15 lines
class CountIterator:
    def __init__(self, max_num):
        self.max_num = max_num
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.max_num:
            raise StopIteration
        self.current += 1
        return self.current

# Generator: 3 lines!
def count_generator(max_num):
    for i in range(1, max_num + 1):
        yield i
```

### 2. Automatic State Management

```python
# Iterator: Manual state tracking
class Fibonacci:
    def __init__(self, n):
        self.n = n
        self.a = 0
        self.b = 1
        self.count = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count >= self.n:
            raise StopIteration
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result

# Generator: Python handles state automatically!
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Both work the same
print(list(Fibonacci(10)))
print(list(fibonacci(10)))
```

### 3. More Readable and Pythonic

Generators read like regular functions, making them easier to understand and maintain.

---

## Checking if Something is an Iterator or Generator

```python
from collections.abc import Iterator
import types

# List iterator
list_iter = iter([1, 2, 3])
print(f"list_iter is Iterator: {isinstance(list_iter, Iterator)}")
print(f"list_iter is Generator: {isinstance(list_iter, types.GeneratorType)}")

# Generator function
def my_gen():
    yield 1

gen = my_gen()
print(f"\ngen is Iterator: {isinstance(gen, Iterator)}")
print(f"gen is Generator: {isinstance(gen, types.GeneratorType)}")

# Generator expression
gen_expr = (x for x in range(5))
print(f"\ngen_expr is Iterator: {isinstance(gen_expr, Iterator)}")
print(f"gen_expr is Generator: {isinstance(gen_expr, types.GeneratorType)}")
```

**Output:**
```
list_iter is Iterator: True
list_iter is Generator: False

gen is Iterator: True
gen is Generator: True

gen_expr is Iterator: True
gen_expr is Generator: True
```

---

## Both Support Iteration

```python
# Iterator
my_iter = iter([1, 2, 3])
for item in my_iter:
    print(item)  # Works!

# Generator
my_gen = (x for x in [1, 2, 3])
for item in my_gen:
    print(item)  # Works!

# Both support next()
iter1 = iter([1, 2, 3])
gen1 = (x for x in [1, 2, 3])

print(next(iter1))  # 1 - Works!
print(next(gen1))   # 1 - Works!
```

---

## Real-World Examples

### Iterator Example: Built-in

```python
# Built-in iterator
my_list = [1, 2, 3, 4, 5, 6]
iterator = iter(my_list)  # Creates a list_iterator

# This is an iterator (but not a generator)
print(type(iterator))  # <class 'list_iterator'>

# Can iterate
for item in iterator:
    print(item)
```

### Generator Example: File Reading

```python
# Generator function for reading large files
def read_large_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

# This is a generator (which is also an iterator)
for line in read_large_file('data.txt'):
    process(line)  # Process one line at a time (memory efficient!)
```

---

## Performance Comparison

### Iterator: Custom Class

```python
class RangeIterator:
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        result = self.current
        self.current += 1
        return result

# Use it
for i in RangeIterator(0, 1000000):
    pass  # Just iterate
```

### Generator: Function

```python
def range_generator(start, end):
    current = start
    while current < end:
        yield current
        current += 1

# Use it (cleaner and just as fast!)
for i in range_generator(0, 1000000):
    pass  # Just iterate
```

**Result:** Generators are typically as fast or faster than custom iterators, with much cleaner code!

---

## Summary Table

| Aspect | Iterator | Generator |
|--------|----------|-----------|
| **What is it?** | Any object with `__iter__` & `__next__` | Special type of iterator |
| **How to create?** | Class with methods OR built-in | Function with `yield` OR `()` expression |
| **Code complexity** | More (need class) | Less (just function) |
| **State management** | Manual | Automatic (Python handles it) |
| **Example types** | `list_iterator`, custom classes | `generator` object |
| **Can iterate?** | ✅ Yes | ✅ Yes |
| **Can use `next()`?** | ✅ Yes | ✅ Yes |
| **Memory efficient?** | Depends | ✅ Always |
| **Readability** | More verbose | More Pythonic |
| **Use case** | Complex iteration logic | Most iteration needs |

---

## The Relationship in Code

```python
from collections.abc import Iterator
import types

# All generators are iterators
generator = (x for x in range(5))
print(isinstance(generator, Iterator))  # True ✅

# Not all iterators are generators
iterator = iter([1, 2, 3])
print(isinstance(iterator, types.GeneratorType))  # False ❌
```

---

## When to Use What?

### Use Custom Iterator Class When:
- You need complex state management
- You want to implement custom methods beyond `__iter__` and `__next__`
- You're building a complex data structure

### Use Generator When:
- You need simple iteration (90% of cases)
- You want clean, readable code
- You're processing large datasets
- You need memory efficiency

---

## Key Takeaways

1. **Generators are iterators** - They implement the iterator protocol automatically
2. **Generators are simpler** - Less boilerplate code
3. **Both can be iterated** - Use `for` loops or `next()`
4. **Generators are Pythonic** - Preferred in modern Python code
5. **Memory efficient** - Both use lazy evaluation (if implemented correctly)

---

## Best Practice Recommendation

**Use generators by default!** Only create custom iterator classes when you need:
- Complex state management
- Multiple iteration methods
- Integration with specific class hierarchies

For 90% of iteration needs, generators are the better choice:
- Cleaner code
- Easier to understand
- Just as efficient
- More Pythonic

---

## Quick Reference

```python
# Iterator (class-based)
class MyIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        result = self.data[self.index]
        self.index += 1
        return result

# Generator (function-based) - RECOMMENDED
def my_generator(data):
    for item in data:
        yield item

# Generator (expression) - MOST CONCISE
gen = (item for item in data)
```

---

**Bottom line:** Generators are a **convenient shorthand** for creating iterators. They do the same job (iteration) but with much simpler syntax. **Use generators whenever possible** because they're easier to write, understand, and maintain!

