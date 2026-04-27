import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "cleaned"
CLEAN_DIR.mkdir(parents=True, exist_ok=True)


def clean_customers():
    df = pd.read_csv(RAW_DIR / "customers_raw.csv")

    # Remove duplicates
    df = df.drop_duplicates(subset=["customer_id"])

    # Strip spaces safely
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Standardize email
    df["email"] = df["email"].str.lower()

    # Remove missing critical values
    df = df.dropna(subset=["customer_id", "customer_name"])

    return df


def clean_products():
    df = pd.read_csv(RAW_DIR / "products_raw.csv")

    df = df.drop_duplicates(subset=["product_id"])

    # Ensure cost <= price
    df = df[df["standard_cost"] <= df["list_price"]]

    # Remove missing categories
    df = df.dropna(subset=["category"])

    return df


def clean_sales():
    df = pd.read_csv(RAW_DIR / "sales_raw.csv")

    # Remove duplicates
    df = df.drop_duplicates(subset=["order_line_id"])

    # Fix types
    df["quantity"] = df["quantity"].clip(lower=1)
    df["unit_price"] = df["unit_price"].clip(lower=0)

    # Fix discount
    df["discount_pct"] = df["discount_pct"].clip(0, 0.30)

    # Recalculate revenue
    df["gross_revenue"] = df["quantity"] * df["unit_price"]
    df["net_revenue"] = df["gross_revenue"] * (1 - df["discount_pct"])

    # Ensure valid status
    valid_status = ["Completed", "Returned", "Cancelled"]
    df = df[df["order_status"].isin(valid_status)]

    # Fix returned flag
    df["returned_flag"] = df["order_status"] == "Returned"

    # Remove invalid rows
    df = df.dropna(subset=["customer_id", "product_id"])

    return df


def clean_costs():
    df = pd.read_csv(RAW_DIR / "costs_raw.csv")

    df = df.drop_duplicates(subset=["cost_id"])

    # Remove invalid values
    df = df[df["amount"] > 0]

    # Strip spaces safely
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    return df


def main():
    customers = clean_customers()
    products = clean_products()
    sales = clean_sales()
    costs = clean_costs()

    customers.to_csv(CLEAN_DIR / "customers_cleaned.csv", index=False)
    products.to_csv(CLEAN_DIR / "products_cleaned.csv", index=False)
    sales.to_csv(CLEAN_DIR / "sales_cleaned.csv", index=False)
    costs.to_csv(CLEAN_DIR / "costs_cleaned.csv", index=False)

    print("Data cleaned successfully.")
    print(f"Customers: {len(customers)}")
    print(f"Products: {len(products)}")
    print(f"Sales: {len(sales)}")
    print(f"Costs: {len(costs)}")


if __name__ == "__main__":
    main()