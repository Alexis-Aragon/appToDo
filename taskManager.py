from tkinter import *
import sqlite3
from customtkinter import *
import os
import appdirs
import platform

myappid = "taskManager-v1.0"

set_appearance_mode("dark")
# customtkinter.set_default_color_theme('')

root = CTk()
root.title('Gestor de Tareas')
root.geometry('500x500')
root.minsize(500,500)

basedir = os.path.dirname(__file__)

# Agregar icono de la app
# Verificar el sistema operativo
if platform.system() == "Windows":
    from ctypes import windll  # Only exists on Windows.
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    root.iconbitmap(os.path.join(basedir, 'taskmanager.ico'))
elif platform.system() == "Linux":
    root.iconphoto(True, PhotoImage(file=os.path.join(basedir, "taskmanager.png")))

frame = CTkFrame(root)
frame.grid(row=0, column=0, padx=30, pady=30, ipadx=30, ipady=30)

root.grid_rowconfigure(1,  weight =1)
root.grid_columnconfigure(0,  weight =1)

frame.grid_rowconfigure(1,  weight =1)
frame.grid_columnconfigure(1,  weight =1)

# Directorio donde se guardara la base de datos
app_name = "taskManager"
app_author = myappid
db_dir = appdirs.user_data_dir(app_name, app_author)
os.makedirs(db_dir, exist_ok=True)

# Conexión a la base de datos
ruta_base_de_datos = os.path.join(db_dir, 'todo.db')
conn =  sqlite3.connect(ruta_base_de_datos)

c = conn.cursor()

c.execute("""
    CREATE TABLE if not exists todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );
""")
    
conn.commit()

def remove(id):
    def _remove():
        c.execute("DELETE FROM todo WHERE  id = ?", (id, ))
        conn.commit()
        render_todos()
    return _remove

# Currying -> retrasamos la funcion
def complete(id): # encapsulamos el valor de id
    def _complete():
        todo = c.execute("SELECT * FROM todo WHERE id = ?", (id, )).fetchone()
        c.execute("UPDATE todo SET completed = ? WHERE id = ?", (not todo[3], id))
        conn.commit()
        render_todos()
    return _complete

def render_todos():
    for widget in lframe.winfo_children():
        widget.destroy()

    rows = c.execute("SELECT * FROM todo").fetchall()
    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        if completed:
            color = '#242424' 
            colortext = '#565B5E'
        else: 
            color = '#343638'
            colortext ='#eee'

        check_btn = CTkCheckBox(lframe, text=description, width=300, command=complete(id), 
                                bg_color=color, 
                                checkbox_height=20, 
                                checkbox_width=20, 
                                text_color=colortext, 
                                hover_color='#eee', 
                                fg_color='#565B5E')
        
        check_btn.grid(row=i, column=0, ipadx=5, ipady=5, columnspan=2)
        btn = CTkButton(lframe, text='Eliminar', command=remove(id), bg_color='#242424',
                        width=90,
                        height=20,
                        border_width=0,
                        corner_radius=10)
        btn.grid(row=i, column=2, padx=5, pady=5)
        check_btn.select() if completed else check_btn.deselect()
        
def addTodo():
    todo = e.get()
    if todo:
        c.execute(""" 
                INSERT INTO todo (description, completed) VALUES (?, ?)
                """, (todo, False))
        conn.commit()
        e.delete(0, END)
        render_todos()
    else:
        pass

l = CTkLabel(frame, text='Tarea')
l.grid(row=0, column=0, padx=40, pady=20, sticky='e')

e = CTkEntry(frame, width=300, height=40, corner_radius=10)
e.grid(row=0, column=1, pady=20, padx=0, sticky='we' )
e.focus()

btn = CTkButton(frame, text='Agregar', command=addTodo,
                            width=100,
                            height=30,
                            border_width=0,
                            corner_radius=8)
btn.grid(row=0, column=2, padx=20, pady=20)

lframe = LabelFrame(frame, text='Mis tareas', bg='#242424', fg='#eee', padx=5, pady=5)
lframe.grid(row=1, column=0, columnspan=3, padx=7, pady=7)

root.bind('<Return>', lambda x: addTodo())
render_todos()

root.mainloop()