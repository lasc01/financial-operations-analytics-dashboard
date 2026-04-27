from pathlib import Path
from google.cloud import bigquery


BASE_DIR = Path(__file__).resolve().parents[1]
CLEAN_DIR = BASE_DIR / "data" / "cleaned"

PROJECT_ID = "project-172dc47b-3315-4168-9d2"
DATASET_ID = "financial_ops_raw"


TABLES = {
    "customers_raw": "customers_cleaned.csv",
    "products_raw": "products_cleaned.csv",
    "sales_raw": "sales_cleaned.csv",
    "costs_raw": "costs_cleaned.csv",
}


def load_csv_to_bigquery(client, table_name, file_name):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    file_path = CLEAN_DIR / file_name

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    with open(file_path, "rb") as file:
        load_job = client.load_table_from_file(
            file,
            table_id,
            job_config=job_config,
        )

    load_job.result()

    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows:,} rows into {table_id}")


def main():
    client = bigquery.Client(project=PROJECT_ID)

    for table_name, file_name in TABLES.items():
        load_csv_to_bigquery(client, table_name, file_name)

    print("All cleaned files loaded to BigQuery successfully.")


if __name__ == "__main__":
    main()