"""Módulo para descargar datos financieros de Yahoo Finance."""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Union


class FinancialDataDownloader:
    """Clase para descargar datos financieros de instrumentos.
    
    Attributes:
        ticker (str): Símbolo del instrumento financiero.
        data (pd.DataFrame): DataFrame con los datos descargados.
    """
    
    def __init__(self, ticker: str):
        """Inicializa el downloader con un ticker específico.
        
        Args:
            ticker: Símbolo del instrumento (e.g., 'AAPL', 'MSFT', 'GOOGL').
        """
        self.ticker = ticker.upper()
        self.data: Optional[pd.DataFrame] = None
        self._ticker_info: Optional[dict] = None
    
    def download_data(
        self,
        days: Optional[int] = None,
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None,
        interval: str = '1d'
    ) -> pd.DataFrame:
        """Descarga datos históricos del instrumento.
        
        Args:
            days: Número de días hacia atrás desde hoy. Si se especifica,
                  se ignoran start_date y end_date.
            start_date: Fecha de inicio (formato: 'YYYY-MM-DD' o datetime).
            end_date: Fecha de fin (formato: 'YYYY-MM-DD' o datetime).
            interval: Intervalo de los datos ('1d', '1h', '1wk', '1mo', etc.).
        
        Returns:
            DataFrame con los datos descargados.
        
        Raises:
            ValueError: Si no se especifican ni days ni start_date/end_date.
        """
        # Determinar las fechas
        if days is not None:
            end = datetime.now()
            start = end - timedelta(days=days)
        elif start_date is not None:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date) if end_date else datetime.now()
        else:
            raise ValueError(
                "Debe especificar 'days' o 'start_date' (y opcionalmente 'end_date')"
            )
        
        print(f"Descargando datos de {self.ticker} desde {start.date()} hasta {end.date()}...")
        
        # Descargar datos
        self.data = yf.download(
            self.ticker,
            start=start,
            end=end,
            interval=interval,
            progress=False
        )
        
        if self.data.empty:
            raise ValueError(f"No se pudieron descargar datos para {self.ticker}")
        
        # Simplificar columnas si hay multi-index
        if isinstance(self.data.columns, pd.MultiIndex):
            self.data.columns = self.data.columns.get_level_values(0)
        
        print(f"✓ Datos descargados: {len(self.data)} registros")
        return self.data
    
    def get_ticker_info(self) -> dict:
        """Obtiene información general del ticker.
        
        Returns:
            Diccionario con información del instrumento.
        """
        if self._ticker_info is None:
            ticker_obj = yf.Ticker(self.ticker)
            self._ticker_info = ticker_obj.info
        return self._ticker_info
    
    def get_company_name(self) -> str:
        """Obtiene el nombre de la compañía.
        
        Returns:
            Nombre de la compañía.
        """
        info = self.get_ticker_info()
        return info.get('longName', self.ticker)
    
    @property
    def close_prices(self) -> pd.Series:
        """Retorna la serie de precios de cierre.
        
        Returns:
            Serie con los precios de cierre.
        
        Raises:
            ValueError: Si no hay datos descargados.
        """
        if self.data is None:
            raise ValueError("Primero debe descargar datos usando download_data()")
        return self.data['Close']
    
    @property
    def volume(self) -> pd.Series:
        """Retorna la serie de volumen.
        
        Returns:
            Serie con el volumen.
        
        Raises:
            ValueError: Si no hay datos descargados.
        """
        if self.data is None:
            raise ValueError("Primero debe descargar datos usando download_data()")
        return self.data['Volume']
