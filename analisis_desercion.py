import pandas as pd

from modulos.analisis import auditar, explorar, responder_preguntas
from modulos.configuracion import PROCESSED, RAW
from modulos.graficos import (
    grafico_distribuciones,
    grafico_faltantes,
    grafico_tasa_asistencia,
    grafico_tasa_programa,
)
from modulos.limpieza import (
    convertir_fechas,
    convertir_numericos,
    crear_variables,
    eliminar_duplicados,
    tratar_faltantes,
    tratar_imposibles,
    unificar_categorias,
)
from modulos.registro import DECISIONES

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)

def guardar(df):
    """Paso 11 del Word: guardar el dataset limpio y la tabla de decisiones. Ya está escrito."""
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED / "dataset_limpio.csv", index=False)
    pd.DataFrame(DECISIONES).to_csv(PROCESSED / "decisiones.csv", index=False)
    print(f"\nDataset limpio guardado: {df.shape[0]} filas, {df.shape[1]} columnas.")


def main():
    original = pd.read_csv(RAW)
    df = original.copy()

    explorar(df)
    auditar(df)
    grafico_faltantes(df)

    df = convertir_numericos(df)
    df = unificar_categorias(df)
    df = convertir_fechas(df)
    df = eliminar_duplicados(df)
    df = tratar_faltantes(df)
    df = tratar_imposibles(df)
    df = crear_variables(df)

    grafico_distribuciones(original, df)
    grafico_tasa_programa(df)
    grafico_tasa_asistencia(df)

    responder_preguntas(df)
    print("\nTabla de decisiones:")
    print(pd.DataFrame(DECISIONES))
    guardar(df)


if __name__ == "__main__":
    main()
