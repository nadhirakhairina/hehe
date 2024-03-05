import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

customers_df = pd.read_csv("customers_dataset.csv")
product_df = pd.read_csv("products_dataset.csv")
order_items_df = pd.read_csv("order_items_dataset.csv")
sales_df = pd.read_csv("sales_data.csv")

# Set up the page
st.set_page_config(page_title="Sales Brazilian-Ecommerce Dashboard", page_icon=":bar_chart:", layout="wide")

# Menampilkan data menggunakan Streamlit
st.sidebar.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", use_column_width=True)
# Menambahkan header pada dashboard
st.header('E-Commerce Dashboard :sparkles:')

# Function to plot distribution of product categories
def plot_product_distribution(product_df):
    plt.figure(figsize=(12, 8))
    sns.countplot(x="product_category_name", data=product_df, palette="viridis",
                  order=product_df["product_category_name"].value_counts().index)
    plt.title("Distribution of Product Categories", fontsize=16)
    plt.xlabel("Product Category", fontsize=14)
    plt.ylabel("Number of Products", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    st.pyplot(plt)

# Function to plot distribution of product dimensions
def plot_product_dimensions(product_df):
    plt.figure(figsize=(10, 6))
    sns.histplot(product_df[["product_length_cm", "product_height_cm", "product_width_cm"]], bins=20, kde=True, multiple="stack")
    plt.title("Distribution of Product Dimensions")
    plt.xlabel("Product Dimensions")
    plt.ylabel("Frequency")
    plt.legend(labels=["Length", "Height", "Width"])
    st.pyplot(plt)

# Function to plot distribution of sales product prices
def plot_sales_price_distribution(sales_df):
    plt.figure(figsize=(10, 6))
    sns.histplot(sales_df["price"], bins=20, color='skyblue', edgecolor='black')
    plt.title("Distribution of Sales Product Prices")
    plt.xlabel("Price")
    plt.ylabel("Count ID")
    st.pyplot(plt)

# Function to plot distribution of sales freight value
def plot_sales_freight_value(sales_df):
    sales_df["freight_value"].plot(kind="hist", bins=20, figsize=(10, 6), title="Distribution of Sales freight_value")
    plt.xlabel("freight_value")
    plt.ylabel("Count ID")
    st.pyplot(plt)

# Function to plot scatter plot of product price vs freight value
def plot_price_vs_freight_value(sales_df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="price", y="freight_value", data=sales_df)
    plt.title("Scatter Plot of Product Price vs Freight Value")
    plt.xlabel("Product Price")
    plt.ylabel("Freight Value")
    st.pyplot(plt)

# Function to plot count of the number of customers per state
def plot_customers_per_state(customers_df):
    customers_per_state = customers_df["customer_state"].value_counts().reset_index()
    customers_per_state.columns = ["customer_state", "count"]
    customers_per_state = customers_per_state.sort_values(by="count", ascending=False)
    total_customers = customers_per_state["count"].sum()
    customers_per_state["percentage"] = (customers_per_state["count"] / total_customers) * 100
    colors = sns.color_palette("hsv", len(customers_per_state))

    plt.figure(figsize=(15, 6))
    plt.title("Count of the Number of Customers per State")
    plt.xlabel("State")
    plt.xticks(rotation="vertical")
    plt.ylabel("Number of Customers")
    sns.barplot(x="customer_state", y="count", data=customers_per_state.reset_index(), palette=colors)
    for i, (count, percent) in enumerate(zip(customers_per_state["count"], customers_per_state["percentage"])):
        plt.text(i, count + 10, f"{percent:.2f}%", ha="center", color="black")
    st.pyplot(plt)

# Function to perform RFM analysis
def perform_rfm_analysis(sales_df):
    # Change the atribut type data
    sales_df["shipping_limit_date"] = pd.to_datetime(sales_df["shipping_limit_date"])

    # Grouping based on order_id and calculating the required attributes
    rfm_df = sales_df.groupby(by="order_id", as_index=False).agg({
        "order_item_id": "nunique", # Counting the number of orders
        "price": "sum", # Calculating the total price
        "shipping_limit_date": "max" # Taking the latest shipping date
    })

    # Renaming columns for better understanding
    rfm_df.columns = ["order_id", "frequency", "monetary", "max_order_item_id"]

    # Memastikan bahwa kolom 'max_order_item_id' adalah tipe datetime
    rfm_df["max_order_item_id"] = pd.to_datetime(rfm_df["max_order_item_id"])

    # Menghitung recency (jumlah hari sejak tanggal pengiriman terakhir)
    recent_date = rfm_df["max_order_item_id"].max().date()
    rfm_df["recency"] = rfm_df["max_order_item_id"].apply(lambda x: (recent_date - x.date()).days)

    # Dropping the max_order_date column as it is no longer needed
    rfm_df.drop("max_order_item_id", axis=1, inplace=True)

    # Create subplots with a specified size
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

    # Define colors for the plots (purple)
    colors = ["#8a2be2", "#8a2be2", "#8a2be2", "#8a2be2", "#8a2be2"]

    # Plot for Recency
    sns.barplot(y="recency", x="order_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel("Recency (days)", fontsize=15)
    ax[0].set_xlabel(None)
    ax[0].set_title("Top 5 by Recency", fontsize=18)
    ax[0].tick_params(axis ='x', labelsize=12)
    ax[0].tick_params(axis='y', labelsize=12)

    # Plot for Frequency
    sns.barplot(y="frequency", x="order_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel("Frequency", fontsize=15)
    ax[1].set_xlabel(None)
    ax[1].set_title("Top 5 by Frequency", fontsize=18)
    ax[1].tick_params(axis='x', labelsize=12)
    ax[1].tick_params(axis='y', labelsize=12)

    # Plot for Monetary
    sns.barplot(y="monetary", x="order_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
    ax[2].set_ylabel("Monetary", fontsize=15)
    ax[2].set_xlabel(None)
    ax[2].set_title("Top 5 by Monetary", fontsize=18)
    ax[2].tick_params(axis='x', labelsize=12)
    ax[2].tick_params(axis='y', labelsize=12)

    # Set x-axis labels as a list below the plot for all subplots
    x_labels_recency = rfm_df.sort_values(by="recency", ascending=True).head(5)["order_id"].tolist()
    x_labels_frequency = rfm_df.sort_values(by="frequency", ascending=False).head(5)["order_id"].tolist()
    x_labels_monetary = rfm_df.sort_values(by="monetary", ascending=False).head(5)["order_id"].tolist()

    ax[0].set_xticklabels(x_labels_recency, rotation=45, ha='right')
    ax[1].set_xticklabels(x_labels_frequency, rotation=45, ha='right')
    ax[2].set_xticklabels(x_labels_monetary, rotation=45, ha='right')

    # Add a title for the overall visualization
    plt.suptitle("Top Customers Based on RFM Parameters (Order ID)", fontsize=20)

    # Adjust layout to prevent overlapping
    plt.tight_layout()

    # Show the plots
    st.pyplot(plt)

def main():
    st.title("Your Dashboard")

    # Plot the distribution of product categories
    st.header("Distribution of Product Categories")
    plot_product_distribution(product_df)

    # Plot the distribution of product dimensions
    st.header("Distribution of Product Dimensions")
    plot_product_dimensions(product_df)

    # Plot the distribution of sales product prices
    st.header("Distribution of Sales Product Prices")
    plot_sales_price_distribution(sales_df)

    # Plot the distribution of sales freight value
    st.header("Distribution of Sales Freight Value")
    plot_sales_freight_value(sales_df)

    # Plot the scatter plot of product price vs freight value
    st.header("Scatter Plot of Product Price vs Freight Value")
    plot_price_vs_freight_value(sales_df)

    # Plot the count of the number of customers per state
    st.header("Count of the Number of Customers per State")
    plot_customers_per_state(customers_df)

    # Perform RFM analysis
    st.header("RFM Analysis")
    perform_rfm_analysis(sales_df)

if __name__ == "__main__":
    main()