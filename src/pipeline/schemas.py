import pyarrow as pa

pubmed_schema = pa.schema(
    [
        ("id", pa.string()),
        ("title", pa.string()),
        ("date", pa.date32()),
        ("journal", pa.string()),
    ]
)

clinical_trials_schema = pa.schema(
    [
        ("id", pa.string()),
        ("scientific_title", pa.string()),
        ("date", pa.date32()),
        ("journal", pa.string()),
    ]
)

drugs_schema = pa.schema([("atccode", pa.string()), ("drug", pa.string())])
