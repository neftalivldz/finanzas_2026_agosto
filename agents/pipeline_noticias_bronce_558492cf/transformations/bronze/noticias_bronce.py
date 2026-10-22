"""Bronce: noticias de empresas desde la API REST de Finnhub.

Cada actualización extrae las noticias del símbolo y la fecha solicitados y
las carga en itesm.reto.noticias_bronce. El flujo usa REPLACE WHERE con la
llave (symbol, date): las filas que ya existan para ese símbolo y fecha se
borran primero y luego se insertan los datos recién extraídos.

Parámetros: se leen del campo "Configuration" del pipeline (spark conf,
leído con spark.conf.get). IMPORTANTE: la sección "Parameters" del pipeline
y el diálogo "Run with different settings" NO funcionan para este archivo,
porque los parámetros de pipeline solo aplican a código fuente SQL:
  - noticias.symbol (o symbol): símbolo del instrumento, p. ej. "NVDA"
  - noticias.fecha (o fecha): fecha de las noticias en formato YYYY-MM-DD;
    si se omite se usa el día actual (UTC)
"""

from datetime import datetime, timedelta, timezone

import requests
from pyspark import pipelines as dp
from pyspark.sql import functions as F
from pyspark.sql.types import (
    LongType,
    StringType,
    StructField,
    StructType,
)

NEWS_TABLE = "itesm.reto.noticias_bronce"
FINNHUB_URL = "https://finnhub.io/api/v1/company-news"
SECRET_SCOPE = "refinitiv_scope"
SECRET_KEY = "finnhub_key"


def _param(name, default=None):
    """Lee un parámetro de la corrida o de la configuración del pipeline.

    Busca primero el valor sobrescrito para la corrida y luego el valor por
    omisión declarado en la configuración del pipeline.
    """
    for key in (name, "noticias." + name):
        try:
            value = spark.conf.get(key)
        except Exception:
            continue
        if value:
            return value
    return default


def _resolve_symbol():
    symbol = _param("symbol", "NVDA")
    return symbol.strip().upper()


def _resolve_news_date():
    """Devuelve la fecha de noticias como YYYY-MM-DD (default: día actual UTC)."""
    raw = (_param("fecha") or "").strip()
    if not raw:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")
    try:
        return datetime.strptime(raw, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(
            "noticias.fecha='" + raw + "' no es una fecha válida; usa YYYY-MM-DD."
        ) from exc


def _fetch_company_news(symbol, from_date, to_date, token):
    """Obtiene las noticias de empresa desde la API de Finnhub.

    IMPORTANTE: el cuerpo de esta función es la llamada HTTP a Finnhub
    (celda 5 del notebook "Noticias NVIDIA con LSEG Data"). El asistente no
    puede escribirla por una restricción de seguridad automatizada; el
    usuario debe pegarla manualmente donde se indica.
    """
    response = requests.get(
        FINNHUB_URL,
        params={
            "symbol": symbol,
            "from": from_date,
            "to": to_date,
            "token": token,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json() or []


SYMBOL = _resolve_symbol()
NEWS_DATE = _resolve_news_date()
# Ventana de extracción: desde el día anterior a NEWS_DATE hasta NEWS_DATE.
NEWS_DATE_1DAY = (
    datetime.strptime(NEWS_DATE, "%Y-%m-%d") - timedelta(days=1)
).strftime("%Y-%m-%d")
# Ventana de reemplazo: solo las filas de este símbolo y fecha se borran
# antes de insertar los datos nuevos; el resto de la tabla queda intacto.
REPLACE_PREDICATE = "symbol = '" + SYMBOL + "' AND date = DATE '" + NEWS_DATE + "'"

_RAW_SCHEMA = StructType(
    [
        StructField("symbol", StringType(), False),
        StructField("date_str", StringType(), False),
        StructField("storyId", StringType(), True),
        StructField("epoch_sec", LongType(), True),
        StructField("headline", StringType(), True),
        StructField("summary", StringType(), True),
        StructField("source", StringType(), True),
        StructField("url", StringType(), True),
    ]
)


@dp.table(
    name=NEWS_TABLE,
    comment=(
        "Noticias de empresas por símbolo y fecha (bronce), extraídas de la "
        "API company-news de Finnhub. Llave: (symbol, date); cada corrida "
        "reemplaza las filas del símbolo y fecha solicitados."
    ),
    replace_where=REPLACE_PREDICATE,
    # Evita que un full refresh borre el historial de otros símbolos/fechas.
    table_properties={"pipelines.reset.allowed": "false"},
)
def noticias_bronce():
    token = dbutils.secrets.get(scope=SECRET_SCOPE, key=SECRET_KEY)

    items = _fetch_company_news(
        symbol=SYMBOL, from_date=NEWS_DATE_1DAY, to_date=NEWS_DATE, token=token
    ) or []

    rows = [
        (
            SYMBOL,
            NEWS_DATE,
            str(item.get("id")) if item.get("id") is not None else None,
            item.get("datetime"),
            item.get("headline"),
            item.get("summary"),
            item.get("source"),
            item.get("url"),
        )
        for item in items
    ]

    return (
        spark.createDataFrame(rows, schema=_RAW_SCHEMA)
        .withColumn("date", F.to_date("date_str"))
        .withColumn("versionCreated", F.timestamp_seconds("epoch_sec"))
        # El texto de la noticia es el titular (columna 'text' del notebook original)
        .withColumn("text", F.col("headline"))
        .select(
            "symbol",
            "date",
            "storyId",
            "versionCreated",
            "text",
            "headline",
            "summary",
            "source",
            "url",
        )
    )
