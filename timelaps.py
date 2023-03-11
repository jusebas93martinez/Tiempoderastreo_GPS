import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from geopy import distance
from shapely.geometry import LineString
import folium
import webbrowser
import time
import math
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Cargar la imagen del icono
icono = Image.open('logo.ico')




# Crear la ventana principal de la interfaz gráfica
ventana = tk.Tk()
ventana.title('Tiempo de Rastreo GPS')
# Convertir la imagen a un formato compatible con tkinter
icono_tk = ImageTk.PhotoImage(icono)
# Establecer el icono de la aplicación
ventana.iconphoto(True, icono_tk)



texto_largo = 'Ingresa las coordenadas del punto de posicionamiento para calculas el tiempo de rastreo con las 4 estaciones permanentes mas cercanas al punto del IGAC (t = 65 min +(3 min x (d - 10)) --> RESOLUCIÓN 643 DE 2018)'
# Crear el widget Label para el texto largo
texto_label = tk.Label(ventana, text=texto_largo, wraplength=600, justify='center')
texto_label.pack(pady=(10, 10))

ventana.geometry("800x400")
texto = tk.Label(ventana, text="By Ing Sebastian Martinez", bg="yellow")
texto.pack(side="bottom", anchor="sw")

# Creamos el widget Treeview
tabla = ttk.Treeview(ventana)


def validate_grados(input):
    if input.isdigit():
        if int(input) <= 360:
            return True
        elif int(input) == 0:
            return True
        else:
            return False
    elif input == "":
        return True
    else:
        return False
    
def validate_minutos(input):
    if input.isdigit():
        if int(input) <= 60:
            return True
        elif int(input) == 0:
            return True
        else:
            return False
    elif input == "":
        return True
    else:
        return False

label_latitud = tk.Label(ventana, text="Latitud")
label_latitud.pack()
frame_latitud = tk.Frame(ventana)
frame_latitud.pack()
entry_latitud_grados = tk.Entry(frame_latitud,width=6, validate="key")
entry_latitud_grados.config(validatecommand=(entry_latitud_grados.register(validate_grados), '%P'))
entry_latitud_grados.pack(side=tk.LEFT)
label_latitud_grados = tk.Label(frame_latitud, text="°")
label_latitud_grados.pack(side=tk.LEFT)

entry_latitud_minutos = tk.Entry(frame_latitud,width=6, validate="key")
entry_latitud_minutos.config(validatecommand=(entry_latitud_minutos.register(validate_minutos), '%P'))
entry_latitud_minutos.pack(side=tk.LEFT)
label_latitud_minutos = tk.Label(frame_latitud, text="'")
label_latitud_minutos.pack(side=tk.LEFT)
entry_latitud_segundos = tk.Entry(frame_latitud,width=8, validate="key")
entry_latitud_segundos.pack(side=tk.LEFT)
label_latitud_segundos = tk.Label(frame_latitud, text="''")
label_latitud_segundos.pack(side=tk.LEFT)


label_longitud = tk.Label(ventana, text="Longitud")
label_longitud.pack()
frame_longitud = tk.Frame(ventana)
frame_longitud.pack()
entry_longitud_grados = tk.Entry(frame_longitud, width=6, validate="key")
entry_longitud_grados.config(validatecommand=(entry_longitud_grados.register(validate_grados), '%P'))
entry_longitud_grados.pack(side=tk.LEFT)
label_longitud_grados = tk.Label(frame_longitud, text="°")
label_longitud_grados.pack(side=tk.LEFT)

entry_longitud_minutos = tk.Entry(frame_longitud, width=6, validate="key")
entry_longitud_minutos.config(validatecommand=(entry_longitud_minutos.register(validate_minutos), '%P'))
entry_longitud_minutos.pack(side=tk.LEFT)
label_longitud_minutos = tk.Label(frame_longitud, text="'")
label_longitud_minutos.pack(side=tk.LEFT)
entry_longitud_segundos = tk.Entry(frame_longitud, width=8, validate="key")
entry_longitud_segundos.pack(side=tk.LEFT)
label_longitud_segundos = tk.Label(frame_longitud, text="''")
label_longitud_segundos.pack(side=tk.LEFT)


def abrir_mapa():

    # Definir la función de distancia usando la fórmula Haversine
    def distancia_haversine(punto):
        lat1r, lon1r = math.radians(punto.geometry.y), math.radians(punto.geometry.x)
        lat2r, lon2r = math.radians(latitud), math.radians(longitud)
        d = 6371 * math.acos(math.cos(lat1r)*math.cos(lat2r)*math.cos(lon2r-lon1r) +math.sin(lat1r)*math.sin(lat2r))
        return d

    # Lee el archivo CSV con pandas
    df = pd.read_csv('igac.csv', encoding='ISO-8859-1')

    # Crea una columna de geometría usando la función Point de Shapely
    df['geometry'] = df.apply(lambda row: Point(row.long, row.lat), axis=1)

    # Convierte el DataFrame en un GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.long, df.lat))
    gdf = gdf.set_crs('EPSG:4326')



    grados_latitud = int(entry_latitud_grados.get())
    minutos_latitud = int(entry_latitud_minutos.get())
    segundos_latitud = float(entry_latitud_segundos.get())

    latitud = grados_latitud + (minutos_latitud / 60) + (segundos_latitud / 3600)

    print(latitud)

    grados_longitud = int(entry_longitud_grados.get())
    minutos_longitud = int(entry_longitud_minutos.get())
    segundos_longitud = float(entry_longitud_segundos.get())

    longitud = (grados_longitud + (minutos_longitud / 60) + (segundos_longitud / 3600)) *-1

    print(longitud)

    mi_punto = Point(longitud, latitud)

    # Agrega una columna con la distancia de cada punto al punto de referencia
    gdf['distancia'] = gdf.apply(distancia_haversine, axis=1)

    # Ordena el GeoDataFrame por distancia ascendente y selecciona los 4 puntos más cercanos
    gdf = gdf.sort_values(by='distancia').head(4)

    # tm = ( 65 + ((3 * km - 10))) formula tiempo de rastreo IGAC

    gdf['Tiempo_rastreo'] = (65 + ((3 * gdf['distancia']) - 10))

    # Calcula el tiempo de rastreo en horas y minutos
    gdf['Tiempo_rastreo_hh'], gdf['Tiempo_rastreo_mm'] = divmod(gdf['Tiempo_rastreo'], 60)

    # Convierte el tiempo de rastreo en formato hh:mm
    gdf['Tiempo_rastreo_horas'] = gdf.apply(lambda row: '{:02d}:{:02d}'.format(int(row['Tiempo_rastreo_hh']), int(row['Tiempo_rastreo_mm'])), axis=1)

    m = folium.Map(location=[gdf.geometry.y.mean(), gdf.geometry.x.mean()], zoom_start=10)


    for index, row in gdf.iterrows():

        folium.PolyLine(locations=[(row.geometry.y, row.geometry.x), (mi_punto.y, mi_punto.x)], color='red',weight=0.7).add_to(m)
        folium.Marker(location=[mi_punto.y, mi_punto.x], popup='Mi Punto', icon=folium.Icon(color='red')).add_to(m)
        folium.Marker(location=[row.geometry.y, row.geometry.x], popup=f"Estación: {row['id']}, Distancia: {round(row['distancia'],2)} km, Tiempo de rastreo: {row['Tiempo_rastreo_horas']} horas").add_to(m)

    # Muestra el mapa
    m
    m.save('mapa_interactivo.html')
    webbrowser.open("mapa_interactivo.html")

    columns = ['id', 'lat', 'long', 'mun', 'dep', 'Tiempo_rastreo_horas', 'distancia']


    # Configuramos las columnas del Treeview
    tabla['columns'] = columns
    tabla.column("#0", width=0, stretch=tk.NO)
    for col in tabla['columns']:
        tabla.column(col, width=110, minwidth=30)
        tabla.heading(col, text=col)
    
    # Insertamos los datos en el Treeview

    for i, row in gdf.iterrows():
        values = [row[col] for col in columns]
        tabla.insert(parent='', index=i, iid=i, text='', values=values)
    

    # Empaquetamos el Treeview en la ventana
    tabla.pack(padx=5, pady=5)
                      



# Crear el botón para generar y abrir el mapa interactivo
boton_generar_mapa = tk.Button(ventana, text='Generar Mapa', command=abrir_mapa)
boton_generar_mapa.pack()

def borrar_todo():
    entry_longitud_grados.delete(0, tk.END)
    entry_longitud_minutos.delete(0, tk.END)
    entry_latitud_grados.delete(0, tk.END)
    entry_latitud_minutos.delete(0, tk.END)
    entry_latitud_segundos.delete(0, tk.END)
    entry_longitud_segundos.delete(0, tk.END)
    tabla.delete(*tabla.get_children())


boton_borrar = tk.Button(ventana, text="Nueva Consulta", command=borrar_todo)
boton_borrar.pack(pady=10)

# Iniciar el bucle principal de la ventana
ventana.mainloop()