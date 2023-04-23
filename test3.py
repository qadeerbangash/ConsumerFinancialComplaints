import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data from CSV

def load_data():
    df = pd.read_csv("client_complaints.csv")
    return df

# Get list of all available states

def get_states(df):
    return sorted(df["state"].unique())

# Main function to display the dashboard
def main():
    # Load data
    df = load_data()

    # # Get list of all available states
    # state = get_states(df)


    # Set the title of the dashboard
    st.title('Consumer Financial Complaints Dashboard')

    # Add some text
    st.subheader('Display Data for “All States” or “Colorado” State (Based on Filter Selected)')

    # Display the data as a table
    st.write(df)









    col1, col2, col3, col4= st.columns(4)

    # Add a drop-down widget to select state
    selected_state =st.sidebar.selectbox("Select a State", sorted(df["state"].unique()))

    # Filter data based on selected state
    filtered_data = df[df["state"] == selected_state]
    # state_filter = st.sidebar.selectbox("Select a State", sorted(df["state"].unique()))


    # Display charts and KPIs based on filtered data
    # st.subheader("Total Number of Complaints")
    col1.metric(label="Total Complaints", value=filtered_data["Complaint_ID"].nunique())

    # st.subheader("Total Number of Closed Complaints")
    closed_data = filtered_data[filtered_data["company_response"].str.contains("Closed")]
    col2.metric(label="Total Closed Complaints", value=closed_data["Complaint_ID"].nunique())

    # st.subheader("% of Timely Responded Complaints")
    timely_data = filtered_data[filtered_data["timely"] == "Yes"]
    percentage = round((timely_data["Complaint_ID"].nunique() / filtered_data["Complaint_ID"].nunique()) * 100, 2)
    col3.metric(label="% Timely Response", value=percentage)

    # st.subheader("Total Number of Complaints with In Progress Status")
    in_progress_data = filtered_data[filtered_data["company_response"] == "In progress"]
    col4.metric(label="In Progress Complaints", value=in_progress_data["complaint_id"].nunique())

    st.subheader("Horizontal Bar Plot of Number of Complaints by Product")
    products = filtered_data.groupby("product").size()
    st.bar_chart(products)

    st.subheader("Line Chart of Number of Complaints Over Time (Month Year)")
    filtered_data["Date received"] = pd.to_datetime(filtered_data["date_received"])
    time_data = filtered_data.groupby(pd.Grouper(key="Date received", freq="M")).size().reset_index(name="Count")
    st.line_chart(time_data.set_index("Date received"))



    

    if selected_state != "All States":
        df = df[df["state"] == selected_state]


    #Pie Chart
    st.subheader("Pie Chart of Number of Complaints by Submitted Via Channel")
    pie_chart_data = df.groupby("submitted_via").agg({"Complaint_ID": "count"}).reset_index()
    fig = px.pie(pie_chart_data, values="Complaint_ID", names="submitted_via")
    st.plotly_chart(fig, use_container_width=True)



    # Tree Map
    treemap_data = df.groupby(["issue", "sub_issue"]).agg({"Complaint_ID": "count"}).reset_index()
    fig = go.Figure(go.Treemap(
    labels=treemap_data["issue"] + " - " + treemap_data["sub_issue"],
    parents=["" for _ in range(len(treemap_data))],
    values=treemap_data["Complaint_ID"]
    ))
    fig.update_layout(margin=dict(t=20, l=0, r=0, b=0))

    st.subheader("Treemap of Number Over Complaints by Issue and Sub-Issue")

    st.plotly_chart(fig, use_container_width=True)

    # Footer
    st.write("Designed by QADEER HUSSAIN")
    





# Run the app
if __name__ == "__main__":
    main()
