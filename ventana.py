from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from clasificacion import Clasificacion

class Ventana(Frame):

    jugadores = Clasificacion()

    #Ventana principal
    def __init__(self, master=None):

        super().__init__(master,width=610, height=246)
        self.master = master
        self.pack()
        self.create_widgets()
        #Variables de clase
        self.id = "----"
        self.seleccion_combo = "Insular"
        #Rellenar la tabla
        self.llenaClasificacion()
        self.habilitarCajas("disabled")
        self.habilitarBotonesGuardar("disabled")

    ##############UTILS###################################
    def habilitarCajas(self,estado):

        self.txtNombre.configure(state=estado)
        self.txtPuntos.configure(state=estado)
        self.txtExacto.configure(state=estado)
        self.txtDoble.configure(state=estado)

    def habilitarBotonesOperaciones(self,estado):

        self.btnNuevo.configure(state=estado)
        self.btnModificar.configure(state=estado)
        self.btnEliminar.configure(state=estado)
        self.btnOrdenar.configure(state=estado)
        self.combo.configure(state=estado)
        self.btnSeleccionar.configure(state=estado)
    
    def habilitarBotonesGuardar(self,estado):

        self.btnGuardar.configure(state=estado)
        self.btnCancelar.configure(state=estado)
    
    def limpiarCajas(self):

        self.txtNombre.delete(0,END)
        self.txtPuntos.delete(0,END)
        self.txtExacto.delete(0,END)
        self.txtDoble.delete(0,END)

    def llenaClasificacion(self):
        
        #Limpiamos la ListView
        for item in self.grid.get_children():
            self.grid.delete(item)
        #Recogemos los datos de la base de datos
        datos = self.jugadores.consulta_clasificacion()
        #Ver que clasificación está seleccionada
        for row in datos:
            if self.seleccion_combo == "Insular":
                self.grid.insert("",END,text=row[0], values=(row[1],row[2],row[3]))
            elif self.seleccion_combo == "Regional":
                self.grid.insert("",END,text=row[0], values=(row[4],row[5],row[6]))
            else:
                self.jugadores.modifica_jugador(row[0],row[1]+row[4],row[2]+row[5],row[3]+row[6],self.seleccion_combo)                                           
                self.grid.insert("",END,text=row[0], values=(row[1]+row[4],row[2]+row[5],row[3]+row[6]))

        if len(self.grid.get_children()) > 0:
            self.grid.selection_clear
            self.id = "----"

    def habilitarGuardado(self, flagGuardar):

        #Forzar el habilitado de Nombre para el caso Modificar
        self.txtNombre.configure(state="normal")
        self.limpiarCajas()
        self.txtNombre.focus()
    
        if flagGuardar:
            self.habilitarCajas("normal")
            self.habilitarBotonesOperaciones("disabled")
            self.habilitarBotonesGuardar("normal")
        else:
            self.habilitarCajas("disabled")
            self.habilitarBotonesOperaciones("normal")
            self.habilitarBotonesGuardar("disabled")

    ##############COMMANDS###################################
    def fNuevo(self):

        self.habilitarGuardado(True)

    def fModificar(self):
        
        selected = self.grid.focus()
        clave = self.grid.item(selected,'text')

        if clave == '':
            messagebox.showwarning("Modificar","Debes seleccionar un jugador de la lista para ser modificado.")
        else:
            self.id = clave
            valores = self.grid.item(selected, 'values')

            self.habilitarGuardado(True)

            self.txtNombre.insert(0,clave)
            self.txtPuntos.insert(0,valores[0])
            self.txtExacto.insert(0,valores[1])
            self.txtDoble.insert(0,valores[2])

            #En el caso de modificar el Nombre debe de quedar seguro, por lo que hay que deshabilitar la caja
            self.txtNombre.configure(state="disabled")

    def fEliminar(self):

        selected = self.grid.focus()
        clave = self.grid.item(selected,'text')

        if clave == '':
            messagebox.showwarning("Eliminar","Debes seleccionar un jugador de la lista para ser eliminado.")
        else:
            asnwer = messagebox.askquestion("Eliminar","¿Deseas eliminar el jugador seleccionado: " + clave + "?")
            if asnwer == messagebox.YES:
                n = self.jugadores.elimina_jugador(clave)
                if n == 1:
                    messagebox.showinfo("Eliminar", "El jugador: " + clave + " fue eliminado correctamente.")
                    self.llenaClasificacion()
                else:
                    messagebox.showerror("Eliminar","No fue posible eliminar al jugador, por favor intente de nuevo.")

    def fOrdenar(self):
        
        #Ordenar la clasificacion dependiendo de la selección
        if self.seleccion_combo == "Insular":
            self.jugadores.ordena_clasificacion("Puntos_Insular","Exacto_Insular")    
        elif self.seleccion_combo == "Regional":
            self.jugadores.ordena_clasificacion("Puntos_Regional","Exacto_Regional")
        else:
            self.jugadores.ordena_clasificacion("Puntos_General","Exacto_General")                            
        self.llenaClasificacion()

    def fSeleccionar(self):
        
        self.seleccion_combo = self.combo.get()
        self.llenaClasificacion()
        #En caso de seleccionar General, que no se pueda realizar acciones
        if self.seleccion_combo == "General":
            self.habilitarBotonesOperaciones("disabled")
            self.btnOrdenar.configure(state="normal")
            self.combo.configure(state="normal")
            self.btnSeleccionar.configure(state="normal")
        else:
            self.habilitarBotonesOperaciones("normal")
            
    def fGuardar(self):

        #Validar que todos los campos estén llenos
        if all([self.txtNombre.get(), self.txtPuntos.get(), self.txtExacto.get(), self.txtDoble.get()]):
            
            try:
                puntos = int(self.txtPuntos.get())
                exacto = int(self.txtExacto.get())
                doble = int(self.txtDoble.get())
                operacionOk = True

                #En caso de que id sea ---- es que es un nuevo jugador, si no es modificar 
                if self.id == "----":
                    #Solo crear el nuevo jugador si aún no existe
                    if not self.jugadores.busca_jugador(self.txtNombre.get()):
                    
                        # Validar tipos de datos
                        if isinstance(self.txtNombre.get(), str) and not self.txtNombre.get().isdigit() and all(isinstance(x, int) for x in [puntos, exacto, doble]):

                            self.jugadores.inserta_jugador(self.txtNombre.get(),puntos,exacto, doble, self.seleccion_combo)                                                      
                            messagebox.showinfo("Nuevo", "El jugador: " + self.txtNombre.get() + " fue añadido correctamente.")
                        else:
                            messagebox.showerror("Nuevo","El campo 'Nombre' debe ser una cadena (str) y los campos 'Puntos', 'Exacto' y 'Dobles' deben ser enteros (int).")
                            operacionOk = False
                    else:
                        messagebox.showerror("Nuevo", "El jugador: " + self.txtNombre.get() + " ya está creado, por favor intente de nuevo.")
                        operacionOk = False
                else:
                    #Caso de Modificar
                    self.jugadores.modifica_jugador(self.txtNombre.get(),self.txtPuntos.get(),
                                                self.txtExacto.get(),self.txtDoble.get(),self.seleccion_combo)
                    messagebox.showinfo("Modificar", "El jugador: " + self.id + " fue modificado correctamente.")
                    self.id == "----"

            except ValueError:
                messagebox.showerror("Error", "Por favor, introduce valores numéricos válidos en los campos 'Puntos', 'Exacto' y 'Dobles'.")
                operacionOk = False
            
        else:
            messagebox.showerror("Error","Todos los campos deben estar llenos.")
            operacionOk = False
        
        if operacionOk:
            self.llenaClasificacion()
            self.habilitarGuardado(False)

    def fCancelar(self):
        
        asnwer = messagebox.askquestion("Cancelar","¿Deseas cancelar la operación seleccionada?")
        if asnwer == messagebox.YES:
            self.habilitarGuardado(False)

    ##############INTERFACE###################################
    def create_widgets(self):
        #Frame Botones###############################################################################################
        frameBotones = Frame(self, bg="lightyellow")
        frameBotones.place(x=0, y=0, width=140, height=246)
        #Botón Nuevo
        self.btnNuevo = Button(frameBotones,text="Nuevo" , command=self.fNuevo, bg = "yellow", fg="blue")
        self.btnNuevo.place(x=25, y=15, width=80, height=25)
        #Botón Modificar
        self.btnModificar = Button(frameBotones,text="Modificar" , command=self.fModificar, bg = "yellow", fg="blue")
        self.btnModificar.place(x=25, y=45, width=80, height=25)
        #Botón Eliminar
        self.btnEliminar = Button(frameBotones,text="Eliminar" , command=self.fEliminar, bg = "yellow", fg="blue")
        self.btnEliminar.place(x=25, y=75, width=80, height=25)
        #Botón Ordenar
        self.btnOrdenar = Button(frameBotones,text="Ordenar" , command=self.fOrdenar, bg = "yellow", fg="blue")
        self.btnOrdenar.place(x=25, y=105, width=80, height=25)
        #Combo Label
        self.labelCombo = Label(frameBotones, text="Selecciona una opción:", bg="lightyellow", fg="navy")
        self.labelCombo.place(x=5, y=150)
        #Combo Box Clasificaciones
        self.combo = ttk.Combobox(frameBotones, values=["Insular", "Regional", "General"], state="readonly")
        self.combo.set("Insular")
        self.combo.place(x=25, y=175, width=80, height=25)
        #Botón Seleccionar
        self.btnSeleccionar = Button(frameBotones,text="Seleccionar" , command=self.fSeleccionar, bg = "yellow", fg="blue")
        self.btnSeleccionar.place(x=25, y=205, width=80, height=25)
        ##############################################################################################################
        #Frame Texto##################################################################################################
        frameTexto = Frame(self, bg="skyblue")
        frameTexto.place(x=140, y=0, width=150, height=246)
        #Label Nombre
        lbl1 = Label(frameTexto, text="NOMBRE: ", bg="skyblue", fg="navy")
        lbl1.place(x=3, y=5)
        self.txtNombre = Entry(frameTexto)
        self.txtNombre.place(x=3, y=25, width=140, height=20)
        #Label Puntos
        lbl2 = Label(frameTexto, text="PUNTOS: ", bg="skyblue", fg="navy")
        lbl2.place(x=3, y=55)
        self.txtPuntos = Entry(frameTexto)
        self.txtPuntos.place(x=3, y=75, width=140, height=20)
        #Label Exacto
        lbl3 = Label(frameTexto, text="EXACTO: ", bg="skyblue", fg="navy")
        lbl3.place(x=3, y=105)
        self.txtExacto = Entry(frameTexto)
        self.txtExacto.place(x=3, y=125, width=140, height=20)
        #Label Doble
        lbl4 = Label(frameTexto, text="DOBLE: ", bg="skyblue", fg="navy")
        lbl4.place(x=3, y=155)
        self.txtDoble = Entry(frameTexto)
        self.txtDoble.place(x=3, y=175, width=140, height=20)
        #Botón Guardar
        self.btnGuardar = Button(frameTexto,text="Guardar" , command=self.fGuardar, bg = "green", fg="white")
        self.btnGuardar.place(x=10, y=210, width=60, height=30)
        #Botón Cancelar
        self.btnCancelar = Button(frameTexto,text="Cancelar" , command=self.fCancelar, bg = "red", fg="white")
        self.btnCancelar.place(x=80, y=210, width=60, height=30)
        #Frame Grid###############################################################################################
        frameTreeView = Frame(self, bg="yellow")
        frameTreeView.place(x=290, y=0, width=320, height=246)
        ##############################################################################################################
        #Grid#########################################################################################################
        style = ttk.Style()
        #Cambia los colores del encabezado
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), foreground="darkblue", background="blue")  
        self.grid = ttk.Treeview(frameTreeView , columns=("col1","col2","col3"))
        self.grid.column("#0",      width=106)
        self.grid.column("col1",    width=65, anchor=CENTER)
        self.grid.column("col2",    width=65, anchor=CENTER)
        self.grid.column("col3",    width=65, anchor=CENTER)
        self.grid.heading("#0",     text="NOMBRE",    anchor=CENTER)
        self.grid.heading("col1",   text="PUNTOS",    anchor=CENTER)
        self.grid.heading("col2",   text="EXACTO",    anchor=CENTER)
        self.grid.heading("col3",   text="DOBLES",    anchor=CENTER)
        self.grid.pack(side=LEFT, fill = Y)
        self.grid['selectmode']='browse'
        #Scrollbar
        sb = Scrollbar(frameTreeView, orient=VERTICAL)
        sb.pack(side=RIGHT, fill = Y)
        self.grid.config(yscrollcommand=sb.set)
        sb.config(command=self.grid.yview)