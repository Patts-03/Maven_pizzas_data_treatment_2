# Maven Pizzas - 2016 Data Treatment

Dados los archivos .csv con la información relativa a los pedidos que ha gestionado la empresa de pizzas Maven Pizzas durante el pasado 2016, creamos un programa que procese dichos archivos, elabore una estimación del número de ingredientes óptimo a comprar por semana y un análisis de los datos en sí.

Antes de poder realizar la recomendación, tendremos que analizar dos de los csvs proporcionados (orders.csv y order_details.csv) , ya que contienen datos erroneos y mal establecidos. Para ello utilizamos el archivo limpieza.py antes de ejecutar el programa que calcula las recomendaciones. Este devolverá como resultado dos csvs que se corresponden a los tratados pero ya limpios y carentes de datos erróneos.

Para la recomendación utilizamos el archivos pizzas.py, en el cual procesaremos los datos siguiendo la estructura de una ETL.
Vamos a crear dos archivos como resultado de este análisis. En primer lugar el análisis_pedidos_semanales.csv, en el cual vamos a incluir, por tipo de pizza, aquellos datos que hemos calculado durante el análisis. Entre ellos estarían magnitudes como la cantidad de pedidos por tamaño que ha habido de esa pizza a lo largo del año, el número total de pedidos a nivel anual, el número de pizzas de ese tipo pedidas por cada semana del año, etc.

El segundo archivo será el de recomendación_ingredientes.csv , el cual va a incluir la estimación del número de ingredientes a comprar por cada semana. Para elaborar la estimación utilizamos el método de ventana deslizante, calculando la moda de entre el número de pedidos semanales por cada tipo de pizza. Así sabremos que la moda de cada tipo será la cantidad estimada de ingredientes a pedir para esa pizza, y así con el resto, sumándolos todos juntos.
Además, tenemos en cuenta también el tamaño de la pizza pedida, de manera que también tendrá influencia en el número de ingredientes a pedir.

Posteriormente, hacemos un análisis de la calidad de los datos proporcionados mediante el analisis.py, que devolverá un .txt con dicho análisis. Por defecto hacemos el análisis sobre los csvs ya limpios, aunque puede ser facilmente modificable por parte del usario siguiendo las especificaciones redactadas en el mismo archivo.
