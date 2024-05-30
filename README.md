## Motivación

Este repositorio se ha generado para hacer llegar a los investigadores unas herramientas que les permitan analizar información de **Telegram** sin que tengan que tener conocimientos de programación. Estas herramientas están en la línea de t-hoarder-R.

Este conjunto de herramientas están programadas en R, en formato **notebook**, que combina código R con texto enriquecido (Markdown). Esto permite una documentación más legible de los pasos a seguir. Se pueden ejecutar desde **RStudio** que es una aplicación de escritorio disponible para Windows, linux y Mac. Están pensados para que se ejecuten de una vez (opción run all) pero pueden ejecutarse paso a paso. Se aconseja ejecutarlos en Rstudio en modo **visual** (pestaña de la ventana de código) para que sea más legible.

El paso de parámetros se realiza en la primera casilla del cuaderno. Podría haber creado una aplicación interactiva con Shiny pero implicaría una configuración más compleja de las herramientas. En este momento me ha parecido lo más razonable y al alcance de todo el mundo organizarlo en **notebook** con la esperanza de que usándose, se despierte la curiosidad por R y algunos se animen a hacer sus pinitos.

## Entorno de trabajo

Estos **notebooks** trabajan con esta estructura de directorios prefijada.

Los cuadernos para acceder a los datos (data) y las claves (keys) lo hacen de manera relativa al directorio dónde está el cuaderno. Aunque está configurado que el directorio de trabajo sea el del cuaderno, no siempre funciona. En el caso de que no encuentre los datos se debe configurar "Session / Set Working Directory / To Source File Location".

```         
dir_raiz ----+-----datos      # Cada dataset en un directorio independiente
             |
             +-----notebooks  # Se guardan los notebooh en R
      
```

Los datos descargados con telegram-tracker se copiarán o descargarán de drive, a un directorio creado debajo del directorio datos.

Si se opta por otra forma de organizar los datos, los notebooks tendrán que ser modificados en la casilla de "Entorno de Trabajo"

## Requisitos

Obtener los datos de los canales Telegram mediante la herramienta telegram-tracker.

En este [repositorio está disponible un fork](https://github.com/congosto/telegram-tracker-t-hoarder_tg) al que se le ha añadido un cuaderno que permite ejecutarlo en el entorno colab de Google.

## Descripción de los notebooks

Estos **notebook** analizan y visualizión los datos descargados de Telegram con telegram_tracker.

Se recomienda ejecutar lo cuadernos en Rstudio en modo Visual para que sean más legibles y tengamos un índice de los chunks ![modo visual](https://github.com/congosto/congosto.github.io/raw/master/modo_visual.png)

El análisis se puede realizar en dos ciclos:

-   **Ciclo simplificado**: los datos se pueden visualizar directamente. Es una forma muy rápida conocer la estructura del dataset, aunque no se podrán generar todas las gráficas por falta de datos.

-   **Ciclo completo** : se procederá a su análisis de red con la herramienta Gephi, que entre otras funciones permite la clasificación de los canales según sus conexiones. Esta clasificación se puede incorporar a los mensajes, permitiendo generar todas las gráficas.

### Ciclo simplificado

Es sencillo y rápido. En solo dos pasos podemos averiguar aspectos importantes de la propagación

![Ciclo Análisis simplificado](https://github.com/congosto/congosto.github.io/raw/master/ciclo_simplificado_t-hoarder-tg.JPG)

-   Fase 1: notebooks de descarga de tweets

    -   Descarga de los canales con telegram-tracker.
    -   Copiar o mover la descarga del canal o canales a un directorio creado debajo del directorio "datos"

-   Fase 2: Notebooks de visualización

    -   Visualizar los datos con tg_viz_channels.Rmd
    -   Extraer metadatos con tg_summarize_channels.Rmd

### Ciclo completo:

Es más elaborado pero permite un análisis en profundidad de la propagación al tener en cuenta los datos del análisis de red.

![Ciclo Análisis completo](https://github.com/congosto/congosto.github.io/raw/master/ciclo_ARS__t-hoarder-tg.JPG)

-   Fase 1: notebooks de descarga de tweets

    -   Descarga de los canales con telegram-tracker.
    -   Copiar o mover la descarga del canal o canales a un directorio creado debajo del directorio "datos"

-   Fase 2: notebook de generación de un fichero gdf para gephi

    -   tg_summarize_channels.Rmd obtiene de los datos descargados un fichero gdf que describe los nodos (canales) y las conexiones por forward

-   Fase 3: Análisis de red en Gephi, con cálculo de la modularidad. Se exportarán de los datos de los nodos a un fichero csv

-   Fase 4: notebook para la incorporación de la clasificación de usuarios de gephi a los tweets

    -   tg_classify_msgs.Rmd clasifica los mensajes en función de la clasificación de usuarios de Gephi

-   Fase 5: Notebooks de visualización

    -   Visualizar los datos con tg_viz_channels.Rmd para visualizar propagación de mensajes

### Funciones

Se incluyen un conjunto de ficharos en R con las funciones compartidas por los notebooks. Las funciones permiten que no haya código duplicado y que los cuadernos sean más legibles. Estas son las funciones:

-   tg_share_functions.R contiene unas funciones básicas utilizadas por todos los notebooks
-   tg_share_functions_viz.R contiene unas funciones básicas para visualización
-   tg_share_functions_viz_channels.R contiene las funciones específicas para la visualización de propagación
