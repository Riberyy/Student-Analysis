import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

FILE_PATH = "student-dataset.csv"


def load_csv_file(file_path):
    """Check that the CSV exists and show a message in the app."""
    if os.path.exists(file_path):
        st.success("File loaded successfully!")
        return True
    st.error(f"File not found: {file_path}")
    return False

# ---------------------------------------------------------------
# Streamlit app
# ---------------------------------------------------------------
st.title("Student Analysis")

if not load_csv_file(FILE_PATH):
    st.stop()  # stop the app if the file is missing

# Load data (only once)
df = pd.read_csv(FILE_PATH)

# txt fle
counts = df["nationality"].value_counts()
summary = f"Most common: {counts.idxmax()}\nLeast common: {counts.idxmin()}"
st.text(summary)
st.download_button("Download file.txt", summary, file_name="file.txt")

# ---------------------------------------------------------------
# Original data
# ---------------------------------------------------------------
st.subheader("Original dataset")
st.write(df)
st.write(df.shape)

# ---------------------------------------------------------------
# Missing values
# ---------------------------------------------------------------
st.subheader("Missing values per column (before handling)")
st.write(df.isnull().sum())

# 1. Remove columns that are completely empty (e.g. ethnic.group)
df = df.dropna(axis=1, how="all")

# 2. Remove rows that are completely empty
df = df.dropna(axis=0, how="all")

# 3. Fill leftover small gaps
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].fillna("Unknown")          # text columns
for col in df.select_dtypes(include="number").columns:
    df[col] = df[col].fillna(df[col].median())   # number columns

st.subheader("After handling missing values")
st.write(df)
st.write(df.shape)

# ---------------------------------------------------------------
# Duplicates (ignore id, because it is unique in every row)
# ---------------------------------------------------------------
before = df.shape[0]
compare_cols = [c for c in df.columns if c != "id"]
df = df.drop_duplicates(subset=compare_cols)
after = df.shape[0]

st.subheader("After handling duplicates")
st.write(f"Duplicate rows removed: {before - after}")
st.write(df)
st.write(df.shape)

# ---------------------------------------------------------------
# Charts (numeric columns only)
# ---------------------------------------------------------------
numeric_cols = df.select_dtypes(include="number").columns.tolist()

x_column = st.selectbox("Select X-axis column", numeric_cols, index=0)

st.subheader(f"Bar Chart of {x_column}")
st.bar_chart(df[x_column].head(10), color="#ff69b4")

st.subheader(f"Line Chart of {x_column}")
st.line_chart(df[x_column].head(60))

st.subheader(f"Scatter Plot of {x_column}")
st.scatter_chart(df[x_column].head(60))

st.subheader(f"Area Chart of {x_column}")
st.area_chart(df[x_column].head(60))

# ---------------------------------------------------------------
# Pie chart (any column; works best with few categories)
# ---------------------------------------------------------------
y_column = st.selectbox("Select column for pie chart", df.columns, index=0, key="pie_column")

st.subheader(f"Pie chart of {y_column}")

counts = df[y_column].head(60).value_counts()

fig, ax = plt.subplots(figsize=(10, 10))
ax.pie(counts.values, autopct="%1.1f%%", labels=counts.index)
ax.set_title(f"Distribution of {y_column}")
st.pyplot(fig)

# Descriptive statistics (numeric columns, without id)
st.subheader("Descriptive statistics")

num = df.select_dtypes(include="number").drop(columns=["id"], errors="ignore")

stats = pd.DataFrame({
    "Mean": num.mean(),
    "Median": num.median(),
    "Mode": num.mode().iloc[0],
    "Variance": num.var(),
    "Std Dev": num.std(),
    "Range": num.max() - num.min(),
})
st.write(stats)