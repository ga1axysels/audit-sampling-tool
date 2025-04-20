import streamlit as st
import pandas as pd

# Functions
def random_sample(df, amount_col, n):
    return df.sample(n=n)

def top_x_sample(df, amount_col, x):
    return df.nlargest(x, amount_col)

def coverage_sample(df, amount_col, target_coverage=0.6):
    df_sorted = df.sort_values(by=amount_col, ascending=False)
    total = df_sorted[amount_col].sum()
    running_total = 0
    selected_rows = []
    
    for idx, row in df_sorted.iterrows():
        running_total += row[amount_col]
        selected_rows.append(idx)
        if running_total / total >= target_coverage:
            break
    return df.loc[selected_rows]

# Streamlit UI
st.title("Audit Sampling Assistant")

uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    # Read uploaded file
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    
    st.write("Here's a preview of your data:")
    st.dataframe(df)

    amount_col = st.selectbox("Select the column containing amounts:", df.columns)

    method = st.selectbox("Choose your sampling method:", ["Random Sampling", "Top X Sampling", "Coverage % Sampling"])

    if method == "Random Sampling":
        n = st.number_input("How many samples do you want?", min_value=1, max_value=len(df), value=5)
        if st.button("Generate Samples"):
            result = random_sample(df, amount_col, int(n))
            st.dataframe(result)

    elif method == "Top X Sampling":
        x = st.number_input("Top X items to select:", min_value=1, max_value=len(df), value=5)
        if st.button("Generate Samples"):
            result = top_x_sample(df, amount_col, int(x))
            st.dataframe(result)

    elif method == "Coverage % Sampling":
        pct = st.slider("Coverage Target (%)", min_value=10, max_value=100, value=60)
        if st.button("Generate Samples"):
            result = coverage_sample(df, amount_col, target_coverage=pct/100)
            st.dataframe(result)

    # Download button
    if 'result' in locals():
        st.download_button("Download Samples as CSV", result.to_csv(index=False), "sampled_data.csv")
