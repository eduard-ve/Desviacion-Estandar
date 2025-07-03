from controlador.controlador import Controlador

#Función principal del programa
def main():
    try:
        controlador = Controlador()
        controlador.ejecutar()
        
    except KeyboardInterrupt:
        print("\n\n Programa interrumpido por el usuario.")# ctrl + c para cerrar
        print("¡Hasta la proxima!")
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        print("Verifica la configuración de la base de datos.")

if __name__ == "__main__":
    main()