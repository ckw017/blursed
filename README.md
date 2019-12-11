# blursed 

(adj.) - Simultaneously blessed and cursed by a situation, object, person, etc...

`blursed` adds a handful of feature's that nobody asked for to Python scripts via a special codec. Consider the following:

```python
print(6(7 + 8))
<stdin>:1: SyntaxWarning: 'int' object is not callable;
perhaps you missed a comma?
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'int' object is not callable
```

The problem here is that while `6(7 + 8)` is perfectly valid multiplication notation, the type of `6` is `int` which doesn't support function calls. The codec silently wraps all integer literals to give them the proper `__call__` dunder method.

Other "features" include:
* "C-like" subscripting
* Original scheme for float subscripting
* Wrappers for all builtin numeric types


# Installation

`pip install --user blursed`

# Usage

Add `# -*- coding: blursed -*-` to the top of the Python file you would like to inflict this package on.

For a better idea of the full range of unfortunate possibilities, try running the following:

```python
# -*- coding: blursed -*-

print("Multiplications")
print(1.5(24 + 12 + 1)(238 * 3)(512))
print(16(12 * 12) + 512)

print("\nIndexing")
sup = "Konichiwhat's up"

print(7[sup])
print(8[sup])
print(9[sup])
print(10[sup])

ohno = [0,1,2,3,4]

print("\nFloat indexing")
print(2.7[ohno])
print(0.5[ohno])

why = [0,5,31,12]

print(1.5[why])
```

# Motivation

Not available.

# Inspiration

The C programming language, asottile's [future-fstrings](https://github.com/asottile/future-fstrings) package.
