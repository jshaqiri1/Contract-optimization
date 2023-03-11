import streamlit as st
from itertools import permutations
from funcAlloc import get_permutations, get_values, get_sorted_pairs, final_message, optimized


# Define the Streamlit app
def app():

   

    st.title("Contract Value Optimization")
    st.caption('By CPA unit')
    
    # Get the number of aggregate classes from the user
    num_aggregate_classes = st.number_input("Enter the number of Aggregate Classes (AC's):", value=5, step=1)

    # Get the names of the contractors from the user
    contractor_names = st.text_input("Enter the names of vendors separated by commas (e.g. Google, Apple, Miscrosoft):")
    contractor_names = [name.strip().upper() for name in contractor_names.split(',')]

    # Get the allocation list from the user
    allocation = []
    allocated_count = 0
    for name in contractor_names:
        max_allocations = num_aggregate_classes - allocated_count
        num_allocations = st.number_input(f"How many AC's do you want to allocate to {name}?", min_value=0, max_value=max_allocations, value=0)
        for i in range(num_allocations):
            allocation.append(name)
        allocated_count += num_allocations


    # Create a form for the user to input the bids
    with st.form("bid_form"):
        bids = []
        for i in range(num_aggregate_classes):
            bid_dict = {}
            st.header(f"Aggregate Class {i+1}")
            for j, name in enumerate(contractor_names):
                bid = st.number_input(f"{name}'s bid amount", value=0, step=1, key=f"bid_{i}_{j}")
                bid_dict[name] = bid
            bids.append(bid_dict)
        submitted = st.form_submit_button("Submit")


    # Display the lowest combination of bids if the form has been submitted
    if submitted:
        my_permutations = get_permutations(allocation)
        values = get_values(my_permutations, bids)
        pairs = get_sorted_pairs(my_permutations, values)
        message = final_message(pairs)
        best = optimized(pairs)

        
        st.markdown('**Optimized Contract Allocation:**')
        st.text(best)
        st.markdown('**Below are all possible combinations sorted by $:**')
        st.text(message)


# Run the app
if __name__ == "__main__":
    app()
