import pandas as pd 
import os
import re
from dotenv import load_dotenv #Load enviornment varaibles from .env file
from openai import OpenAI #OpenAI API client

# Load API key
load_dotenv() #Loads environment variables --> OPEN_API_KEY
client = OpenAI() #Initialize OPENAI client using API ket from environment

def clean_price(value):
    """Clean euro-formatted price like '€350,000' or 'AMV: 1400000'."""
    if pd.isna(value):
        return None
    value = str(value)
    value = re.sub(r"[^\d.]", "", value) #Remove  symbols like €, commas, AMV
    return float(value) if value else None

def extract_number(val):
    """Extract numeric part of strings like '3 Bed' or 'Studio'."""
    if pd.isna(val):
        return None
    match = re.search(r"\d+(\.\d+)?", str(val)) #Extract numerical values from strings like '3 Bed' or '2.5 Bathrooms'.
    return float(match.group()) if match else None

#Dynamically create a prompt string for GPT based on dataset stats.
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
    df = pd.read_csv(csv_path) #load the data

    # Clean numerical columns - applying our function above to dataset columns
    df["Price"] = df["Price"].apply(clean_price)
    df["Number of Bedrooms"] = df["Number of Bedrooms"].apply(extract_number)
    df["Number of Bathrooms"] = df["Number of Bathrooms"].apply(extract_number)
    df["Floor Area (m2)"] = df["Floor Area (m2)"].apply(extract_number)

    print("\n EDA Preprocessing Steps")
    print("\nFirst 10 rows:")
    print(df.head(10))
    
    print('\Dataset Shape')
    print(df.shape)

    print("\nDataset info:")
    print(df.info())

    print("\nNull value counts:")
    print(df.isnull().sum())

    # Drop rows with missing critical values
    df = df.dropna(subset=["Price", "Number of Bedrooms", "Number of Bathrooms", "Floor Area (m2)"])

    # Check Correlation of the independent features
    print("\nCorrelation matrix:")
    corr = df[["Price", "Number of Bathrooms", "Floor Area (m2)", "Latitude", "Longitude", "Listing Views", "Date of Construction"]].corr()
    print(corr)

    # Drop low-correlated features from price
    low_corr_cols = corr["Price"][abs(corr["Price"]) < 0.05].index.tolist()
    print("\nDropping low-correlated columns (to Price):", low_corr_cols)
    
    print('\Dataset Shape after EDA')
    print(df.shape)

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

    # Get AI-generated summary - define model and messages
    #Configure parameters for the model
    response = client.chat.completions.create(  #method call to generate a chat completion usng OpenAI Chat API
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You are a data analyst."}, #lettiing the system know its role in the interaction - data analyst
            {"role": "user", "content": prompt} #passing the prompt created above
        ],
        temperature=0.7, #setting temperature allows for more creative/randomness in the housing_summary.txt file
        max_tokens=300 #limiting the reponse to 300 tokens 300 --> This can be increased depending on the needs
    )

    summary = response.choices[0].message.content.strip() #model resonse is returned as a reponse object and removing any leading/tailing whitespaces
    print("\n AI Summary:\n", summary)

    # Save summary
    with open("housing_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    return summary

if __name__ == "__main__":
    analyze_housing_data()
