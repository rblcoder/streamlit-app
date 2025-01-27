import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import requests

# Function to fetch data from the GraphQL endpoint
def fetch_data_from_graphql(query, endpoint):
    response = requests.post(endpoint, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}")


# Define a GraphQL query for the Countries API
graphql_query_country = """
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
graphql_url_country = "https://countries.trevorblades.com/"

# Fetch data
data = fetch_data_from_graphql(query=graphql_query_country, endpoint=graphql_url_country)

# Extract the countries data from the JSON response
countries_data = data['data']['countries']

# Create a pandas DataFrame from the countries data
df_countries = pd.DataFrame(countries_data)

# Print the DataFrame
print(df_countries)

st.title('Data from Countries GraphQL API')

st.write('### Countries Data', df_countries)


# Define the GraphQL endpoint for the Pokémon API
graphql_endpoint = "https://beta.pokeapi.co/graphql/v1beta"

# Define your GraphQL query to fetch data
query = """
{
  pokemon_v2_pokemon(limit: 10) {
    id
    name
    height
    weight
    base_experience
    pokemon_v2_pokemontypes {
      pokemon_v2_type {
        name
      }
    }
  }
}
"""


# Fetch data
data = fetch_data_from_graphql(query, graphql_endpoint)

print(data)

# Convert fetched data to pandas DataFrame
pokemon_list = []
for p in data['data']['pokemon_v2_pokemon']:
    for t in p['pokemon_v2_pokemontypes']:
        pokemon_list.append({
            "id": p["id"],
            "name": p["name"],
            "height": p["height"],
            "weight": p["weight"],
            "base_experience": p["base_experience"],
            "type": t["pokemon_v2_type"]["name"]
        })

pokemon_df = pd.DataFrame(pokemon_list)

# Print the DataFrame
print(pokemon_df)

st.title('Data from Pokemon GraphQL API')

st.write('### Pokemon Data', pokemon_df)




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