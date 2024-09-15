import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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