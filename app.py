import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('salaries.csv')



df = data.groupby('work_year')['salary_in_usd'].mean().reset_index()


st.title('Salary vs Year for ML Jobs')

st.write('### Salary Data', df)

fig, ax = plt.subplots()
ax.plot(df['work_year'], df['salary_in_usd'], marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Salary in USD')
ax.set_title('Salary vs Year for ML Jobs')

# Display the plot
st.pyplot(fig)


# print(df.info())