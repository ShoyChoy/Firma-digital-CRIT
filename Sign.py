import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkdocviewer import *
import tkinterDnD  # Importing the tkinterDnD module
import os
import glob
import fitz
from Firmas import *

global dfc, logged_usr, l_user_psw, preftheme
dfc=pd.read_csv('usr n psw.csv')
logged_usr=''
l_user_psw=''
prefs=[]

with open('Preferencias.txt') as f:
    try:
        prefs= f.readlines()
        lastusr,preftheme=prefs
        lastusr=lastusr[:-1]
    except:
        lastusr=''
        preftheme='light'

def change_theme():
    global preftheme
    # NOTE: The theme's real name is sun-valley-<mode>
    if root.tk.call("ttk::style", "theme", "use") == "sun-valley-dark":
        # Set light theme
        root.tk.call("set_theme", "light")
        preftheme='light'
    else:
        # Set dark theme
        root.tk.call("set_theme", "dark")
        preftheme='dark'

global tab
tab=[]  
# You have to use the tkinterDnD.Tk object for super easy initialization,
# and to be able to use the main window as a dnd widget
root = tkinterDnD.Tk()  
root.title("Firma m'esta")
root.resizable(False, False) 
root.geometry("225x180")

big_frame = ttk.Frame(root)
big_frame.grid(row=0, column=0, sticky='nsew')

signin = ttk.Frame(root)
signin.grid(row=0, column=0, sticky='nsew')

#signup = ttk.Frame(root)
#signup.grid(row=0, column=0, sticky='nsew')

signin.tkraise()

menubar = tk.Menu(root)
root.config(menu=menubar)
prefmenu = tk.Menu(menubar, tearoff=0)
prefmenu.add_command(label="Cambiar tema", command=change_theme)
menubar.add_cascade(label="Preferencias", menu=prefmenu)

files_frame=ttk.Frame(big_frame, width=300)
files_frame.pack(fill=tk.BOTH, side=tk.LEFT)

notebook = ttk.Notebook(big_frame)
#notebook.grid(row=0, column=1)
notebook.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

stringvar = tk.StringVar()
stringvar.set('Drop or Select here!')

user = tk.StringVar(value=lastusr)
user2 = tk.StringVar()
name = tk.StringVar()
pos = tk.StringVar()
confpass = tk.StringVar()
password = tk.StringVar()
password2 = tk.StringVar()

root.tk.call("source", "source\sun-valley.tcl")
root.tk.call("set_theme", preftheme)

def close_window(window,entry): 
    p=entry.get()
    if p=="":
        entry.state(['invalid'])
    else:    
        window.destroy()
        button_1.config(state='normal',onfiledrop=drop)

def add_menu(usrtype):
    if usrtype==1:
        configmenu = tk.Menu(menubar, tearoff=0)
        configmenu.add_command(label="Cambiar Contraseña", command=change_theme)
        menubar.add_cascade(label="Configuraciones", menu=configmenu)
        configmenu.add_separator
    else:
        configmenu = tk.Menu(menubar, tearoff=0)
        configmenu.add_command(label="Cambiar Contraseña", command=change_theme)
        configmenu.add_command(label="Dar de alta usuario administrador", command=lambda: signup_clicked(0))
        configmenu.add_command(label="Eliminar usuario", command=change_theme)
        menubar.add_cascade(label="Configuraciones", menu=configmenu)
        configmenu.add_separator

def login_clicked():
    global logged_in, logged_usr, l_user_psw
    psw=password_entry.get()
    usr=user_entry.get()

    try:
        usr=int(usr)
    except:
        user_entry.state(['invalid'])

    auth = psw.encode()
    auth_hash = hashlib.md5(auth).hexdigest()

    try:
        cpsw=dfc.loc[dfc['ID'] == usr, 'Contraseña'].values[0]
        if cpsw==auth_hash:
            big_frame.tkraise()
            root.geometry("310x150")
            logged_usr=usr
            l_user_psw=auth_hash

            usrtype=dfc.loc[dfc['ID'] == usr, 'Tipo de Usuario'].values[0]
            add_menu(usrtype)
        else:
            password_entry.delete(0, tk.END)
            password_entry.state(['invalid'])
            showinfo(title='ERROR',
                message='Contraseña incorrecta'
            )
    except:
        user_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        user_entry.state(['invalid'])
        user_entry.focus()
        showinfo(title='ERROR',
                message='Usuario no existe'
        )

def signup_clicked(type):
    signup = tk.Toplevel()
    signup.geometry('225x430')
    signup.resizable(False, False)
    
    ##Signup

    # user
    user_label = ttk.Label(signup, text="ID del Empleado:", anchor='center')
    user_label.pack(expand=True, fill=tk.X, padx=5,pady=6)

    user_entry2 = ttk.Entry(signup, textvariable=user2)
    user_entry2.pack(expand=True, fill=tk.X, padx=5,pady=6)
    user_entry2.focus()

    # name
    name_label = ttk.Label(signup, text="Nombre Completo:", anchor='center')
    name_label.pack(expand=True, fill=tk.X, padx=5,pady=6)

    name_entry = ttk.Entry(signup, textvariable=name)
    name_entry.pack(expand=True, fill=tk.X, padx=5,pady=6)

    # pos
    pos_label = ttk.Label(signup, text="Puesto:", anchor='center')
    pos_label.pack(expand=True, fill=tk.X, padx=5,pady=6)

    pos_entry = ttk.Entry(signup, textvariable=pos)
    pos_entry.pack(expand=True, fill=tk.X, padx=5,pady=6)

    # password
    password_label = ttk.Label(signup, text="Contraseña:", anchor='center')
    password_label.pack(expand=True, fill=tk.X, padx=5,pady=6)

    password_entry2 = ttk.Entry(signup, textvariable=password2, show="*")
    password_entry2.pack(expand=True, fill=tk.X, padx=5,pady=6)

    confpass_label = ttk.Label(signup, text="Confirmar Contraseña:", anchor='center')
    confpass_label.pack(expand=True, fill=tk.X, padx=5,pady=6)

    confpass_entry = ttk.Entry(signup, textvariable=confpass, show="*")
    confpass_entry.pack(expand=True, fill=tk.X, padx=5,pady=6)

    # signup button

    signup_button = ttk.Button(signup, text="Crear Usuario", style='Accent.TButton')
    signup_button.bind("<Button-1>", (lambda event: usercreate_clicked(type, user_entry2,name_entry,password_entry2,
                                                                        confpass_entry,pos_entry)))
    signup_button.pack(expand=True, fill=tk.X, padx=5,pady=6)

    user_entry2.bind('<Return>',(lambda event: name_entry.focus()))
    name_entry.bind('<Return>',(lambda event: pos_entry.focus()))
    pos_entry.bind('<Return>',(lambda event: password_entry2.focus()))
    password_entry2.bind('<Return>',(lambda event: confpass_entry.focus()))
    confpass_entry.bind('<Return>',(lambda event: usercreate_clicked(type,signup, user_entry2,name_entry,password_entry2,
                                                                    confpass_entry,pos_entry)))
    signup.grab_set()
    #signup.tkraise()
    #root.geometry("225x460")


def usercreate_clicked(tipo, window,user_entry2,name_entry,password_entry2,confpass_entry,pos_entry):
    global dfc
    emp_id=user_entry2.get()
    try:
        emp_id=int(emp_id)
    except:
        user_entry2.state(['invalid'])
        emp_id=0

    nombre=name_entry.get()
    psw=password_entry2.get()
    cpsw=confpass_entry.get()

    if (emp_id in dfc['ID'].unique()) or (psw != cpsw):
        user_entry2.focus()
        user_entry2.state(['invalid'])
        user_entry2.delete(0, tk.END)
        name_entry.state(['invalid'])
        pos_entry.state(['invalid'])
        password_entry2.state(['invalid'])
        password_entry2.delete(0, tk.END)
        confpass_entry.state(['invalid'])
        confpass_entry.delete(0, tk.END)
        showinfo(title='ERROR',
                message='El usuario ya existe, o la contraseña no coincide'
        )
    else:
        enc = psw.encode()
        hash1 = hashlib.md5(enc).hexdigest()
        datos_reg=[emp_id,nombre,pos_entry.get(),hash1]

        dfcontra = {'ID': emp_id, 'Usuario': nombre, 'Contraseña': hash1, 'Tipo de Usuario':tipo}
        dfc = dfc.append(dfcontra, ignore_index = True)
        dfc.to_csv('usr n psw.csv', index =  False)
        registro('Usuarios y claves publicas.csv','Pruebas firma',tipo, datos_reg)

        close_window(window,user_entry2)
        #signin.tkraise()
        #root.geometry("225x180")
    

def verify_signature():
    
    v=True
    s='Persona'

    if v:
        m=f'La firma es válida \nHa sido firmada por {s}'

    showinfo(
            title='Verificación de firma',
            message=m
        )

def add_signature():
    button_1.config(state='disable',onfiledrop=donothing)
    psw = tk.StringVar()
    window = tk.Toplevel()

    window.geometry('300x100')
    window.resizable(False, False)
    newlabel = ttk.Label(window, text = "Contraseña:")
    newlabel.grid(row=0, column=0,padx=10,pady=6)
    newentry = ttk.Entry(window, textvariable=psw, show="*")
    newentry.grid(row=0, column=1, padx=5,pady=6, sticky='ew')
    newentry.focus()

    newbutton = ttk.Button(window, text = "OK",style='Accent.TButton')
    newbutton.bind("<Button-1>", (lambda event: close_window(window,newentry)))
    newbutton.grid(row=1, column=0,columnspan=2,padx=5,pady=6)

    #window.bind('<Return>',close_window(window))
    newentry.bind('<Return>',(lambda event: close_window(window,newentry)))
    window.grab_set()

def preview(sl):
    root.geometry("1100x500")
    root.resizable(True, True) 
    button_2.config(style='Accent.TButton', state='normal')
    button_3.config(style='Accent.TButton', state='normal')
    button_4.config(style='Accent.TButton', state='normal')
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

def donothing(event):
    print('nothing done')

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
        
        global paths
        paths=s

        preview(sl)

# With DnD hook you just pass the command to the proper argument,
# and tkinterDnD will take care of the rest
# NOTE: You need a ttk widget to use these arguments
button_1 = ttk.Button(files_frame, onfiledrop=drop,textvar=stringvar, padding=30, command=select_file)
button_1.grid(row=0, column=0, columnspan = 3, padx=5,pady=5)

button_2= ttk.Button(files_frame, text="Verificar Firma", command=verify_signature, state='disable')
button_2.grid(row=1, column=0, padx=5,pady=6)

button_3= ttk.Button(files_frame, text="Firmar", command=add_signature, state='disable')
button_3.grid(row=1, column=1, padx=5,pady=6)

button_4= ttk.Button(files_frame, text="Unificar Firmas", state='disable')
button_4.grid(row=1, column=2, padx=5,pady=6)

##LOGIN

# user
user_label = ttk.Label(signin, text="ID del Empleado:", anchor='center')
user_label.grid(row=0,column=0,columnspan=2,sticky='ew')

user_entry = ttk.Entry(signin, textvariable=user)
user_entry.grid(row=1,column=0,columnspan=2,sticky='ew', padx=5,pady=6)

# password
password_label = ttk.Label(signin, text="Contraseña:", anchor='center')
password_label.grid(row=2,column=0,columnspan=2,sticky='ew')

password_entry = ttk.Entry(signin, textvariable=password, show="*")
password_entry.grid(row=3,column=0,columnspan=2,sticky='ew', padx=5,pady=6)

if (user_entry.get()=='') :
    user_entry.delete(0,tk.END)
    user_entry.focus()
else:
    password_entry.focus()

# login button
signup_button = ttk.Button(signin, text="Crear Usuario", style='Accent.TButton')
signup_button.bind("<Button-1>", (lambda event: signup_clicked(1)))
signup_button.grid(row=4,column=0, padx=5, pady=10)

login_button = ttk.Button(signin, text="Iniciar Sesión", command=login_clicked, style='Accent.TButton')
login_button.grid(row=4,column=1, padx=5, pady=10)

user_entry.bind('<Return>',(lambda event: password_entry.focus()))
password_entry.bind('<Return>',(lambda event: login_clicked()))




root.columnconfigure(0, weight=1, minsize=75)
root.rowconfigure(0, weight=1, minsize=50)

root.mainloop()


files = glob.glob('Temp_imgs/*')
for f in files:
    os.remove(f)

#prefs[0]=str(logged_usr)
#prefs[1]=preftheme

with open("Preferencias.txt","w") as f:
    f.write(str(logged_usr)+'\n'+preftheme)