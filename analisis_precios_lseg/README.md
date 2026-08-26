# Análisis de Precios Financieros con LSEG Data & Analytics

Paquete Python modular para descargar, analizar y visualizar datos financieros usando **LSEG Data & Analytics** (anteriormente Refinitiv Data Platform).

## 📋 Descripción

Este proyecto proporciona herramientas para:
- 📥 **Descargar** datos históricos de instrumentos financieros desde LSEG Data & Analytics
- 📊 **Analizar** estadísticas, rendimientos, volatilidad y métricas clave
- 📈 **Visualizar** precios, rendimientos y comparaciones entre instrumentos

## 📦 Estructura del Proyecto

```
analisis_precios_lseg/
├── data/                    # Módulo de descarga de datos
│   ├── downloader.py        # Clase LSEGDataDownloader
│   └── __init__.py
├── analysis/                # Módulo de análisis estadístico
│   ├── analyzer.py          # Clase FinancialAnalyzer
│   └── __init__.py
├── visualization/           # Módulo de visualización
│   ├── plotter.py           # Clase FinancialPlotter
│   └── __init__.py
├── examples/                # Ejemplos de uso
│   └── run_analysis.py      # Script de ejemplo completo
├── __init__.py
├── README.md                # Este archivo
└── USAGE.md                 # Guía de uso detallada
```

## 🔧 Requisitos

### Paquetes Python
```python
lseg-data         # API de LSEG Data & Analytics
pandas            # Manejo de datos
numpy             # Cálculos numéricos
matplotlib        # Visualización
```

### Credenciales LSEG
Necesitas credenciales de LSEG Data & Analytics:
- **App Key** (API Key)
- **Username** (correo electrónico)
- **Password**

**Recomendación**: Almacena tus credenciales en **Databricks Secrets** para mayor seguridad.

## 🚀 Instalación

### 1. Instalar lseg-data
```python
%pip install lseg-data --quiet
```

### 2. Configurar Databricks Secrets (Recomendado)
```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Crear secret scope
w.secrets.create_scope(scope="refinitiv_scope")

# Almacenar credenciales
w.secrets.put_secret(scope="refinitiv_scope", key="app_key", string_value="TU_APP_KEY")
w.secrets.put_secret(scope="refinitiv_scope", key="username", string_value="tu_email@ejemplo.com")
w.secrets.put_secret(scope="refinitiv_scope", key="password", string_value="TU_PASSWORD")
```

## 📖 Uso Básico

### Ejemplo Completo

```python
import sys
sys.path.append('/Workspace/Users/tu_email@ejemplo.com')

from analisis_precios_lseg.data import LSEGDataDownloader
from analisis_precios_lseg.analysis import FinancialAnalyzer
from analisis_precios_lseg.visualization import FinancialPlotter

# 1. Descargar datos (usa credentials de Databricks Secrets automáticamente)
downloader = LSEGDataDownloader('AAPL.O')  # Apple en NYSE
data = downloader.download_data(days=180)   # Últimos 180 días

# 2. Analizar
analyzer = FinancialAnalyzer(data, ticker='AAPL.O')
analyzer.print_summary()

# 3. Visualizar
plotter = FinancialPlotter(data, ticker='AAPL.O')
plotter.plot_price_series(show_volume=True)
plotter.plot_with_moving_averages()
plotter.create_dashboard()

# 4. Cerrar sesión
downloader.close_session()
```

### Sin usar Databricks Secrets

```python
downloader = LSEGDataDownloader(
    'AAPL.O',
    app_key="TU_APP_KEY",
    username="tu_email@ejemplo.com",
    password="TU_PASSWORD",
    use_secrets=False
)
```

## 📄 Ejemplos de Reuters Instrument Codes (RIC)

| Instrumento | RIC |
|------------|-----|
| Apple | AAPL.O |
| Microsoft | MSFT.O |
| Google | GOOGL.O |
| Amazon | AMZN.O |
| Tesla | TSLA.O |
| Meta | META.O |

## 📊 Funcionalidades

### 1. Descarga de Datos (`LSEGDataDownloader`)
- Descarga histórica por número de días o rango de fechas
- Manejo automático de sesión LSEG
- Integración con Databricks Secrets
- Datos OHLCV (Open, High, Low, Close, Volume)

### 2. Análisis (`FinancialAnalyzer`)
- Estadísticas básicas (min, max, mean, std)
- Cálculo de rendimientos
- Volatilidad anualizada
- Medias móviles
- Puntos extremos (máximos y mínimos)
- Reporte completo de análisis

### 3. Visualización (`FinancialPlotter`)
- Gráfico de serie de tiempo con volumen
- Precios con medias móviles
- Distribución de rendimientos
- Comparación entre instrumentos
- Dashboard completo

## 📝 Diferencias con `analisis_precios` (Yahoo Finance)

| Aspecto | analisis_precios | analisis_precios_lseg |
|---------|------------------|----------------------|
| Fuente de datos | Yahoo Finance (yfinance) | LSEG Data & Analytics |
| Autenticación | No requiere | Requiere credenciales |
| Símbolos | Tickers (AAPL, MSFT) | RIC (AAPL.O, MSFT.O) |
| Calidad de datos | Gratis, limitada | Profesional, de pago |
| Cobertura | Instrumentos públicos | Mercados globales |

## 🛠️ Troubleshooting

### Error de autenticación
```python
# Verifica que tus credenciales estén correctas
downloader = LSEGDataDownloader(
    'AAPL.O',
    app_key="TU_APP_KEY",
    username="tu_email@ejemplo.com",
    password="TU_PASSWORD",
    use_secrets=False
)
```

### No se encuentran datos
- Verifica que el RIC sea correcto (AAPL.O, no AAPL)
- Algunos instrumentos pueden no tener datos históricos completos
- Intenta con un rango de fechas diferente

## 📚 Más Información

Consulta [USAGE.md](./USAGE.md) para ejemplos avanzados y casos de uso adicionales.

## 📝 Licencia

Proyecto educativo - ITESM 2026

## ✍️ Autor

Creado para el curso de Finanzas 2026 - Agosto
