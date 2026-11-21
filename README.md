# Un país que cambia

Cinco historias con datos sobre Cuba, escritas en noviembre de 2026. Cada historia ocupa dos páginas, trabaja con cifras públicas citadas con su fuente y va acompañada de un análisis crítico del arquetipo narrativo que usa.

El hilo de la serie: las que estudian, los que no nacen, los que envejecen, los que se van, los que se quedan y los que no vienen.

Las cinco reunidas están en [un-pais-que-cambia-serie-completa.pdf](un-pais-que-cambia-serie-completa.pdf).

## Las historias

| # | Historia | De qué trata |
|---|----------|--------------|
| 1 | [La ciencia cubana tiene nombre de mujer](historias/historia-1-el-heroe-mujeres-en-la-ciencia.pdf) | Las mujeres en la ciencia cubana: 49 de cada 100 personas que investigan son mujeres, y en la Academia de Ciencias ocupan 39 de cada 100 asientos en el período 2024-2029. |
| 2 | [Los que no nacen y los que envejecen](historias/historia-2-el-sabio-los-que-no-nacen-y-los-que-envejecen.pdf) | Nacimientos y envejecimiento: en 2024 nacieron 71.358 niños y murieron 128.098 personas; el 25,7 % de la población tiene 60 años o más. |
| 3 | [El caso de los millones que faltan](historias/historia-3-el-detective-la-emigracion.pdf) | La caída de la población: de 11.239.224 habitantes en 2016 a 9.748.007 en 2024, con un saldo migratorio de -251.221 personas en el último año. |
| 4 | [Los que se quedaron y emprendieron](historias/historia-4-la-transformacion-las-mipymes.pdf) | Las mipymes privadas: 9.550 registradas en marzo de 2025 y 262.000 trabajadores en los nuevos actores económicos. |
| 5 | [Las playas que se quedaron esperando](historias/historia-5-la-sombra-el-turismo-que-no-vuelve.pdf) | El turismo que no vuelve: de 4,6 millones de visitantes en 2018 a 2,2 millones en 2024. |

## Los análisis críticos

Cada historia tiene su análisis en la carpeta [analisis](analisis/): el arquetipo en su tradición, cómo se usó en la historia, lo que aporta al dato, lo que deforma o esconde, qué se haría distinto y un veredicto. Cada análisis incluye la tabla del producto (audiencia, método y lo que el dato no permite afirmar) y el respaldo en la literatura sobre dramaturgia de datos, con referencias como Segel y Heer (2010), Hullman y Diakopoulos (2011) y Weber, Engebretsen y Kennedy (2018).

## Datos

La carpeta [datos](datos/) guarda la base de la serie: nueve archivos CSV con la fuente declarada en cada fila, el GeoJSON de las provincias usado en el mapa de envejecimiento y el documento [fuentes-ubicaciones.md](datos/fuentes-ubicaciones.md), con la dirección exacta donde se consulta cada fuente. Las instituciones citadas son la Oficina Nacional de Estadística e Información (ONEI), la UNESCO, la Academia de Ciencias de Cuba y el Ministerio de Economía y Planificación (MEP).

## Cómo se generan los PDF

Los dos scripts de Python de la carpeta `src` generan todos los documentos con fpdf2 y matplotlib: `build.py` produce las historias y `analisis.py` los análisis. Los PDF generados quedan en una carpeta `pdf` en la raíz del repo.

```
pip install -r requirements.txt
python src/build.py
python src/analisis.py
```

## Autora

Dagmary Pérez Aguiar, estudiante de Ciencia de Datos en MATCOM, Universidad de La Habana. Serie elaborada para la asignatura Comunicación en Ciencia de Datos. La Habana, noviembre de 2026.
