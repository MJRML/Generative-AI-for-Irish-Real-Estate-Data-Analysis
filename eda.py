import pandas as pd

def perform_eda(csv_path="data/daft_housing_data.csv"):
    # Load dataset
    df = pd.read_csv(csv_path)

    print(" Null value counts:\n", df.isnull().sum())
    print("\n DataFrame info:")
    print(df.info())
    print("\n First 10 rows of data:")
    print(df.head(10))

    # Clean price for correlation
    df["Price"] = (
        df["Price"]
        .astype(str)
        .str.replace("€", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.extract(r"(\d+\.?\d*)")[0]
        .astype(float)
    )

    # Correlation matrix
    corr_matrix = df.corr(numeric_only=True)
    print("\n Correlation matrix:\n", corr_matrix)

    # Drop columns with weak correlation to Price (abs < 0.1)
    if "Price" in corr_matrix.columns:
        low_corr_cols = corr_matrix.columns[corr_matrix["Price"].abs() < 0.1].tolist()
        print(f"\n Dropping low-correlated columns: {low_corr_cols}")
        df = df.drop(columns=low_corr_cols)

    return df

# Run if script is executed directly
if __name__ == "__main__":
    df = perform_eda()