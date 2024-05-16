from dbfread import DBF
from pyproj import Transformer
from pandas import DataFrame
import altair as alt
import pandas as pd
import plotly.express as px
import seaborn as sns

import matplotlib.pyplot as plt

import seaborn as sns
import pandas as pd

import pandas as pd
import altair as alt
from ipywidgets import interact, Dropdown


def show_covid_interact(x, y):
    # Carga de datos
    spain_data = pd.read_csv(
        "https://raw.githubusercontent.com/victorvicpal/COVID19_es/master/data/final_data/dataCOVID19_es.csv"
    )

    # Asegurarse de que 'fecha' se interprete como fecha
    spain_data["fecha"] = pd.to_datetime(spain_data["fecha"])

    # Crear un gráfico de dispersión
    chart = (
        alt.Chart(spain_data)
        .mark_point(color="gray")
        .encode(
            x=x,
            y=y,
            tooltip=[alt.Tooltip(x, title="X axis"), alt.Tooltip(y, title="Y axis")],
        )
        .properties(title="COVID-19 Data Visualization", width=800, height=600)
    )

    return chart


def plot_seaborn_sample():
    data = {
        "Ciudad": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza"],
        "Visitantes": [500000, 600000, 200000, 300000, 150000],
    }
    df = pd.DataFrame(data)
    sns.barplot(x="Ciudad", y="Visitantes", data=df)
    plt.title("Número de Visitantes por Ciudad en España")
    plt.show()


def plot_matplotlib_sample():
    data = {
        "Ciudad": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza"],
        "Visitantes": [500000, 600000, 200000, 300000, 150000],
    }
    fig, ax = plt.subplots()
    ax.bar(data["Ciudad"], data["Visitantes"])
    ax.set_title("Número de Visitantes por Ciudad en España")
    ax.set_xlabel("Ciudad")
    ax.set_ylabel("Visitantes")
    plt.show()


def get_pluviodata():
    """
    muestra los datos plubiometricos en un dataframe
    """
    pluvio = DBF("aemet_pluviometricas/Estaciones_Pluviometricas.dbf")
    pluvio = DataFrame(pluvio)
    transformer = Transformer.from_crs("EPSG:25830", "EPSG:4326")
    pluvio[["COORD_Y", "COORD_X"]] = pluvio.apply(
        lambda x: transformer.transform(x.COORD_X, x.COORD_Y),
        axis=1,
        result_type="expand",
    )
    pluvio.to_parquet(path="aemet_pluviometricas/pluvio.parquet", index=False)
    #    print(pluvio.head())
    print("Pluviometric stations data saved to 'aemet_pluviometricas/pluvio.parquet'.")
    return pluvio


def get_altair_sample():
    # Simulando un conjunto de datos
    data = {
        "Ciudad": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza"],
        "Visitantes": [500000, 600000, 200000, 300000, 150000],
    }

    df = pd.DataFrame(data)

    # Creando el gráfico
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="Ciudad", y="Visitantes", color="Ciudad", tooltip=["Ciudad", "Visitantes"]
        )
        .properties(
            width=600, height=400, title="Número de Visitantes por Ciudad en España"
        )
    )
    chart.save("Número de Visitantes por Ciudad en España.html")


def get_plotly_figure():
    df = pd.DataFrame(
        {
            "Ciudad": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza"],
            "Visitantes": [500000, 600000, 200000, 300000, 150000],
        }
    )
    fig = px.bar(
        df,
        x="Ciudad",
        y="Visitantes",
        color="Ciudad",
        title="Número de Visitantes por Ciudad en España",
    )
    fig.show()


def seaborn_figure():
    df = pd.DataFrame(
        {
            "Ciudad": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza"],
            "Visitantes": [500000, 600000, 200000, 300000, 150000],
        }
    )
    sns.barplot(x="Ciudad", y="Visitantes", hue="Ciudad", data=df)
    plt.title("Número de Visitantes por Ciudad en España")
    plt.show()

    # Load the data


def show_covid():
    # header
    # CCAA,fecha,casos,IA,UCI,muertes,nuevos,Hospitalizados,HospitalizadosNuevos,
    # UCINuevos,muertesNuevos,curados,curadosNuevos,PCR,testrap,incr %,postestrap,
    # posAsintomaticos,posTOTAL

    # Carga de datos
    spain_data = pd.read_csv(
        "https://raw.githubusercontent.com/victorvicpal/COVID19_es/master/data/final_data/dataCOVID19_es.csv"
    )

    # Asegurarse de que 'fecha' se interprete como fecha
    spain_data["fecha"] = pd.to_datetime(spain_data["fecha"])

    # Crear un gráfico de dispersión de casos confirmados por fecha
    chart = (
        alt.Chart(spain_data)
        .mark_point(color="gray")
        .encode(
            x="fecha:T",  # Cambiado de 'date' a 'fecha'
            y="casos:Q",  # Cambiado de 'confirmed' a 'casos'
            tooltip=[
                alt.Tooltip("fecha:T", format="%Y-%m-%d", title="Fecha"),
                alt.Tooltip("casos:Q", title="Casos Confirmados"),
            ],
        )
        .properties(title="Confirmed Cases of COVID-19 in Spain", width=800, height=600)
    )
    path = "datos_COVID19.html"
    print(f"file saved in {path}")
    # Guardar el gráfico como HTML
    chart.save(path)


def interact_jupyter_covid():
    # Obtener los nombres de las columnas para las opciones del eje X e Y
    data = pd.read_csv(
        "https://raw.githubusercontent.com/victorvicpal/COVID19_es/master/data/final_data/dataCOVID19_es.csv"
    )
    options = list(data.columns)

    # Crear widgets de dropdown para seleccionar las columnas para los ejes X e Y
    x_dropdown = Dropdown(options=options, value="fecha", description="X-axis:")
    y_dropdown = Dropdown(options=options, value="casos", description="Y-axis:")

    # Usar interact para actualizar el gráfico basado en las selecciones
    interact(show_covid_interact, x=x_dropdown, y=y_dropdown)


if __name__ == "__main__":

    get_pluviodata()
    get_altair_sample()
    get_plotly_figure()
    seaborn_figure()
    plot_matplotlib_sample()
    plot_seaborn_sample()

    print("Done!")
