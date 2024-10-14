import pandas as pd

# Dictionary with data jobs
data = {"Job title":["Software Engineer", "Data Scientist", "Machine Learning Engineer", "Product Manager", "Professor"],
        "Location": ["Chicago, IL", "Seattle, WA", "Houston, TX", "Denver, CO", "New York, NY"],
        "Salary": [100000, 60000, 55000, 80000, 90000,],
        "Remote": [True, False, False, False, True, ],}

# Transform the dictionary into Pandas dataframe
df = pd.DataFrame(data, index=["Job1", "Job2", "Job3", "Job4", "Job5"])
print(df)
print()

# Access a column by its name
print(df["Job title"])
print()

# Access a specific row by its index
print(df.iloc[2])
print()

# Access a specific row by its label
print(df.loc["Job4"])

print()
# Display all values > 65000
print(df[df["Salary"] > 65000])






