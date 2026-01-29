# Métricas de Facebook e Instagram con Meta Graph API

Este proyecto implementa una automatización para la obtención de métricas de Facebook e Instagram mediante la **Meta Graph API**, permitiendo extraer, estructurar y analizar datos de desempeño de páginas administradas.

---

## Tecnologías utilizadas

- Python  
- Meta Graph API  
- facebook-sdk  
- pandas  

---

## Instalación de dependencias

```bash
pip install facebook-sdk
pip install pandas
```
## Token de cuenta
Se utiliza un User Access Token para acceder a las páginas administradas por la cuenta.
```python
import facebook-sdk
import pandas

# datos de la app creada en Facebook Developers
app_id = '1234'
app_secret = 'abcd'
token = ''

graph = facebook.GraphAPI(access_token=user_long_token, version=3.1)
```
## Token de página
A partir del token de usuario se obtiene el Page Access Token para consultar métricas de una página específica.
```python
page_data = graph.get_object('/me/accounts')

permanent_page_token = page_data['data'][#id de cuenta]['access_token']
graph = facebook.GraphAPI(access_token=permanent_page_token, version=3.1)
page_data = graph.get_object('/me/accounts')
```
## Obtencion de métricas
Ejemplo de consulta de interacciones diarias utilizando el endpoint insights:
```python
interacciones = graph.get_connections(
    id=page_id,
    connection_name='insights',
    metric='page_post_engagements',
    period='day',
    since='2026-01-01',
    until='2026-01-12'
)
```
## Uso de los datos
Las métricas obtenidas pueden utilizarse para:
*Análisis de desempeño de contenidos
*Seguimiento de KPIs
*Automatización de reportes
*Integración con dashboards (Power BI, Tableau, etc.)

## Fuentes y documentación

- **Meta Graph API (documentación oficial)**  
  https://developers.facebook.com/docs/graph-api/

- **Insights API**  
  https://developers.facebook.com/docs/graph-api/reference/insights/

- **Page Insights**  
  https://developers.facebook.com/docs/graph-api/reference/page/insights/

- **facebook-sdk (Python)**  
  https://github.com/mobolic/facebook-sdk


