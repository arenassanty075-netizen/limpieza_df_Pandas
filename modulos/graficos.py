import matplotlib.pyplot as plt
import seaborn as sns

from .configuracion import GRAFICOS


def grafico_faltantes(df):
    """Gráfico 1: mapa de faltantes del dataset original.

    Pista: sns.heatmap(df.isnull(), cbar=False)
    """
    plt.figure(figsize=(12, 6))
    sns.heatmap(df.isnull(), cbar=False)
    plt.title("Mapa de colores faltantes")
    plt.tight_layout()
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    plt.savefig(GRAFICOS / "mapa_faltantes.png")
    plt.show()





def grafico_distribuciones(antes, despues):
    """Gráfico 2: boxplots de promedio_acumulado y edad, antes y después de limpiar.

    Pregunta: ¿qué cambió en cada distribución? ¿Por qué?
    """

    fig, ejes = plt.subplots(2, 2, figsize=(12, 8))

    variables = [
        ("promedio_acumulado", "Promedio"),
        ("edad", "Edad")
    ]

    for fila, (columna, etiqueta) in enumerate(variables):
        for posicion, (datos, momento) in enumerate([
            (antes, "antes"),
            (despues, "después")
        ]):
            ax = ejes[fila, posicion]

            ax.boxplot(datos[columna].dropna())
            ax.set_title(f"{etiqueta} {momento} de limpiar")
            ax.set_ylabel(etiqueta)
            ax.set_xticks([])
            ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()

    GRAFICOS.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        GRAFICOS / "distribuciones_antes_despues.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()



def grafico_tasa_programa(df):
    """Gráfico 3: tasa de deserción por programa.

    Pista: df.groupby("programa")["desertor"].mean()
    """
    tasas = df.groupby("programa")["desertor"].mean()
    porcentajes = tasas * 100
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(porcentajes.index, porcentajes.values)
    ax.set_title("Tasa de deserción por programa")
    ax.set_xlabel("Deserción (%)")
    ax.set_ylabel("Programa")
    fig.tight_layout()
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    fig.savefig(GRAFICOS / "tasa_desercion_por_programa.png")
    plt.show()





def grafico_tasa_asistencia(df):
    """Gráfico 4: tasa de deserción por cuartil de asistencia.

    Pista: df.groupby("cuartil_asistencia", observed=True)["desertor"].mean()
    """
    tasas = df.groupby(
        "cuartil_asistencia", observed=True
    )["desertor"].mean()
    porcentajes = tasas * 100
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(porcentajes.index.astype(str), porcentajes.values)
    ax.set_title("Tasa de deserción por cuartil de asistencia")
    ax.set_xlabel("Cuartil de asistencia (%)")
    ax.set_ylabel("Deserción (%)")
    fig.tight_layout()
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    fig.savefig(GRAFICOS / "tasa_desercion_por_asistencia.png")
    plt.show()
