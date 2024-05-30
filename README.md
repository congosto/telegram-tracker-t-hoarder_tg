## Motivaci�n

Este repositorio se ha generado para hacer llegar a los investigadores unas herramientas que les permitan analizar informaci�n de **Telegram** sin que tengan que tener conocimientos de programaci�n. Estas herramientas est�n en la l�nea de t-hoarder-R.

Este conjunto de herramientas est�n programadas en R, en formato **notebook**, que combina c�digo R con texto enriquecido (Markdown). Esto permite una documentaci�n m�s legible de los pasos a seguir. Se pueden ejecutar desde **RStudio** que es una aplicaci�n de escritorio disponible para Windows, linux y Mac. Est�n pensados para que se ejecuten de una vez (opci�n run all) pero pueden ejecutarse paso a paso. Se aconseja ejecutarlos en Rstudio en modo **visual** (pesta�a de la ventana de c�digo) para que sea m�s legible.

El paso de par�metros se realiza en la primera casilla del cuaderno. Podr�a haber creado una aplicaci�n interactiva con Shiny pero implicar�a una configuraci�n m�s compleja de las herramientas. En este momento me ha parecido lo m�s razonable y al alcance de todo el mundo organizarlo en **notebook** con la esperanza de que us�ndose, se despierte la curiosidad por R y algunos se animen a hacer sus pinitos.

## Entorno de trabajo

Estos **notebooks** trabajan con esta estructura de directorios prefijada.

Los cuadernos para acceder a los datos (data) y las claves (keys) lo hacen de manera relativa al directorio d�nde est� el cuaderno. Aunque est� configurado que el directorio de trabajo sea el del cuaderno, no siempre funciona. En el caso de que no encuentre los datos se debe configurar "Session / Set Working Directory / To Source File Location".

```         
dir_raiz ----+-----datos      # Cada dataset en un directorio independiente
             |
             +-----notebooks  # Se guardan los notebooh en R
      
```

Los datos descargados con telegram-tracker se copiar�n o descargar�n de drive, a un directorio creado debajo del directorio datos.

Si se opta por otra forma de organizar los datos, los notebooks tendr�n que ser modificados en la casilla de "Entorno de Trabajo"

## Requisitos

Obtener los datos de los canales Telegram mediante la herramienta telegram-tracker.

En este [repositorio est� disponible un fork](https://github.com/congosto/telegram-tracker-t-hoarder_tg) al que se le ha a�adido un cuaderno que permite ejecutarlo en el entorno colab de Google.

## Descripci�n de los notebooks

Estos **notebook** analizan y visualizi�n los datos descargados de Telegram con telegram_tracker.

Se recomienda ejecutar lo cuadernos en Rstudio en modo Visual para que sean m�s legibles y tengamos un �ndice de los chunks ![modo visual](https://github.com/congosto/congosto.github.io/raw/master/modo_visual.png)

El an�lisis se puede realizar en dos ciclos:

-   **Ciclo simplificado**: los datos se pueden visualizar directamente. Es una forma muy r�pida conocer la estructura del dataset, aunque no se podr�n generar todas las gr�ficas por falta de datos.

-   **Ciclo completo** : se proceder� a su an�lisis de red con la herramienta Gephi, que entre otras funciones permite la clasificaci�n de los canales seg�n sus conexiones. Esta clasificaci�n se puede incorporar a los mensajes, permitiendo generar todas las gr�ficas.

### Ciclo simplificado

Es sencillo y r�pido. En solo dos pasos podemos averiguar aspectos importantes de la propagaci�n

![Ciclo An�lisis simplificado](https://github.com/congosto/congosto.github.io/raw/master/ciclo_simplificado_t-hoarder-tg.JPG)

-   Fase 1: notebooks de descarga de tweets

    -   Descarga de los canales con telegram-tracker.
    -   Copiar o mover la descarga del canal o canales a un directorio creado debajo del directorio "datos"

-   Fase 2: Notebooks de visualizaci�n

    -   Visualizar los datos con tg_viz_channels.Rmd
    -   Extraer metadatos con tg_summarize_channels.Rmd

### Ciclo completo:

Es m�s elaborado pero permite un an�lisis en profundidad de la propagaci�n al tener en cuenta los datos del an�lisis de red.

![Ciclo An�lisis completo](https://github.com/congosto/congosto.github.io/raw/master/ciclo_ARS__t-hoarder-tg.JPG)

-   Fase 1: notebooks de descarga de tweets

    -   Descarga de los canales con telegram-tracker.
    -   Copiar o mover la descarga del canal o canales a un directorio creado debajo del directorio "datos"

-   Fase 2: notebook de generaci�n de un fichero gdf para gephi

    -   tg_summarize_channels.Rmd obtiene de los datos descargados un fichero gdf que describe los nodos (canales) y las conexiones por forward

-   Fase 3: An�lisis de red en Gephi, con c�lculo de la modularidad. Se exportar�n de los datos de los nodos a un fichero csv

-   Fase 4: notebook para la incorporaci�n de la clasificaci�n de usuarios de gephi a los tweets

    -   tg_classify_msgs.Rmd clasifica los mensajes en funci�n de la clasificaci�n de usuarios de Gephi

-   Fase 5: Notebooks de visualizaci�n

    -   Visualizar los datos con tg_viz_channels.Rmd para visualizar propagaci�n de mensajes

### Funciones

Se incluyen un conjunto de ficharos en R con las funciones compartidas por los notebooks. Las funciones permiten que no haya c�digo duplicado y que los cuadernos sean m�s legibles. Estas son las funciones:

-   tg_share_functions.R contiene unas funciones b�sicas utilizadas por todos los notebooks
-   tg_share_functions_viz.R contiene unas funciones b�sicas para visualizaci�n
-   tg_share_functions_viz_channels.R contiene las funciones espec�ficas para la visualizaci�n de propagaci�n
