'''
Main calculation interface, used in main.py
'''
import re
from compiler import compiler, baseconvert
from operator import add, mul, pow, sub, truediv

operators = {
  '^': pow,
  '÷': truediv,
  '×': mul,
  '+': add,
  '-': sub
}

bases = ['2', '8', '10', '16']

def calculate(s, base):
  if base not in bases:
    raise ValueError(f'Base needs to be 2, 8, 10, or 16, current base: {base}')
  s = compiler(s, base)
  if not re.findall('[^0-9a-fA-F.]', s):
    return baseconvert(s, '10', base)
  for c in operators.keys():
    left, operator, right = s.partition(c)
    if operator in operators:
      # We don't talk about this monstrosity
      return baseconvert(str(operators[operator](_calculate(left, base), _calculate(right, base))), '10', base) 

def _calculate(s, base):
  '''A copy of calculate(), but without compiler() and base conversion of numbers'''
  if base not in bases:
    raise ValueError(f'Base needs to be 2, 8, 10, or 16, current base: {base}')
  if not re.findall('[^0-9a-fA-F.]', s):
    return int(float(s))
  for c in operators.keys():
    left, operator, right = s.partition(c)
    if operator in operators:
      return operators[operator](_calculate(left, base), _calculate(right, base))
