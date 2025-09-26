## Python Variables and Data Types – Detailed Guide with Examples

This guide covers Python variables and data types you’ll use most often. It includes explanations, common operations, gotchas, and hands‑on examples.

### Variables 101
- **Assignment**: Variables are created by assignment. Types are inferred dynamically.
```python
count = 3              # int
price = 19.99          # float
message = "Hello"       # str
is_active = True       # bool
```
- **Naming**: Use lowercase_with_underscores. Avoid reserved words (`for`, `class`, `def`, ...).
- **Mutability**: Some types are immutable (int, float, str, tuple, bool), others are mutable (list, dict, set).
- **Rebinding vs mutation**:
```python
x = 10
x = x + 1     # rebinding an int (immutable)

items = [1, 2]
items.append(3)  # mutating a list (mutable)
```

---

### Basic Data Types

#### 1) Integers (`int`)
- Arbitrary precision whole numbers (no fixed upper/lower bound).
- Common operations: `+ - * // % **` and comparisons.
```python
a = 42
b = -7
c = 1_000_000           # underscores improve readability
base16 = int("FF", 16)   # 255, parse with base
quotient = 7 // 3        # 2 (floor division)
remainder = 7 % 3        # 1
power = 2 ** 10          # 1024
```

#### 2) Floating-Point Numbers (`float`)
- IEEE‑754 double precision (binary). Expect rounding artifacts.
```python
x = 0.1 + 0.2
print(x)                 # 0.30000000000000004

# Compare with tolerance
import math
math.isclose(x, 0.3)     # True
```
- For exact decimal money math, use `decimal.Decimal`.
```python
from decimal import Decimal, ROUND_HALF_UP

price = Decimal("19.99")
tax = Decimal("0.05")
total = (price * (Decimal(1) + tax)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

#### 3) Strings (`str`)
- Unicode text, immutable. Use single, double, or triple quotes.
```python
name = "Ada"
greeting = f"Hello, {name}!"     # f-strings
multiline = """Line 1\nLine 2"""

"python".upper()                 # 'PYTHON'
"  trim  ".strip()               # 'trim'
"a,b,c".split(",")              # ['a', 'b', 'c']
"-".join(["2025", "09", "26"])  # '2025-09-26'
```
- Slicing:
```python
s = "abcdef"
s[0]        # 'a'
s[-1]       # 'f'
s[1:4]      # 'bcd'
```

#### 4) Booleans (`bool`)
- Only two values: `True`, `False`. Subclass of `int` (True == 1, False == 0), but use for logic.
```python
is_empty = len([]) == 0      # True
bool("")                    # False (empty string is falsy)
bool("False")               # True (non-empty string is truthy!)

3 < 5 < 8                    # True (chained comparisons)
```

---

### Advanced (Built-in) Data Types

#### 5) Lists (`list`)
- Ordered, mutable sequences.
```python
nums = [1, 2, 3]
nums.append(4)              # [1, 2, 3, 4]
nums.extend([5, 6])         # [1, 2, 3, 4, 5, 6]
nums.insert(0, 0)           # [0, 1, 2, 3, 4, 5, 6]
last = nums.pop()           # 6, nums -> [0, 1, 2, 3, 4, 5]
nums[2:5]                   # [2, 3, 4]

# List comprehension
squares = [n * n for n in range(5)]  # [0, 1, 4, 9, 16]

# Copy vs alias
a = [[1, 2], [3, 4]]
b = a[:]                 # shallow copy
a[0].append(99)
b[0]                     # [1, 2, 99] (inner lists shared)
```

#### 6) Tuples (`tuple`)
- Ordered, immutable sequences. Great for fixed-size records and unpacking.
```python
point = (10, 20)
x, y = point

# Useful for returning multiple values
def min_max(values):
    return min(values), max(values)

lo, hi = min_max([3, 8, 1])   # lo=1, hi=8
```

#### 7) Sets (`set`)
- Unordered collections of unique elements.
```python
a = {1, 2, 3}
b = {3, 4}
a | b        # {1, 2, 3, 4} union
a & b        # {3} intersection
a - b        # {1, 2} difference

unique_words = set("to be or not to be".split())  # {'to', 'or', 'not', 'be'}

immutable = frozenset([1, 2, 2, 3])               # frozenset({1, 2, 3})
```

#### 8) Dictionaries (`dict`)
- Key–value mappings. Keys must be hashable (e.g., str, int, tuple of immutables).
```python
user = {"id": 1, "name": "Ada", "active": True}
user["name"]            # 'Ada'
user.get("email", "n/a")  # 'n/a' (safe access)

# Add/Update
user["email"] = "ada@example.com"

# Iteration preserves insertion order (Python 3.7+)
for key, value in user.items():
    print(key, value)

# Merge dictionaries
defaults = {"theme": "light", "notifications": True}
overrides = {"theme": "dark"}
settings = defaults | overrides     # {'theme': 'dark', 'notifications': True}

# Comprehension
names = ["alice", "bob", "carol"]
length_by_name = {n: len(n) for n in names}
```

---

### Type Conversion (Casting)
Common constructors: `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`, `set()`, `dict()`.
```python
int("42")          # 42
float("3.14")      # 3.14
str(123)           # '123'
bool(0)            # False
list("abc")        # ['a', 'b', 'c']
tuple([1, 2])      # (1, 2)
set([1, 1, 2])     # {1, 2}
dict([("a", 1), ("b", 2)])  # {'a': 1, 'b': 2}
```
Gotchas:
- `int("3.0")` raises `ValueError` (string isn’t a pure integer). Use `int(float("3.0"))` if appropriate.
- `bool("False")` is `True` because any non-empty string is truthy.
- Floats may not round as expected; for money use `Decimal`.

---

### Practical Examples

#### Example 1: Word Frequency Counter
```python
text = "to be or not to be"
counts = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1

print(counts)  # {'to': 2, 'be': 2, 'or': 1, 'not': 1}
unique = set(counts)
print(unique)  # {'to', 'or', 'not', 'be'}
```

#### Example 2: Average Score with Safe Division
```python
scores = [88, 92, 79, 94]
total = sum(scores)
avg = total / len(scores) if scores else 0.0
print(avg)
```

#### Example 3: Parsing CSV-like Numbers to Integers
```python
raw = "10,20,30,40"
values = [int(x) for x in raw.split(",")]
print(values)  # [10, 20, 30, 40]
```

---

### Quick Reference
- **Immutable**: `int`, `float`, `bool`, `str`, `tuple`, `frozenset`
- **Mutable**: `list`, `dict`, `set`
- **Truthy/Falsy**: `0`, `0.0`, `""`, `[]`, `{}`, `set()` are falsy; most others are truthy.
- **Conversions**: Prefer explicit casts for clarity; beware float precision and string truthiness.

---

### Practice Tasks
- Convert a list of temperatures in Celsius to Fahrenheit using a list comprehension.
- Given a sentence, produce a dict mapping each word to its length.
- Deduplicate a list of emails while preserving insertion order.


