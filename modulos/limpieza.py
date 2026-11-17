import numpy as np
import pandas as pd

from .configuracion import VALIDOS
from .registro import registrar


def convertir_numericos(df):
    """Paso 3 del Word: columnas que deberían ser numéricas, pero llegan como texto.

    Pistas: quitar el símbolo % con str.replace; reemplazar '-' por nulo;
    convertir con pd.to_numeric(..., errors="coerce"); reemplazar 999 por nulo en distancia_km.
    Registra cada conversión con registrar().
    """
    df["asistencia_pct"] = df["asistencia_pct"].str.replace("%", "", regex=False)
    df["asistencia_pct"] = df["asistencia_pct"].replace("-", np.nan)
    df["asistencia_pct"] = pd.to_numeric(df["asistencia_pct"], errors="coerce")
    df["horas_trabajo_semana"] = df["horas_trabajo_semana"].replace("-", np.nan)
    df["horas_trabajo_semana"] = pd.to_numeric(df["horas_trabajo_semana"], errors="coerce")
    distancias_faltantes = df["distancia_km"].eq(999).sum()
    df["distancia_km"] = df["distancia_km"].replace(999, np.nan)
    df["distancia_km"] = pd.to_numeric(df["distancia_km"], errors="coerce")
    registrar(
    3,
    "asistencia_pct",
    "Convertir a número",
    len(df),
    "Se quita el símbolo % y se convierten los guiones en nulos."
    )
    registrar(
    3,
    "horas_trabajo_semana",
    "Convertir a número",
    len(df),
    "Se convierten los guiones en nulos porque representan datos faltantes."
    )
    registrar(
    3,
    "distancia_km",
    "Convertir a número y reemplazar 999 por nulo",
    distancias_faltantes,
    "El código 999 representa un dato faltante, no una distancia real."
   )

    return df


def unificar_categorias(df):
    """Paso 4 del Word: errores tipográficos en columnas categóricas.

    Pistas: primero df[col].str.strip().str.lower(); después .replace(diccionario)
    con las variantes que encontraste con value_counts(). Los valores correctos están en VALIDOS.
    Pregunta: ¿qué variantes son el mismo valor? ¿Hay alguna que no debas unificar?
    """
    variantes = {
        "programa": {
            "ingenieria de sistemas": "Ingeniería de Sistemas",
            "psicologia": "Psicología",
        },
        "genero": {"f": "Femenino", "m": "Masculino"},
        "ciudad_procedencia": {"bogota": "Bogotá", "medellin": "Medellín"},
    }
    for columna, validos in VALIDOS.items():
        originales = df[columna]
        equivalencias = {nombre.lower(): nombre for nombre in validos}
        equivalencias.update(variantes.get(columna, {}))
        normalizados = originales.str.strip().str.lower().replace(equivalencias)
        modificados = originales.notna() & originales.ne(normalizados)
        df[columna] = normalizados
        registrar(
            4,
            columna,
            "Unificar variantes de escritura",
            modificados.sum(),
            "Se unifican espacios, mayúsculas, tildes y abreviaturas conocidas "
            "con los valores de VALIDOS; se conservan los nulos.",
        )

    return df


def convertir_fechas(df):
    """Paso 5 del Word: fechas escritas en dos formatos.

    Pista: intenta el formato AAAA-MM-DD y luego DD/MM/AAAA, cada uno con errors="coerce",
    y junta los resultados con fillna(). Registra cuántas fechas tenían el segundo formato.
    """
    fechas_guion = pd.to_datetime(
        df["fecha_matricula"],
        format="%Y-%m-%d",
        errors="coerce"
    )
    fechas_barra = pd.to_datetime(
        df["fecha_matricula"],
        format="%d/%m/%Y",
        errors="coerce"
    )
    df["fecha_matricula"] = fechas_guion.fillna(fechas_barra)

    registrar(
        5,
        "fecha_matricula",
        "Unificar formatos de fecha",
        fechas_barra.notna().sum(),
        "Se convierten ambos formatos a tipo fecha y se unen los resultados con fillna."
    )
    return df


def eliminar_duplicados(df):
    """Paso 6 del Word: filas repetidas.

    Pregunta: ¿podrían existir dos estudiantes distintos con todos los datos iguales?
    Pista: duplicated() y drop_duplicates(), con reset_index(drop=True).
    """
    duplicados = df.duplicated().sum()
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    registrar(
        6,
        "Todas las columnas",
        "Eliminar filas duplicadas",
        duplicados,
        "Se eliminan repeticiones exactas, incluido id_estudiante, conservando la primera aparición."
    )
    return df


def tratar_faltantes(df):
    """Paso 7 del Word: decidir qué hacer con los nulos reales.

    Preguntas:
    - ¿Puedes inventar una nota? ¿Qué pasa si imputas el promedio?
    - Para ciudad o tipo de colegio, ¿conviene eliminar la fila o marcar el dato como 'Sin dato'?
    - motivo_retiro tiene muchos nulos. ¿Son errores? (Pista: ¿para quiénes aplica esa columna?)
    """
    faltantes_ciudad = df["ciudad_procedencia"].isna().sum()
    df["ciudad_procedencia"] = df["ciudad_procedencia"].fillna("Sin dato")
    faltantes_colegio = df["tipo_colegio"].isna().sum()
    df["tipo_colegio"] = df["tipo_colegio"].fillna("Sin dato")
    print(pd.crosstab(
        df["estado"],
        df["motivo_retiro"].isna(),
        colnames=["motivo_retiro_nulo"]
    ))

    registrar(
        7,
        "promedio_acumulado",
        "Conservar valores nulos",
        df["promedio_acumulado"].isna().sum(),
        "No se imputan notas para evitar alterar su distribución; se conservan los estudiantes para otros análisis."
    )
    registrar(
        7,
        "ciudad_procedencia",
        "Reemplazar nulos por Sin dato",
        faltantes_ciudad,
        "Se conserva al estudiante sin inventar su ciudad de procedencia."
    )
    registrar(
        7,
        "tipo_colegio",
        "Reemplazar nulos por Sin dato",
        faltantes_colegio,
        "Se conserva al estudiante sin asumir si su colegio era público o privado."
    )
    registrar(
        7,
        "motivo_retiro",
        "Conservar nulos porque no aplica",
        df["motivo_retiro"].isna().sum(),
        "Los nulos corresponden a estudiantes activos o graduados; todos los desertores tienen motivo registrado."
    )
    return df


def tratar_imposibles(df):
    """Paso 8 del Word: valores que no pueden existir.

    Preguntas:
    - La escala del promedio es de 0 a 5. ¿Qué harías con un 45?
    - Una edad de 150 años es un error. ¿Qué valor pondrías en su lugar?
    - Si el estudiante no trabaja, ¿cuántas horas de trabajo tiene? ¿Cómo lo aplicas en código?
    """
    promedios_invalidos = (
        (df["promedio_acumulado"] < 0) |
        (df["promedio_acumulado"] > 5)
    )
    print(df.loc[promedios_invalidos, ["id_estudiante", "promedio_acumulado"]])
    df.loc[promedios_invalidos, "promedio_acumulado"] = np.nan
    print(df["promedio_acumulado"].isna().sum())
    edades_invalidas = (df["edad"] < 15) | (df["edad"] > 60)
    print(df.loc[edades_invalidas, ["id_estudiante", "edad"]])
    df.loc[edades_invalidas, "edad"] = np.nan
    print(df["edad"].isna().sum())
    print(df.loc[
        df["trabaja"].eq("no"),
        "horas_trabajo_semana"
    ].value_counts(dropna=False))
    horas_faltantes_no_trabaja = (
        df["trabaja"].eq("no") &
        df["horas_trabajo_semana"].isna()
    )
    df.loc[horas_faltantes_no_trabaja, "horas_trabajo_semana"] = 0
    print(df.loc[df["trabaja"].eq("no"), "horas_trabajo_semana"].isna().sum())
    horas_excesivas = df["horas_trabajo_semana"] > 100
    print(df.loc[
        horas_excesivas,
        ["id_estudiante", "trabaja", "horas_trabajo_semana"]
    ])
    df.loc[horas_excesivas, "horas_trabajo_semana"] = np.nan
    mediana_trabajadores = df.loc[
        df["trabaja"].eq("sí"), "horas_trabajo_semana"
    ].median()
    df.loc[horas_excesivas, "horas_trabajo_semana"] = mediana_trabajadores
    print((df["horas_trabajo_semana"] > 100).sum())
    registrar(
        8,
        "promedio_acumulado",
        "Reemplazar valores fuera de escala por nulos",
        promedios_invalidos.sum(),
        "La escala válida es de 0 a 5; se desconoce la nota correcta y no se inventa un reemplazo."
    )
    registrar(
        8,
        "edad",
        "Reemplazar edades fuera del rango por nulos",
        edades_invalidas.sum(),
        "Se usa el rango de 15 a 60 definido en el taller; se desconoce la edad correcta."
    )
    registrar(
        8,
        "horas_trabajo_semana",
        "Completar horas faltantes con cero para quienes no trabajan",
        horas_faltantes_no_trabaja.sum(),
        "Si el estudiante indica que no trabaja, sus horas de trabajo son cero."
    )
    registrar(
        8,
        "horas_trabajo_semana",
        "Reemplazar horas imposibles por la mediana de quienes trabajan",
        horas_excesivas.sum(),
        f"Se convierten las horas mayores a 100 en nulos y se completan con la mediana de quienes trabajan ({mediana_trabajadores:g} horas), como indica la guía."
    )
    return df


def crear_variables(df):
    """Paso 9 del Word: variables nuevas para el análisis.

    Crea:
    - desertor: True si estado es 'desertor', False si no.
    - cuartil_asistencia: divide asistencia_pct en cuatro grupos iguales con pd.qcut.
    Pregunta: ¿por qué conviene usar cuartiles y no valores exactos de asistencia?
    """
    df["desertor"] = df["estado"].eq("desertor")
    print(df["desertor"].value_counts())
    df["cuartil_asistencia"] = pd.qcut(
     df["asistencia_pct"],
        q=4
    )
    print(df["cuartil_asistencia"].value_counts(dropna=False).sort_index())
    registrar(
        9,
        "desertor",
        "Crear indicador de deserción",
        len(df),
        "Es True si estado es desertor y False si es activo o graduado."
    )
    registrar(
        9,
        "cuartil_asistencia",
        "Agrupar asistencia en cuatro cuartiles",
        df["cuartil_asistencia"].notna().sum(),
        "Se crean grupos de tamaño aproximado para comparar la deserción según asistencia; los nulos permanecen sin grupo."
    )
    return df
