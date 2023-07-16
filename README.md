<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/er2parquet.svg?branch=main)](https://cirrus-ci.com/github/<USER>/er2parquet)
[![ReadTheDocs](https://readthedocs.org/projects/er2parquet/badge/?version=latest)](https://er2parquet.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/er2parquet/main.svg)](https://coveralls.io/r/<USER>/er2parquet)
[![PyPI-Server](https://img.shields.io/pypi/v/er2parquet.svg)](https://pypi.org/project/er2parquet/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/er2parquet.svg)](https://anaconda.org/conda-forge/er2parquet)
[![Monthly Downloads](https://pepy.tech/badge/er2parquet/month)](https://pepy.tech/project/er2parquet)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/er2parquet)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# er2parquet

> A tool to transform the register-data for all legal entities in Norway from a JSON-format to a parquet-format, which can be read faster, with less memory consumption and with more useful datatypes.

_Important! This is NOT an officially supported distribution - it is purely a private initiative primarily to solve my own needs :-)_

## A more efficient copy of the Register for Legal Entities
The Brønnøysund Register Centre (Brønnøysundregistrene) publishes the data from  the Central Coordinating Register for Legal Entities (CCR), a register which also includes data from the Norwegian Register of Business Enterprises, as Open Data. The data can be accessed via an API, for individual records or queries, returning at most 10.000 records. But it is also possible to download the full dataset either as a JSON-file (zipped) or an Excel-file.

Since there are more than 1.000.000 entities in the CCR, the Excel-file, is about 200 MB and has data across two sheets, and is heavy to work with. On my computer it takes approximatly 1 minute to open the file. In order to do any analysis, I also have to take into account that the data is spread across two sheets.

For repeated tasks, automating with Python can be a good idea. Reading the Excel-file with Python/pandas is very slow, though. In fact, it is faster to convert the Excel-file to CSV-format, and reading the CSV-file (just remember to make sure you convert _both_ sheets with data, [something I forgot myself](https://github.com/sskagemo/br_opne_data_eksempler/blob/main/last_ned_og_analyser_enhetsregisteret.ipynb).)

Reading the JSON-file is also fast, but, when unzipped, it is more than 1.0 GB (although the size of the zipped file is only approx. 60 MB). And as with the other formats, the JSON-format has limited information about the type of data in each column. Dates are strings, as are years. And for many of the columns there are a limited set of relevant values (for instance the type of the legal entity), but these are repeated as text.

With the parquet-file, we get a file that is similar to the zipped JSON-file in size, is very fast to read, while also including metadata that makes it much more efficient to read, and the resulting size of the pandas dataframe is less than half the size of what you will get when reading the Excel-file or JSON-file directly (approx 130 MB when reading the parquet-file vs approx 350 from JSON or Excel)

## Why?
With todays access to computing power, it might seem a bit irrelevant to worry about the file size. But I would like to offer an opportunity to work with the data using Python and Pandas, also for those who does not have Python installed on their own machine. This can be achieved using "somebody elses computer", i.e. the cloud. But then someone have to pay the bill of that computer, and if you are doing some analysis that somehow can disclose business secrets, like for instance who are your customers or who you are targeting, then you might prefer to doing all the work on your own machine.

In that case, Python in the browser might be your only option. And although it is now possible to run Python in the browser in ways that gives almost the exact same functionality as having it installed locally, it is definitly worth thinking about file-sizes and memory consumption!

## Usage
Primary function for end-user:

Read the parquet-file written by er2parquet into a pandas DataFrame:
```python
>>> from er2parquet.from_parquet import from_parquet
>>> df = from_parquet('enheter_alle.parquet')
``` 

Functionality for creating the parquet-file:

Read enheter_alle.json.gz-file into a pandas DataFrame:
```python
>>> df = json2df('../../tests/testdata/enheter_alle.json.gz')
```

Generate a parquet-file from the dataframe:
```python
>>> to_parquet(df, 'enheter_alle.parquet')
```


## Benchmarks
Converting the Excel-file to CSV using Xlsx2csv:
```python
%time Xlsx2csv("er.xlsx", outputencoding="utf-8").convert("er.csv")

CPU times: user 8min 6s, sys: 12.2 s, total: 8min 18s
Wall time: 8min 19s
```

Reading the JSON-file, with er2parquet's json2df() (which includes conversion of datatypes):
```python
%time df = json2df('../../tests/testdata/enheter_alle.json.gz')

CPU times: user 1min 26s, sys: 5.96 s, total: 1min 32s
Wall time: 1min 33s
```

Reading the parquet-file, produced by er2parquet from_parquet() (which is only two commands: Pandas read_parquet() and convert_dtypes()):
```python
%time df = from_parquet('../../test.parquet')

CPU times: user 1.81 s, sys: 70.1 ms, total: 1.88 s
Wall time: 1.99 s
```

So, reading a parquet-file, with the correct datatypes for the data, takes 2 _seconds_, while reading and converting data from the JSON-file is 50 times slower, and reading the data from Excel is likely to be 250 times slower ...

## Issues:
- Currently only main entities (hovedenheter). Could probably be extended to 
sub-entities (underenheter) as well as persons/roles
- Could probably also include functionality to add updates since the latest update of the file, to simplify keeping a local, updated copy without having to download the complete file
- When introducing unit='D' for conversion from string to datetime, it suddenly went from half
a million non-null values for stiftelsesdato, to zero non-null values ... why?
- using unit 'D' for datetime still results in dtype ```datatime64[ns]``` ... why?

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.4. For details and usage
information on PyScaffold see https://pyscaffold.org/.
