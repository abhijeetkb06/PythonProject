import streamlit as st
import math

def calculate_ram_usage(ram_allocated_per_node, total_nodes, ram_usage_slider):
    currently_used_ram_per_node = (ram_allocated_per_node * total_nodes * ram_usage_slider / 100.0) / total_nodes
    return round(currently_used_ram_per_node, 2)

def calculate_additional_nodes(ram_allocated_per_node, total_nodes, currently_used_ram_per_node, desired_ram_usage):
    current_ram_usage = currently_used_ram_per_node / ram_allocated_per_node
    target_ram_usage = desired_ram_usage / 100.0
    if target_ram_usage != 0:
        add_more_nodes = math.ceil((current_ram_usage - target_ram_usage) * total_nodes / target_ram_usage)
    else:
        add_more_nodes = 0
    return add_more_nodes

st.title("Couchbase Node Growth Insight")

ram_allocated_per_node = st.number_input("RAM Allocated per Node (GB):", value=256.0, step=0.1)
total_nodes = st.number_input("Total Cluster Nodes (Data/Index):", value=36, step=1)
ram_usage_slider = st.slider("Average RAM Utilization (%):", min_value=0, max_value=100, value=90)

currently_used_ram_per_node = calculate_ram_usage(ram_allocated_per_node, total_nodes, ram_usage_slider)
st.text(f"RAM Usage per Node (GB): {currently_used_ram_per_node}")

desired_ram_usage = st.slider("Desired Average RAM Usage (%):", min_value=0, max_value=100, value=0)

if st.button("Analyze Node Adjustment"):
    more_nodes_for_desired_ram = calculate_additional_nodes(ram_allocated_per_node, total_nodes, currently_used_ram_per_node, desired_ram_usage)
    st.text(f"Total Node Adjustment(Data/Index): {more_nodes_for_desired_ram}")

if st.button("Clear"):
    ram_allocated_per_node = 256.0
    total_nodes = 36
    ram_usage_slider = 90
    desired_ram_usage = 0.0