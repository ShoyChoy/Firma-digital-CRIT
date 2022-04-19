import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkdocviewer import *
import tkinterDnD  # Importing the tkinterDnD module
import os
import glob
import fitz

def change_theme():
    # NOTE: The theme's real name is sun-valley-<mode>
    if root.tk.call("ttk::style", "theme", "use") == "sun-valley-dark":
        # Set light theme
        root.tk.call("set_theme", "light")
    else:
        # Set dark theme
        root.tk.call("set_theme", "dark")

global tab
tab=[]  
# You have to use the tkinterDnD.Tk object for super easy initialization,
# and to be able to use the main window as a dnd widget
root = tkinterDnD.Tk()  
root.title("Firma m'esta")
root.resizable(False, False) 
#root.geometry("850x750")

big_frame = ttk.Frame(root)
#big_frame.pack(fill="both", expand=True)
big_frame.grid(row=0, column=0, sticky='nsew')

signin = ttk.Frame(root)
#signin.pack(fill="both", expand=True)
signin.grid(row=0, column=0, sticky='nsew')

signin.tkraise()

menubar = tk.Menu(root)
configmenu = tk.Menu(menubar, tearoff=0)
configmenu.add_command(label="Change theme", command=change_theme)
menubar.add_cascade(label="Configuraciones", menu=configmenu)

files_frame=ttk.Frame(big_frame, width=300)
files_frame.pack(fill=tk.BOTH, side=tk.LEFT)

notebook = ttk.Notebook(big_frame)
#notebook.grid(row=0, column=1)
notebook.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

stringvar = tk.StringVar()
stringvar.set('Drop or Select here!')

user = tk.StringVar()
password = tk.StringVar()


root.tk.call("source", "source\sun-valley.tcl")
root.tk.call("set_theme", "light")


def login_clicked():
    big_frame.tkraise()
    root.geometry("200x150")

def preview(sl):
    root.geometry("1100x500")
    root.resizable(True, True) 
    #sl=path.split('\n')
    global tab
    for i in range(100):
        try:
            notebook.hide(i)
        except:
            break
    tab=[]

    for t in range(len(sl)):
        t= ttk.Frame(notebook, width=700, height=500)
        tab.append(t)
    
    for i in range(len(sl)):
        tab[i].pack(fill=tk.BOTH, expand=True)
        notebook.add(tab[i], text=os.path.basename(sl[i]))

        doc = fitz.open(sl[i])
        page = doc.load_page(0)  # number of page
        pix = page.get_pixmap()
        output = f"Temp_imgs\outfile{i}.png"
        pix.save(output)

    # Display some document
    for v in range(len(sl)): 
        p = DocViewer(tab[v], width=800, height=500,enable_downscaling=True)
        p.pack(expand=True, fill=tk.BOTH)
        p.display_file(sl[v])
        #p.display_file("Temp_imgs\outfile"+str(v)+".png")

def drop(event):
    s=str(event.data)[1:-1]
    s=s.replace('} {', '\n')
    sl=s.split('\n')
    s2=''
    for st in sl:
        s2=s2+os.path.basename(st)+'\n'

    s2=s2[:-1]

    stringvar.set(s2)
    print('Item dropped: ', s)
    global paths
    paths=s

    preview(sl)

def drag_command(event):
    # This function is called at the start of the drag,
    # it returns the drag type, the content type, and the actual content
    return (tkinterDnD.LINK, tkinterDnD.TEXT, "Some nice dropped text.")

def select_file():
    filetypes = (
        ('PDF files', '*.pdf'),
        ('XML files', '*.xml'),
        ('All files', '*.*')
    )

    filenames = fd.askopenfilenames(
        title='Open a file',
        initialdir='This PC',
        filetypes=filetypes)

    if filenames!='':
        s=str(filenames)[2:-2].replace('\'', '')
        s=s.replace(', ', '\n')
        sl=s.split('\n')
        s2=''
        
        for st in sl:
            s2=s2+os.path.basename(st)+'\n'
            

        s2=s2[:-1]

        stringvar.set(s2)
        print('Item selected: ', filenames)
        #showinfo(
        #    title='Selected File',
        #    message=s2
        #)
        global paths
        paths=s

        preview(sl)

#label_1=ttk.Label(root,textvar=s2)
#label_1.pack()


# With DnD hook you just pass the command to the proper argument,
# and tkinterDnD will take care of the rest
# NOTE: You need a ttk widget to use these arguments
button_1 = ttk.Button(files_frame, onfiledrop=drop, ondragstart=drag_command,
                    textvar=stringvar, padding=30, command=select_file)
button_1.grid(row=0, column=0, columnspan = 2, padx=5,pady=5)

button_2= ttk.Button(files_frame, text="Verificar Firma", command=change_theme, style="Accent.TButton")
button_2.grid(row=1, column=0, padx=5,pady=6)

button_3= ttk.Button(files_frame, text="Firmar", command=change_theme, style="Accent.TButton")
button_3.grid(row=1, column=1, padx=5,pady=6)


##LOGIN

# user
user_label = ttk.Label(signin, text="Usuario:", anchor='center')

user_label.pack(fill=tk.X, expand=True)

user_entry = ttk.Entry(signin, textvariable=user)
user_entry.pack(fill='x', expand=True, padx=5,pady=6)
user_entry.focus()

# password
password_label = ttk.Label(signin, text="Contraseña:", anchor='center')
password_label.pack(fill='x', expand=True)

password_entry = ttk.Entry(signin, textvariable=password, show="*")
password_entry.pack(fill='x', expand=True, padx=5,pady=6)

# login button
login_button = ttk.Button(signin, text="Login", command=login_clicked, style='Accent.TButton')
login_button.pack(fill='x', expand=True, padx=5, pady=10)

root.columnconfigure(0, weight=1, minsize=75)
root.rowconfigure(0, weight=1, minsize=50)

root.config(menu=menubar)
root.mainloop()


files = glob.glob('Temp_imgs/*')
for f in files:
    os.remove(f)