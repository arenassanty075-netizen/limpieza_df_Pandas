import pandas as pd


def explorar(df):
    """Paso 1 del Word: primera mirada al dataset.

    Muestra la forma, los tipos y los nulos de cada columna, las estadísticas
    numéricas, y los valores de las columnas programa, jornada, genero y estado.
    Pregunta: ¿alguna columna numérica aparece como texto? ¿Por qué crees que pasa?
    """
    # PASO 1 COMPLETADO: tamaño, tipos, estadísticas y categorías.
    print("\nTamaño del dataset (filas, columnas):")
    print(df.shape)
    print("\nInformación de las columnas:")
    df.info()
    print("\nEstadísticas de las columnas numéricas:")
    print(df.describe())
    print("\nCantidad de registros por programa:")
    print(df["programa"].value_counts())
    print("\nCantidad de registros por jornada:")
    print(df["jornada"].value_counts())
    print("\nCantidad de registros por género:")
    print(df["genero"].value_counts())
    print("\nCantidad de registros por ciudad:")
    print(df["ciudad_procedencia"].value_counts(dropna=False))
    print("\nCantidad de registros por estado:")
    print(df["estado"].value_counts(dropna=False))


def auditar(df):
    """Paso 2 del Word: buscar problemas sin corregirlos todavía.

    Revisa: nulos reales, faltantes disfrazados ('-', 999), valores imposibles
    (edad, promedio, horas), duplicados y formatos de fecha.
    Pregunta: ¿cuál de estos problemas afecta más el análisis? ¿Por qué?
    """
    # PASO 2 COMPLETADO: conteos de problemas de calidad.
    print("\nDatos faltantes por columna:")
    print(df.isnull().sum())
    print("\nGuiones en asistencia:")
    print(df["asistencia_pct"].eq("-").sum())
    print("\nGuiones en horas de trabajo:")
    print(df["horas_trabajo_semana"].eq("-").sum())
    print("\nDistancia con codigo 999:")
    print(df["distancia_km"].eq(999).sum())
    print("\nAsistencias con símbolo %:")
    print(df["asistencia_pct"].str.contains("%", regex=False, na=False).sum())
    print("\nFilas duplicadas:")
    print(df.duplicated().sum())
    print("\nEdades fuera del rango de 15 a 60:")
    print(((df["edad"] < 15) | (df["edad"] > 60)).sum())
    print("\nPromedios fuera de la escala de 0 a 5:")
    print(((df["promedio_acumulado"] < 0) |
           (df["promedio_acumulado"] > 5)).sum())
    horas = pd.to_numeric(df["horas_trabajo_semana"], errors="coerce")

    print("\nHoras de trabajo mayores de 100:")
    print((horas > 100).sum())
    print("\nFechas con barras:")
    print(df["fecha_matricula"].str.contains("/", regex=False, na=False).sum())
    print("\nFechas con guiones:")
    print(df["fecha_matricula"].str.contains("-", regex=False, na=False).sum())


def responder_preguntas(df):
    """Paso 10 del Word: las cinco preguntas de la institución.

    Cada pregunta debe imprimir el resultado con el número de estudiantes por grupo.
    Pregunta 1: ¿Qué programa presenta la tasa de deserción más alta?
    Pregunta 2: ¿Hay diferencia en la deserción entre becados y no becados?
    Pregunta 3: ¿Qué jornada tiene el menor promedio acumulado?
    Pregunta 4: ¿Cuántas materias reprobadas tienen en promedio los desertores frente a los activos?
                (Excluye a los graduados.)
    Pregunta 5: ¿La deserción aumenta conforme baja la asistencia?
                (Usa cuartil_asistencia.)
    """

    # Pregunta 1
    por_programa = df.groupby("programa").agg(
        estudiantes=("desertor", "size"),
        tasa_desercion=("desertor", "mean")
    )
    por_programa["tasa_desercion"] *= 100
    por_programa = por_programa.sort_values(
        "tasa_desercion", ascending=False
    )

    print("\n1. ¿Qué programa presenta la mayor tasa de deserción? (%)")

    print(por_programa.round(2))

    # Pregunta 2
    por_beca = df.groupby("beca").agg(
        estudiantes=("desertor", "size"),
        tasa_desercion=("desertor", "mean")
    )
    por_beca["tasa_desercion"] *= 100

    print("\n2. ¿Hay diferencia entre becados y no becados? (%)")
    print(por_beca.round(2))

    # Pregunta 3
    por_jornada = df.groupby("jornada").agg(
        estudiantes=("promedio_acumulado", "size"),
        promedio_acumulado=("promedio_acumulado", "mean")
    ).sort_values("promedio_acumulado")

    print("\n3. ¿Qué jornada tiene el menor promedio acumulado?")
    print(por_jornada.round(2))

    # Pregunta 4
    sin_graduados = df[df["estado"].isin(["desertor", "activo"])]
    por_estado = sin_graduados.groupby("estado").agg(
        estudiantes=("materias_reprobadas", "size"),
        promedio_reprobadas=("materias_reprobadas", "mean")
    )

    print("\n4. ¿Cuántas materias reprueban en promedio activos y desertores?")
    print(por_estado.round(2))

    # Pregunta 5
    por_asistencia = df.groupby(
        "cuartil_asistencia", observed=True
    ).agg(
        asistencia_promedio=("asistencia_pct", "mean"),
        estudiantes=("desertor", "size"),
        tasa_desercion=("desertor", "mean")
    )
    por_asistencia["tasa_desercion"] *= 100

    print("\n5. ¿La deserción aumenta conforme baja la asistencia? (%)")
    print(por_asistencia.round(2))
