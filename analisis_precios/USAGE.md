# Guía Rápida de Uso

## Cómo usar el paquete desde cualquier notebook

### Paso 1: Instalar dependencias

```python
%pip install yfinance
```

### Paso 2: Importar el paquete

```python
import sys
sys.path.append('/Workspace/Users/nvaldez@tec.mx')

from analisis_precios.data.downloader import FinancialDataDownloader
from analisis_precios.analysis.analyzer import FinancialAnalyzer
from analisis_precios.visualization.plotter import FinancialPlotter
```

### Paso 3: Usar las clases

```python
# Descargar datos
downloader = FinancialDataDownloader('AAPL')
data = downloader.download_data(days=180)

# Analizar
analyzer = FinancialAnalyzer(data, 'AAPL')
analyzer.print_summary()

# Visualizar
plotter = FinancialPlotter(data, 'AAPL')
plotter.plot_price_series(show_volume=True)
```

## Ejemplos Rápidos

### Analizar cualquier instrumento

```python
# Solo cambia el ticker
for ticker in ['AAPL', 'MSFT', 'GOOGL', 'TSLA']:
    downloader = FinancialDataDownloader(ticker)
    data = downloader.download_data(days=90)
    
    analyzer = FinancialAnalyzer(data, ticker)
    print(f"\nRendimiento de {ticker}: {analyzer.calculate_cumulative_return():.2f}%")
```

### Usar fechas personalizadas

```python
downloader = FinancialDataDownloader('AAPL')
data = downloader.download_data(
    start_date='2023-01-01',
    end_date='2023-12-31'
)
```

### Comparar dos instrumentos

```python
# Instrumento 1
downloader1 = FinancialDataDownloader('AAPL')
data1 = downloader1.download_data(days=365)

# Instrumento 2
downloader2 = FinancialDataDownloader('MSFT')
data2 = downloader2.download_data(days=365)

# Comparar
plotter = FinancialPlotter(data1, 'AAPL')
plotter.plot_comparison(data2, 'MSFT', normalize=True)
```

### Crear dashboard

```python
downloader = FinancialDataDownloader('TSLA')
data = downloader.download_data(days=180)

plotter = FinancialPlotter(data, 'TSLA')
plotter.create_dashboard()
```

## Métodos Disponibles

### FinancialDataDownloader

* `download_data(days=N)` - Descargar últimos N días
* `download_data(start_date='YYYY-MM-DD', end_date='YYYY-MM-DD')` - Fechas específicas
* `get_company_name()` - Nombre de la compañía
* `get_ticker_info()` - Información completa del ticker
* `close_prices` - Serie de precios de cierre
* `volume` - Serie de volumen

### FinancialAnalyzer

* `get_basic_statistics()` - Estadísticas básicas
* `calculate_returns(period=1)` - Rendimientos
* `calculate_volatility(window=30)` - Volatilidad
* `calculate_cumulative_return()` - Rendimiento total
* `calculate_moving_averages(windows=[20,50,200])` - Medias móviles
* `find_extremes()` - Máximos y mínimos
* `get_summary_report()` - Reporte JSON completo
* `print_summary()` - Imprime resumen formateado

### FinancialPlotter

* `plot_price_series(show_volume=True/False)` - Serie de tiempo
* `plot_with_moving_averages(windows=[20,50])` - Precio con MAs
* `plot_returns_distribution()` - Histograma de rendimientos
* `plot_comparison(other_data, other_ticker, normalize=True)` - Comparar instrumentos
* `create_dashboard()` - Dashboard completo

## Tips

* ➡️ **Usa fechas reales**: Los datos vienen de Yahoo Finance, fechas futuras no funcionan
* ➡️ **Tickers válidos**: Verifica que el ticker exista en Yahoo Finance
* ➡️ **Normaliza para comparar**: Cuando compares instrumentos con precios muy diferentes, usa `normalize=True`
* ➡️ **Ajusta ventanas**: Para períodos cortos (<90 días), usa ventanas más pequeñas en las MAs

## Ver Más

* [README.md](README.md) - Documentación completa
* [examples/run_analysis.py](examples/run_analysis.py) - Ejemplos avanzados
* [Ejemplo Uso analisis_precios](#notebook-3166066755026715) - Notebook interactivo