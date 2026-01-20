import mysql.connector
import os

# Configuración de tu conexión a Aiven
config = {
    'user': 'avnadmin',
    'password': 'AVNS_pFwiEHMe7XalGTeSN7l',
    'host': 'db-conecta-joven-snunedi-afb6.j.aivencloud.com',
    'port': 18771,
    'database': 'defaultdb',
    'ssl_ca': 'ca.pem'
}

def ejecutar_migracion():
    try:
        # 1. Leer el archivo SQL de XAMPP
        print("Buscando el archivo conecta_joven_db.sql...")
        if not os.path.exists('conecta_joven_db.sql'):
            print("ERROR: No se encuentra el archivo 'conecta_joven_db.sql' en esta carpeta.")
            return

        with open('conecta_joven_db.sql', 'r', encoding='utf8') as f:
            sql_file = f.read()
            # Separamos el archivo por el punto y coma
            comandos = sql_file.split(';')

        # 2. Conectar a Aiven
        print("Conectando a la base de datos en Aiven...")
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # --- PASO CLAVE PARA AIVEN ---
        # Desactivamos la restricción de Primary Key para que acepte la estructura de XAMPP
        print("Configurando sesión de Aiven para permitir la importación...")
        cursor.execute("SET SESSION sql_require_primary_key = 0;")

        # 3. Ejecutar los comandos uno por uno
        print("Iniciando migración de tablas (esto puede tardar)...")
        cont_exito = 0
        for comando in comandos:
            cmd_limpio = comando.strip()
            
            # Saltamos comandos problemáticos o vacíos
            if not cmd_limpio or any(x in cmd_limpio.upper() for x in ["CREATE DATABASE", "USE ", "SET SQL_MODE"]):
                continue
            
            try:
                cursor.execute(cmd_limpio)
                cont_exito += 1
            except Exception as e:
                # Si la tabla ya existe, no lo mostramos como error crítico
                if "already exists" in str(e):
                    continue
                else:
                    print(f"Nota en comando: {e}")

        conn.commit()
        print("\n" + "="*50)
        print(f"¡PROCESO FINALIZADO!")
        print(f"Se ejecutaron {cont_exito} comandos exitosamente.")
        print("Tus tablas p_001_... deberían estar listas en la nube.")
        print("="*50)

    except Exception as e:
        print(f"ERROR CRÍTICO: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    ejecutar_migracion()