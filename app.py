import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import requests

def fetch_data_from_graphql_api(query, url):
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        url,
        json={'query': query},
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

# Define your GraphQL query for the Countries API
graphql_query = """
{
  countries {
    name
    code
    capital
    currency
    emoji
  }
}
"""

# URL of the Countries GraphQL endpoint
graphql_url = "https://countries.trevorblades.com/"

# Fetch data
data = fetch_data_from_graphql_api(graphql_query, graphql_url)

# Extract the countries data from the JSON response
countries_data = data['data']['countries']

# Create a pandas DataFrame from the countries data
df_countries = pd.DataFrame(countries_data)

# Print the DataFrame
print(df_countries)

st.title('Data from Countries GraphQL API')

st.write('### Countries Data', df_countries)

data = pd.read_csv('salaries.csv')



# df = data.groupby('work_year')['salary_in_usd'].mean().reset_index()

df = data.groupby('work_year').agg({'work_year' : 'size', 'salary_in_usd' : 'mean'}) \
.rename(columns={'work_year':'count','salary_in_usd':'mean_salary_in_usd'}) \
       .reset_index()

print(df)

st.title('Salary vs Year for ML Jobs')

st.write('### Salary and Job Data', df)

fig, ax = plt.subplots()
ax.plot(df['work_year'], df['mean_salary_in_usd'], marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Salary in USD')
ax.set_title('Salary vs Year for ML Jobs')

# Display the plot
st.pyplot(fig)


fig, ax = plt.subplots()
ax.plot(df['work_year'], df['count'], marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Count of Jobs')
ax.set_title('Count of Jobs vs Year for ML Jobs')

# Display the plot
st.pyplot(fig)


# print(df.info())
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection('single', use_checkbox=True)
grid_options = gb.build()

grid_response = AgGrid(
       df,
       gridOptions=grid_options,
       update_mode=GridUpdateMode.SELECTION_CHANGED,
       height=200,
       width='100%',
)

selected_rows = grid_response['selected_rows']
if selected_rows is not None:

    print(selected_rows)
    selected_row = selected_rows['work_year']
    st.write("Details of Selected Row")
#     st.write(pd.DataFrame([selected_row]))
#     st.write(pd.DataFrame([selected_row]).iloc[0,0])
#     value = str(pd.DataFrame([selected_row]).iloc[0,0])
#     st.write(value)
    value = pd.DataFrame([selected_row]).iloc[0,0]
    filtered_data = data.loc[data['work_year'] == value]
    st.write(filtered_data['job_title'].value_counts())