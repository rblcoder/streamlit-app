import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

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
    st.write(pd.DataFrame([selected_row]))
