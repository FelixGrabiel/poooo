import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Datos de ejemplo
datos_ubicacion = {
    'AMAZONAS': 13451,
    'ANCASH': 52491,
    'APURIMAC': 24032,
    'AREQUIPA': 90900,
    'AYACUCHO': 35608,
    'CAJAMARCA': 28956,
    'CALLAO': 26789,
    'CUSCO': 81015,
    'HUANCAVELICA': 16338,
    'HUÁNUCO': 31059,
    'ICA': 38889,
    'JUNIN': 59764,
    'LA LIBERTAD': 50471,
    'LAMBAYEQUE': 22542,
    'LIMA': 308882,
    'LORETO': 23248,
    'MADRE DE DIOS': 8063,
    'MOQUEGUA': 9670,
    'PASCO': 12089,
    'PIURA': 45642,
    'PUNO': 40610,
    'SAN MARTÍN': 39940,
    'TACNA': 17954,
    'TUMBES': 13080,
    'UCAYALI': 12018
}

datos_genero = {
    'Hombres': 156083,
    'Mujeres': 947418
}

datos_anio = {
    '2018': 81009,
    '2019': 113727,
    '2020': 155092,
    '2021': 362694
}

datos_tipos_violencia = {
    'Psicológica': 398699,
    'Física': 327876,
    'Sexual': 101563,
    'Económica': 3905
}

datos_tipos_violencia_genero = {
    'Mujeres': {
        'Psicológica': 313632,
        'Física': 384516,
        'Sexual': 610925,
        'Económica': 708613
    },
    'Hombres': {
        'Psicológica': 279010,
        'Física': 208126,
        'Sexual': 18283,
        'Económica': 115971
    }
}

datos_casos_edad = {
    '0-5': 45660,
    '6-11': 98986,
    '12-17': 121434,
    '18-29': 190476,
    '30-59': 323638,
    '60+': 52208
}

# Definir los colores de los gráficos
colores = {
    'bar': '#FF4500',
    'line': 'red',
    'pie': 'green',
    'box': '#DA70D6',
    'violin': 'purple',
    'histogram': '#87CEEB',
    'network': '#FF00FF'
}

# Definir el estilo CSS para el contenedor principal
estilos_contenedor = {
    'width': '60%',
    'margin': '0 auto',
    'text-align': 'center',
    'font-family': 'Arial, sans-serif'
}

# Definir el estilo CSS para el título
estilos_titulo = {
    'margin-top': '30px',
    'margin-bottom': '50px',
    'font-size': '30px',
    'color': '#000080',
    'text-decoration': 'underline'
}

# Definir el estilo CSS para los dropdowns
estilos_dropdown = {
    'width': '300px',
    'margin-bottom': '30px',
    'font-size': '18px',
    'color': '#FF4500',
    'background-color': '#98FB98',
    'border': 'none',
    'border-radius': '5px',
    'padding': '10px'
}

# Definir el estilo CSS para el gráfico
estilos_grafico = {
    'width': '800px',
    'height': '400px',
    'margin': '0 auto'
    
}

# Definir el diseño de la aplicación
app.layout = html.Div(style=estilos_contenedor, children=[
    html.H1(style=estilos_titulo, children='Gráfico interactivo violencia familiar'),

    html.Div([
        html.H3('Selecciona un dato:'),
        dcc.Dropdown(
            id='dropdown-dato',
            options=[
                {'label': 'Ubicación', 'value': 'ubicacion'},
                {'label': 'Género', 'value': 'genero'},
                {'label': 'Año', 'value': 'anio'},
                {'label': 'Tipos de violencia', 'value': 'datos_tipos_violencia'},
                {'label': 'Tipo de violencia por género', 'value': 'datos_tipos_violencia_genero'},
                {'label': 'Casos por edad', 'value': 'datos_casos_edad'},
            ],
            value='ubicacion',
            style=estilos_dropdown
        ),
    ]),

    html.Div([
        html.H3('Selecciona una comparación:'),
        dcc.Dropdown(
            id='dropdown-comparacion',
            options=[
                {'label': 'Ninguna', 'value': 'ninguna'},
                {'label': 'Ubicación', 'value': 'ubicacion'},
                {'label': 'Género', 'value': 'genero'},
                {'label': 'Año', 'value': 'anio'},
                {'label': 'Tipos de violencia', 'value': 'datos_tipos_violencia'},
                {'label': 'Tipo de violencia por género', 'value': 'datos_tipos_violencia_genero'},
                {'label': 'Casos por edad', 'value': 'datos_casos_edad'},
            ],
            value='ninguna',

            

            style=estilos_dropdown
        ),
    ]),

    html.Div([
        html.H3('Selecciona un tipo de gráfico:'),
        dcc.Dropdown(
            id='dropdown-tipo-grafico',
            options=[
                {'label': 'Barras', 'value': 'bar'},
                {'label': 'Líneas', 'value': 'line'},
                {'label': 'Pastel', 'value': 'pie'},
                {'label': 'Caja y Bigote', 'value': 'box'},
                {'label': 'Violín', 'value': 'violin'},
                {'label': 'Histograma', 'value': 'histogram'},
                {'label': 'Red', 'value': 'network'}
            ],
            value='bar',
            style=estilos_dropdown
        ),
    ]),

    html.Div(id='div-grafico', children=[
        dcc.Graph(id='grafico')
    ], style=estilos_grafico)
])

# Actualizar el gráfico según las selecciones del usuario
@app.callback(
    Output('grafico', 'figure'),
    [Input('dropdown-dato', 'value'),
     Input('dropdown-comparacion', 'value'),
     Input('dropdown-tipo-grafico', 'value')])
def actualizar_grafico(dato, comparacion, tipo_grafico):
    if dato == 'ubicacion':
        if comparacion == 'ninguna':
            datos = datos_ubicacion
            titulo = 'Casos de violencia por ubicación'
        else:
            datos = datos_tipos_violencia_genero[comparacion]
            titulo = f'Casos de violencia por ubicación y género ({comparacion})'
    elif dato == 'genero':
        if comparacion == 'ninguna':
            datos = datos_genero
            titulo = 'Casos de violencia por género'
        else:
            datos = datos_tipos_violencia_genero[comparacion]
            titulo = f'Casos de violencia por género y ubicación ({comparacion})'
    elif dato == 'anio':
        if comparacion == 'ninguna':
            datos = datos_anio
            titulo = 'Casos de violencia por año'
        else:
            datos = datos_tipos_violencia_genero[comparacion]
            titulo = f'Casos de violencia por año y ubicación ({comparacion})'
    elif dato == 'datos_tipos_violencia':
        datos = datos_tipos_violencia
        titulo = 'Casos de violencia por tipo'
    elif dato == 'datos_tipos_violencia_genero':
        datos = datos_tipos_violencia_genero
        titulo = 'Casos de violencia por tipo y género'
    elif dato == 'datos_casos_edad':
        datos = datos_casos_edad
        titulo = 'Casos de violencia por edad'

    figura = go.Figure()
    if tipo_grafico == 'bar':
        figura.add_trace(go.Bar(x=list(datos.keys()), y=list(datos.values()), marker_color=colores[tipo_grafico]))
    elif tipo_grafico == 'line':
        figura.add_trace(go.Scatter(x=list(datos.keys()), y=list(datos.values()), mode='lines', marker_color=colores[tipo_grafico]))
    elif tipo_grafico == 'pie':
        figura.add_trace(go.Pie(labels=list(datos.keys()), values=list(datos.values()), marker=dict(colors=[colores[tipo_grafico]])))
    elif tipo_grafico == 'box':
        figura.add_trace(go.Box(y=list(datos.values()), marker_color=colores[tipo_grafico]))
    elif tipo_grafico == 'violin':
        figura.add_trace(go.Violin(y=list(datos.values()), marker_color=colores[tipo_grafico]))
    elif tipo_grafico == 'histogram':
        figura.add_trace(go.Histogram(x=list(datos.values()), marker_color=colores[tipo_grafico]))
    elif tipo_grafico == 'network':
        figura.add_trace(go.Scatter(x=[0, 1, 2, 3], y=[1, 3, 2, 0], mode='lines', marker_color=colores[tipo_grafico]))

    figura.update_layout(title=titulo)

    return figura


if __name__ == '__main__':
    app.run_server(debug=True)