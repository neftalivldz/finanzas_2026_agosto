# Análisis de Precios - Sistema de Análisis Financiero

Sistema orientado a objetos para análisis de instrumentos financieros en Python, diseñado con buenas prácticas y arquitectura modular.

## 📁 Estructura del Proyecto

```
analisis_precios/
├── __init__.py
├── README.md
├── data/
│   ├── __init__.py
│   └── downloader.py          # Clase para descargar datos de Yahoo Finance
├── analysis/
│   ├── __init__.py
│   └── analyzer.py             # Clase para análisis estadístico
├── visualization/
│   ├── __init__.py
│   └── plotter.py              # Clase para visualización de datos
└── examples/
    ├── __init__.py
    └── run_analysis.py         # Ejemplos de uso
```

## 🎯 Características

### 1. Descarga de Datos (`FinancialDataDownloader`)
- Descarga datos históricos de cualquier instrumento de Yahoo Finance
- Soporte para períodos personalizados (días, fechas específicas)
- Diferentes intervalos (diario, semanal, mensual, horario)
- Acceso a información de la compañía

### 2. Análisis Estadístico (`FinancialAnalyzer`)
- Estadísticas básicas (mínimo, máximo, promedio, desviación estándar)
- Cálculo de rendimientos (simples y acumulados)
- Volatilidad anualizada
- Medias móviles simples
- Identificación de extremos
- Reportes completos

### 3. Visualización (`FinancialPlotter`)
- Gráficos de series de tiempo
- Precio con volumen
- Medias móviles
- Distribución de rendimientos
- Comparación entre instrumentos
- Dashboards completos

## 🚀 Instalación

### Requisitos
```python
pip install yfinance pandas numpy matplotlib
```

## 💡 Uso Básico

### Ejemplo 1: Análisis Simple

```python
import sys
sys.path.append('/Workspace/Users/nvaldez@tec.mx')

from analisis_precios.data.downloader import FinancialDataDownloader
from analisis_precios.analysis.analyzer import FinancialAnalyzer
from analisis_precios.visualization.plotter import FinancialPlotter

# 1. Descargar datos
downloader = FinancialDataDownloader('AAPL')
data = downloader.download_data(days=180)

# 2. Analizar
analyzer = FinancialAnalyzer(data, 'AAPL')
analyzer.print_summary()

# 3. Visualizar
plotter = FinancialPlotter(data, 'AAPL')
plotter.plot_price_series(show_volume=True)
```

### Ejemplo 2: Análisis con Fechas Específicas

```python
downloader = FinancialDataDownloader('MSFT')
data = downloader.download_data(
    start_date='2023-01-01',
    end_date='2023-12-31'
)
```

### Ejemplo 3: Comparación de Instrumentos

```python
# Descargar dos instrumentos
downloader1 = FinancialDataDownloader('AAPL')
data1 = downloader1.download_data(days=365)

downloader2 = FinancialDataDownloader('MSFT')
data2 = downloader2.download_data(days=365)

# Comparar
plotter = FinancialPlotter(data1, 'AAPL')
plotter.plot_comparison(data2, 'MSFT', normalize=True)
```

### Ejemplo 4: Dashboard Completo

```python
downloader = FinancialDataDownloader('TSLA')
data = downloader.download_data(days=180)

plotter = FinancialPlotter(data, 'TSLA')
plotter.create_dashboard()
```

## 📊 API Reference

### FinancialDataDownloader

```python
downloader = FinancialDataDownloader(ticker='AAPL')

# Métodos principales
downloader.download_data(days=180)  # Últimos N días
downloader.download_data(start_date='2023-01-01', end_date='2023-12-31')
downloader.get_ticker_info()  # Información del ticker
downloader.get_company_name()  # Nombre de la compañía

# Propiedades
downloader.close_prices  # Serie de precios de cierre
downloader.volume  # Serie de volumen
```

### FinancialAnalyzer

```python
analyzer = FinancialAnalyzer(data, ticker='AAPL')

# Métodos principales
analyzer.get_basic_statistics()  # Dict con stats básicas
analyzer.calculate_returns(period=1)  # Rendimientos
analyzer.calculate_volatility(window=30)  # Volatilidad
analyzer.calculate_cumulative_return()  # Rendimiento acumulado
analyzer.calculate_moving_averages(windows=[20, 50, 200])
analyzer.find_extremes()  # Máximos y mínimos
analyzer.get_summary_report()  # Reporte completo
analyzer.print_summary()  # Imprime resumen formateado
```

### FinancialPlotter

```python
plotter = FinancialPlotter(data, ticker='AAPL')

# Métodos de visualización
plotter.plot_price_series(show_volume=True)
plotter.plot_with_moving_averages(windows=[20, 50, 200])
plotter.plot_returns_distribution()
plotter.plot_comparison(other_data, other_ticker, normalize=True)
plotter.create_dashboard()  # Dashboard completo
```

## 🎓 Ejemplos Avanzados

Ver el archivo `examples/run_analysis.py` para ejemplos completos de:
- Análisis individual de instrumentos
- Comparación entre múltiples instrumentos
- Generación de reportes

## 🏗️ Arquitectura y Buenas Prácticas

### Principios Aplicados

1. **Separación de Responsabilidades (SRP)**
   - `downloader.py`: Solo descarga datos
   - `analyzer.py`: Solo análisis estadístico
   - `plotter.py`: Solo visualización

2. **Encapsulación**
   - Atributos privados con propiedades públicas
   - Validación de datos en constructores

3. **Reutilización**
   - Clases genéricas aplicables a cualquier instrumento
   - Métodos parametrizables

4. **Documentación**
   - Docstrings en formato Google
   - Type hints en todos los métodos
   - Comentarios explicativos

5. **Manejo de Errores**
   - Validación de inputs
   - Mensajes de error descriptivos
   - Excepciones apropiadas

### Extensibilidad

El sistema está diseñado para ser fácilmente extensible:

```python
# Ejemplo: Agregar nuevos análisis
class AdvancedAnalyzer(FinancialAnalyzer):
    def calculate_sharpe_ratio(self, risk_free_rate=0.02):
        # Tu implementación
        pass
    
    def calculate_beta(self, market_data):
        # Tu implementación
        pass
```

## 📝 Notas

- Todos los precios asumen USD
- La volatilidad se anualiza usando 252 días de trading
- Los datos provienen de Yahoo Finance
- Se requiere conexión a internet para descargar datos

## 🤝 Contribuciones

Para agregar nuevas funcionalidades:
1. Mantén la estructura modular
2. Documenta todos los métodos
3. Sigue las convenciones de naming de Python
4. Agrega ejemplos de uso

## 📧 Contacto

Proyecto desarrollado para ITESM 2026

---

**Última actualización:** Agosto 2026