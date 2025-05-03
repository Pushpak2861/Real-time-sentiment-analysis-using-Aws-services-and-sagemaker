import boto3
import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt

def pull_data_from_dynamo():
    dynamodb_resource = boto3.resource("dynamodb" , region_name = "eu-west-1")
    table = dynamodb_resource.Table("sentiment-01")
    response = table.scan()
    df = pd.DataFrame(response["Items"])
    return df
    
def streamlit_service():
    df = pull_data_from_dynamo()
    st.title("Review Sentiment per Category")

    all_categories = df['category'].unique().tolist()

    selected_categories = st.multiselect("Choose one or more categories", all_categories)

    if selected_categories:
        for cat in selected_categories:
            st.subheader(f"Category: {cat}")
            cat_df = df[df['category'] == cat]

            if cat_df.empty:
                st.warning(f"No data found for category: {cat}")
                continue

            label_counts = cat_df['label'].value_counts()

            fig, ax = plt.subplots()
            label_counts.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title(f"Label Counts for {cat}")
            ax.set_xlabel("Label")
            ax.set_ylabel("Count")
            st.pyplot(fig)

            #this is a raw table with value and counts for more information
            with st.expander("More information"):
                st.write(label_counts.reset_index().rename(columns={'index': 'Label', 'label': 'Count'}))
    else:
        st.info("Please select at least one category to display the charts.")

if __name__ == "__main__":
    streamlit_service()





