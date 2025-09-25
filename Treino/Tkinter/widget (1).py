from tkinter import *
from tkinter import ttk

root = Tk()
content = ttk.Frame(root)
button = ttk.Button(content)

def print_hierarchy(w, depth=0):
    print('  '*depth + w.winfo_class() + ' w=' + str(w.winfo_width()) + ' h=' + str(w.winfo_height()) + ' x=' + str(w.winfo_x()) + ' y=' + str(w.winfo_y()))
    for i in w.winfo_children():
        print_hierarchy(i, depth+1)

print_hierarchy(root)

# Q U A D R O ----------------------------------------

frame = ttk.Frame(parent)
f['padding'] = 5           # 5 pixels on all sides
f['padding'] = (5,10)      # 5 on left and right, 10 on top and bottom
f['padding'] = (5,7,10,12) # left: 5, top: 7, right: 10, bottom: 12
frame['borderwidth'] = 2
frame['relief'] = 'sunken'
s = ttk.Style()
s.configure('Danger.TFrame', background='red', borderwidth=5, relief='raised')
ttk.Frame(root, width=200, height=200, style='Danger.TFrame').grid()

# L A B E L ----------------------------------------------

label = ttk.Label(parent, text='Full name:')
resultsContents = StringVar()
label['textvariable'] = resultsContents
resultsContents.set('New value to display')
image = PhotoImage(file='myimage.gif')
label['image'] = image          # compound são text(somente texto), image(somente imagem), center(texto no centro da imagem), top(imagem acima do texto), left, bottom, e right.
label['font'] = "TkDefaultFont" # anchor para especificar em qual borda ou canto a label deve ser fixada, o que deixaria qualquer espaço vazio na borda ou canto oposto. 
# Os valores são como direções da bússola: n(norte/borda superior), ne, (nordeste/canto superior direito), e, se, s, sw, w, nw ou center.
# wraplength, que especifica o comprimento máximo de uma linha (em pixels, centímetros, etc.).
# Você também pode controlar como o texto é justificado - justify - Ele pode ter os valores left, center, ou right. Se você tiver apenas uma única linha de texto, provavelmente você vai querer a anchor.

# Button ------------------------------------------------------

action = ttk.Button(root, text="Action", default="active", command=myaction)
root.bind('<Return>', lambda e: action.invoke())

# A lista completa de sinalizadores de estado disponíveis para widgets temáticos é: active, disabled, focus, pressed, selected, background, readonly, alternate, e invalid.

b.state(['disabled'])          # set the disabled flag
b.state(['!disabled'])         # clear the disabled flag
b.instate(['disabled'])        # true if disabled, else false
b.instate(['!disabled'])       # true if not disabled, else false
b.instate(['!disabled'], cmd)  # execute 'cmd' if not disabled

#Checkbutton -----------------------------------------------------------------------

measureSystem = StringVar()
check = ttk.Checkbutton(parent, text='Use Metric', 
	    command=metricChanged, variable=measureSystem,
	    onvalue='metric', offvalue='imperial')

check.instate(['alternate'])

s = StringVar(value="abc")   # default value is ''
b = BooleanVar(value=True)   # default is False
i = IntVar(value=10)         # default is 0
d = DoubleVar(value=10.5)    # default is 0.0



# RadioBunttons ----------------------------------------------------------------

phone = StringVar()
home = ttk.Radiobutton(parent, text='Home', variable=phone, value='home')
office = ttk.Radiobutton(parent, text='Office', variable=phone, value='office')
cell = ttk.Radiobutton(parent, text='Mobile', variable=phone, value='cell')

# Entry Input ----------------------------------------------------------------------------------

username = StringVar()
name = ttk.Entry(parent, textvariable=username)

print('current value is %s' % name.get())
name.delete(0,'end')          # delete between two indices, 0-based
name.insert(0, 'your name')   # insert new text at a given index
passwd = ttk.Entry(parent, textvariable=password, show="*")

def it_has_been_written(*args):
    ...
username.trace_add("write", it_has_been_written)

import re
def check_num(newval):
    return re.match('^[0-9]*$', newval) is not None and len(newval) <= 5
check_num_wrapper = (root.register(check_num), '%P')

num = StringVar()
e = ttk.Entry(root, textvariable=num, validate='key', validatecommand=check_num_wrapper)
e.grid(column=0, row=0, sticky='we')


import re
errmsg = StringVar()
formatmsg = "Zip should be ##### or #####-####"

def check_zip(newval, op):
    errmsg.set('')
    valid = re.match('^[0-9]{5}(\-[0-9]{4})?$', newval) is not None
    btn.state(['!disabled'] if valid else ['disabled'])
    if op=='key':
        ok_so_far = re.match('^[0-9\-]*$', newval) is not None and len(newval) <= 10
        if not ok_so_far:
            errmsg.set(formatmsg)
        return ok_so_far
    elif op=='focusout':
        if not valid:
            errmsg.set(formatmsg)
    return valid
check_zip_wrapper = (root.register(check_zip), '%P', '%V')

zip = StringVar()
f = ttk.Frame(root)
f.grid(column=0, row=0)
ttk.Label(f, text='Name:').grid(column=0, row=0, padx=5, pady=5)
ttk.Entry(f).grid(column=1, row=0, padx=5, pady=5)
ttk.Label(f, text='Zip:').grid(column=0, row=1, padx=5, pady=5)
e = ttk.Entry(f, textvariable=zip, validate='all', validatecommand=check_zip_wrapper)
e.grid(column=1, row=1, padx=5, pady=5)
btn = ttk.Button(f, text="Process")
btn.grid(column=2, row=1, padx=5, pady=5)
btn.state(['disabled'])
msg = ttk.Label(f, font='TkSmallCaptionFont', foreground='red', textvariable=errmsg)
msg.grid(column=1, row=2, padx=5, pady=5, sticky='w')


# combobox --------------------------------------------------------------------------

countryvar = StringVar()
country = ttk.Combobox(parent, textvariable=countryvar)
country.bind('<<ComboboxSelected>>', function)
country['values'] = ('USA', 'Canada', 'Australia')
country.state(["readonly"])


# fim ##################################################################################



from tkinter import *
from tkinter import ttk

root = Tk()

content = ttk.Frame(root, padding=(3,3,12,12))
frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
namelbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)

onevar = BooleanVar()
twovar = BooleanVar()
threevar = BooleanVar()

onevar.set(True)
twovar.set(False)
threevar.set(True)

one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
ok = ttk.Button(content, text="Okay")
cancel = ttk.Button(content, text="Cancel")

content.grid(column=0, row=0, sticky=(N, S, E, W))
frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), padx=5)
name.grid(column=3, row=1, columnspan=2, sticky=(N,E,W), pady=5, padx=5)
one.grid(column=0, row=3)
two.grid(column=1, row=3)
three.grid(column=2, row=3)
ok.grid(column=3, row=3)
cancel.grid(column=4, row=3)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)

root.mainloop()

##Ambos columnconfiguretambém rowconfigureusam uma minsizeopção de grade, que especifica um tamanho mínimo além do qual você realmente não quer que a coluna ou linha encolha.


## outro -------------------------------------------------------------------------------------

from tkinter import *
from tkinter import ttk

root = Tk()

content = ttk.Frame(root)
frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
namelbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)

onevar = BooleanVar(value=True)
twovar = BooleanVar(value=False)
threevar = BooleanVar(value=True)

one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
ok = ttk.Button(content, text="Okay")
cancel = ttk.Button(content, text="Cancel")

content.grid(column=0, row=0)
frame.grid(column=0, row=0, columnspan=3, rowspan=2)
namelbl.grid(column=3, row=0, columnspan=2)
name.grid(column=3, row=1, columnspan=2)
one.grid(column=0, row=3)
two.grid(column=1, row=3)
three.grid(column=2, row=3)
ok.grid(column=3, row=3)
cancel.grid(column=4, row=3)

root.mainloop()