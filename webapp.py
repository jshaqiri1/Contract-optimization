import streamlit as st
import pandas as pd
from itertools import permutations
from funcAlloc import get_permutations, get_values, get_sorted_pairs, final_message, optimized


# Define the Streamlit app
def app():
   
    st.title("Contract Value Optimization")
    st.caption('Juxhin Shaqiri')
    
    # Get the number of aggregate classes from the user
    num_aggregate_classes = st.number_input("Enter the number of Aggregate Classes (AC's) [max 10]:", value=5, step=1, max_value=10)

    # Get the names of the contractors from the user
    contractor_names = st.text_input("Enter the names of vendors that will receive awards separated by commas (e.g. Google, Apple, Miscrosoft):")
    contractor_names = [name.strip().upper() for name in contractor_names.split(',')]
   
    st.subheader(f'Enter how you would like to split the {num_aggregate_classes} ACs:' )

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
        best = optimized(pairs,num_aggregate_classes)
        itnum = len(my_permutations)
         
      # Add a download button to download the results as a CSV file
     df = pd.DataFrame(columns=['Vendor', 'Aggregate Class', 'Bid Amount', 'Cost', 'Optimal Allocation'])
     for i in range(num_aggregate_classes):
         for j, vendor in enumerate(contractor_names):
             df = df.append({'Vendor': vendor,
                             'Aggregate Class': f'Aggregate Class {i+1}',
                             'Bid Amount': bids[i][vendor],
                             'Cost': pairs[i*num_aggregate_classes+j][1],
                             'Optimal Allocation': best[j][i]}, ignore_index=True)

          

        #df = pd.DataFrame({'Vendor': allocation, 'Aggregate Class': [f'Aggregate Class {i+1}' for i in range(num_aggregate_classes)], 'Bid Amount': [bids[i][vendor] for i in range(num_aggregate_classes) for vendor in contractor_names], 'Cost': [pair[1] for pair in pairs], 'Optimal Allocation': best})
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="results.csv">Download Results as CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

        
        st.markdown('**Optimized Contract Allocation:**')
        st.text(best)
        st.markdown(f'**Below are all {itnum} unique combinations sorted by $:**')
        st.text(message)


# Run the app
if __name__ == "__main__":
    app()
