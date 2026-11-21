# Datos de la serie Un país que cambia

Base de datos de las cinco historias. Cada cifra que aparece en los PDF debe poder rastrearse hasta una fila de estos CSV y, desde ahí, hasta su fuente en `csv/fuentes.csv`.

## Estructura

- `csv/` — los datos en formato tidy (una observación por fila).
- `fuentes/` — documentos originales descargados: el GeoJSON de límites provinciales. El PDF de la ONEI sobre envejecimiento no se pudo descargar desde esta máquina el 2026-11-20 (el servidor no respondió a la descarga directa); su tabla 3 se transcribió de la copia indexada del propio PDF en onei.gob.cu, consultada ese mismo día, y los valores de Villa Clara (29,1), La Habana (28,1) y Guantánamo (22,5) coinciden con los que la prensa y la propia ONEI destacaron del informe.

## Archivos

- `envejecimiento_provincias.csv` — grado de envejecimiento (% de población de 60 años o más) por provincia, serie completa 2017-2024 de la tabla 3 del informe de la ONEI, más la media nacional de 2015 y 2024. Nota del informe: a partir de 2021 los datos corresponden a la población efectiva.
- `ciencia_mujeres.csv` — indicadores de la historia 1 (Academia de Ciencias, comparaciones UNESCO, fuerza laboral).
- `poblacion_serie.csv` — población al cierre de 2016, 2020, 2023 y 2024, con el tipo de población declarado en cada fila (residente o efectiva). No mezclar ambos tipos sin avisar: es el error que la historia 3 debe evitar en su gráfico.
- `componentes_2024.csv` — nacimientos, defunciones y saldo migratorio de 2024. La suma cuadra: 10.055.968 + 71.358 − 128.098 − 251.221 = 9.748.007.
- `turismo_visitantes.csv` y `turismo_extra.csv` — serie de visitantes y datos de mercados emisores.
- `demografia_2024.csv` — nacimientos, defunciones, fecundidad, dependencia y extremos municipales.
- `mipymes.csv` — conteos del registro del MEP, distribución sectorial, empleo y perfil de los socios.
- `fuentes.csv` — registro de fuentes con institución, documento, año, URL cuando existe y fecha de consulta.

## Convenciones

- Los CSV usan punto decimal (formato legible por máquina). En los textos de los PDF se escribe con coma, como corresponde en español.
- Los valores calculados por la autora (porcentajes de caída, restos hasta 100, diferencias) llevan la nota «cálculo de la autora» en la fila correspondiente.
- Fecha de corte de esta base: 2026-11-20.

## Estado de la migración

El mapa de envejecimiento de la historia 2 ya se genera leyendo `envejecimiento_provincias.csv` y `fuentes/provincias.geojson`. El resto de los gráficos de `build.py` todavía toma los valores escritos en el propio script; migrarlos a estos CSV es el paso siguiente para que toda la serie se regenere desde la base.
