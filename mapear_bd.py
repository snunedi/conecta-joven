import mysql.connector

# Configuración de conexión
db_config = {
    'user': 'avnadmin',
    'password': 'AVNS_pFwiEHMe7XalGTeSN7l',
    'host': 'db-conecta-joven-snunedi-afb6.j.aivencloud.com',
    'port': 18771,
    'database': 'defaultdb',
    'ssl_ca': 'ca.pem'
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 1. Obtener la lista de todas las tablas que empiezan con p_001
    cursor.execute("SHOW TABLES LIKE 'p_001_%'")
    tablas = [t[0] for t in cursor.fetchall()]

    print("=== DICCIONARIO DE DATOS CONECTA JOVEN ===\n")

    for tabla in tablas:
        print(f"TABLA: {tabla}")
        # 2. Obtener columnas, tipos de datos y si son llaves
        cursor.execute(f"DESCRIBE {tabla}")
        columnas = cursor.fetchall()
        
        for col in columnas:
            nombre = col[0]
            tipo = col[1]
            extra = col[3] # Ver si es PRI (Primary Key)
            print(f"  - {nombre} ({tipo}) {'[PK]' if extra == 'PRI' else ''}")
        print("-" * 40)

    conn.close()
except Exception as e:
    print(f"Error al mapear: {e}")