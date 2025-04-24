# 📊 Linealytics AutoProduction

Una solución integral y automatizada para la **planificación y optimización de la producción industrial**, desarrollada para el **Talen Hackaton 2025 Track Micron** por el equipo **Linealytics**.


### Objetivo Pricipal:

Crear un sistema con Python junto con el ecosistema empresarial de Microsoft, para automatizar los cálculos necesarios para equilibrar la producción con la demanda, permitiendo una planificación más precisa y eficiente y reduciendo los costes, mediante un modelo de XGBoost, Bootstrapping y un sistema de programación lineal.


###  Criterios Principales:

Optimizar el plan de producción mediante programación lineal para satisfacer la demanda minimizando la productividad,teniendo en cuenta el rendimiento, la densidad, el stock de seguridad y un stock objetivo final de cero.Args:initial_stock (float): El nivel de stock inicial.demands (lista de float): La demanda para cada periodo.yield_percentage (float): El porcentaje de rendimiento (0 a 1).density (float): El factor de densidad de producción.max_productivity (float): La productividad máxima por periodo.safety_stocks (lista de float, opcional): El stock de seguridad para cada periodo.Si None, no se aplica ninguna restricción de stock de seguridad.  Debe tener la misma longitud que las demandas si se proporciona.Devuelve:dict: La productividad total óptima.- 'production_levels': Una lista de los niveles óptimos de producción para cada período.- 'ending_stocks': Una lista de los niveles de existencias finales para cada período.- 'status': El estado de la optimización ('Óptimo', 'Inviable', etc.).


### 🚀 Características

- **Predicción precisa de demanda** semanal a través de modelos de Machine Learning.
- **Escenarios simulados** para gestionar la incertidumbre y evitar sobreproducción o escasez.
- **Planificación de producción óptima** semanal basada en restricciones reales.
- **Visualización en dashboards interactivos** para toma de decisiones ejecutiva.
- **Automatización completa del flujo de trabajo** desde la ingesta de datos hasta el envío de reportes.
- **Alertas automáticas** vía email sobre riesgos críticos.
- **Interacción por lenguaje natural** con Microsoft Copilot.


### ⚙️ Tecnologías Utilizadas

- **Frontend:** Power BI
- **Backend:** Python, XGBoost, Bootstrapping, Linear Programming
- **Infraestructura:** Microsoft Azure
- **Automatización:** Power Automate, Microsoft Copilot
- **Metodologías:** SCRUM + CRISP-DM



## Arquitectura


### Host:

Azure


### Data:

- 🎲 **Trasponer** 
- 🧮 **Conversion de trimestres a registros Semanales** 
- 🔍 **EDA**


### BackEnd:

- 🔍 **Predicción de demanda** con XGBoost
- 🎲 **Simulación de escenarios** con Bootstrapping
- 🧮 **Optimización de la producción** con Programación Lineal


### FrontEnd:

- ☁️ **Despliegue automatizado y visualización** con Microsoft Azure, Power BI y Power Automate


### Automatizacion con Microsoft Power Automate

- 📥 Ingesta de datos desde Excel
- 🔧 Transformación a CSV semanales
- 🤖 Modelos predictivos (XGBoost)
- 🎲 Simulaciones (Bootstrapping)
- 🧮 Optimización (Programación Lineal)
- 📊 Visualización (Power BI)
- 📧 Alertas automáticas (Power Automate)



### Notificaciones Via Mail.
Agregar Top Loss o un equivalencia para poder automatizar la notificacion en casos concretos como por ejemplo cuando el modelo detecte sobreproduccion o ruptura de Stock, Reportes semanales de PowerBI, etc. 


### Copilot:

Uso de lenguaje natural para usuarios finales, y que pueden hacer preguntas acerca de los data sets o exceles, PowerBI, etc


## Imagenes


<!-- Imagen 0 -->


<!-- Imagen 1 -->
<h3 align="center">Imagen 1</h3>
<p align="center">
  <img src="Imagenes/1.jpg" width="500px">
</p>

<!-- Imagen 2 -->
<h3 align="center">Imagen 2</h3>
<p align="center">
  <img src="Imagenes/2.jpg" width="500px">
</p>

<!-- Imagen 3 -->
<h3 align="center">Imagen 3</h3>
<p align="center">
  <img src="Imagenes/3.jpg" width="500px">
</p>

<!-- Imagen 4 -->
<h3 align="center">Imagen 4</h3>
<p align="center">
  <img src="Imagenes/4.jpg" width="500px">
</p>

<!-- Imagen 5 -->
<h3 align="center">Imagen 5</h3>
<p align="center">
  <img src="Imagenes/5.jpg" width="500px">
</p>

<!-- Imagen 6 -->
<h3 align="center">Imagen 6</h3>
<p align="center">
  <img src="Imagenes/6.jpg" width="500px">
</p>

<!-- Imagen 7 -->
<h3 align="center">Imagen 7</h3>
<p align="center">
  <img src="Imagenes/7.jpg" width="500px">
</p>

<!-- Imagen 8 -->
<h3 align="center">Imagen 8</h3>
<p align="center">
  <img src="Imagenes/8.jpg" width="500px">
</p>

<!-- Imagen 9 -->
<h3 align="center">Imagen 9</h3>
<p align="center">
  <img src="Imagenes/9.jpg" width="500px">
</p>

<!-- Imagen 10 -->
<h3 align="center">Imagen 10</h3>
<p align="center">
  <img src="Imagenes/10.jpg" width="500px">
</p>

<!-- Imagen 11 -->
<h3 align="center">Imagen 11</h3>
<p align="center">
  <img src="Imagenes/11.jpg" width="500px">
</p>

<!-- Imagen 12 -->
<h3 align="center">Imagen 12</h3>
<p align="center">
  <img src="Imagenes/12.png" width="500px">
</p>

<!-- Imagen 13 -->
<h3 align="center">Imagen 13</h3>
<p align="center">
  <img src="Imagenes/13.jpg" width="500px">
</p>

<!-- Imagen 14 -->
<h3 align="center">Imagen 14</h3>
<p align="center">
  <img src="Imagenes/14.png" width="500px">
</p>

<!-- Imagen 15 -->
<h3 align="center">Imagen 15</h3>
<p align="center">
  <img src="Imagenes/15.png" width="500px">
</p>

<!-- Imagen 16 -->
<h3 align="center">Imagen 16</h3>
<p align="center">
  <img src="Imagenes/16.jpg" width="500px">
</p>

<!-- Imagen 17 -->
<h3 align="center">Imagen 17</h3>
<p align="center">
  <img src="Imagenes/17.jpg" width="500px">
</p>

<!-- Imagen 18 -->
<h3 align="center">Imagen 18</h3>
<p align="center">
  <img src="Imagenes/18.png" width="500px">
</p>

<!-- Imagen 19 -->
<h3 align="center">Imagen 19</h3>
<p align="center">
  <img src="Imagenes/19.png" width="500px">
</p>
