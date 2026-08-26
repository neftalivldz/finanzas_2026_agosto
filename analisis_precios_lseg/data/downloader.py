"""Módulo para descargar datos financieros de LSEG Data & Analytics."""

import lseg.data as ld
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Union


class LSEGDataDownloader:
    """Clase para descargar datos financieros usando LSEG Data & Analytics.
    
    Attributes:
        ric (str): Reuters Instrument Code del instrumento financiero.
        data (pd.DataFrame): DataFrame con los datos descargados.
        session: Sesión activa de LSEG Data.
    """
    
    def __init__(self, ric: str, app_key: Optional[str] = None, 
                 username: Optional[str] = None, password: Optional[str] = None,
                 use_secrets: bool = True):
        """Inicializa el downloader con un RIC específico.
        
        Args:
            ric: Reuters Instrument Code (e.g., 'AAPL.O', 'MSFT.O', 'GOOGL.O').
            app_key: API key de LSEG (opcional si use_secrets=True).
            username: Usuario de LSEG (opcional si use_secrets=True).
            password: Contraseña de LSEG (opcional si use_secrets=True).
            use_secrets: Si True, obtiene credenciales de Databricks Secrets.
        """
        self.ric = ric.upper()
        self.data: Optional[pd.DataFrame] = None
        self.session = None
        
        # Obtener credenciales
        if use_secrets:
            try:
                import dbutils
                self.app_key = dbutils.secrets.get(scope="refinitiv_scope", key="app_key")
                self.username = dbutils.secrets.get(scope="refinitiv_scope", key="username")
                self.password = dbutils.secrets.get(scope="refinitiv_scope", key="password")
            except:
                raise ValueError(
                    "No se pueden obtener credenciales de Databricks Secrets. "
                    "Proporcione app_key, username y password manualmente."
                )
        else:
            if not all([app_key, username, password]):
                raise ValueError(
                    "Debe proporcionar app_key, username y password si use_secrets=False"
                )
            self.app_key = app_key
            self.username = username
            self.password = password
        
        # Inicializar sesión
        self._initialize_session()
    
    def _initialize_session(self):
        """Inicializa la sesión de LSEG Data."""
        try:
            # Crear y abrir sesión
            self.session = ld.session.platform.Definition(
                app_key=self.app_key,
                grant=ld.session.platform.GrantPassword(
                    username=self.username,
                    password=self.password
                ),
                signon_control=True
            ).get_session()
            
            result = self.session.open()
            
            # Establecer como sesión por defecto
            ld.session.set_default(self.session)
            
            print(f"✓ Sesión LSEG iniciada correctamente")
        except Exception as e:
            raise ConnectionError(f"Error al inicializar sesión LSEG: {e}")
    
    def download_data(
        self,
        days: Optional[int] = None,
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None,
        interval: str = '1D',
        fields: Optional[list] = None
    ) -> pd.DataFrame:
        """Descarga datos históricos del instrumento.
        
        Args:
            days: Número de días hacia atrás desde hoy. Si se especifica,
                  se ignoran start_date y end_date.
            start_date: Fecha de inicio (formato: 'YYYY-MM-DD' o datetime).
            end_date: Fecha de fin (formato: 'YYYY-MM-DD' o datetime).
            interval: Intervalo de los datos ('1D' para diario, '1W' para semanal, etc.).
            fields: Lista de campos a descargar. Por defecto incluye OHLCV.
        
        Returns:
            DataFrame con los datos descargados.
        
        Raises:
            ValueError: Si no se especifican ni days ni start_date/end_date.
        """
        # Campos por defecto si no se especifican
        if fields is None:
            fields = [
                "TR.PriceClose.date",
                "TR.PriceOpen",
                "TR.PriceHigh",
                "TR.PriceLow",
                "TR.PriceClose",
                "TR.Volume"
            ]
        
        # Determinar las fechas
        if days is not None:
            end = datetime.now()
            start = end - timedelta(days=days)
            end_str = end.strftime("%Y-%m-%d")
            start_str = start.strftime("%Y-%m-%d")
        elif start_date is not None:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date) if end_date else datetime.now()
            start_str = start.strftime("%Y-%m-%d")
            end_str = end.strftime("%Y-%m-%d")
        else:
            raise ValueError(
                "Debe especificar 'days' o 'start_date' (y opcionalmente 'end_date')"
            )
        
        print(f"Descargando datos de {self.ric} desde {start_str} hasta {end_str}...")
        
        try:
            # Descargar datos usando lseg.data
            self.data = ld.get_history(
                universe=self.ric,
                fields=fields,
                interval=interval,
                start=start_str,
                end=end_str
            )
            
            if self.data.empty:
                raise ValueError(f"No se pudieron descargar datos para {self.ric}")
            
            # Renombrar columnas para compatibilidad
            column_mapping = {
                'Price Open': 'Open',
                'Price High': 'High',
                'Price Low': 'Low',
                'Price Close': 'Close',
                'Volume': 'Volume'
            }
            
            self.data = self.data.rename(columns=column_mapping)
            
            # Establecer fecha como índice si existe
            if 'Date' in self.data.columns:
                self.data.set_index('Date', inplace=True)
            
            print(f"✓ Datos descargados: {len(self.data)} registros")
            return self.data
            
        except Exception as e:
            raise RuntimeError(f"Error al descargar datos de LSEG: {e}")
    
    def close_session(self):
        """Cierra la sesión de LSEG Data."""
        if self.session:
            try:
                self.session.close()
                print("✓ Sesión LSEG cerrada")
            except Exception as e:
                print(f"Advertencia al cerrar sesión: {e}")
    
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
    
    def __del__(self):
        """Destructor para cerrar la sesión automáticamente."""
        self.close_session()
