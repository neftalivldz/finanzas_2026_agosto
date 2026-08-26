"""Módulo para descargar datos de portafolio con múltiples instrumentos."""

import pandas as pd
from datetime import datetime
from typing import Optional, List, Union
from .downloader import LSEGDataDownloader


class PortfolioDownloader:
    """Clase para descargar datos de precios de cierre para un portafolio de instrumentos.
    
    Esta clase permite descargar datos históricos de múltiples RICs simultáneamente,
    combinando los precios de cierre en un solo DataFrame con cada RIC como columna.
    
    Attributes:
        rics (List[str]): Lista de Reuters Instrument Codes.
        data (pd.DataFrame): DataFrame con los precios de cierre de cada instrumento.
    """
    
    def __init__(self, rics: List[str], app_key: Optional[str] = None,
                 username: Optional[str] = None, password: Optional[str] = None,
                 use_secrets: bool = True):
        """Inicializa el downloader de portafolio.
        
        Args:
            rics: Lista de Reuters Instrument Codes (e.g., ['AAPL.O', 'MSFT.O', 'GOOGL.O']).
            app_key: API key de LSEG (opcional si use_secrets=True).
            username: Usuario de LSEG (opcional si use_secrets=True).
            password: Contraseña de LSEG (opcional si use_secrets=True).
            use_secrets: Si True, obtiene credenciales de Databricks Secrets.
        """
        if not rics or len(rics) == 0:
            raise ValueError("Debe proporcionar al menos un RIC en la lista")
        
        self.rics = [ric.upper() for ric in rics]
        self.data: Optional[pd.DataFrame] = None
        self._credentials = {
            'app_key': app_key,
            'username': username,
            'password': password,
            'use_secrets': use_secrets
        }
    
    def download_portfolio(
        self,
        days: Optional[int] = None,
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None,
        interval: str = '1D'
    ) -> pd.DataFrame:
        """Descarga datos de precios de cierre para todos los instrumentos del portafolio.
        
        Args:
            days: Número de días hacia atrás desde hoy. Si se especifica,
                  se ignoran start_date y end_date.
            start_date: Fecha de inicio (formato: 'YYYY-MM-DD' o datetime).
            end_date: Fecha de fin (formato: 'YYYY-MM-DD' o datetime).
            interval: Intervalo de los datos ('1D' para diario, '1W' para semanal, etc.).
        
        Returns:
            DataFrame con fechas como índice y cada RIC como columna, conteniendo
            los precios de cierre. Los valores faltantes se rellenan con el último
            precio conocido (forward fill).
        
        Raises:
            ValueError: Si no se especifican ni days ni start_date/end_date.
            RuntimeError: Si ocurre un error al descargar datos.
        """
        print(f"Descargando datos para {len(self.rics)} instrumentos...")
        
        portfolio_data = {}
        successful_downloads = 0
        failed_rics = []
        
        for ric in self.rics:
            try:
                print(f"  Descargando {ric}...", end=" ")
                
                # Crear downloader para este RIC
                downloader = LSEGDataDownloader(
                    ric=ric,
                    **self._credentials
                )
                
                # Descargar datos
                data = downloader.download_data(
                    days=days,
                    start_date=start_date,
                    end_date=end_date,
                    interval=interval
                )
                
                # Extraer solo la columna Close y renombrarla con el RIC
                if 'Close' in data.columns:
                    portfolio_data[ric] = data['Close']
                    successful_downloads += 1
                    print("✓")
                else:
                    print(f"⚠ No se encontró columna 'Close'")
                    failed_rics.append(ric)
                
                # Cerrar la sesión del downloader
                downloader.close_session()
                
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                failed_rics.append(ric)
                continue
        
        if successful_downloads == 0:
            raise RuntimeError(
                f"No se pudo descargar datos para ningún instrumento. "
                f"RICs fallidos: {failed_rics}"
            )
        
        # Combinar todos los DataFrames usando Full Join (outer join)
        print(f"\nCombinando datos de {successful_downloads} instrumentos...")
        self.data = pd.DataFrame(portfolio_data)
        
        # Rellenar valores faltantes usando el último precio conocido (forward fill)
        print("Rellenando valores faltantes con último precio conocido...")
        self.data = self.data.fillna(method='ffill')
        
        # Información de resumen
        print(f"\n{'='*60}")
        print(f"RESUMEN DE DESCARGA DE PORTAFOLIO")
        print(f"{'='*60}")
        print(f"Instrumentos exitosos: {successful_downloads}/{len(self.rics)}")
        if failed_rics:
            print(f"Instrumentos fallidos: {', '.join(failed_rics)}")
        print(f"Período: {self.data.index.min()} a {self.data.index.max()}")
        print(f"Total de fechas: {len(self.data)}")
        print(f"\nColumnas del DataFrame: {list(self.data.columns)}")
        print(f"Shape: {self.data.shape}")
        print(f"{'='*60}\n")
        
        return self.data
    
    def get_returns(self, log_returns: bool = False) -> pd.DataFrame:
        """Calcula los retornos del portafolio.
        
        Args:
            log_returns: Si True, calcula retornos logarítmicos. Si False, retornos simples.
        
        Returns:
            DataFrame con los retornos de cada instrumento.
        
        Raises:
            ValueError: Si no hay datos descargados.
        """
        if self.data is None:
            raise ValueError("Primero debe descargar datos usando download_portfolio()")
        
        if log_returns:
            import numpy as np
            return np.log(self.data / self.data.shift(1))
        else:
            return self.data.pct_change()
    
    def get_correlation_matrix(self) -> pd.DataFrame:
        """Calcula la matriz de correlación entre los instrumentos.
        
        Returns:
            DataFrame con la matriz de correlación.
        
        Raises:
            ValueError: Si no hay datos descargados.
        """
        if self.data is None:
            raise ValueError("Primero debe descargar datos usando download_portfolio()")
        
        returns = self.get_returns()
        return returns.corr()
    
    def summary(self):
        """Imprime un resumen estadístico del portafolio.
        
        Raises:
            ValueError: Si no hay datos descargados.
        """
        if self.data is None:
            raise ValueError("Primero debe descargar datos usando download_portfolio()")
        
        print(f"\n{'='*60}")
        print(f"RESUMEN ESTADÍSTICO DEL PORTAFOLIO")
        print(f"{'='*60}\n")
        
        print("Estadísticas de Precios:")
        print(self.data.describe())
        
        print(f"\n{'='*60}")
        print(f"Retornos Acumulados:")
        print(f"{'='*60}")
        cumulative_returns = (self.data.iloc[-1] / self.data.iloc[0] - 1) * 100
        for ric, ret in cumulative_returns.items():
            print(f"{ric}: {ret:.2f}%")
        
        print(f"\n{'='*60}\n")
