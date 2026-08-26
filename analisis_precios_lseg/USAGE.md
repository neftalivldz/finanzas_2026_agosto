# Guía de Uso Detallada - analisis_precios_lseg

## 📑 Tabla de Contenidos

1. [Configuración Inicial](#configuración-inicial)
2. [Descarga de Datos](#descarga-de-datos)
3. [Análisis Estadístico](#análisis-estadístico)
4. [Visualización](#visualización)
5. [Ejemplos Avanzados](#ejemplos-avanzados)

---

## 🔧 Configuración Inicial

### Instalación de Dependencias

```python
# Instalar lseg-data
%pip install lseg-data --quiet
```

### Configurar Databricks Secrets

**Opción 1: Usando Python (Recomendado)**

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Crear scope
try:
    w.secrets.create_scope(scope="refinitiv_scope")
    print("✓ Scope creado")
except Exception as e:
    print(f"Scope ya existe o error: {e}")

# Guardar credenciales
w.secrets.put_secret(
    scope="refinitiv_scope",
    key="app_key",
    string_value="TU_APP_KEY_AQUI"
)

w.secrets.put_secret(
    scope="refinitiv_scope",
    key="username",
    string_value="tu_email@ejemplo.com"
)

w.secrets.put_secret(
    scope="refinitiv_scope",
    key="password",
    string_value="TU_PASSWORD_AQUI"
)

print("✓ Credenciales guardadas en Databricks Secrets")
```

**Opción 2: Usar credenciales directamente (No recomendado para producción)**

```python
from analisis_precios_lseg.data import LSEGDataDownloader

downloader = LSEGDataDownloader(
    'AAPL.O',
    app_key="TU_APP_KEY",
    username="tu_email@ejemplo.com",
    password="TU_PASSWORD",
    use_secrets=False
)
```

---

## 📥 Descarga de Datos

### 1. Importar el Módulo

```python
import sys
sys.path.append('/Workspace/Users/tu_email@ejemplo.com')

from analisis_precios_lseg.data import LSEGDataDownloader
```

### 2. Crear Instancia del Downloader

```python
# Con Databricks Secrets (Recomendado)
downloader = LSEGDataDownloader('AAPL.O')

# Sin Secrets
downloader = LSEGDataDownloader(
    'AAPL.O',
    app_key="TU_APP_KEY",
    username="tu_email@ejemplo.com",
    password="TU_PASSWORD",
    use_secrets=False
)
```

### 3. Descargar Datos

**Por número de días:**

```python
# Últimos 30 días
data = downloader.download_data(days=30)

# Últimos 6 meses (~180 días)
data = downloader.download_data(days=180)

# Último año (~365 días)
data = downloader.download_data(days=365)
```

**Por rango de fechas:**

```python
data = downloader.download_data(
    start_date='2023-01-01',
    end_date='2023-12-31'
)
```

**Con diferentes intervalos:**

```python
# Datos diarios (por defecto)
data = downloader.download_data(days=90, interval='1D')

# Datos semanales
data = downloader.download_data(days=365, interval='1W')

# Datos mensuales
data = downloader.download_data(days=730, interval='1M')
```

### 4. Acceder a Propiedades

```python
# Precios de cierre
close_prices = downloader.close_prices

# Volumen
volume = downloader.volume

# DataFrame completo
df = downloader.data
print(df.head())
```

### 5. Cerrar Sesión
```python
# Siempre cerrar la sesión al terminar
downloader.close_session()
```

---

## 📊 Análisis Estadístico

### 1. Crear Analizador

```python
from analisis_precios_lseg.analysis import FinancialAnalyzer

analyzer = FinancialAnalyzer(data, ticker='AAPL.O')
```

### 2. Estadísticas Básicas

```python
stats = analyzer.get_basic_statistics()
print(f"Precio actual: ${stats['current']:.2f}")
print(f"Mínimo: ${stats['min']:.2f}")
print(f"Máximo: ${stats['max']:.2f}")
print(f"Promedio: ${stats['mean']:.2f}")
print(f"Desv. Estándar: ${stats['std']:.2f}")
```

### 3. Rendimientos

```python
# Rendimientos diarios
returns = analyzer.calculate_returns(period=1)

# Rendimientos semanales
weekly_returns = analyzer.calculate_returns(period=5)

# Rendimiento acumulado del período
cum_return = analyzer.calculate_cumulative_return()
print(f"Rendimiento acumulado: {cum_return:.2f}%")
```

### 4. Volatilidad

```python
# Volatilidad de los últimos 30 días
vol_30 = analyzer.calculate_volatility(window=30)
print(f"Volatilidad 30d anualizada: {vol_30:.2f}%")

# Volatilidad de los últimos 60 días
vol_60 = analyzer.calculate_volatility(window=60)
print(f"Volatilidad 60d anualizada: {vol_60:.2f}%")
```

### 5. Medias Móviles

```python
# Calcular medias móviles de 20, 50 y 200 días
mas = analyzer.calculate_moving_averages(windows=[20, 50, 200])
print(mas.tail())
```

### 6. Puntos Extremos

```python
extremes = analyzer.find_extremes()

print(f"Máximo histórico:")
print(f"  Fecha: {extremes['max']['date']}")
print(f"  Precio: ${extremes['max']['price']:.2f}")

print(f"\nMínimo histórico:")
print(f"  Fecha: {extremes['min']['date']}")
print(f"  Precio: ${extremes['min']['price']:.2f}")
```

### 7. Reporte Completo

```python
# Imprimir reporte formateado
analyzer.print_summary()

# O obtener diccionario con todos los datos
report = analyzer.get_summary_report()
```

---

## 📈 Visualización

### 1. Crear Plotter

```python
from analisis_precios_lseg.visualization import FinancialPlotter

plotter = FinancialPlotter(data, ticker='AAPL.O')
```

### 2. Serie de Precios

```python
# Gráfico simple
plotter.plot_price_series()

# Con volumen
plotter.plot_price_series(show_volume=True)

# Personalizado
plotter.plot_price_series(
    title="Apple - Análisis 2023",
    figsize=(16, 8),
    color='#FF6600',
    show_volume=True
)
```

### 3. Precios con Medias Móviles

```python
# Medias por defecto (20, 50, 200)
plotter.plot_with_moving_averages()

# Medias personalizadas
plotter.plot_with_moving_averages(
    windows=[10, 30, 90],
    figsize=(16, 8)
)
```

### 4. Distribución de Rendimientos

```python
plotter.plot_returns_distribution()
```

### 5. Comparación entre Instrumentos

```python
# Descargar segundo instrumento
downloader2 = LSEGDataDownloader('MSFT.O')
data2 = downloader2.download_data(days=180)

# Comparar normalizado
plotter.plot_comparison(data2, 'MSFT.O', normalize=True)

# Comparar precios absolutos
plotter.plot_comparison(data2, 'MSFT.O', normalize=False)

downloader2.close_session()
```

### 6. Dashboard Completo

```python
plotter.create_dashboard()
```

---

## 🎓 Ejemplos Avanzados

### Ejemplo 1: Análisis Completo de un Instrumento

```python
def analisis_completo(ric: str, days: int = 180):
    """Análisis completo de un instrumento."""
    # 1. Descargar
    downloader = LSEGDataDownloader(ric)
    data = downloader.download_data(days=days)
    
    # 2. Analizar
    analyzer = FinancialAnalyzer(data, ticker=ric)
    analyzer.print_summary()
    
    # 3. Visualizar
    plotter = FinancialPlotter(data, ticker=ric)
    plotter.plot_price_series(show_volume=True)
    plotter.plot_with_moving_averages()
    plotter.plot_returns_distribution()
    plotter.create_dashboard()
    
    # 4. Limpiar
    downloader.close_session()
    
    return data, analyzer, plotter

# Uso
data, analyzer, plotter = analisis_completo('AAPL.O', days=365)
```

### Ejemplo 2: Comparación de Múltiples Instrumentos

```python
def comparar_multiples(rics: list, days: int = 180):
    """Compara múltiples instrumentos."""
    datos = {}
    
    # Descargar todos los datos
    for ric in rics:
        print(f"Descargando {ric}...")
        downloader = LSEGDataDownloader(ric)
        datos[ric] = downloader.download_data(days=days)
        downloader.close_session()
    
    # Analizar cada uno
    for ric, data in datos.items():
        print(f"\n{'='*60}")
        print(f"ANÁLISIS DE {ric}")
        print(f"{'='*60}")
        analyzer = FinancialAnalyzer(data, ticker=ric)
        analyzer.print_summary()
    
    # Comparar gráficamente
    ric_base = rics[0]
    plotter = FinancialPlotter(datos[ric_base], ticker=ric_base)
    
    for ric_comp in rics[1:]:
        plotter.plot_comparison(
            datos[ric_comp],
            ric_comp,
            normalize=True
        )
    
    return datos

# Uso: Comparar FAANG
faang = ['META.O', 'AAPL.O', 'AMZN.O', 'NFLX.O', 'GOOGL.O']
datos = comparar_multiples(faang, days=365)
```

### Ejemplo 3: Análisis de Volatilidad en Ventanas Móviles

```python
import matplotlib.pyplot as plt

def analizar_volatilidad(ric: str, days: int = 365, windows: list = [30, 60, 90]):
    """Analiza la volatilidad en diferentes ventanas."""
    downloader = LSEGDataDownloader(ric)
    data = downloader.download_data(days=days)
    
    analyzer = FinancialAnalyzer(data, ticker=ric)
    
    # Calcular volatilidad para cada ventana
    fig, ax = plt.subplots(figsize=(14, 6))
    
    for window in windows:
        vol = analyzer.calculate_volatility(window=window)
        # Calcular serie de volatilidad móvil
        returns = analyzer.calculate_returns()
        rolling_vol = returns.rolling(window=window).std() * np.sqrt(252)
        ax.plot(rolling_vol.index, rolling_vol, label=f'Vol {window}d')
    
    ax.set_title(f'Volatilidad Móvil - {ric}')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Volatilidad Anualizada (%)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()
    
    downloader.close_session()

# Uso
analizar_volatilidad('TSLA.O', days=730, windows=[30, 60, 90, 120])
```

---

## 📌 Reuters Instrument Codes (RIC) Comunes

### Acciones de Tecnología
- Apple: `AAPL.O`
- Microsoft: `MSFT.O`
- Google/Alphabet: `GOOGL.O`
- Amazon: `AMZN.O`
- Meta/Facebook: `META.O`
- Tesla: `TSLA.O`
- NVIDIA: `NVDA.O`
- Netflix: `NFLX.O`

### Índices
- S&P 500: `.SPX`
- Dow Jones: `.DJI`
- NASDAQ: `.IXIC`

### Formato General
- `.O` = NYSE/NASDAQ
- `.N` = New York Stock Exchange
- `.L` = London Stock Exchange
- `.T` = Tokyo Stock Exchange

---

## ⚠️ Consideraciones Importantes

1. **Manejo de Sesiones**: Siempre cierra la sesión con `downloader.close_session()`
2. **Límites de API**: LSEG puede tener límites en el número de requests
3. **Credenciales**: Usa Databricks Secrets en producción
4. **RIC vs Ticker**: No confundas RIC (AAPL.O) con ticker tradicional (AAPL)
5. **Datos Históricos**: La disponibilidad varía según tu suscripción LSEG

---

## 🔗 Recursos Adicionales

- [LSEG Data & Analytics Documentation](https://developers.lseg.com/)
- [Databricks Secrets Guide](https://docs.databricks.com/security/secrets/index.html)
- README.md en este proyecto
