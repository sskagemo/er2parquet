
'''
Plan:
1. Laste ned JSON
2. Konvertere til Pandas DataFrame
3. Sette riktige datatyper (hvis det ikke kan skje i forrige steg)
4. Skrive til Parquet
5. Lagre et egnet sted ... Google Disk?
6. gjøre noen sammenligninger? Med og uten PyArrow?
7. Blir datatypene riktige ved lesing av parquet?
'''
import pandas as pd
import json
import gzip

from er2parquet.metadata import kolonner

def json2df(filnavn: str) -> pd.DataFrame:
    with gzip.open(filnavn, 'rb') as f:
        content = f.read()
        data = json.loads(content.decode('utf-8'))

    df = pd.json_normalize(data)

    # Vi må rydde bort klammeparenteser for å få riktig konvertering i neste steg.
    # gjelder postadresse.adresse og forretningsadresse.adresse og frivilligMvaRegistrertBeskrivelser
    # Tester at vi ikke gjør noe dumt ...
    # Noen av de ikke-tomme-feltene inneholder bare [], og da blir det feil å fjerne klammeparentesene OG anførselstegnene
    # Må bruke .loc for å unngå SettingWithCopyWarning

    object_kolonner = ['postadresse.adresse', 'forretningsadresse.adresse', 'frivilligMvaRegistrertBeskrivelser']

    for kolonne in object_kolonner:
        if \
            df[df[kolonne].notnull()][kolonne].astype(str).str.startswith("[").all() & \
            df[df[kolonne].notnull()][kolonne].astype(str).str.endswith("]").all():
            df.loc[df[kolonne].notnull(), kolonne] = df[df[kolonne].notnull()][kolonne].astype(str).str[1:-1].str.replace("'", "") # men her treffer vi vel også tomme?
        else:
            print("Noe er galt med kolonne ", kolonne)


    # Automatisk konvertering av en rekke typer, bl.a. object til string:
    df = pd.DataFrame.convert_dtypes(df)

    # Gjenstående konverteringer

    # Konvertere datoer
    df['stiftelsesdato'] = pd.to_datetime(df['stiftelsesdato'], unit='D', errors='coerce')
    df['registreringsdatoEnhetsregisteret'] = pd.to_datetime(df['registreringsdatoEnhetsregisteret'], unit='D', errors='coerce')

    # Konvertere til kategorier
    df = df.astype({k: v for k, v in kolonner.items() if v == 'category'})

    # Årstall som int
    df['sisteInnsendteAarsregnskap'] = pd.to_numeric(df['sisteInnsendteAarsregnskap'], downcast='integer')

    # Redusere størrelsen på tallformatet for antall ansatte
    df['antallAnsatte'] = pd.to_numeric(df['antallAnsatte'], downcast='integer')


    return df[list(kolonner.keys())]



if __name__ == '__main__':
    from er2parquet.to_parquet import to_parquet
    from er2parquet.from_parquet import from_parquet

    df = json2df('tests/testdata/enheter_alle.json.gz')
    print(df.info())
    to_parquet(df, 'enheter_alle.parquet')
    df = from_parquet('enheter_alle.parquet')
    print(df.info())