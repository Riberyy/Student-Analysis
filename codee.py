import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

def load_csv_file(file_path):
    try:
        with open(file_path, "r") as file:
            st.success("File loaded successfully!")
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
file_path = "student-dataset.csv"
load_csv_file(file_path)

def write_csv(df, file_path):
    try:
        df.to_csv(file_path, index=False)
    except IOError:
        print(f"Error writing to file: {file_path}")

def check_file_exists(file_path):
    return os.path.exists(file_path)
# Load data
df = pd.read_csv('student-dataset.csv')

# Load your dataset (replace with your actual data)
df = pd.read_csv('student-dataset.csv')
max_Temp = df.loc[df['nationality'].idxmax(), 'city']
min_Temp = df.loc[df['nationality'].idxmin(), 'city']
# Create the summary text
summary_text = f"Highest population nationality: {max_Temp}\nLowest population nationality: {min_Temp}"

# Write the summary to a text file
with open('file.txt', 'w') as summary_file:
    summary_file.write(summary_text)    
print("save file.txt")

# Streamlit app
st.title('EDA of Student Analysis')

# Printing the DataFrame
st.subheader('Original dataset')
st.write(df)
st.write(df.shape)

# Printing the Update Dataframe
# Null values
st.subheader("After handling missing values")
st.write(df)
st.write(df.shape)

# Handle duplicates
df.drop_duplicates(inplace=True)
st.subheader("After handling duplicates")
st.write(df)
st.write(df.shape)


x_column = st.selectbox("Select X-axis column", df.columns, index=0)
if x_column != 0:
    st.subheader('Bar Chart')
    st.bar_chart(df[x_column].head(10), color='#ff69b4')

    st.subheader('Line Chart')
    st.line_chart(df[x_column].head(60))

    st.subheader('Scatter Plot')
    st.scatter_chart(df[x_column].head(60))
    st.subheader("area chart")
    st.area_chart(df[x_column].head(60))


    st.subheader("Pie chart using matplotlib")
    y_column = st.selectbox("Select x-axis column", df.columns, index=0)
    st.subheader("Maths grade")

plt.figure(figsize=[10, 10])
plt.pie(df[y_column].head(60).value_counts().values,
                autopct='%1.1f%%',
                labels=df[y_column].head(60).value_counts().index,
                colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
st.pyplot(plt)
