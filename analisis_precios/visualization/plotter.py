"""Módulo para visualización de datos financieros."""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Optional, Tuple, List


class FinancialPlotter:
    """Clase para crear gráficos de datos financieros.
    
    Attributes:
        data (pd.DataFrame): DataFrame con los datos financieros.
        ticker (str): Símbolo del instrumento.
    """
    
    def __init__(self, data: pd.DataFrame, ticker: str = ""):
        """Inicializa el plotter con datos financieros.
        
        Args:
            data: DataFrame con los datos financieros.
            ticker: Símbolo del instrumento.
        """
        self.data = data
        self.ticker = ticker
        self.default_style = {
            'figure.figsize': (14, 7),
            'axes.grid': True,
            'grid.alpha': 0.3,
        }
    
    def plot_price_series(
        self,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (14, 7),
        color: str = '#0066cc',
        show_volume: bool = False
    ):
        """Grafica la serie de tiempo de precios de cierre.
        
        Args:
            title: Título del gráfico (se genera automáticamente si no se especifica).
            figsize: Tamaño de la figura (ancho, alto).
            color: Color de la línea.
            show_volume: Si True, muestra el volumen en un subplot.
        """
        if show_volume and 'Volume' in self.data.columns:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, 
                                           height_ratios=[3, 1],
                                           sharex=True)
        else:
            fig, ax1 = plt.subplots(figsize=figsize)
        
        # Gráfico de precio
        ax1.plot(self.data.index, self.data['Close'], 
                linewidth=2, color=color, label='Precio de Cierre')
        
        if title is None:
            days = (self.data.index[-1] - self.data.index[0]).days
            title = f'Precio de Cierre de {self.ticker} - Últimos {days} días'
        
        ax1.set_title(title, fontsize=16, fontweight='bold')
        ax1.set_ylabel('Precio (USD)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Gráfico de volumen
        if show_volume and 'Volume' in self.data.columns:
            ax2.bar(self.data.index, self.data['Volume'], 
                   color='gray', alpha=0.5, width=1)
            ax2.set_ylabel('Volumen', fontsize=12)
            ax2.set_xlabel('Fecha', fontsize=12)
            ax2.grid(True, alpha=0.3)
        else:
            ax1.set_xlabel('Fecha', fontsize=12)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def plot_with_moving_averages(
        self,
        windows: List[int] = [20, 50, 200],
        figsize: Tuple[int, int] = (14, 7)
    ):
        """Grafica precio con medias móviles.
        
        Args:
            windows: Lista de ventanas para medias móviles.
            figsize: Tamaño de la figura.
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Precio de cierre
        ax.plot(self.data.index, self.data['Close'], 
               linewidth=2, color='#0066cc', label='Precio', alpha=0.7)
        
        # Medias móviles
        colors = ['orange', 'green', 'red']
        for i, window in enumerate(windows):
            ma = self.data['Close'].rolling(window=window).mean()
            color = colors[i % len(colors)]
            ax.plot(self.data.index, ma, 
                   linewidth=1.5, color=color, 
                   label=f'MA {window}', alpha=0.8, linestyle='--')
        
        days = (self.data.index[-1] - self.data.index[0]).days
        ax.set_title(
            f'{self.ticker} - Precio con Medias Móviles ({days} días)',
            fontsize=16, fontweight='bold'
        )
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel('Precio (USD)', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def plot_returns_distribution(
        self,
        figsize: Tuple[int, int] = (14, 6)
    ):
        """Grafica la distribución de rendimientos diarios.
        
        Args:
            figsize: Tamaño de la figura.
        """
        returns = self.data['Close'].pct_change() * 100
        returns = returns.dropna()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Histograma
        ax1.hist(returns, bins=50, color='#0066cc', alpha=0.7, edgecolor='black')
        ax1.axvline(returns.mean(), color='red', linestyle='--', 
                   linewidth=2, label=f'Media: {returns.mean():.2f}%')
        ax1.set_title(f'Distribución de Rendimientos Diarios\n{self.ticker}',
                     fontsize=14, fontweight='bold')
        ax1.set_xlabel('Rendimiento (%)', fontsize=11)
        ax1.set_ylabel('Frecuencia', fontsize=11)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Serie temporal de rendimientos
        ax2.plot(returns.index, returns, linewidth=1, color='#0066cc', alpha=0.7)
        ax2.axhline(0, color='black', linestyle='-', linewidth=0.5)
        ax2.axhline(returns.mean(), color='red', linestyle='--', linewidth=1.5)
        ax2.fill_between(returns.index, 0, returns, 
                        where=(returns > 0), color='green', alpha=0.3)
        ax2.fill_between(returns.index, 0, returns, 
                        where=(returns < 0), color='red', alpha=0.3)
        ax2.set_title('Serie Temporal de Rendimientos',
                     fontsize=14, fontweight='bold')
        ax2.set_xlabel('Fecha', fontsize=11)
        ax2.set_ylabel('Rendimiento (%)', fontsize=11)
        ax2.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def plot_comparison(
        self,
        other_data: pd.DataFrame,
        other_ticker: str,
        normalize: bool = True,
        figsize: Tuple[int, int] = (14, 7)
    ):
        """Compara dos instrumentos en el mismo gráfico.
        
        Args:
            other_data: DataFrame del otro instrumento.
            other_ticker: Símbolo del otro instrumento.
            normalize: Si True, normaliza ambas series a 100 en el día inicial.
            figsize: Tamaño de la figura.
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        if normalize:
            # Normalizar ambas series
            series1 = (self.data['Close'] / self.data['Close'].iloc[0]) * 100
            series2 = (other_data['Close'] / other_data['Close'].iloc[0]) * 100
            ylabel = 'Precio Normalizado (Base 100)'
        else:
            series1 = self.data['Close']
            series2 = other_data['Close']
            ylabel = 'Precio (USD)'
        
        ax.plot(series1.index, series1, linewidth=2, 
               color='#0066cc', label=self.ticker)
        ax.plot(series2.index, series2, linewidth=2, 
               color='#ff6600', label=other_ticker)
        
        ax.set_title(
            f'Comparación: {self.ticker} vs {other_ticker}',
            fontsize=16, fontweight='bold'
        )
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def create_dashboard(self):
        """Crea un dashboard completo con múltiples gráficos."""
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. Precio de cierre
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(self.data.index, self.data['Close'], 
                linewidth=2, color='#0066cc')
        ax1.set_title(f'{self.ticker} - Precio de Cierre', 
                     fontsize=14, fontweight='bold')
        ax1.set_ylabel('Precio (USD)')
        ax1.grid(True, alpha=0.3)
        
        # 2. Volumen
        if 'Volume' in self.data.columns:
            ax2 = fig.add_subplot(gs[1, 0])
            ax2.bar(self.data.index, self.data['Volume'], 
                   color='gray', alpha=0.5)
            ax2.set_title('Volumen de Transacciones', fontsize=12)
            ax2.set_ylabel('Volumen')
            ax2.grid(True, alpha=0.3)
        
        # 3. Rendimientos
        ax3 = fig.add_subplot(gs[1, 1])
        returns = self.data['Close'].pct_change() * 100
        ax3.hist(returns.dropna(), bins=30, color='#0066cc', 
                alpha=0.7, edgecolor='black')
        ax3.set_title('Distribución de Rendimientos', fontsize=12)
        ax3.set_xlabel('Rendimiento (%)')
        ax3.set_ylabel('Frecuencia')
        ax3.grid(True, alpha=0.3)
        
        # 4. Medias móviles
        ax4 = fig.add_subplot(gs[2, :])
        ax4.plot(self.data.index, self.data['Close'], 
                linewidth=2, color='#0066cc', label='Precio', alpha=0.7)
        for window, color in zip([20, 50], ['orange', 'green']):
            ma = self.data['Close'].rolling(window=window).mean()
            ax4.plot(self.data.index, ma, linewidth=1.5, 
                    color=color, label=f'MA {window}', linestyle='--')
        ax4.set_title('Precio con Medias Móviles', fontsize=12)
        ax4.set_xlabel('Fecha')
        ax4.set_ylabel('Precio (USD)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle(f'Dashboard de Análisis - {self.ticker}', 
                    fontsize=16, fontweight='bold', y=0.995)
        plt.show()
