import json

from flask import Flask, render_template, request
import pandas as pd
import altair as alt

app = Flask(__name__)

# Carga de datos
spain_data = pd.read_csv(
    "https://raw.githubusercontent.com/victorvicpal/COVID19_es/master/data/final_data/dataCOVID19_es.csv"
)
print("Spain data initialized!")

# Asegurarse de que 'fecha' se interprete como fecha
spain_data["fecha"] = pd.to_datetime(spain_data["fecha"])

# Lista de columnas para seleccionar
columnas = spain_data.columns.tolist()


@app.route("/", methods=["GET", "POST"])
def show_covid():

    x_axis = request.form.get("x_axis", "fecha")
    y_axis = request.form.get("y_axis", "casos")
    print(
        f"x_axis: {x_axis} {spain_data[x_axis].dtype}, y_axis: {y_axis} {spain_data[y_axis].dtype}"
    )

    # Crear un gráfico de dispersión
    chart = (
        alt.Chart(spain_data)
        .mark_point(color="gray")
        .encode(
            x=alt.X(
                x_axis,
                type=(
                    "quantitative"
                    if spain_data[x_axis].dtype != "object"
                    else "nominal"
                ),
            ),
            y=alt.Y(y_axis, type="quantitative"),
            tooltip=[
                alt.Tooltip(x_axis, title=x_axis),
                alt.Tooltip(y_axis, title=y_axis),
            ],
        )
        .properties(title=f"{y_axis} vs {x_axis} in Spain", width=800, height=600)
        .interactive()
    )

    # Convertir el gráfico a JSON
    chart_json = json.dumps(chart.to_dict(), indent=2)

    print(json.dumps(chart_json, indent=5))
    return render_template(
        "index.html", chart=chart_json, columnas=columnas, x_axis=x_axis, y_axis=y_axis
    )


if __name__ == "__main__":
    app.run(debug=True)
