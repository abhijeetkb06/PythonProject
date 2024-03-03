import streamlit as st
from datetime import timedelta
from couchbase.exceptions import CouchbaseException, DocumentNotFoundException
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
import json

# Replace placeholders with your actual Couchbase information
endpoint = "couchbases://cb.wepvz44n89bkywd0.cloud.couchbase.com"
username = "abhijeet"
password = "Password@P1"
bucket_name = "ShoppingCart"
scope_name = "_default"

# Connect options - authentication
auth = PasswordAuthenticator(username, password)

# Get a reference to our cluster
options = ClusterOptions(auth)

# Use the pre-configured profile below to avoid latency issues with your connection.
options.apply_profile("wan_development")

# Cluster and bucket setup with error handling
try:
    cluster = Cluster(endpoint, options)
    cluster.wait_until_ready(timedelta(seconds=5))
    cb = cluster.bucket(bucket_name)
    collection = cb.default_collection()
except Exception as e:
    st.error(f"Error connecting to Couchbase: {e}")
    exit(1)

# Define Product Class
class Product:
    def __init__(self, id, name, price, description):
        self.id = id
        self.name = name
        self.price = price
        self.description = description

# Load Demo Product Data
def load_demo_products():
    products = [
        Product("1", "Product 1", 10.99, "Description for Product 1"),
        Product("2", "Product 2", 19.99, "Description for Product 2"),
        Product("3", "Product 3", 29.99, "Description for Product 3"),
    ]
    return products

# Fetch Products from Couchbase or Load Demo Products
def fetch_products():
    return load_demo_products()

# Fetch Cart from Couchbase
def fetch_cart_from_couchbase():
    try:
        result = collection.get("cart")
        if result.success:
            return result.content_as[list]
    except DocumentNotFoundException:
        pass
    return []

# Save Cart to Couchbase
def save_cart_to_couchbase(cart):
    try:
        collection.upsert("cart", cart)
    except Exception as e:
        print(f"Error saving cart to Couchbase: {e}")

# Save Order to Couchbase
def save_order_to_couchbase(order):
    try:
        collection.upsert("order", order)
    except Exception as e:
        print(f"Error saving order to Couchbase: {e}")

# Fetch Order from Couchbase
def fetch_order_from_couchbase():
    try:
        result = collection.get("order")
        if result.success:
            return result.content_as[list]
    except DocumentNotFoundException:
        pass
    return []

# Main Function to Display Products and Cart
def main():
    st.title("E-commerce Platform")

    # Fetch Products
    products = fetch_products()

    # Display Products
    st.subheader("Products")
    for product in products:
        st.write(f"**{product.name}** - ${product.price}")
        st.write(product.description)
        if st.button(f"Add to Cart - {product.name}_{product.price}_{product.id}", key=f"add_{product.id}"):
            cart = fetch_cart_from_couchbase()
            cart.append(product.name)
            save_cart_to_couchbase(cart)
            st.success(f"{product.name} added to cart!")

    # Check if "Order" button is clicked
    if st.button("Order", key="order_button"):
        cart = fetch_cart_from_couchbase()
        save_order_to_couchbase(cart)
        st.success("Order placed successfully!")

    # Show Cart
    st.sidebar.title("Shopping Cart")
    cart = fetch_cart_from_couchbase()
    if not cart:
        st.sidebar.write("Your cart is empty.")
    else:
        st.sidebar.write("Your Cart:")
        for item in cart:
            st.sidebar.write(item)

    # Show Order
    st.sidebar.title("Order")
    order = fetch_order_from_couchbase()
    if not order:
        st.sidebar.write("No order placed.")
    else:
        st.sidebar.write("Your Order:")
        for item in order:
            st.sidebar.write(item)

if __name__ == "__main__":
    main()