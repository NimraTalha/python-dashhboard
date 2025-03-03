
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Advanced Data Dashboard", layout="wide")

st.title("📊 Advanced Data Dashboard")

# Upload CSV File
uploaded_file = st.file_uploader("📂 Choose a CSV file", type="csv")

if uploaded_file is not None: 
    df = pd.read_csv(uploaded_file)

    # Sidebar for navigation
    st.sidebar.header("⚙️ Dashboard Settings")

    # Display data preview
    st.subheader("🔍 Data Preview")
    st.write(df.head())

    # Display statistical summary
    st.subheader("📊 Data Summary")
    st.write(df.describe())

    # Multi-column filtering
    st.sidebar.subheader("🔎 Filter Data")
    columns = df.columns.tolist()
    selected_columns = st.sidebar.multiselect("Select columns to filter by", columns)

    filtered_df = df.copy()
    for col in selected_columns:
        unique_values = df[col].dropna().unique().tolist()
        selected_value = st.sidebar.selectbox(f"Select a value from {col}", unique_values, key=col)
        filtered_df = filtered_df[filtered_df[col] == selected_value]

    # Display filtered data
    st.subheader("📋 Filtered Data")
    st.write(filtered_df)

    # Download button for filtered data
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(label="📥 Download Filtered Data as CSV", data=csv, file_name="filtered_data.csv", mime="text/csv")

    # Data visualization
    st.subheader("📈 Data Visualization")
    numeric_columns = filtered_df.select_dtypes(include=['number']).columns.tolist()

    if numeric_columns:
        chart_type = st.selectbox("Select chart type", ["Histogram", "Line Chart", "Bar Chart", "Scatter Plot", "Correlation Heatmap"])

        selected_numeric_column = st.selectbox("Select a numeric column", numeric_columns)

        fig, ax = plt.subplots(figsize=(8, 5))

        if chart_type == "Histogram":
            filtered_df[selected_numeric_column].hist(bins=20, ax=ax)
            ax.set_title(f"Histogram of {selected_numeric_column}")

        elif chart_type == "Line Chart":
            st.line_chart(filtered_df[selected_numeric_column])

        elif chart_type == "Bar Chart":
            st.bar_chart(filtered_df[selected_numeric_column])

        elif chart_type == "Scatter Plot":
            selected_numeric_column_2 = st.selectbox("Select another numeric column", numeric_columns)
            sns.scatterplot(data=filtered_df, x=selected_numeric_column, y=selected_numeric_column_2, ax=ax)
            ax.set_title(f"Scatter Plot: {selected_numeric_column} vs {selected_numeric_column_2}")

        elif chart_type == "Correlation Heatmap":
            st.subheader("📊 Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(filtered_df.corr(), annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
            st.pyplot(fig)

        st.pyplot(fig)
    else:
        st.warning("⚠️ No numeric columns available for visualization.")

else:
    st.info("📂 Please upload a CSV file to get started.")
