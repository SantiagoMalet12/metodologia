import mysql.connector
from mysql.connector import Error

try:
    # 1. Establecer la conexión con los datos de tu Workbench
    conexion = mysql.connector.connect(
        host='localhost',          # O '127.0.0.1'
        user='root',               # Tu usuario de MySQL
        password='12345',  # Cambia esto por tu contraseña real
        database='tp_metodologia'       # Tu base de datos creada en Workbench
    )

    if conexion.is_connected():
        cursor = conexion.cursor()

        # 1. Definir la consulta SQL con marcadores de posición (%s)
        # Reemplaza 'usuarios', 'nombre' y 'email' con los nombres reales de tu tabla y columnas
        sql_insertar = "INSERT INTO resultado (idejercicio, nombreia, resultado, tiempoejercicio) VALUES (%s, %s, %s, %s)"

        # 2. Los datos reales que vas a meter (en una tupla)
        valores = (
            "EJ-001",        # idejercicio (VARCHAR)
            "Rutina_A",      # nombreia (VARCHAR)
            "Completado",    # resultado (VARCHAR)
            "00:45:00"       # tiempoejercicio (TIME -> Formato HH:MM:SS para 45 minutos)
        )

        # 3. Ejecutar la consulta pasando el SQL y los valores por separado
        cursor.execute(sql_insertar, valores)

        # 4. ¡EL PASO CLAVE! Confirmar y guardar los cambios en la base de datos
        conexion.commit()

        print(f"¡Registro insertado con éxito! Filas afectadas: {cursor.rowcount}")

except Error as e:
    print(f"Error al conectar a MySQL: {e}")

finally:
    # 3. Importante: Siempre cerrar la conexión al terminar
    if 'conexion' in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión cerrada limpiamente.")