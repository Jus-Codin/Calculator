'''
Compiler for numbers, used by calculate.py
'''
import re

operators = ['^', '÷', '×', '+', '-']

def compiler(s, base):
	'''Converts string of bases to their base 10 equivalant'''
	s = re.sub(r'[^0-9A-Fa-f\+\-×÷.\^]', '', s)
	chars = list(s)
	assembledchars = []
	assembled = str()
	for i in chars:
		if i not in operators:
			assembled += i
		else:
			assembledchars.append(baseconvert(assembled, base, '10'))
			assembledchars.append(i)
			assembled =	str()
	if not assembledchars or assembledchars[-1] in operators:
		assembledchars.append(baseconvert(assembled, base, '10'))
	print(assembledchars)
	return ''.join(assembledchars)

def baseconvert(s, current_base, resultant_base='10'):
	'''Converts base to other bases, used for internal proccessing'''
	# Trial and error, inefficient but works
	base_funcs = {
		'2'   : bin,
		'8'   : oct,
		'10'  : int,
		'16'  : hex,
	}
	bases = ['2', '8', '10', '16']
	if current_base not in bases or resultant_base not in bases:
		raise ValueError(f'Bases must be 2, 8, 10, or 16, current bases: {(current_base, resultant_base)}')
	elif current_base == resultant_base:
		return s
	check = re.findall('[^0-9a-fA-F]', s)
	if not check:
		pass
	elif '.' in check:
		raise ValueError(f'Type "float" cannot be converted to base {resultant_base}')
	else:
		raise ValueError(f'Unaccepted value(s) in string : {check}')
	base_func = base_funcs[resultant_base]
	if base_func == int:
		return str(base_func(s, int(current_base)))
	else:
		return base_func(int(baseconvert(s, current_base, '10')))[2:]
