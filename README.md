Explicación de las funcionalidades:

Argumentos del Script:

-q o --query: Define la consulta de búsqueda.

-e o --export: Guarda los resultados en un archivo.

-r o --results: Define el número de resultados a obtener (all para todos los resultados).

-v o --verbose: Activa el modo verboso para mostrar más detalles durante la ejecución.

-f o --folder: Crea una estructura de carpetas según la URL.

-d o --download: Descarga los archivos desde las URLs y los guarda en la estructura de carpetas correspondiente.

Guardar Resultados en un Archivo:

La función save_results_to_file guarda los enlaces en un archivo de texto.

Crear Estructura de Carpetas y Guardar Archivo:

La función create_folder_tree_and_save_file crea una estructura de carpetas basada en la URL y guarda el contenido del archivo en su correspondiente carpeta.

Descargar Archivos:

La función download_files descarga cada URL y guarda el contenido en la estructura de carpetas creada.

Para ejecutar el script, puedes usar las siguientes opciones según lo necesites.

Por ejemplo:

python dork.py -q 'site:"www.dominio.com" file:"pdf"' -e resultados.txt -r 10 -v -f -d

Limitaciones por el api de Google
