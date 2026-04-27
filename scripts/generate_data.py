from pathlib import Path
from datetime import datetime, timedelta
import random

import numpy as np
import pandas as pd
from faker import Faker


fake = Faker("en_IE")
Faker.seed(42)
random.seed(42)
np.random.seed(42)


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


N_CUSTOMERS = 5000
N_PRODUCTS = 250
N_SALES = 50000
N_COSTS = 8000

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)


REGIONS = {
    "Dublin": ["Dublin City", "Tallaght", "Swords", "Blanchardstown"],
    "Cork": ["Cork City", "Ballincollig", "Midleton", "Cobh"],
    "Galway": ["Galway City", "Oranmore", "Athenry", "Tuam"],
    "Limerick": ["Limerick City", "Newcastle West", "Adare", "Annacotty"],
}

SALES_CHANNELS = ["Website", "Mobile App", "In Store", "Partner Marketplace"]
PAYMENT_METHODS = ["Card", "Bank Transfer", "PayPal", "Apple Pay"]
AGE_GROUPS = ["18 to 24", "25 to 34", "35 to 44", "45 to 54", "55 plus"]
SEGMENTS = ["Standard", "Premium", "VIP"]
LOYALTY_STATUS = ["Bronze", "Silver", "Gold"]

PRODUCT_CATEGORIES = {
    "Electronics": ["Audio", "Mobile Accessories", "Smart Devices", "Computing"],
    "Home Goods": ["Kitchen", "Decor", "Furniture", "Storage"],
    "Fashion": ["Menswear", "Womenswear", "Footwear", "Outerwear"],
    "Beauty": ["Skincare", "Haircare", "Fragrance", "Makeup"],
    "Accessories": ["Bags", "Watches", "Jewellery", "Travel"],
}

BRANDS = ["Nova", "UrbanEdge", "BrightLine", "CoreStyle", "PureNest", "Flexora"]
SUPPLIERS = ["GreenLine Supplies", "Atlantic Wholesale", "Prime Source Ltd", "Metro Distribution"]

DEPARTMENTS = ["Marketing", "Operations", "Logistics", "Customer Support", "IT", "Administration"]

COST_OPTIONS = {
    "Marketing": ["Advertising", "Influencer Campaigns", "Email Marketing"],
    "Operations": ["Packaging", "Warehouse Supplies", "Quality Control"],
    "Logistics": ["Delivery", "Courier Fees", "Fuel"],
    "Customer Support": ["Salaries", "Training", "Support Software"],
    "IT": ["Software", "Cloud Services", "Security Tools"],
    "Administration": ["Rent", "Utilities", "Office Supplies"],
}


def random_date(start_date, end_date):
    days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days))


def generate_customers():
    rows = []

    for i in range(1, N_CUSTOMERS + 1):
        region = random.choice(list(REGIONS.keys()))
        city = random.choice(REGIONS[region])
        first_name = fake.first_name()
        last_name = fake.last_name()

        rows.append(
            {
                "customer_id": f"CUST{i:06d}",
                "customer_name": f"{first_name} {last_name}",
                "gender": random.choice(["Male", "Female"]),
                "age_group": random.choices(
                    AGE_GROUPS,
                    weights=[0.15, 0.30, 0.25, 0.18, 0.12],
                    k=1,
                )[0],
                "region": region,
                "city": city,
                "acquisition_date": random_date(datetime(2022, 1, 1), END_DATE).date(),
                "acquisition_channel": random.choice(SALES_CHANNELS),
                "segment": random.choices(SEGMENTS, weights=[0.70, 0.25, 0.05], k=1)[0],
                "email": f"{first_name.lower()}.{last_name.lower()}{i}@example.com",
                "loyalty_status": random.choices(LOYALTY_STATUS, weights=[0.55, 0.32, 0.13], k=1)[0],
                "preferred_channel": random.choice(SALES_CHANNELS),
                "is_active": random.choices([True, False], weights=[0.88, 0.12], k=1)[0],
            }
        )

    return pd.DataFrame(rows)


def generate_products():
    rows = []

    for i in range(1, N_PRODUCTS + 1):
        category = random.choice(list(PRODUCT_CATEGORIES.keys()))
        subcategory = random.choice(PRODUCT_CATEGORIES[category])
        brand = random.choice(BRANDS)

        standard_cost = round(random.uniform(5, 220), 2)
        markup = random.uniform(1.25, 2.80)
        list_price = round(standard_cost * markup, 2)

        rows.append(
            {
                "product_id": f"PROD{i:04d}",
                "product_name": f"{brand} {subcategory} Item {i}",
                "category": category,
                "subcategory": subcategory,
                "brand": brand,
                "supplier_name": random.choice(SUPPLIERS),
                "standard_cost": standard_cost,
                "list_price": list_price,
                "launch_date": random_date(datetime(2022, 1, 1), datetime(2025, 6, 30)).date(),
                "product_status": random.choices(["Active", "Discontinued"], weights=[0.92, 0.08], k=1)[0],
            }
        )

    return pd.DataFrame(rows)


def generate_sales(customers_df, products_df):
    rows = []

    customer_ids = customers_df["customer_id"].tolist()
    product_records = products_df[["product_id", "list_price"]].to_dict("records")

    for i in range(1, N_SALES + 1):
        order_id = f"ORD{i // 2 + 1:07d}"
        product = random.choice(product_records)

        sales_channel = random.choices(
            SALES_CHANNELS,
            weights=[0.42, 0.30, 0.18, 0.10],
            k=1,
        )[0]

        quantity = random.choices(
            [1, 2, 3, 4, 5],
            weights=[0.55, 0.25, 0.12, 0.06, 0.02],
            k=1,
        )[0]

        unit_price = float(product["list_price"])

        if sales_channel == "Website":
            unit_price *= random.uniform(1.00, 1.08)

        elif sales_channel == "Mobile App":
            unit_price *= random.uniform(1.03, 1.12)

        elif sales_channel == "In Store":
            unit_price *= random.uniform(0.96, 1.04)

        elif sales_channel == "Partner Marketplace":
            unit_price *= random.uniform(0.88, 0.96)

        unit_price = round(unit_price, 2)

        if sales_channel == "Partner Marketplace":
            discount_pct = random.choices(
                [0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
                weights=[0.10, 0.18, 0.25, 0.22, 0.15, 0.10],
                k=1,
            )[0]

        elif sales_channel == "Mobile App":
            discount_pct = random.choices(
                [0.00, 0.05, 0.10, 0.15, 0.20],
                weights=[0.45, 0.25, 0.18, 0.08, 0.04],
                k=1,
            )[0]

        elif sales_channel == "Website":
            discount_pct = random.choices(
                [0.00, 0.05, 0.10, 0.15, 0.20],
                weights=[0.35, 0.25, 0.20, 0.13, 0.07],
                k=1,
            )[0]

        else:
            discount_pct = random.choices(
                [0.00, 0.05, 0.10, 0.15, 0.20, 0.25],
                weights=[0.30, 0.22, 0.20, 0.15, 0.09, 0.04],
                k=1,
            )[0]

        gross_revenue = round(quantity * unit_price, 2)
        net_revenue = round(gross_revenue * (1 - discount_pct), 2)

        order_status = random.choices(
            ["Completed", "Returned", "Cancelled"],
            weights=[0.88, 0.07, 0.05],
            k=1,
        )[0]

        if order_status == "Cancelled":
            net_revenue = 0.00
            tax_amount = 0.00
            shipping_fee = 0.00
        else:
            tax_amount = round(net_revenue * 0.23, 2)
            shipping_fee = round(random.choice([0, 3.99, 4.99, 5.99, 7.99]), 2)

        order_dt = random_date(START_DATE, END_DATE)
        order_ts = order_dt + timedelta(
            hours=random.randint(8, 22),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59),
        )

        rows.append(
            {
                "order_id": order_id,
                "order_line_id": f"OL{i:08d}",
                "customer_id": random.choice(customer_ids),
                "product_id": product["product_id"],
                "order_date": order_dt.date(),
                "order_timestamp": order_ts,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount_pct": discount_pct,
                "gross_revenue": gross_revenue,
                "net_revenue": net_revenue,
                "sales_channel": sales_channel,
                "region": random.choice(list(REGIONS.keys())),
                "payment_method": random.choice(PAYMENT_METHODS),
                "order_status": order_status,
                "shipping_fee": shipping_fee,
                "tax_amount": tax_amount,
                "returned_flag": order_status == "Returned",
            }
        )

    return pd.DataFrame(rows)


def generate_costs():
    rows = []

    vendors = [
        "Meta Ads",
        "Google Ads",
        "DHL Ireland",
        "An Post Commerce",
        "AWS",
        "Microsoft",
        "Zendesk",
        "OfficeHub",
        "City Properties",
    ]

    for i in range(1, N_COSTS + 1):
        department = random.choice(DEPARTMENTS)
        cost_type = random.choice(COST_OPTIONS[department])

        base_amount = {
            "Marketing": (80, 2500),
            "Operations": (50, 1800),
            "Logistics": (40, 2200),
            "Customer Support": (60, 1500),
            "IT": (100, 3000),
            "Administration": (200, 4500),
        }[department]

        amount = round(random.uniform(*base_amount), 2)

        rows.append(
            {
                "cost_id": f"COST{i:07d}",
                "cost_date": random_date(START_DATE, END_DATE).date(),
                "region": random.choice(list(REGIONS.keys())),
                "department": department,
                "cost_category": cost_type,
                "cost_type": cost_type,
                "amount": amount,
                "vendor_name": random.choice(vendors),
                "description": f"{cost_type} expense for {department}",
                "fixed_variable_flag": random.choices(["Fixed", "Variable"], weights=[0.35, 0.65], k=1)[0],
            }
        )

    return pd.DataFrame(rows)


def main():
    customers_df = generate_customers()
    products_df = generate_products()
    sales_df = generate_sales(customers_df, products_df)
    costs_df = generate_costs()

    customers_df.to_csv(RAW_DIR / "customers_raw.csv", index=False)
    products_df.to_csv(RAW_DIR / "products_raw.csv", index=False)
    sales_df.to_csv(RAW_DIR / "sales_raw.csv", index=False)
    costs_df.to_csv(RAW_DIR / "costs_raw.csv", index=False)

    print("Synthetic data generated successfully.")
    print(f"Customers: {len(customers_df):,}")
    print(f"Products: {len(products_df):,}")
    print(f"Sales: {len(sales_df):,}")
    print(f"Costs: {len(costs_df):,}")
    print(f"Files saved to: {RAW_DIR}")


if __name__ == "__main__":
    main()