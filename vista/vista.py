import matplotlib.pyplot as plt
from datetime import datetime

class Vista:
    def __init__(self):
        pass
    
    def mostrar_menu_principal(self):
        print("\n" + "="*50)
        print("    CALCULADORA DE DESVIACIÓN ESTÁNDAR")
        print("="*50)
        print("1. Calcular desviación de forma manual")
        print("2. Calcular con librería NumPy")
        print("3. Ver historial de análisis")
        print("4. Eliminar todos los datasets")
        print("5. Salir")
        print("="*50)
    
    def solicitar_opcion(self):
        while True:
            try:
                opcion = int(input("Seleccione una opción (1-5): "))
                if 1 <= opcion <= 5:
                    return opcion
                else:
                    print(" Opción inválida. Ingrese un número del 1 al 5.")
            except ValueError:
                print("Por favor ingrese un número válido.")
    
    def solicitar_datos(self):
        print("\n--- INGRESAR DATOS ---")
        print("Ingrese los números. Escriba 'f' para terminar.")
        datos = []
        
        while True:
            entrada = input(f"Dato {len(datos) + 1}: ")
            
            # Si el usuario escribe 'f', terminamos la lista de numeros(f de fin)
            if entrada.lower() == 'f':
                if len(datos) >= 2:
                    break
                else:
                    print("Necesita al menos 2 datos para calcular.")
                    continue
            
            # Intentar convertir la entrada a número
            try:
                numero = float(entrada)
                datos.append(numero)
                print(f"Dato agregado: {numero}")
            except ValueError:
                print("Ingrese un número válido o 'f' para terminar.")
        
        return datos
    
    def mostrar_tabla_analisis(self, datos, media, desviacion, tipo_calculo):
        print("\n" + "="*40)
        print("           ANÁLISIS")
        print("="*40)
        print(f"{'Métrica':<20} {'Valor':<15}")
        print("-" * 40)
        print(f"{'Media':<20} {media:.4f}")
        print(f"{'Desviación Estándar':<20} {desviacion:.4f}")
        print(f"{'Cantidad de Datos':<20} {len(datos)}")
        print(f"{'Fecha':<20} {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'Tipo de Cálculo':<20} {tipo_calculo}")
        print("="*40)
        print(f"Datos utilizados: {datos}")
    
    def mostrar_historial(self, historial):
        if not historial:
            print("\nNo hay análisis en el historial.")
            return
        
        print("\n" + "="*80)
        print("                    HISTORIAL DE ANÁLISIS")
        print("="*80)
        print(f"{'ID':<3} {'Dataset':<20} {'Media':<8} {'Desv.Est':<8} {'Cant':<4} {'Fecha':<16} {'Tipo':<8}")
        print("-" * 80)
        
        for registro in historial:
            id_analisis = registro[0]
            dataset = registro[1][:17] + "..." if len(registro[1]) > 20 else registro[1]
            media = registro[2]
            desviacion = registro[3]
            cantidad = registro[4]
            fecha = registro[5].strftime('%Y-%m-%d %H:%M')
            tipo = registro[6]
            
            print(f"{id_analisis:<3} {dataset:<20} {media:<8.2f} {desviacion:<8.2f} {cantidad:<4} {fecha:<16} {tipo:<8}")
    
    def mostrar_estadisticas_generales(self, estadisticas):
        print("\n" + "="*50)
        print("           ESTADÍSTICAS GENERALES")
        print("="*50)
        print(f"Total de análisis: {estadisticas['total_analisis']}")
        print(f"Total datos procesados: {estadisticas['total_datos']}")
        
        if estadisticas['mas_reciente']:
            print(f"Análisis más reciente: {estadisticas['mas_reciente']}")
        else:
            print("Análisis más reciente: N/A")
            
        if estadisticas['mas_antiguo']:
            print(f"Análisis más antiguo: {estadisticas['mas_antiguo']}")
        else:
            print("Análisis más antiguo: N/A")
        print("="*50)
    
    # Crea y muestra el gráfico de los datos analizados
    def crear_grafico(self, datos, media, desviacion, tipo_calculo):
        plt.figure(figsize=(8, 4))
        
        # Subgráfico 1: Línea de datos
        plt.subplot(1, 2, 1)
        plt.plot(range(1, len(datos) + 1), datos, 'bo-', linewidth=2, markersize=8)
        plt.axhline(y=media, color='r', linestyle='--', linewidth=2, label=f'Media: {media:.2f}')
        plt.title(f'Datos Analizados - {tipo_calculo}')
        plt.xlabel('Número de Dato')
        plt.ylabel('Valor')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Subgráfico 2: Histograma
        plt.subplot(1, 2, 2)
        n_bins = min(10, len(datos)//2 + 1) if len(datos) > 4 else 3
        plt.hist(datos, bins=n_bins, alpha=0.7, color='skyblue', edgecolor='black')
        plt.axvline(media, color='r', linestyle='--', linewidth=2, label=f'Media: {media:.2f}')
        plt.axvline(media + desviacion, color='orange', linestyle=':', linewidth=2, 
                   label=f'+1σ: {media + desviacion:.2f}')
        plt.axvline(media - desviacion, color='orange', linestyle=':', linewidth=2,
                   label=f'-1σ: {media - desviacion:.2f}')
        plt.title('Distribución de los Datos')
        plt.xlabel('Valor')
        plt.ylabel('Frecuencia')
        plt.legend()
        
        plt.tight_layout()
        plt.show()
    
    def confirmar_eliminacion(self):
        while True:
            respuesta = input("¿Está seguro de eliminar todos los datos? (s/n): ").lower()
            if respuesta in ['s', 'si', 'sí']:
                return True
            elif respuesta in ['n', 'no']:
                return False
            else:
                print("Responda 's' para sí o 'n' para no.")
    
    def pausar(self):
        input("\nPresione Enter para continuar...")
    
    def mostrar_mensaje(self, mensaje):
        print(mensaje)