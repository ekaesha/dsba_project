import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
sns.set_theme()
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


data = pd.read_csv('ds_salaries.csv')


st.markdown("""The remaining dateset called 'Data Science Job Salaries' includes the data on the salaries of jobs in the Data Science domain. Next, an analysis of the columns and rows of this dataset can be found and graphs containing all the relevant information will be presented.""")

st.title('DS overview')

st.markdown("""Let's start with a general overview. Let's see what the dataset is and what information it contains.""")


data.head(10)


st.write("Rows & Columns")
st.write(data.shape)


st.markdown("""In total, this dataset has 607 rows and 12 columns. Let's figure out what each line is responsible for and whether its values are unique.""")

data.describe()


fig = px.imshow(data.corr(), text_auto=True)
fig.show()


st.write('Оutput the data in the format:')
st.write('type', '&', 'unique el', '&', 'col name')
for col in data:
 st.write(data[col].dtypes, '-', len(data[col].unique()), '-', col)


st.markdown("""You can see that each row contains unique values. Let's check the presence of zeros in each row.""")


data.isnull().sum()


st.title('DS Cleanup')

st.markdown("""Note that there are some columns, such as 'salary', 'salary_currency' and 'Unnamed: 0'. Since the column 'Unnamed: 0' has no value and does not carry any useful information, and columns 'salary' and 'salary_currency' can be easily replaced, having a column 'salary_in_usd', it is possible to remove those columns.""")


data.drop(data[['salary','salary_currency','Unnamed: 0']],axis=1, inplace=True)


st.markdown("""Let's display the number of columns and the straw and see that in the process of clearing the dataset, the number of columns decreased by three.""")



st.write("Rows & Columns")
st.write(data.shape)
data.head(5)


st.markdown("""Let us consider in more detail what each column and row are responsible for and what parameters they have.""")


st.write(f"Based on the data obtained above 'work_year' has 3 unique values. Consider them")
data.work_year.unique()


st.write("Let's look and find out also specific values 'employment_type' 'remote_ratio.unique', 'experience_year'")
st.write('', *data.remote_ratio.unique(), '\n',*data.employment_type.unique(), '\n', *data.experience_level.unique(), '\n', *data.company_size.unique())

st.markdown("""Let's describe what each parameter means.

1. work_year: the year the salary was paid ( type: int64, unique_el: 3 )
parametrs: year[2020, 2021, 2022]

2. experience_level: the experience level in the job during the year with the following possible values ( type: object, unique_el: 4 )
parametrs:
MI - Mid-level
SE - Senior-level
EN - Entry-level
EX - Executive-level

3. employment_type: the type of employement for the role ( type: object, unique_el: 4 )
parametrs:
FT - Full-time
CT - Contract
PT - Part-time
FL - Freelance

4. job_title: job name ( type: object, unique_el: 4 )

5. salaryinusd: salary level ( type: int64, unique_el: 369 )

6. employee_residence: the country where the workers live ( type: object, unique_el: 57 )

7. remote_ratio: amount of work done remotely ( type: int64, unique_el: 3 )
0 - work was not done remotely
50 - 50 units of work completed remotely
100 - 100 units of work completed remotely

8. company_location: country where the company is located ( type: object, unique_el: 50 ) 

9. company_size: the average number of people that worked for the company during the year ( type: object, unique_el: 3 )
paramets:
L - Large enterprise
S - Small business
M - Mid-market enterprise""")


st.title('Statistics')

st.markdown("""In the following lines mean, median and standard deviation on statistics on salary are presented.""")


st.write('Mean total salaries (in $):',data['salary_in_usd'].mean())
st.write('Median total salaries (in $):',data['salary_in_usd'].median())
st.write("Standard Deviation of the salary is % s "%(statistics.stdev(data['salary_in_usd'])))


st.title('Data Transformation')

st.markdown("""One of the most important sets of information is the salary level. Thus, one more column can be added to this dataset, generalizing and characterizing the index, which is responsible for the amount of money received for the work.""")
# 

st.markdown("""To implement this, we will first calculate the mean of the salary and print it.""")


med_salary = data['salary_in_usd'].mean()
st.write(med_salary)


st.markdown("""To make dataset more convinient to look at, let's add the column called 'salary_ratio'.""")


data = data.assign(salary_ratio = data.salary_in_usd / med_salary)
st.write(data)

data = data.assign(salary_level = 'a')
st.write(data)


st.markdown("""Then, it is logically to add a column with the level of salary. If the index of 'salary_ratio' is lower than 0.75, then the value of 'salary level' will take on the meaning 'low', if higher than 0,75 and less than 1.25 - 'medium', if higher than 1.25 - 'high'.""")

data.loc[(data['salary_ratio'] < 0.75), 'salary_level'] = 'low'
data.loc[(data['salary_ratio'] >= 0.75) & (data['salary_ratio'] <= 1.25), 'salary_level'] = 'medium'
data.loc[(data['salary_ratio'] > 1.25), 'salary_level'] = 'high'
st.write(data)


st.markdown("""Now, we have obtained our dataset, so it has two new columns. Let's make a hypothesis: the 'high' salary has increased over the period from 2020 to 2022.""")


fig=px.histogram(data_frame=data,
                 x="work_year",
                 color_discrete_sequence=px.colors.sequential.Magma_r,
                 template="plotly_white",
                 title="The Level of Salary",
                 color="salary_level",
                 barmode="group",
                 histnorm="percent",
                 text_auto=".2f")

fig.update_layout(yaxis_title="Amount of employees",
                  xaxis_title="Work Year",
                  xaxis={"categoryorder":"total descending"})
st.plotly_chart(fig)


st.markdown("""Based on this histogram, we can conclude that the hypothesis is correct. Indeed, the level of salaries has become significantly higher two years after 2020.""")

st.title('Vizual analysis')

st.markdown("""Let's delve into the study of the dataset. Let's create a few simple graphs that summarize the data in the dataset.""")

st.markdown("""Let's start with an analysis of the most popular jobs. There is Top 10 of the most relevant jobs pie chart.""")

sum_counts = data['job_title'].value_counts()[:10]
fig = go.Figure()
pull = [0]*len(sum_counts)
pull[sum_counts.tolist().index(sum_counts.max())] = 0
fig.add_trace(go.Pie(values=sum_counts, labels=sum_counts.index, pull=pull, hole=0.9))

fig.update_layout(
    margin=dict(l=0, r=0, t=30, b=0),
    legend_orientation="h",
    annotations=[dict(text='Top 10 Job Titles', x=0.5, y=0.5, font_size=20, showarrow=False)])
st.plotly_chart(fig)


st.markdown("""Having considered the number of employees who have chosen one or another job, we note that 4 of the jobs: 'Data Scientist', 'Data Engineer', 'Data Analyst' and 'Machine Learning Engineer' - stand out from the rest and occupy a leading position.""")

st.markdown("""Let's also consider two more graphs. The first one shows information about the amount of professionals working annually and the level of their experience. The second one demonstrates the distribution of salary among the number of workers in USD$.""")

exp_lvl = data['experience_level'].value_counts()[:50]
fig = px.bar(y=exp_lvl.values, 
             x=exp_lvl.index, 
             color = exp_lvl.index,
             color_discrete_sequence=px.colors.sequential.Magma_r,
             text=exp_lvl.values,
             title= 'Professionals on each lecel',
             template= 'plotly_white')

fig.update_layout(
    xaxis_title="Experience Level",
    yaxis_title="Amount of Professionals ",
    font = dict(size=17,family="Franklin Gothic"))
st.plotly_chart(fig)


fig=px.histogram(data_frame=data,
                 x="salary_in_usd",
                 color_discrete_sequence=px.colors.sequential.Viridis_r,
                 template="plotly_white",
                 title="Distribution of Salary in USD $")

fig.update_layout(yaxis_title="Count",
                  xaxis_title="Salary in USD",
                  xaxis={"categoryorder":"total descending"})
st.plotly_chart(fig)

st.markdown("""Due to the following graph we can obtain, that the vast majority of workers get 100k as a salary. It can be concluded that increasing your income in half is a challenging task.""")
st.markdown("""The number of work places, the size of companies and level of experience can influence a lot on the level of salary. There is the analysis of the number of different levels of companies, in which data scientists may work and the statistics on the number of companies located in different countries.""")

fig=px.histogram(data_frame=data,
                 x="company_size",
                 color_discrete_sequence=px.colors.sequential.Viridis_r,
                 template="plotly_white",
                 title="Company Size")

fig.update_layout(yaxis_title="Amount of Companies",
                  xaxis_title="Company Size",
                  xaxis={"categoryorder":"total descending"})
st.plotly_chart(fig)

st.markdown("""It can be clearly seen from the graph, that the Mid-market companies are leading among other tepes of companies, due to having the average number of employees - 50-200 workers - in comparison with large and small companies.""")

fig = px.histogram(data,
                   x='company_location',
                   color_discrete_sequence=px.colors.sequential.Viridis_r,
                   template="plotly_white",
                   title="Company Location")
st.plotly_chart(fig)

st.markdown("""From this, it can be obtained that the highest amount of companies is located in US. So, the better chance to get a job in data science field - move to the USA, the country with the most succesfull IT-companies and a lot of employability prospects.""")
st.title('Detailed Overview')
st.markdown("""Hypothesis: do programmers improve their skills every year?""")

fig=px.histogram(data_frame=data,
                 x="experience_level",
                 color_discrete_sequence=px.colors.sequential.Magma_r,
                 template="plotly_white",
                 title="Distribution of Experience Level/Employment Type %",
                 color="work_year",
                 barmode="group",
                 histnorm="percent",
                 text_auto=".2f")

fig.update_layout(yaxis_title="Amount of employees",
                  xaxis_title="Experience Level",
                  xaxis={"categoryorder":"total descending"})
st.plotly_chart(fig)

st.markdown("""According to this graph, we see that this hypothesis was confirmed. We can draw this conclusion from the fact that, the amount of Senior-level programmers has boosted, while the number of Mid-level и Entry-level programmers has diminished.""")
st.markdown("""Hypothesis: will the level of salary increase in case of transition of an employee to remote work?""")

fig=px.histogram(data_frame=data,
                 x="salary_in_usd",
                 color_discrete_sequence=px.colors.sequential.Magma_r,
                 template="plotly_white",
                 title="Level of Salaries According to Remote Ratio",
                 color="remote_ratio",
                 barmode="group",
                 histnorm="percent",
                 text_auto=".2f")

fig.update_layout(yaxis_title="Amount of Employees",
                  xaxis_title="Salary in USD",
                  xaxis={"categoryorder":"total descending"})
st.plotly_chart(fig)

st.markdown("""As it can be seen from the graph - definitely, yes. It can be obtained, while the level of salaries is increasing, the amount of numbers of hours, spent on remote work is also increasing.""")
st.markdown("""To understand deeper, how the amount of remote working hours corresponds withe the level of incomes, the statistics can be interpreted as a correlation between these two indices.""")

fig = px.scatter(data[(data['remote_ratio']>10)&(data['salary_in_usd']/(10**9)<300)], 
x='remote_ratio', 
y='salary_in_usd', 
trendline="ols",
title='Correlation between Remote Ratio and Salary in USD')
st.plotly_chart(fig)
st.markdown("""It is clear that the positive correlation shows, that the later hypothesis is true.""")
