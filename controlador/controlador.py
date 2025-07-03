from modelo.modelo import BaseDatos, CalculadoraEstadisticas
from vista.vista import Vista

class Controlador:
    def __init__(self):
        self.base_datos = BaseDatos()
        self.calculadora = CalculadoraEstadisticas()
        self.vista = Vista()
    
    def ejecutar(self):
        self.vista.mostrar_mensaje("Iniciando Calculadora de Desviación Estándar")
        
        while True:
            # Mostrar menú y obtener opción del usuario
            self.vista.mostrar_menu_principal()
            opcion = self.vista.solicitar_opcion()
            
            if opcion == 1:
                self.calcular_manual()
            elif opcion == 2:
                self.calcular_con_numpy()
            elif opcion == 3:
                self.mostrar_historial()
            elif opcion == 4:
                self.eliminar_datos()
            elif opcion == 5:
                self.salir()
                break
    
    def calcular_manual(self):
        self.vista.mostrar_mensaje("\n CÁLCULO MANUAL DE DESVIACIÓN ESTÁNDAR")
        
        datos = self.vista.solicitar_datos()

        # Realizar cálculo manual
        media = self.calculadora.calcular_media_manual(datos)
        desviacion = self.calculadora.calcular_desviacion_manual(datos)
        
        self.vista.mostrar_tabla_analisis(datos, media, desviacion, "Manual")
        self.vista.crear_grafico(datos, media, desviacion, "Cálculo Manual")
        
        # Guardar registros en base de datos
        if self.base_datos.guardar_analisis(datos, media, desviacion, len(datos), "Manual"):
            self.vista.mostrar_mensaje("Análisis guardado correctamente.")
        else:
            self.vista.mostrar_mensaje("Error al guardar el análisis.")
        
        self.vista.pausar()
    
    def calcular_con_numpy(self):
        self.vista.mostrar_mensaje("\n CÁLCULO CON NUMPY")
        
        datos = self.vista.solicitar_datos()
        
        # Realizar cálculos con NumPy
        media, desviacion = self.calculadora.calcular_con_numpy(datos)
        
        self.vista.mostrar_tabla_analisis(datos, media, desviacion, "NumPy")
        self.vista.crear_grafico(datos, media, desviacion, "Cálculo con NumPy")
        
        # Guardar en base de datos
        if self.base_datos.guardar_analisis(datos, media, desviacion, len(datos), "NumPy"):
            self.vista.mostrar_mensaje("Análisis guardado correctamente.")
        else:
            self.vista.mostrar_mensaje("Error al guardar el análisis.")
        
        self.vista.pausar()
    
    def mostrar_historial(self):
        self.vista.mostrar_mensaje("\nHISTORIAL DE ANÁLISIS")
        
        # Obtener datos del historial
        historial = self.base_datos.obtener_historial()
        self.vista.mostrar_historial(historial)
        
        # Obtener y mostrar estadísticas generales
        estadisticas = self.base_datos.obtener_estadisticas_generales()
        self.vista.mostrar_estadisticas_generales(estadisticas)
        
        self.vista.pausar()
    
    def eliminar_datos(self):
        self.vista.mostrar_mensaje("\n ELIMINAR TODOS LOS DATASETS")
        
        # Pedir confirmación al usuario
        if self.vista.confirmar_eliminacion():
            if self.base_datos.eliminar_todos_los_datos():
                self.vista.mostrar_mensaje("Todos los datos han sido eliminados.")
            else:
                self.vista.mostrar_mensaje("Error al eliminar los datos.")
        else:
            self.vista.mostrar_mensaje("Operación cancelada.")
        
        self.vista.pausar()
    
    def salir(self):
        self.vista.mostrar_mensaje("\nCerrando el programa...")
        self.base_datos.cerrar_conexion()
        self.vista.mostrar_mensaje("Conexión cerrada.")