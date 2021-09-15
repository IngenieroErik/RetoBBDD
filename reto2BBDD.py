from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import tkinter as tk
   

def crearBBDD ():
    try:
    
        mi_conexion = sqlite3.connect("HOSPITAL")
        mi_cursor = mi_conexion.cursor()       
        mi_cursor.execute("CREATE TABLE PACIENTES( ID_PACIENTES INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE VARCHAR (50), EDAD INTEGER (50), NUMERO_HIS INTEGER(20), PRIORIDAD INTEGER (20), RIESGO INTEGER (20))")
        mi_cursor.execute("CREATE TABLE PACIENTE_ANCIANO( ID_ANCIANO INTEGER PRIMARY KEY AUTOINCREMENT, TIENE_DIETA VARCHAR(10), FOREIGN KEY(ID_ANCIANO) REFERENCES PACIENTES(ID_PACIENTES))")
        mi_cursor.execute("CREATE TABLE PACIENTE_JOVEN( ID_JOVEN INTEGER PRIMARY KEY AUTOINCREMENT, FUMADOR VARCHAR(10), FOREIGN KEY(ID_JOVEN) REFERENCES PACIENTES(ID_PACIENTES))")
        mi_cursor.execute("CREATE TABLE PACIENTE_NIÑO( ID_NIÑO INTEGER PRIMARY KEY AUTOINCREMENT, PESO VARCHAR(10), ESTATURA VARCHAR(10), FOREIGN KEY(ID_NIÑO) REFERENCES PACIENTES(ID_PACIENTES))")
        mi_cursor.execute("CREATE TABLE CONSULTA( ID_CONSULTAS INTEGER PRIMARY KEY AUTOINCREMENT, CANT_PACIENTES INTEGER(20), NOMBRE_ESPECIALISTA VARCHAR(50), TIPO_CONSULTA VARCHAR(50), ESTADO VARCHAR(30))")
        
        messagebox.showinfo("BBDD", "BBDD Y TABLAS CREADAS CON EXITO")

    except:
        messagebox.showwarning("BBDD YA EXISTE")


def calcular_prio_ries ():
    
    if int(entry_edad.get()) >= 1 and int(entry_edad.get()) <= 5:
        elevado = float(entry_estatura.get())
        suma = (float(entry_peso.get()) / pow(elevado,2)) + 3
        suma2 = (float(entry_edad.get())* suma)/100
        return prioridad.set(round(suma)), riesgo.set(round(suma2))

    elif int(entry_edad.get()) >=6 and int(entry_edad.get()) <=12:
        elevado = float(entry_estatura.get())
        suma = (float(entry_peso.get()) / pow(elevado,2)) + 2
        suma2 = (float(entry_edad.get())* suma)/100
        return prioridad.set(round(suma)), riesgo.set(round(suma2))

    elif int(entry_edad.get()) >= 13 and int(entry_edad.get()) <= 15:
        elevado = float(entry_estatura.get())
        suma = (float(entry_peso.get()) / pow(elevado,2)) + 1
        suma2 = (float(entry_edad.get())* suma)/100
        return prioridad.set(round(suma)), riesgo.set(round(suma2))

    elif int(entry_edad.get()) >= 16 and int(entry_edad.get()) < 41 and fumador_si_no.get() == "SI":
        edad = int(entry_edad.get())
        años = int(entry_añosFumando.get())
        prioridad1 = años/4+2
        return prioridad.set(round(prioridad1)), riesgo.set(round(edad * prioridad1 / 100))
    
    elif int(entry_edad.get()) >= 16 and int(entry_edad.get()) < 41 and fumador_si_no.get() != "SI":
        edad = int(entry_edad.get())
        prioridad2 = 2
        return prioridad.set(prioridad2), riesgo.set(round(edad * prioridad2 / 100))
            
    elif int(entry_edad.get()) >= 41:
        edad = int(entry_edad.get())
        prioridad1 = float(edad / 30 + 3)
        return prioridad.set(round(prioridad1)), riesgo.set(round(edad * prioridad1 / 100 + 5.3))
    
    elif int(entry_edad.get()) >=60 and int(entry_edad.get()) <= 100 and dieta_asignada.get() == "SI":
        edad = int(entry_edad.get())
        prioridad1 = float(edad / 20 + 4) 
        return prioridad.set(round(prioridad1)), riesgo.set(round(edad * prioridad1 / 100 + 5.3))

    elif dieta_asignada.get() == "NO":
        edad = int(entry_edad.get())
        prioridad1 = float(edad / 20 + 4)
        return prioridad.set(round(edad/30+3)), riesgo.set(round((edad * prioridad1)/100+5.3))

# funcion REGISTRO datos paciente

def registro_pacientes():
    
    mi_conexion = sqlite3.connect("HOSPITAL")
    mi_cursor = mi_conexion.cursor()

    datos = mi_nombre.get(), mi_edad.get(), mi_num_his.get(), prioridad.get(), riesgo.get()
    mi_cursor.execute("INSERT INTO PACIENTES VALUES (NULL, ?,?,?,?,?)", (datos))
    
    if int(entry_edad.get()) >=1 and int(entry_edad.get()) <=15:
        datos_niños = mi_id.get(), mi_peso.get(), mi_estatura.get()
        mi_cursor.execute("INSERT INTO PACIENTE_NIÑO VALUES (?,?,?)", (datos_niños))

    elif int(entry_edad.get()) >=16 and int(entry_edad.get()) <= 40:
        datos_joven = mi_id.get(), fumador.get()
        mi_cursor.execute("INSERT INTO PACIENTE_JOVEN VALUES (?,?)", (datos_joven))

    elif int(entry_edad.get()) >=41:
        datos_ancianos = mi_id.get(), mi_dieta.get()
        mi_cursor.execute("INSERT INTO PACIENTE_ANCIANO VALUES (?,?)", (datos_ancianos)) 
  
  
    mi_conexion.commit()

    messagebox.showinfo("BBDD", "Registro Exitoso")

def Listar_Pacientes_Mayor_Riesgo():
    
    mi_conexion = sqlite3.connect("HOSPITAL")
    
    sql = []
    sql= "SELECT * FROM PACIENTES WHERE NUMERO_HIS="
    
    mi_cursor = mi_conexion.cursor(sql)
    
    listaP=mi_cursor.fetchall()

    for i in listaP:
        print(i)

    mi_conexion.commit()





# ventana consultas

def ventanaConsulta():

    consultas = Toplevel(root)
    root.iconify()
    consultas.title("CONSULTAS")
    consultas.config(bg='#55B4B0')
    
    #zona de label
    
    label_id_consulta=Label(consultas,text='Id:')
    label_id_consulta.grid(row=0, column=0, sticky="e", padx=10, pady=10)
    
    label_cant_pacientes=Label(consultas,text='Cant Pacientes:')
    label_cant_pacientes.grid(row=1, column=0, sticky="e", padx=10, pady=10)
    
    label_nombre_especialista=Label(consultas,text='Nombre Especialista:')
    label_nombre_especialista.grid(row=2, column=0, sticky="e", padx=10, pady=10)
    
    label_tipo_consulta=Label(consultas,text='Tipo Consulta:')
    label_tipo_consulta.grid(row=3, column=0, sticky="e", padx=10, pady=10)

    label_estado_consulta=Label(consultas,text='Estado Consulta:')
    label_estado_consulta.grid(row=4, column=0, sticky="e", padx=10, pady=10)
    
    # zona de entry

    entry_id_consulta = Entry(consultas)
    entry_id_consulta.grid(row=0, column=1, padx=10, pady=10)
    
    label_cant_pacientes=Label(consultas, bg='yellow')
    label_cant_pacientes.grid(row=1, column=1, sticky="e", padx=10, pady=10)

    entry_nombre_especialista = Entry(consultas)
    entry_nombre_especialista.grid(row=2, column=1, padx=10, pady=10)

    tipo_consulta = ttk.Combobox(consultas, width=17, state="readonly")
    tipo_consulta.place(x=30, y=77)
    tipo_consulta.grid(row=3, column=1)

    valores_lista = ["PEDIATRIA", "URGENCIAS", "MEDICINA INT"]

    tipo_consulta['values']=valores_lista
    
    label_estado_consulta=Label(consultas, bg='yellow')
    label_estado_consulta.grid(row=4, column=1, sticky="e", padx=10, pady=10)

    #zona botones

    boton_consulta = Button(consultas, text ="listaMayorRiesgo", command=Listar_Pacientes_Mayor_Riesgo)
    boton_consulta.grid(row=5, column =0, sticky="e", padx=10, pady=10)


  
# aqui empieza el root  
    
root = Tk()

mi_nombre = StringVar()
mi_edad = StringVar()
mi_num_his = StringVar()
prioridad = StringVar()
riesgo = StringVar()
mi_dieta = StringVar()
mi_id = StringVar()
fumador = StringVar()
mi_peso = StringVar()
mi_estatura = StringVar()

# frame centro

mi_frame = Frame(root, width = 300, height = 300)
mi_frame.pack()


# zona de labels

label_numero_historia = Label(mi_frame, text = "Numero_H_Clinica")
label_numero_historia.grid(row=0, column=0, sticky="e", padx=10, pady=10)

label_nombre = Label(mi_frame, text = "Nombre")
label_nombre.grid(row=1, column=0, sticky="e", padx=10, pady=10)

label_edad = Label(mi_frame, text = "Edad")
label_edad.grid(row=2, column=0, sticky="e", padx=10, pady=10)

label_prioridad = Label(mi_frame, text = "Prioridad:")
label_prioridad.grid(row=0, column=2, sticky="e", padx=10, pady=10)

label_riesgo = Label(mi_frame, text="Riesgo:")
label_riesgo.grid(row=1, column=2, sticky="e", padx=10, pady=10)

label_peso = Label(mi_frame, text="Peso:")
label_peso.grid(row=3, column=0, sticky="e", padx=10, pady=10)

label_tipo_consul = Label(mi_frame, text="Estatura:")
label_tipo_consul.grid(row=4, column=0, sticky="e", padx=10, pady=10)

label_fumador = Label(mi_frame, text="Fumador:")
label_fumador.grid(row=5, column=0, sticky="e", padx=10, pady=10)

label_años_fum = Label(mi_frame, text="Años fumando:")
label_años_fum.grid(row=5, column=2, sticky="e", padx=10, pady=10)

label_dieta_asig = Label(mi_frame, text="Dieta Asignada:")
label_dieta_asig.grid(row=6, column=0, sticky="e", padx=10, pady=10)

label_id = Label(mi_frame, text= "ID:")
label_id.grid(row=2, column=2, sticky="e", padx=10, pady=10)

# zona de los entry

entry_numero_historia = Entry(mi_frame, textvariable=mi_num_his)
entry_numero_historia.grid(row=0, column=1, padx=10, pady=10)

entry_nombre = Entry(mi_frame, textvariable=mi_nombre)
entry_nombre.grid(row=1, column=1, padx=10, pady=10)

entry_edad = Entry(mi_frame, textvariable=mi_edad)
entry_edad.grid(row=2, column=1, padx=10, pady=10)
    
label_prioridad = Label(mi_frame, textvariable= prioridad)
label_prioridad.grid(row=0, column=3, padx=10, pady=10)

label_riesgo = Label(mi_frame, textvariable= riesgo)
label_riesgo.grid(row=1, column=3, padx=10, pady=10)

entry_peso = Entry(mi_frame, textvariable=mi_peso)
entry_peso.grid(row=3, column=1, padx=10, pady=10)

entry_estatura = Entry(mi_frame, textvariable=mi_estatura)
entry_estatura.grid(row=4, column=1, padx=10, pady=10)

entry_id = Entry(mi_frame, textvariable = mi_id)
entry_id.grid(row=2, column=3, padx=10, pady=10)

# lista desp fumador si o no

fumador_si_no = ttk.Combobox(mi_frame, width=17, state="readonly", textvariable = fumador)
fumador_si_no.place(x=30, y=77)
fumador_si_no.grid(row=5, column=1)

valores_lista = ["SI","NO"]

fumador_si_no['values']=valores_lista

# lista desp dieta_asignada o no

dieta_asignada =ttk.Combobox(mi_frame, width=17, state="readonly", textvariable = mi_dieta)
dieta_asignada.place(x=30, y=77)
dieta_asignada.grid(row=6, column=1)

valores_lista = ["SI","NO"]

dieta_asignada['values']=valores_lista

# entry.. años de fumando
entry_añosFumando = Entry(mi_frame)
entry_añosFumando.grid(row=5, column=3, padx=10, pady=10)

# botones inferiores

mi_frame_inferior = Frame(root)
mi_frame_inferior.pack()

registroPaciente = Button(mi_frame_inferior, text ="crear BBDD", command=crearBBDD)
registroPaciente.grid(row=1, column =1, sticky="e", padx=10, pady=10)

boton_calculo_registro = Button(mi_frame_inferior, text ="Calcular Datos", command = calcular_prio_ries)
boton_calculo_registro.grid(row=1, column =2, sticky="e", padx=10, pady=10)

boton_niño = Button(mi_frame_inferior, text ="REGISTRAR PACIENTE", command= registro_pacientes)
boton_niño.grid(row=1, column =3, sticky="e", padx=10, pady=10)

boton_consulta = Button(mi_frame_inferior, text ="CONSULTAS", command=ventanaConsulta)
boton_consulta.grid(row=1, column =4, sticky="e", padx=10, pady=10)

root.mainloop()