import pyodbc
conn = pyodbc.connect(Driver='{SQL Server}';Server=Tarea_BD;Database=Tarea_1;Trusted_Connection=yes)

cursor = conn.cursor()
cursor.execute("CREATE TABLE Cancion(position int NOT NULL, artist_name VARCHAR(56) NOT NULL, song_name VARCHAR(56) NOT NULL, days int NOT NULL, peak_position int(10), peak_position_time VARCHAR(5), peak_streams int, total_streams int, PRYMARY KEY(id))")
'''
Abrir archivo, separar en tuplas la info y cuadrarla en la tabla
'''