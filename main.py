from tkinter import *
from ventana import *

# Función main
def main():
    root = Tk()
    root.wm_title("Clasificación Terrero y Gloria")
    app = Ventana(root)  # Asumiendo que la clase Ventana está definida en el archivo ventana.py
    app.mainloop()

# Ejecución del archivo
if __name__ == "__main__":
    main()
