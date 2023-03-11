# Tiempoderastreo_GPS
El código proporciona una interfaz gráfica para calcular el tiempo de rastreo GPS en función de las coordenadas del punto de posicionamiento y las 4 estaciones permanentes más cercanas al punto del IGAC.

El código utiliza las bibliotecas Pandas, Geopandas, Shapely, Matplotlib, Geopy, Folium, tkinter y PIL para crear una interfaz gráfica de usuario y realizar cálculos.

La interfaz gráfica de usuario incluye campos para que el usuario ingrese la latitud y la longitud del punto de posicionamiento en grados, minutos y segundos. Una vez que se ingresan las coordenadas, se puede hacer clic en el botón "Calcular tiempo de rastreo" para calcular el tiempo de rastreo.

El tiempo de rastreo se calcula utilizando la fórmula t = 65 min + (3 min x (d - 10)), donde t es el tiempo de rastreo en minutos, d es la distancia en kilómetros entre el punto de posicionamiento y la estación permanente más cercana, y se considera un tiempo de 10 minutos de margen de error.

El código también lee un archivo CSV que contiene la información de las estaciones permanentes y sus ubicaciones geográficas. Se utiliza la biblioteca Geopandas para crear un GeoDataFrame y realizar cálculos espaciales.

El código muestra los resultados en una tabla en la interfaz gráfica de usuario y también crea un mapa interactivo utilizando la biblioteca Folium. El mapa muestra el punto de posicionamiento, las 4 estaciones permanentes más cercanas y la ruta más corta para llegar a la estación permanente más cercana.

Toca instalar todas las librerias indicadas en el archivo requirements.txt
    pip3 install -r requirements.txt
    
