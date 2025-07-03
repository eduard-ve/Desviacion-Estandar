import mysql.connector
import numpy as np
from datetime import datetime
from config.config import DATABASE_CONFIG, DATABASE_NAME, CREATE_TABLE_QUERY

# Clase maneja la base de datos
class BaseDatos:
    def __init__(self):
        self.conexion = None
        self.cursor = None
        self.conectar()
        self.crear_tabla()
    
    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(**DATABASE_CONFIG)
            self.cursor = self.conexion.cursor()
            print("Conexión exitosa a la base de datos")
        except mysql.connector.Error as error:
            print(f"Error al conectar: {error}")
            print("Creando base de datos...")
            self.crear_base_datos()
    
    def crear_base_datos(self):
        try:
            # Conexión nueva base de datos
            config_temp = DATABASE_CONFIG.copy()
            del config_temp['database']
            
            conexion_temp = mysql.connector.connect(**config_temp)
            cursor_temp = conexion_temp.cursor()
            cursor_temp.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
            cursor_temp.close()
            conexion_temp.close()
            
            self.conectar()
        except mysql.connector.Error as error:
            print(f"Error creando base de datos: {error}")
    
    def crear_tabla(self):
        try:
            self.cursor.execute(CREATE_TABLE_QUERY)
            self.conexion.commit()
        except mysql.connector.Error as error:
            print(f"Error creando tabla: {error}")
    
    def guardar_analisis(self, dataset, media, desviacion, cantidad, tipo):
        #Guarda el análisis en la base de datos
        query = """
        INSERT INTO analisis (dataset, media, desviacion_estandar, cantidad_datos, fecha, tipo_calculo)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        fecha_actual = datetime.now()
        datos_str = ','.join(map(str, dataset))
        
        try:
            self.cursor.execute(query, (datos_str, media, desviacion, cantidad, fecha_actual, tipo))
            self.conexion.commit()
            return True
        except mysql.connector.Error as error:
            print(f"Error guardando análisis: {error}")
            return False
    
    def obtener_historial(self):
        query = "SELECT * FROM analisis ORDER BY fecha DESC"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"Error obteniendo historial: {error}")
            return []
    
    def obtener_estadisticas_generales(self):
        queries = {
            'total_analisis': "SELECT COUNT(*) FROM analisis",
            'total_datos': "SELECT SUM(cantidad_datos) FROM analisis",
            'mas_reciente': "SELECT fecha FROM analisis ORDER BY fecha DESC LIMIT 1",
            'mas_antiguo': "SELECT fecha FROM analisis ORDER BY fecha ASC LIMIT 1"
        }
        
        estadisticas = {}
        for nombre, query in queries.items():
            try:
                self.cursor.execute(query)
                resultado = self.cursor.fetchone()
                estadisticas[nombre] = resultado[0] if resultado and resultado[0] else 0
            except mysql.connector.Error as error:
                print(f"Error en estadística {nombre}: {error}")
                estadisticas[nombre] = 0
        
        return estadisticas
    
    def eliminar_todos_los_datos(self):
        try:
            self.cursor.execute("DELETE FROM analisis")
            self.conexion.commit()
            return True
        except mysql.connector.Error as error:
            print(f"Error eliminando datos: {error}")
            return False
    
    def cerrar_conexion(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()

# Clase principal que contiene los calculos manual y numpy
class CalculadoraEstadisticas:
    def __init__(self):
        pass
    
    #Calcular media 
    def calcular_media_manual(self, datos):
        suma = 0
        for numero in datos:
            suma += numero
        media = suma / len(datos)
        return media
    
    #Calcula la desviación estándar de forma manual
    def calcular_desviacion_manual(self, datos):
        # Paso 1: Calcular la media
        media = self.calcular_media_manual(datos)
        
        # Paso 2: Calcular la suma de diferencias al cuadrado
        suma_diferencias = 0
        for numero in datos:
            diferencia = numero - media
            diferencia_cuadrada = diferencia ** 2
            suma_diferencias += diferencia_cuadrada
        
        # Paso 3: Calcular la varianza
        varianza = suma_diferencias / len(datos)
        
        # Paso 4: Calcular la desviación estándar (raíz cuadrada de la varianza)
        desviacion = varianza ** 0.5
        return desviacion
    
    # Calcula media y desviación usando NumPy
    def calcular_con_numpy(self, datos):
        array_datos = np.array(datos)
        media = np.mean(array_datos)
        desviacion = np.std(array_datos)
        return media, desviacion