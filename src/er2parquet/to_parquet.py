
import pandas as pd

def to_parquet(df: pd.DataFrame, filnavn: str) -> None:
    pd.DataFrame.to_parquet(df, filnavn, engine='fastparquet')
    return None