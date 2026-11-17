# Taller práctico proyecto integrador: calidad de datos para la retención estudiantil

Una institución de educación superior quiere entender qué factores están asociados a la deserción, para diseñar estrategias de retención tempranas. Antes de responder preguntas de análisis, el equipo de datos debe garantizar que la información sea confiable. Este taller trabaja justo ese paso: auditar, limpiar y documentar los datos, y después responder cinco preguntas con esos datos limpios.

Los datos son sintéticos. Fueron generados para el taller y no corresponden a estudiantes reales.

## Requisitos

- Python 3.10 o superior
- Git
- Lo visto en los talleres de Pandas y de limpieza de datos

## Cómo empezar

1. Clona el repositorio y entra a la carpeta del proyecto:

   ```
   git clone <URL-DEL-REPOSITORIO>
   cd <NOMBRE-DE-LA-CARPETA>
   ```

2. Crea y activa un ambiente virtual. Las instrucciones para Windows y Mac/Linux están en `LEEME_ambiente.txt`.

3. Instala las librerías:

   ```
   pip install -r requirements.txt
   ```

4. Ejecuta el script:

   ```
   python analisis_desercion.py
   ```

Ejecuta el comando desde la carpeta del proyecto.

## Estructura del proyecto

```
proyecto/
├── analisis_desercion.py   Script principal. Tiene un TODO por cada paso.
├── requirements.txt        Versiones de las librerías.
├── LEEME_ambiente.txt      Pasos para crear el ambiente virtual.
├── README.md               Este archivo.
├── .gitignore              Archivos que Git no debe subir.
└── Data/
    ├── raw/
    │   └── datos_estudiantes.csv   Dataset original. No lo modifiques.
    └── processed/
        ├── .gitkeep                Mantiene la carpeta en el repositorio.
        ├── dataset_limpio.csv      Lo genera el script. No se sube (está en .gitignore).
        ├── decisiones.csv          Lo genera el script. Sí se sube.
        └── graficos/               Lo genera el script. Sí se sube.
```

Lo que genera el script (`dataset_limpio.csv`, `decisiones.csv` y `graficos/`) aparece en `Data/processed/` al ejecutarlo. Los dos últimos se suben al repositorio, porque son parte de la entrega.

## Qué debes hacer

Completa los TODO de `analisis_desercion.py` en orden. Cada función tiene un docstring con preguntas: respóndelas antes de escribir el código. Cada decisión que tomes debe quedar registrada con `registrar()`.

Cuando termines, el script debe producir:

- `Data/processed/dataset_limpio.csv`: el dataset limpio.
- `Data/processed/decisiones.csv`: la tabla de decisiones.
- `Data/processed/graficos/`: los cuatro gráficos.

La guía del taller (`Taller_Retencion_Estudiantil.docx`) explica cada método antes de usarlo, con ejemplos y errores frecuentes.

## Entrega

Sube tu código completo al repositorio y envía el enlace por el formulario de entrega. La entrega es individual.

El repositorio debe incluir:

- `analisis_desercion.py` con todos los TODO completados.
- `Data/processed/decisiones.csv` y la carpeta `Data/processed/graficos/`.
- Un `README.md` al final de este archivo, con una sección titulada **Mis decisiones y respuestas**. Debe incluir:
  0. El diccionario de datos: la tabla de las 23 columnas con tipo, descripción y rol, completada según el paso 1 de la guía.
  1. Tu diagnóstico de calidad: qué problemas encontraste y en qué columnas.
  2. Tus decisiones de limpieza, con su justificación.
  3. Las respuestas a las cinco preguntas, cada una con el número de estudiantes por grupo.
  4. Tu respuesta a la reflexión sobre asociación y causalidad.
  5. Tu respuesta a la reflexión sobre `motivo_retiro` y la predicción.
  6. Tu respuesta a la reflexión sobre el uso de variables sensibles.

El script debe ejecutarse sin errores desde cero. Cada decisión necesita una justificación, y cada conclusión debe apoyarse en un número del análisis.

## Mis decisiones y respuestas

### Paso 1. Exploración de los datos

El dataset contiene 10.150 filas y 23 columnas.
Para explorarlo utilicé shape, info(), describe() y value_counts().

### Diccionario de datos

| Columna | Tipo | Descripción | Rol |
|---|---|---|---|
| id_estudiante | Texto | Identificador del estudiante | Identificación |
| programa | Categórica | Programa académico del estudiante | Explicativa |
| facultad | Categórica | Facultad a la que pertenece el programa | Explicativa |
| jornada | Categórica | Jornada de estudio: Diurna, Nocturna o Fin de semana | Explicativa |
| semestre | Numérica discreta | Semestre académico que cursa el estudiante | Explicativa |
| promedio_acumulado | Numérica continua | Promedio acumulado de calificaciones, en escala de 0 a 5 | Explicativa |
| creditos_aprobados | Numérica discreta | Cantidad de créditos aprobados por el estudiante | Explicativa |
| materias_reprobadas | Numérica discreta | Cantidad de materias reprobadas por el estudiante | Explicativa |
| asistencia_pct | Numérica continua | Porcentaje de asistencia del estudiante, de 0 a 100 | Explicativa |
| sesiones_tutoria | Numérica discreta | Cantidad de sesiones de tutoría del estudiante | Explicativa |
| cambios_programa | Numérica discreta | Cantidad de veces que el estudiante ha cambiado de programa | Explicativa |
| estrato | Categórica ordinal | Estrato socioeconómico registrado del estudiante, de 1 a 6 | Explicativa |
| beca | Categórica | Indica si el estudiante recibe una beca: sí o no | Explicativa |
| trabaja | Categórica | Indica si el estudiante trabaja: sí o no | Explicativa |
| horas_trabajo_semana | Numérica continua | Cantidad de horas que trabaja el estudiante por semana | Explicativa |
| distancia_km | Numérica continua | Distancia registrada en kilómetros | Explicativa |
| edad | Numérica discreta | Edad del estudiante registrada en años cumplidos | Explicativa |
| genero | Categórica | Género registrado del estudiante | Explicativa |
| ciudad_procedencia | Categórica | Ciudad de procedencia del estudiante | Explicativa |
| tipo_colegio | Categórica | Tipo de colegio de procedencia: público o privado | Explicativa |
| fecha_matricula | Fecha | Fecha en que se matriculó el estudiante | Explicativa |
| estado | Categórica | Situación del estudiante: activo, desertor o graduado | Resultado |
| motivo_retiro | Categórica | Motivo del retiro, registrado después de la deserción | Resultado |

### Hallazgos de la exploración

- asistencia_pct y horas_trabajo_semana aparecen como texto, aunque representan cantidades.
- promedio_acumulado tiene un máximo de 78, fuera de la escala válida de 0 a 5.
- edad tiene un máximo de 150 años que requiere revisión.
- programa y ciudad_procedencia presentan variantes por tildes y mayúsculas.
- jornada presenta diferencias de mayúsculas y minúsculas.
- genero contiene abreviaturas y variantes de escritura.
- promedio_acumulado tiene 304 valores faltantes: 10.150 registros menos 9.846 valores presentes.

Estos hallazgos muestran problemas que debemos revisar antes del análisis.
En esta etapa solo exploramos los datos; todavía no los corregimos.

### Paso 2. Auditoría de calidad

| Problema detectado | Columna | Cantidad |
|---|---|---:|
| Datos faltantes | promedio_acumulado | 304 |
| Datos faltantes | distancia_km | 199 |
| Datos faltantes | ciudad_procedencia | 103 |
| Datos faltantes | tipo_colegio | 152 |
| Datos faltantes | motivo_retiro | 6877 |
| Guiones como faltantes | asistencia_pct | 202 |
| Guiones como faltantes | horas_trabajo_semana | 2822 |
| Código 999 como faltante | distancia_km | 152 |
| Valores con símbolo % | asistencia_pct | 300 |
| Filas duplicadas | Todas las columnas | 150 |
| Edades fuera de 15 a 60 | edad | 12 |
| Promedios fuera de 0 a 5 | promedio_acumulado | 17 |
| Horas mayores de 100 | horas_trabajo_semana | 30 |
| Fechas con barras | fecha_matricula | 3052 |
| Fechas con guiones | fecha_matricula | 7098 |

En esta etapa detecté problemas sin modificar los datos originales.
Los nulos de motivo_retiro pueden ser esperados en estudiantes activos
o graduados, porque no corresponde registrar un retiro.

Los promedios fuera de escala pueden distorsionar las estadísticas,
y las categorías escritas de distintas maneras separan grupos que
deberían analizarse juntos.

### Paso 3. Conversión de columnas numéricas

- En asistencia_pct eliminé el símbolo %, reemplacé los 202 guiones por nulos y convertí la columna a número.
- En horas_trabajo_semana reemplacé los 2822 guiones por nulos y convertí la columna a número. No los reemplacé por cero porque un dato faltante no significa que el estudiante no trabaje.
- En distancia_km reemplacé los 152 códigos 999 por nulos, porque representan datos faltantes, y aseguré que la columna fuera numérica.

Utilicé pd.to_numeric(..., errors="coerce") para convertir los valores a números y dejar como nulos los que no pudieran convertirse.

Registré las tres decisiones con registrar(). En este paso no eliminé filas ni corregí los valores imposibles; estos se tratarán después.

### Paso 4. Unificación de categorías

Normalicé los textos con str.strip() y str.lower() para quitar espacios en los extremos y unificar mayúsculas y minúsculas. Después corregí las variantes y recuperé la escritura definida en VALIDOS.

| Columna | Corrección | Registros modificados |
|---|---|---:|
| programa | Variantes sin tilde de Ingeniería de Sistemas y Psicología | 260 |
| jornada | Diferencias de mayúsculas y minúsculas | 485 |
| genero | Abreviaturas F y M, y la variante femenino | 559 |
| ciudad_procedencia | Variantes de Bogotá y Medellín por tildes y mayúsculas | 542 |

Unifiqué únicamente variantes que representan la misma categoría. Conservé los programas y ciudades distintos, así como la categoría Otra ciudad.

Los 103 nulos de ciudad_procedencia se conservaron para tratarlos en el paso de faltantes.

Registré las cuatro decisiones con registrar(). No eliminé filas en este paso.

### Paso 5. Conversión de fechas

La columna fecha_matricula contenía dos formatos: AAAA-MM-DD y DD/MM/AAAA.

Convertí cada formato por separado con pd.to_datetime() y errors="coerce". Después uní los resultados con fillna() para conservar las fechas de ambos formatos.

Se identificaron 3052 fechas en formato DD/MM/AAAA. Al finalizar, la columna quedó como tipo fecha y no quedaron valores nulos.

Registré la decisión con registrar(). No eliminé filas en este paso.

### Paso 6. Eliminación de duplicados

Encontré 150 filas repetidas al comparar todas las columnas, incluido id_estudiante. Se trataba de copias exactas de registros, no de estudiantes distintos con características similares.

Utilicé duplicated().sum() para contarlas y drop_duplicates() para eliminarlas, conservando la primera aparición.

Después apliqué reset_index(drop=True) para volver a numerar las filas sin crear una columna adicional.

El dataset pasó de 10150 a 10000 filas y conservó sus 23 columnas. Registré la decisión con registrar().

### Paso 7. Tratamiento de datos faltantes

- Conservé los 298 nulos de promedio_acumulado para no inventar notas ni alterar su distribución. Los estudiantes permanecen disponibles para otros análisis.
- Reemplacé los 100 nulos de ciudad_procedencia y los 150 de tipo_colegio por "Sin dato", sin asumir categorías desconocidas.
- Conservé los 6764 nulos de motivo_retiro: corresponden a 5878 estudiantes activos y 886 graduados, para quienes no aplica un motivo de retiro. Los 3236 desertores sí tienen motivo registrado.

Registré las cuatro decisiones con registrar(). No eliminé filas en este paso.

### Paso 8. Tratamiento de valores imposibles

- Reemplacé por nulos 15 promedios fuera de la escala de 0 a 5. No asumí que fueran errores de posición decimal, porque desconozco las notas correctas. El total de promedios nulos pasó de 298 a 313.
- Reemplacé por nulos 12 edades fuera del rango de 15 a 60 utilizado en el taller: ocho registros con 150 años y cuatro con 12 años. No inventé edades para reemplazarlas.
- Completé con cero las horas faltantes de 2781 estudiantes que indicaron que no trabajan.
- Reemplacé por nulos 30 registros con 200 horas de trabajo semanales. Son imposibles porque una semana tiene 168 horas y se desconoce el valor correcto.

Utilicé condiciones y df.loc para modificar únicamente las filas identificadas. Registré las cuatro decisiones con registrar().

No eliminé estudiantes: el dataset conserva 10000 filas y 23 columnas.

### Paso 9. Creación de variables

Creé desertor: True para los 3236 estudiantes con estado desertor y False para los 6764 activos o graduados.

Creé cuartil_asistencia con pd.qcut(..., q=4), agrupando a los 9800 estudiantes con asistencia registrada:

| Asistencia | Estudiantes |
|---|---:|
| De 48 a 80.5, incluidos ambos extremos | 2456 |
| Mayor de 80.5 y hasta 87.8 | 2466 |
| Mayor de 87.8 y hasta 95 | 2431 |
| Mayor de 95 y hasta 100 | 2447 |

Los 200 estudiantes con asistencia nula quedaron sin cuartil.

Los cuartiles permiten comparar la deserción entre niveles de asistencia con cantidades similares de estudiantes. Los tamaños no son exactamente iguales porque hay porcentajes repetidos.

Registré ambas decisiones. El dataset conserva 10000 filas y ahora tiene 25 columnas.

## Paso 10: Mapa de valores faltantes

Se creó un mapa de calor con `sns.heatmap(df.isnull(), cbar=False)`
para visualizar los datos faltantes del dataset original.

Cada fila representa un registro y cada columna una variable.
Los colores permiten distinguir los datos presentes de los nulos.

Se observó una mayor concentración de nulos en `motivo_retiro`.
Estos valores no necesariamente son errores: para estudiantes
activos o graduados, un motivo de retiro no aplica.

El gráfico se guardó en:
`Data/processed/graficos/mapa_faltantes.png`.

## Paso 11: Distribuciones antes y después de limpiar

Se crearon cuatro diagramas de caja con Matplotlib para comparar:

- El promedio acumulado antes y después de la limpieza.
- La edad antes y después de la limpieza.

En cada gráfico, la línea dentro de la caja representa la mediana,
es decir, el valor central de los datos ordenados. La caja contiene
la mitad central de los datos y los puntos fuera de los bigotes
representan valores alejados del resto. Estos puntos no necesariamente
son errores.

Durante la limpieza, los promedios fuera de la escala de 0 a 5
y las edades fuera del rango definido de 15 a 60 años se reemplazaron
por nulos. Los gráficos excluyen esos nulos, lo que permite comparar
la distribución antes y después de retirar los valores imposibles.

La imagen se guardó con buena resolución para que los textos
y los detalles se vean claros en:
`Data/processed/graficos/distribuciones_antes_despues.png`.

## Paso 12: Tasa de deserción por programa

Se calculó la tasa de deserción de cada programa utilizando
`df.groupby("programa")["desertor"].mean()`.

Como la columna `desertor` contiene True para quienes desertaron
y False para los demás, su promedio representa la proporción
de desertores. Este resultado se multiplicó por 100 para
expresarlo como porcentaje.

Se creó un gráfico de barras horizontales con Matplotlib.
Cada barra representa un programa y su longitud indica el
porcentaje de estudiantes que desertaron.

Esto permite comparar programas considerando su cantidad de
estudiantes, en lugar de comparar únicamente el número de desertores.

El gráfico se guardó en:
`Data/processed/graficos/tasa_desercion_por_programa.png`.

## Paso 13: Tasa de deserción por cuartil de asistencia

Se agruparon los estudiantes en los cuatro cuartiles de asistencia
creados en el paso 9. Para cada grupo se calculó la proporción
de desertores con:

`df.groupby("cuartil_asistencia", observed=True)["desertor"].mean()`

El resultado se multiplicó por 100 y se representó en un gráfico
de barras con Matplotlib.

Se observaron las siguientes tasas aproximadas de deserción:

- Asistencia entre 48 % y 80,5 %: 62 %.
- Asistencia mayor de 80,5 % y hasta 87,8 %: 37 %.
- Asistencia mayor de 87,8 % y hasta 95 %: 21 %.
- Asistencia mayor de 95 % y hasta 100 %: 9 %.

En estos datos, la deserción disminuye conforme aumenta la
asistencia. Esto muestra una asociación entre ambas variables,
pero no demuestra que una menor asistencia cause la deserción.

El gráfico se guardó en:
`Data/processed/graficos/tasa_desercion_por_asistencia.png`.

## Respuestas a las cinco preguntas

### 1. ¿Qué programa presenta la mayor tasa de deserción?

| Programa | Estudiantes | Deserción |
|---|---:|---:|
| Ingeniería Industrial | 1322 | 40,17 % |
| Ingeniería de Sistemas | 1432 | 38,27 % |
| Diseño Gráfico | 870 | 35,75 % |
| Enfermería | 1167 | 31,28 % |
| Derecho | 1501 | 30,65 % |
| Administración de Empresas | 1343 | 29,41 % |
| Contaduría Pública | 1196 | 26,84 % |
| Psicología | 1169 | 26,09 % |

Ingeniería Industrial presenta la mayor tasa de deserción:
40,17 %, sobre un total de 1322 estudiantes.

Diseño Gráfico es el programa con menos estudiantes, con 870.
Aunque no es un grupo de apenas unos pocos casos, conviene
considerar las diferencias de tamaño al comparar las tasas.

### 2. ¿Hay diferencia entre becados y no becados?

| Beca | Estudiantes | Deserción |
|---|---:|---:|
| No | 7243 | 36,32 % |
| Sí | 2757 | 21,94 % |

Los becados presentan una tasa de deserción aproximadamente
14,38 puntos porcentuales menor que los no becados.

Esta diferencia no demuestra que la beca cause la permanencia.
Los grupos podrían diferir también en rendimiento académico,
condiciones económicas u otros factores relacionados con la
asignación de becas y la continuidad de los estudios.

### 3. ¿Qué jornada tiene el menor promedio acumulado?

| Jornada | Estudiantes | Promedio acumulado |
|---|---:|---:|
| Nocturna | 2754 | 3,46 |
| Fin de semana | 984 | 3,70 |
| Diurna | 6262 | 3,72 |

La jornada nocturna tiene el menor promedio acumulado: 3,46.

Las cantidades corresponden al total de estudiantes por jornada.
Los promedios se calcularon únicamente con las notas disponibles,
excluyendo los valores nulos.

### 4. ¿Cuántas materias reprueban en promedio los desertores frente a los activos?

| Estado | Estudiantes | Promedio de materias reprobadas |
|---|---:|---:|
| Activo | 5878 | 0,62 |
| Desertor | 3236 | 3,07 |

Los desertores tienen un promedio de 3,07 materias reprobadas,
frente a 0,62 entre los activos.

Se excluyeron los 886 graduados porque la pregunta compara
únicamente estudiantes activos y desertores.


### 5. ¿La deserción aumenta conforme baja la asistencia?

| Cuartil | Asistencia promedio | Estudiantes | Deserción |
|---|---:|---:|---:|
| Q1: menor asistencia | 73,89 % | 2456 | 61,81 % |
| Q2 | 84,39 % | 2466 | 36,98 % |
| Q3 | 91,32 % | 2431 | 20,69 % |
| Q4: mayor asistencia | 98,67 % | 2447 | 9,28 % |

Sí. En los datos analizados, la deserción aumenta conforme
disminuye la asistencia.

El cuartil de menor asistencia tiene una asistencia promedio
de 73,89 % y una deserción de 61,81 %. En cambio, el de mayor
asistencia tiene una asistencia promedio de 98,67 % y una
deserción de 9,28 %.

Los grupos tienen cantidades similares de estudiantes.
Los 200 estudiantes sin asistencia registrada quedaron
fuera de esta comparación.

Esta relación no demuestra que la baja asistencia cause
la deserción. Factores como dificultades económicas,
laborales o personales podrían influir en ambas.

### Reflexión 1: asociación y causalidad

Los becados presentan menor deserción: 21,94 %, frente a
36,32 % entre los no becados. Sin embargo, esto no demuestra
que la beca cause la permanencia.

Podrían existir otras diferencias entre los grupos, como
el rendimiento académico o las condiciones económicas,
que influyan tanto en recibir una beca como en continuar
estudiando.

Para estudiar si la beca tiene un efecto, sería necesario
comparar estudiantes con características similares y
analizar cómo se asignaron las becas.

### Reflexión 2: variables que no deberían usarse para predecir

No usaría `motivo_retiro` para predecir la deserción porque
solo se conoce después de que el estudiante abandona sus estudios.
Usarlo introduciría información que no estaría disponible
al momento de hacer una predicción temprana.

Tampoco usaría `estado` ni `desertor` como variables explicativas:
indican directamente el resultado que se quiere predecir.

Otras columnas, como promedio, asistencia y materias reprobadas,
solo deberían usarse con los valores disponibles hasta el momento
de la predicción, sin incluir información registrada después.

### Reflexión 3: variables sensibles

Género, estrato y ciudad de procedencia pueden ayudar a detectar
desigualdades y necesidades de apoyo. Sin embargo, una asociación
con la deserción no justifica tomar decisiones únicamente
por pertenecer a uno de estos grupos.

Usarlas sin cuidado podría generar discriminación, reforzar
estereotipos o dejar sin apoyo a estudiantes que también
lo necesitan.

La institución debería considerar las necesidades individuales,
proteger la privacidad y revisar si sus criterios distribuyen
los apoyos de manera justa. Estas variables podrían servir
para evaluar desigualdades, sin convertirse en una razón
automática para negar oportunidades.