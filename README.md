# SymbDiff
A symbolic differentiator implemented in Python 3.10.

### Examples
Basic Trig differentiation:
```python
from executor.simplify import simplify_expression
from symbols.overload import as_expression

expression = 'dx(sin(x) + cos(x))'
print(simplify_expression(as_expression(expression)).as_display())
# => cos (x) + -sin(x)
```

More derivatives:
```python
from executor.simplify import simplify_expression
from symbols.overload import as_expression

expression = 'dx(x ** x)'
print(simplify_expression(as_expression(expression)).as_display())
# => exp(x * log x) * (1.0 + log x)

expression = 'dz(sin(log(x)) + z)'
print(simplify_expression(as_expression(expression)).as_display())
# => 1.0

expression = 'dx(2**x * sin(x) / cos(2*x))'
print(simplify_expression(as_expression(expression)).as_display())
# => 'try it yourself'
```

### API
- `symbols/` contains the AST tree nodes
- `executor/` contains the transformation, simplification, interpretation methods 
- `executor/rules/` contains the simplification and differentiation rules