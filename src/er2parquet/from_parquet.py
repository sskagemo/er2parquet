
from er2parquet.metadata import kolonner
import pandas as pd

def from_parquet(filnavn: str) -> pd.DataFrame:
    df = pd.read_parquet(filnavn, engine='fastparquet')
    if list(kolonner.keys()) != list(df.columns):
        raise ValueError("Kolonner i DataFrame er ikke som forventet.")
    df = pd.DataFrame.convert_dtypes(df)
    return df