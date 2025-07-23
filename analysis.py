import pandas as pd
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
client = OpenAI()

def clean_price(value):
    """Clean euro-formatted price like '€350,000' or 'AMV: 1400000'."""
    if pd.isna(value):
        return None
    value = str(value)
    value = re.sub(r"[^\d.]", "", value)
    return float(value) if value else None

def extract_number(val):
    """Extract numeric part of strings like '3 Bed' or 'Studio'."""
    if pd.isna(val):
        return None
    match = re.search(r"\d+(\.\d+)?", str(val))
    return float(match.group()) if match else None

def prompt_from_housing_stats(stats):
    return f"""
Housing Market Summary (Daft dataset):
- Average price: €{stats['avg_price']:,.0f}
- Average bedrooms: {stats['avg_bedrooms']:.1f}
- Average bathrooms: {stats['avg_bathrooms']:.1f}
- Average floor area: {stats['avg_floor_area']:.1f} m²
- Most common property type: {stats['most_common_type']}
- Most listed county: {stats['most_common_county']}

Write a short analysis of this housing market data, and mention any interesting patterns.
"""

def analyze_housing_data(csv_path="data/daft_housing_data.csv"):
    df = pd.read_csv(csv_path)

    # Clean numerical columns
    df["Price"] = df["Price"].apply(clean_price)
    df["Number of Bedrooms"] = df["Number of Bedrooms"].apply(extract_number)
    df["Number of Bathrooms"] = df["Number of Bathrooms"].apply(extract_number)
    df["Floor Area (m2)"] = df["Floor Area (m2)"].apply(extract_number)

    print("\n🔎 EDA Preprocessing Steps")
    print("\nFirst 10 rows:")
    print(df.head(10))

    print("\nDataset info:")
    print(df.info())

    print("\nNull value counts:")
    print(df.isnull().sum())

    # Drop rows with missing critical values
    df = df.dropna(subset=["Price", "Number of Bedrooms", "Number of Bathrooms", "Floor Area (m2)"])

    # Correlation check
    print("\nCorrelation matrix:")
    corr = df[["Price", "Number of Bathrooms", "Floor Area (m2)", "Latitude", "Longitude", "Listing Views", "Date of Construction"]].corr()
    print(corr)

    # Drop low-correlated features from stats (optional)
    low_corr_cols = corr["Price"][abs(corr["Price"]) < 0.05].index.tolist()
    print("\nDropping low-correlated columns (to Price):", low_corr_cols)

    # Compute statistics for prompt
    stats = {
        "avg_price": df["Price"].mean(),
        "avg_bedrooms": df["Number of Bedrooms"].mean(),
        "avg_bathrooms": df["Number of Bathrooms"].mean(),
        "avg_floor_area": df["Floor Area (m2)"].mean(),
        "most_common_type": df["Property Type"].mode().iloc[0],
        "most_common_county": df["County"].mode().iloc[0],
    }

    # Generate GPT prompt
    prompt = prompt_from_housing_stats(stats)

    # Get AI-generated summary
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You are a data analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )

    summary = response.choices[0].message.content.strip()
    print("\n AI Summary:\n", summary)

    # Save summary
    with open("housing_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    return summary

if __name__ == "__main__":
    analyze_housing_data()
