"""Paquete de análisis de precios de instrumentos financieros."""

__version__ = '1.0.0'
__author__ = 'ITESM'

from analisis_precios.data.downloader import FinancialDataDownloader
from analisis_precios.analysis.analyzer import FinancialAnalyzer
from analisis_precios.visualization.plotter import FinancialPlotter

__all__ = [
    'FinancialDataDownloader',
    'FinancialAnalyzer',
    'FinancialPlotter',
]
