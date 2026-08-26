"""Script de ejemplo para análisis completo de instrumentos financieros con LSEG.

Este script muestra cómo:
1. Descargar datos históricos de LSEG Data & Analytics
2. Realizar análisis estadístico
3. Crear visualizaciones
"""

import sys
sys.path.append('/Workspace/Users/nvaldez@tec.mx')

from analisis_precios_lseg.data import LSEGDataDownloader
from analisis_precios_lseg.analysis import FinancialAnalyzer
from analisis_precios_lseg.visualization import FinancialPlotter


def analizar_instrumento(ric: str, days: int = 180):
    """Realiza un análisis completo de un instrumento financiero.
    
    Args:
        ric: Reuters Instrument Code (e.g., 'AAPL.O').
        days: Número de días de historia a analizar.
    """
    print(f"\n{'='*70}")
    print(f"INICIANDO ANÁLISIS DE {ric}")
    print(f"{'='*70}\n")
    
    try:
        # 1. Descargar datos
        print("1️⃣ DESCARGANDO DATOS...")
        downloader = LSEGDataDownloader(ric, use_secrets=True)
        data = downloader.download_data(days=days)
        
        print(f"\n✅ Datos descargados exitosamente: {len(data)} registros\n")
        
        # 2. Análisis estadístico
        print("\n2️⃣ REALIZANDO ANÁLISIS ESTADÍSTICO...")
        analyzer = FinancialAnalyzer(data, ticker=ric)
        analyzer.print_summary()
        
        # 3. Visualizaciones
        print("\n3️⃣ GENERANDO VISUALIZACIONES...\n")
        plotter = FinancialPlotter(data, ticker=ric)
        
        # Gráfico de precio con volumen
        print("📈 Gráfico 1: Precio con Volumen")
        plotter.plot_price_series(show_volume=True)
        
        # Precio con medias móviles
        print("\n📈 Gráfico 2: Precio con Medias Móviles")
        plotter.plot_with_moving_averages(windows=[20, 50, 200])
        
        # Distribución de rendimientos
        print("\n📈 Gráfico 3: Distribución de Rendimientos")
        plotter.plot_returns_distribution()
        
        # Dashboard completo
        print("\n📈 Gráfico 4: Dashboard Completo")
        plotter.create_dashboard()
        
        # 4. Cerrar sesión
        downloader.close_session()
        
        print(f"\n{'='*70}")
        print("✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
        print(f"{'='*70}\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        raise


def comparar_instrumentos(ric1: str, ric2: str, days: int = 180):
    """Compara dos instrumentos financieros.
    
    Args:
        ric1: Primer Reuters Instrument Code.
        ric2: Segundo Reuters Instrument Code.
        days: Número de días de historia.
    """
    print(f"\n{'='*70}")
    print(f"COMPARANDO {ric1} vs {ric2}")
    print(f"{'='*70}\n")
    
    try:
        # Descargar datos del primer instrumento
        print(f"Descargando {ric1}...")
        downloader1 = LSEGDataDownloader(ric1, use_secrets=True)
        data1 = downloader1.download_data(days=days)
        
        # Descargar datos del segundo instrumento
        print(f"Descargando {ric2}...")
        downloader2 = LSEGDataDownloader(ric2, use_secrets=True)
        data2 = downloader2.download_data(days=days)
        
        # Visualizar comparación
        print("\nGenerando gráfico de comparación...\n")
        plotter1 = FinancialPlotter(data1, ticker=ric1)
        plotter1.plot_comparison(data2, ric2, normalize=True)
        
        # Análisis individual
        print(f"\n{'='*70}")
        print(f"ANÁLISIS DE {ric1}")
        print(f"{'='*70}")
        analyzer1 = FinancialAnalyzer(data1, ticker=ric1)
        analyzer1.print_summary()
        
        print(f"\n{'='*70}")
        print(f"ANÁLISIS DE {ric2}")
        print(f"{'='*70}")
        analyzer2 = FinancialAnalyzer(data2, ticker=ric2)
        analyzer2.print_summary()
        
        # Cerrar sesiones
        downloader1.close_session()
        downloader2.close_session()
        
        print(f"\n{'='*70}")
        print("✅ COMPARACIÓN COMPLETADA")
        print(f"{'='*70}\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        raise


if __name__ == "__main__":
    # Ejemplo 1: Análisis individual de Apple
    print("\n\n🍎 EJEMPLO 1: ANÁLISIS DE APPLE (AAPL.O)")
    analizar_instrumento('AAPL.O', days=180)
    
    # Ejemplo 2: Comparación Apple vs Microsoft
    print("\n\n🆚 EJEMPLO 2: COMPARACIÓN APPLE vs MICROSOFT")
    comparar_instrumentos('AAPL.O', 'MSFT.O', days=180)
    
    # Ejemplo 3: Análisis de Tesla
    print("\n\n🚗 EJEMPLO 3: ANÁLISIS DE TESLA (TSLA.O)")
    analizar_instrumento('TSLA.O', days=365)
