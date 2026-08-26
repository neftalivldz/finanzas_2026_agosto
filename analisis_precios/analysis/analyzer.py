"""Módulo para análisis estadístico de datos financieros."""

import pandas as pd
import numpy as np
from typing import Dict, Optional


class FinancialAnalyzer:
    """Clase para realizar análisis estadístico de instrumentos financieros.
    
    Attributes:
        data (pd.DataFrame): DataFrame con los datos financieros.
        ticker (str): Símbolo del instrumento.
    """
    
    def __init__(self, data: pd.DataFrame, ticker: str = ""):
        """Inicializa el analizador con datos financieros.
        
        Args:
            data: DataFrame con los datos financieros (debe tener columna 'Close').
            ticker: Símbolo del instrumento.
        """
        self.data = data
        self.ticker = ticker
        
        if 'Close' not in self.data.columns:
            raise ValueError("El DataFrame debe contener una columna 'Close'")
    
    def get_basic_statistics(self) -> Dict[str, float]:
        """Calcula estadísticas básicas de precios de cierre.
        
        Returns:
            Diccionario con estadísticas: min, max, mean, std, current.
        """
        close_prices = self.data['Close']
        
        stats = {
            'min': float(close_prices.min()),
            'max': float(close_prices.max()),
            'mean': float(close_prices.mean()),
            'median': float(close_prices.median()),
            'std': float(close_prices.std()),
            'current': float(close_prices.iloc[-1]),
            'first': float(close_prices.iloc[0])
        }
        
        return stats
    
    def calculate_returns(self, period: int = 1) -> pd.Series:
        """Calcula los rendimientos del instrumento.
        
        Args:
            period: Período para calcular rendimientos (default: 1 = diario).
        
        Returns:
            Serie con los rendimientos porcentuales.
        """
        close_prices = self.data['Close']
        returns = close_prices.pct_change(periods=period) * 100
        return returns.dropna()
    
    def calculate_volatility(self, window: int = 30) -> float:
        """Calcula la volatilidad (desviación estándar de rendimientos).
        
        Args:
            window: Ventana de días para calcular volatilidad.
        
        Returns:
            Volatilidad anualizada.
        """
        returns = self.calculate_returns()
        volatility = returns.tail(window).std()
        # Anualizar (asumiendo 252 días de trading)
        annualized_volatility = volatility * np.sqrt(252)
        return float(annualized_volatility)
    
    def calculate_cumulative_return(self) -> float:
        """Calcula el rendimiento acumulado del período.
        
        Returns:
            Rendimiento acumulado en porcentaje.
        """
        close_prices = self.data['Close']
        cumulative_return = (
            (close_prices.iloc[-1] - close_prices.iloc[0]) / close_prices.iloc[0]
        ) * 100
        return float(cumulative_return)
    
    def calculate_moving_averages(
        self, 
        windows: list = [20, 50, 200]
    ) -> pd.DataFrame:
        """Calcula medias móviles simples.
        
        Args:
            windows: Lista de ventanas para las medias móviles.
        
        Returns:
            DataFrame con las medias móviles.
        """
        close_prices = self.data['Close']
        mas = pd.DataFrame(index=self.data.index)
        
        for window in windows:
            mas[f'MA_{window}'] = close_prices.rolling(window=window).mean()
        
        return mas
    
    def find_extremes(self) -> Dict[str, Dict]:
        """Encuentra los puntos de máximo y mínimo.
        
        Returns:
            Diccionario con información de máximos y mínimos.
        """
        close_prices = self.data['Close']
        
        max_idx = close_prices.idxmax()
        min_idx = close_prices.idxmin()
        
        extremes = {
            'max': {
                'date': max_idx,
                'price': float(close_prices.loc[max_idx]),
            },
            'min': {
                'date': min_idx,
                'price': float(close_prices.loc[min_idx]),
            }
        }
        
        return extremes
    
    def get_summary_report(self) -> Dict:
        """Genera un reporte completo de análisis.
        
        Returns:
            Diccionario con todas las métricas de análisis.
        """
        stats = self.get_basic_statistics()
        extremes = self.find_extremes()
        
        report = {
            'ticker': self.ticker,
            'period': {
                'start': str(self.data.index[0].date()),
                'end': str(self.data.index[-1].date()),
                'days': len(self.data)
            },
            'price_statistics': stats,
            'extremes': extremes,
            'returns': {
                'cumulative': self.calculate_cumulative_return(),
                'volatility_annualized': self.calculate_volatility()
            }
        }
        
        return report
    
    def print_summary(self):
        """Imprime un resumen formateado del análisis."""
        report = self.get_summary_report()
        
        print(f"\n{'='*60}")
        print(f"REPORTE DE ANÁLISIS: {report['ticker']}")
        print(f"{'='*60}")
        
        print(f"\nPeríodo: {report['period']['start']} a {report['period']['end']}")
        print(f"Días de datos: {report['period']['days']}")
        
        print(f"\nESTADÍSTICAS DE PRECIO:")
        stats = report['price_statistics']
        print(f"  Precio actual: ${stats['current']:.2f}")
        print(f"  Precio máximo: ${stats['max']:.2f}")
        print(f"  Precio mínimo: ${stats['min']:.2f}")
        print(f"  Precio promedio: ${stats['mean']:.2f}")
        print(f"  Desviación estándar: ${stats['std']:.2f}")
        
        print(f"\nRENDIMIENTO:")
        print(f"  Rendimiento acumulado: {report['returns']['cumulative']:.2f}%")
        print(f"  Volatilidad anualizada: {report['returns']['volatility_annualized']:.2f}%")
        
        print(f"\nEXTREMOS:")
        extremes = report['extremes']
        print(f"  Máximo histórico: ${extremes['max']['price']:.2f} ({extremes['max']['date'].date()})")
        print(f"  Mínimo histórico: ${extremes['min']['price']:.2f} ({extremes['min']['date'].date()})")
        
        print(f"\n{'='*60}")
