import pymysql

class Clasificacion:

    def __init__(self):
        # Conexión a la base de datos
        self.miConexcion = pymysql.connect(host="localhost", user="root", passwd="Mariana_9128", database="prueba")

    def consulta_clasificacion(self):
        cur = self.miConexcion.cursor()
        cur.execute("SELECT * FROM clasificacion")
        datos = cur.fetchall()     
        cur.close()

        return datos
    
    def ordena_clasificacion(self, columna_puntos, columna_exacto):

        cur = self.miConexcion.cursor()
        #Obtener datos ordenados por puntos
        consulta_sql = f"""
        SELECT * FROM clasificacion 
        ORDER BY {columna_puntos} DESC, {columna_exacto} DESC
        """
        cur.execute(consulta_sql)
        datos = cur.fetchall()
        #Borrar todos los datos de la tabla original
        cur.execute("DELETE FROM clasificacion")
        #Insertar los datos en el nuevo orden
        for fila in datos:
            sql_insert = '''
            INSERT INTO clasificacion (Nombre, Puntos_Insular, Exacto_Insular, Dobles_Insular, Puntos_Regional, Exacto_Regional, Dobles_Regional, Puntos_General, Exacto_General, Dobles_General) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cur.execute(sql_insert, fila)

        self.miConexcion.commit()     
        cur.close()

        return datos

    def inserta_jugador(self, valor_nombre, valor_puntos, valor_exacto, valor_dobles, seleccion):

        cur = self.miConexcion.cursor()
        #Ejecuta la consulta insertando los valores dependiendo de la seleccion
        if seleccion == "Insular":
            sql_insert = '''
            INSERT INTO clasificacion (Nombre, Puntos_Insular, Exacto_Insular, Dobles_Insular) 
            VALUES (%s, %s, %s, %s)
            '''
        else:
            sql_insert = '''
            INSERT INTO clasificacion (Nombre, Puntos_Regional, Exacto_Regional, Dobles_Regional) 
            VALUES (%s, %s, %s, %s)
            '''
        #Ejecuta la consulta pasando los valores como parámetros
        cur.execute(sql_insert, (valor_nombre, valor_puntos, valor_exacto, valor_dobles))
        #Confirma los cambios
        self.miConexcion.commit()
        cur.close()
        #Devuelve el número de filas afectadas
        return cur.rowcount

    def elimina_jugador(self, valor_nombre):

        cur = self.miConexcion.cursor()
        #Ejecuta la consulta eliminando por nombre
        sql='''DELETE FROM clasificacion WHERE Nombre = %s'''
        cur.execute(sql, (valor_nombre))
        #Confirma los cambios
        self.miConexcion.commit()
        cur.close()
        #Devuelve el número de filas afectadas
        return cur.rowcount
    
    def busca_jugador(self, valor_nombre):

        cur = self.miConexcion.cursor()
        #Ejecuta la consulta buscando por nombre
        sql='''SELECT * FROM clasificacion WHERE Nombre = %s'''
        cur.execute(sql, (valor_nombre))
        #Guarda la selección como resultado
        resultado = cur.fetchone()
        cur.close()
        #Devuelve si encontró al jugador
        return resultado is not None
    
    def modifica_jugador(self, valor_nombre, valor_puntos, valor_exacto, valor_dobles, seleccion):

        cur = self.miConexcion.cursor()
        #Ejecuta la consulta modificando los valores dependiendo de la seleccion
        if seleccion == "Insular":
            sql='''UPDATE clasificacion SET Puntos_Insular = %s, Exacto_Insular = %s, Dobles_Insular = %s WHERE Nombre = %s'''
        elif seleccion == "Regional":
            sql='''UPDATE clasificacion SET Puntos_Regional = %s, Exacto_Regional = %s, Dobles_Regional = %s WHERE Nombre = %s'''
        else:
            sql='''UPDATE clasificacion SET Puntos_General = %s, Exacto_General = %s, Dobles_General = %s WHERE Nombre = %s'''
        cur.execute(sql, (valor_puntos, valor_exacto, valor_dobles, valor_nombre))
        #Confirma los cambios
        self.miConexcion.commit()
        cur.close()
        #Devuelve el número de filas afectadas
        return cur.rowcount
