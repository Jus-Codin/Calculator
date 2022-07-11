from tkinter import Tk, Button, Text
from calculate import calculate
from compiler import baseconvert
from functools import partial
import traceback

# Main window stuff-------------------------------------------------------------
window = Tk()
window.title('Calculator Mk6')
window['bg'] = '#3B3B3B'
window.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], minsize=30, weight=1)
window.columnconfigure([0, 1, 2, 3, 4], minsize=70, weight=1)
window.resizable(width=0, height=0)
window.attributes('-alpha', 0.9)

# Variables---------------------------------------------------------------------
global baseN, memory, ans, answered, error, memreg
baseN = '10'
memory = '0'
ans = '0'
answered = False
error = False

operators = ('+', '-', '×', '÷', '^', '.')

# Custom Tkinter Classes--------------------------------------------------------
class HoverButton(Button):
  def __init__(self, master, **kwargs):
    Button.__init__(self, master, **kwargs)
    self['background'] = '#222222'
    self['foreground'] = '#E1E1E1'
    self['activebackground'] = '#515151'
    self['activeforeground'] = '#F7F7F7'
    self['relief'] = 'flat'
    self['borderwidth'] = 0
    self.bind('<Enter>', self.on_enter)
    self.bind('<Leave>', self.on_leave)

  def on_enter(self, e):
    if self['bg'] == '#222222':
      self['bg'] = '#2A2A2A'

  def on_leave(self, e):
    if self['bg'] == '#2A2A2A':
      self['bg'] = '#222222'

class BaseNButton(HoverButton):
  def __init__(self, master, selected, **kwargs):
    HoverButton.__init__(self, master, **kwargs)
    if selected:
      self['bg'] = '#E1E1E1'
      self['fg'] = '#222222'

# Button functions---------------------------------------------------------------
def numbtn(number):
  global answered, error
  if answered:
    answered = False
    text.delete(0.0, 'end')
  elif error:
    return
  text.insert('end', number)

def opbtn(operator):
  global answered
  if answered:
    text.delete(0.0, 'end')
    text.insert('end', ans)
    answered = False
  if (last := text.get('%s-1c' % 'insert', 'insert')) in operators and not error:
    if last == '×' and operator == '×':
      text.replace('%s-1c' % 'insert', 'insert', '^')
      return
    else:
      text.delete('%s-1c' % 'insert', 'insert')
  text.insert('end', operator)

def membtn(function):
  global error, memory, ans
  if error:
    return
  elif function == 'M+':
    cmdequals()
    memory = str(int(memory)+int(ans))
  elif function == 'M-':
    cmdequals()
    memory = str(int(memory)-int(ans))
  else:
    numbtn(memory)
    return
  text.insert('end', function)
    
def editbtn(function):
  global answered, error, ans, baseN, memory
  if function == '⌫':
    if answered:
      text.delete(0.0, 'end')
      text.insert('end', ans)
    elif error:
      return
    text.delete('%s-1c' % 'insert', 'insert')
  elif function == 'AC':
    editbtn('C')
    baseN = '10'
    memory = '0'
  elif function == 'C':
    text.delete(0.0, 'end')
    ans = '0'
    answered = False
    error = False
  else:
    cmdequals()

def basebtn(base):
  global ans, error, answered, baseN
  basetobtn = {
    '2'  : bina,
    '8'  : octa,
    '10' : deci,
    '16' : hexa
  }
  if not error:
    if not answered:
      cmdequals()
    ans = baseconvert(ans, baseN, base)
    text.replace(0.0, 'end', ans)
    for basenum, btnvar in basetobtn.items():
      if basenum == base:
        btnvar['bg'] = '#E1E1E1'
        btnvar['fg'] = '#222222'
      else:
        btnvar['bg'] = '#222222'
        btnvar['fg'] = '#E1E1E1'
    baseN = base
    
    

def cmdequals():
  global error, answered, ans
  if not error:
    request_string = str(text.get(0.0, 'end'))
    editbtn('C')
    if request_string == '\n':
      return
    try:
      ans = calculate(request_string, baseN)
      text.insert('end', ans)
      answered = True
    except ZeroDivisionError:
      error = True
      text.insert('end', 'Numbers cannot be divided by zero, press C to continue')
    except Exception as e:
      error = True
      tb = traceback.format_exc()
      text.insert('end', f'{e}, Check shell for full traceback, press C to continue')
      print(tb)


# Layout:
#__________________
#|________________|
#|          d  h  |
#| M+ M- M        |
#|	        b  o  |  
#| 7  8  9 ⌫  AC |
#| 4  5  6  +  -  |
#| 1  2  3  *  /  |
#| 0  .  C    =   |

# GUI-------------------------------------------------------------------------
text = Text(window,
            bg='#222222',
            fg='#E1E1E1',
            width=6,
            height=1,
            font=75,
            relief='flat')
text.grid(row=0, rowspan=4, column=0, columnspan=5, sticky='nsew', padx=1, pady=1)

BUTTONS = {
  # Stored in format : Text : (row, column, columnspan, command)
  'M+' :   (4, 0, 1, membtn),
  'M-' :   (4, 1, 1, membtn),
  'M'  :   (4, 2, 1, membtn),
  '7'  :   (6, 0, 1, numbtn),
  '8'  :   (6, 1, 1, numbtn),
  '9'  :   (6, 2, 1, numbtn),
  '⌫' :  (6, 3, 1, editbtn),
  'AC' :  (6, 4, 1, editbtn),
  '4'  :   (8, 0, 1, numbtn),
  '5'  :   (8, 1, 1, numbtn),
  '6'  :   (8, 2, 1, numbtn),
  '+'  :    (8, 3, 1, opbtn),
  '-'  :    (8, 4, 1, opbtn),
  '1'  :  (10, 0, 1, numbtn),
  '2'  :  (10, 1, 1, numbtn),
  '3'  :  (10, 2, 1, numbtn),
  '×'  :   (10, 3, 1, opbtn),
  '÷'  :   (10, 4, 1, opbtn),
  '0'  :  (12, 0, 1, numbtn),
  '.'  :   (12, 1, 1, opbtn),
  'C'  : (12, 2, 1, editbtn),
  '='  : (12, 3, 2, editbtn)
}

for name, var in BUTTONS.items():
  btn = HoverButton(
    window,
    text = name,
    font = 75
    )
  btn['command'] = partial(var[3], name)
  btn.grid(
    row = var[0],
    rowspan = 2,
    column = var[1],
    columnspan = var[2],
    sticky = 'nsew',
    padx = 1,
    pady = 1
    )

deci = BaseNButton(window, True, text='Dec', font=75, command=partial(basebtn, '10'))
deci.grid(row=4, column=3, sticky='nsew', padx=1, pady=1)
hexa = BaseNButton(window, False, text='Hex', font=75, command=partial(basebtn, '16'))
hexa.grid(row=4, column=4, sticky='nsew', padx=1, pady=1)
bina = BaseNButton(window, False, text='Bin', font=75, command=partial(basebtn, '2'))
bina.grid(row=5, column=3, sticky='nsew', padx=1, pady=1)
octa = BaseNButton(window, False, text='Oct', font=75, command=partial(basebtn, '8'))
octa.grid(row=5, column=4, sticky='nsew', padx=1, pady=1)

window.mainloop()
