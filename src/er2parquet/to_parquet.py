
from er2parquet.metadata import kolonner
import pandas as pd

def to_parquet(df: pd.DataFrame, filnavn: str) -> None:
    pd.DataFrame.to_parquet(df[list(kolonner.keys())], filnavn, engine='fastparquet')
    return None