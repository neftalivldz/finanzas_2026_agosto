"""Paquete para análisis de precios financieros usando LSEG Data & Analytics."""

from .data import LSEGDataDownloader
from .analysis import FinancialAnalyzer
from .visualization import FinancialPlotter

__version__ = '1.0.0'
__all__ = ['LSEGDataDownloader', 'FinancialAnalyzer', 'FinancialPlotter']
