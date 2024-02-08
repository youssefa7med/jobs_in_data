import streamlit as st 
import pandas as pd 
import numpy  as np 
import plotly.express as px


st.title("Streamlit App about Jobs in Data")
st.image('https://datasciencedojo.com/wp-content/uploads/data-analyst-job-scaled.jpg')
st.divider()

# Load the dataset  
df = pd.read_csv('jobs_in_data.csv')
df.drop_duplicates(inplace=True)

num_cols = df.select_dtypes(include='number').columns
cat_cols = df.select_dtypes(include='O').columns

st.sidebar.header("User Input Features")

selected_col = st.sidebar.selectbox("Select Column", ['Univariate','Bivariate', 'Multivariate'])

if  selected_col == "Univariate":

    num_col= st.radio('Select a numerical column to filter by:', num_cols)
    fig1 = px.histogram(df,x=num_col,template='simple_white',title= f'Histogram of {num_col}')
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    cat_col1 = st.selectbox('Select one category column to filter by:', cat_cols )
    ws = df[cat_col1].value_counts().reset_index()
    fig2 = px.bar(ws,x='index',y=cat_col1,text_auto=True,color = 'index',template='presentation',title=f'Number of {cat_col1}')
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()


    cat_col2 = st.radio('Select one category column to filter by:', ['company_location','company_size'] )
    fig3 = px.pie(df[cat_col2].value_counts().nlargest(10).reset_index(),names='index',values=cat_col2,hole=0.45,template='presentation',title = f'Pie of {cat_col2}')
    st.plotly_chart(fig3)

    st.divider()

    st.write('For that reason we will work with only United States')
    fig3 = px.pie(df['company_location'].value_counts().nlargest(10).reset_index(),names='index',values='company_location',color_discrete_sequence=px.colors.sequential.BuGn_r,template='presentation',title = 'Pie of company_location')
    st.plotly_chart(fig3)

us = df[df['company_location']=='United States']
columns = us.columns
    
if selected_col == "Bivariate":
    col1 = st.selectbox('Select column for bivariate analysis it with salary in usd :',['company_size','experience_level','employment_type','job_category','work_year'] )
    if col1 != 'work_year':
        fig4 = px.bar(us.groupby(col1)['salary_in_usd'].mean().reset_index().round(2),text_auto=True,template='simple_white',title=f'Salary per {col1} ',x=col1,y='salary_in_usd',color=col1)
        st.plotly_chart(fig4)
    else:
        fig4 = px.line(us.groupby('work_year')['salary_in_usd'].mean().reset_index().round(2),x='work_year',y='salary_in_usd',markers=True ,template='presentation',title='Salary about all jobs in USA per year')
        st.plotly_chart(fig4)

        st.divider()

    year = st.radio('Select year does you want to visualize it :',[2020,2021,2022,2023])
    st.write('This is a barplot about salary for each category per the year of {}'.format(year))
    year_sal = us.groupby(['work_year','job_category'])['salary_in_usd'].mean()
    fig5 = px.bar(year_sal.get(year).reset_index(),x='job_category',text_auto=True,y='salary_in_usd',color='job_category',template='simple_white',title=f'Year of {year}')
    st.plotly_chart(fig5)

    

if selected_col == "Multivariate":

    year = st.radio('Select year does you want to visualize it:',[2020,2021,2022,2023])
    st.write('This is a barplot about work setting for each experience level per the year of {}'.format(year))
    exp_work = us.groupby(['work_year','experience_level','work_setting'])['job_title'].count()
    fig6 = px.bar(exp_work.get(year).reset_index(),x='experience_level',y='job_title',color='work_setting',barmode='group',template='presentation',text_auto=True)
    st.plotly_chart(fig6)




