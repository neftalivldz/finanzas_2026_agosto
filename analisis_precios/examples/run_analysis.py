"""Ejemplo de uso del paquete analisis_precios.

Este script demuestra cómo usar las clases del paquete para:
1. Descargar datos financieros de cualquier instrumento
2. Realizar análisis estadístico
3. Crear visualizaciones
"""

import sys
sys.path.append('/Workspace/Users/nvaldez@tec.mx')

from analisis_precios.data.downloader import FinancialDataDownloader
from analisis_precios.analysis.analyzer import FinancialAnalyzer
from analisis_precios.visualization.plotter import FinancialPlotter


def analizar_instrumento(ticker: str, days: int = 180):
    """Realiza un análisis completo de un instrumento financiero.
    
    Args:
        ticker: Símbolo del instrumento (e.g., 'AAPL', 'MSFT', 'TSLA').
        days: Número de días de historia a analizar.
    """
    print(f"\n{'='*70}")
    print(f"ANÁLISIS DE {ticker}")
    print(f"{'='*70}")
    
    # 1. Descargar datos
    print("\n[1/3] Descargando datos...")
    downloader = FinancialDataDownloader(ticker)
    data = downloader.download_data(days=days)
    
    # Mostrar información del instrumento
    try:
        company_name = downloader.get_company_name()
        print(f"Compañía: {company_name}")
    except Exception as e:
        print(f"No se pudo obtener información adicional: {e}")
    
    # 2. Realizar análisis
    print("\n[2/3] Realizando análisis estadístico...")
    analyzer = FinancialAnalyzer(data, ticker)
    analyzer.print_summary()
    
    # 3. Crear visualizaciones
    print("\n[3/3] Generando visualizaciones...")
    plotter = FinancialPlotter(data, ticker)
    
    # Gráfico de precio con volumen
    plotter.plot_price_series(show_volume=True)
    
    # Gráfico con medias móviles
    plotter.plot_with_moving_averages(windows=[20, 50])
    
    # Distribución de rendimientos
    plotter.plot_returns_distribution()
    
    print("\n✓ Análisis completado!")
    print(f"{'='*70}\n")
    
    return downloader, analyzer, plotter


def comparar_instrumentos(ticker1: str, ticker2: str, days: int = 180):
    """Compara dos instrumentos financieros.
    
    Args:
        ticker1: Símbolo del primer instrumento.
        ticker2: Símbolo del segundo instrumento.
        days: Número de días de historia.
    """
    print(f"\n{'='*70}")
    print(f"COMPARACIÓN: {ticker1} vs {ticker2}")
    print(f"{'='*70}\n")
    
    # Descargar datos de ambos instrumentos
    print(f"Descargando {ticker1}...")
    downloader1 = FinancialDataDownloader(ticker1)
    data1 = downloader1.download_data(days=days)
    
    print(f"Descargando {ticker2}...")
    downloader2 = FinancialDataDownloader(ticker2)
    data2 = downloader2.download_data(days=days)
    
    # Análisis comparativo
    analyzer1 = FinancialAnalyzer(data1, ticker1)
    analyzer2 = FinancialAnalyzer(data2, ticker2)
    
    stats1 = analyzer1.get_basic_statistics()
    stats2 = analyzer2.get_basic_statistics()
    
    print(f"\n{ticker1}:")
    print(f"  Rendimiento: {analyzer1.calculate_cumulative_return():.2f}%")
    print(f"  Volatilidad: {analyzer1.calculate_volatility():.2f}%")
    print(f"  Precio actual: ${stats1['current']:.2f}")
    
    print(f"\n{ticker2}:")
    print(f"  Rendimiento: {analyzer2.calculate_cumulative_return():.2f}%")
    print(f"  Volatilidad: {analyzer2.calculate_volatility():.2f}%")
    print(f"  Precio actual: ${stats2['current']:.2f}")
    
    # Gráfico comparativo
    print("\nGenerando gráfico comparativo...")
    plotter = FinancialPlotter(data1, ticker1)
    plotter.plot_comparison(data2, ticker2, normalize=True)
    
    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    # Ejemplo 1: Análisis individual de Apple
    print("\n" + "#"*70)
    print("# EJEMPLO 1: Análisis de Apple (AAPL)")
    print("#"*70)
    analizar_instrumento('AAPL', days=180)
    
    # Ejemplo 2: Comparación entre dos compañías
    print("\n" + "#"*70)
    print("# EJEMPLO 2: Comparación Apple vs Microsoft")
    print("#"*70)
    comparar_instrumentos('AAPL', 'MSFT', days=180)