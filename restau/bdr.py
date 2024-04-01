import sqlite3
conn = sqlite3.connect("restaurante.db")

conn.execute(
    """
    CREATE TABLE PLATOS
    (id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio DECIMAL NOT NULL,
    categoria TEXT NOT NULL);
    """
)


conn.execute(
    """
    INSERT INTO PLATOS (nombre, precio, categoria) 
    VALUES ('Pizza', 10.99, 'Italiana')
    """
)
conn.execute(
    """
    INSERT INTO PLATOS (nombre, precio, categoria) 
    VALUES ('Hamburguesa', 8.99, 'Americana')
    """
)
conn.execute(
    """
    INSERT INTO PLATOS (nombre, precio, categoria) 
    VALUES ('Sushi', 12.99, 'Japonesa')
    """
)
conn.execute(
    """
    INSERT INTO PLATOS (nombre, precio, categoria) 
    VALUES ('Ensalada', 6.99, 'Vegetariana')
    """
)

print("PLATOS:")
cursor = conn.execute("SELECT * FROM PLATOS")
for row in cursor:
    print(row)


conn.execute(
    """
    CREATE TABLE MESAS
    (id INTEGER PRIMARY KEY,
    numero INTEGER NOT NULL);
    """
)

conn.execute(
    """
    INSERT INTO MESAS (numero) 
    VALUES (1)
    """
)
conn.execute(
    """
    INSERT INTO MESAS (numero) 
    VALUES (2)
    """
)
conn.execute(
    """
    INSERT INTO MESAS (numero) 
    VALUES (3)
    """
)
conn.execute(
    """
    INSERT INTO MESAS (numero) 
    VALUES (4)
    """
)

print("\nMESAS:")
cursor = conn.execute("SELECT * FROM MESAS")
for row in cursor:
    print(row)


conn.execute(
    """
    CREATE TABLE PEDIDOS
    (id INTEGER PRIMARY KEY,
    platos_id INTEGER NOT NULL,
    mesas_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (platos_id) REFERENCES PLATOS(id),
    FOREIGN KEY (mesas_id) REFERENCES MESAS(id));
    """
)

# Insertar datos de matriculación
conn.execute(
    """
    INSERT INTO PEDIDOS (platos_id, mesas_id, cantidad, fecha) 
    VALUES (1, 2, 2, '2024-04-01')
    """
)
conn.execute(
    """
    INSERT INTO PEDIDOS (platos_id, mesas_id, cantidad, fecha) 
    VALUES (2, 3, 1,'2024-04-01')
    """
)

conn.execute(
    """
    INSERT INTO PEDIDOS (platos_id, mesas_id, cantidad, fecha) 
    VALUES (3, 1, 3, '2024-04-02')
    """
)

conn.execute(
    """
    INSERT INTO PEDIDOS (platos_id, mesas_id, cantidad, fecha) 
    VALUES (4, 4, 1, '2024-04-02')
    """
)


print("\nPEDIDOS:")
cursor = conn.execute(
    """
    SELECT PLATOS.nombre, MESAS.numero, PEDIDOS.cantidad, PEDIDOS.fecha 
    FROM PEDIDOS
    JOIN PLATOS ON PEDIDOS.platos_id = PLATOS.id 
    JOIN MESAS ON PEDIDOS.mesas_id = MESAS.id
    """
)
for row in cursor:
    print(row)


# Cerrar conexión
conn.close()



