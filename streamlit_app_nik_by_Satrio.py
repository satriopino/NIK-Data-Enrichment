import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide')

# --- READ DATA ---
customer_merge = pd.read_pickle('customer_merge.pkl')
coord = pd.read_csv('coordinate.csv')

# --- ROW 1 ---
st.write('# Customers Demography Dashboard')
st.write('by **Muhammad Satrio Pinoto Negoro**')
st.write('**Linkedin**: https://www.linkedin.com/in/satriopino/')
st.write("""Welcome to the Customers Demography Dashboard – your comprehensive view of our customer base's
          demographics. This interactive dashboard provides valuable insights into the diverse 
         characteristics of our customers, allowing you to explore and understand the composition of our 
         audience.""")


# --- ROW 2 ---
st.write('### Customers Count across Indonesia')
## -- INPUT SELECT --
input_select_prof = st.selectbox(
    label='Select Prfession',
    options=customer_merge['Profession'].unique().sort_values()
)
## --- MAP PLOT ---
# data: map
cust_prof = customer_merge[customer_merge['Profession'] == input_select_prof]
prov_gender = pd.crosstab(index=cust_prof['province'],
                   columns=cust_prof['gender'],
                   colnames=[None])
prov_gender['Total'] = prov_gender['Female'] + prov_gender['Male']
df_map = prov_gender.merge(coord, on='province')

# plot: map
plot_map = px.scatter_mapbox(data_frame=df_map, lat='latitude', lon='longitude',
                             mapbox_style='carto-positron', zoom=3,
                             size='Total',
                             hover_name='province',
                             color_discrete_sequence=['green'],
                             hover_data={'Male': True,
                                         'Female': True,
                                         'latitude': False,
                                         'longitude': False})

st.plotly_chart(plot_map, use_container_width=True)

st.divider()

# --- ROW 3 ---
col1, col2 = st.columns(2)

col1.write('### Customer Count per Province')

## --- INPUT SLIDER --- Income
customer_merge['Annual_Income'] = customer_merge['Annual_Income'].astype('int64')
input_slider_income = col1.slider(
    label='Select Annual Income range',
    min_value=customer_merge['Annual_Income'].min(),
    max_value=customer_merge['Annual_Income'].max(),
    value=[30000000,100000000]
)

min_slider_income = input_slider_income[0]
max_slider_income = input_slider_income[1]

## Barplot Customer Count per Province
### Data Customer Count per Province
cust_income = customer_merge[customer_merge['Annual_Income'].between(left=min_slider_income, right=max_slider_income)]
customer_per_province = pd.crosstab(index=cust_income['province'],
                   columns='Total Customers',
                   colnames=[None]).sort_values(by='Total Customers')

### plot Customer Count per Province
customer_per_province_plot = px.bar(customer_per_province.reset_index().tail(10), x='Total Customers', y='province', 
            labels={'index': 'Province', 'province': 'Province'},
             color_discrete_sequence=['green'])

col1.plotly_chart(customer_per_province_plot, use_container_width=True)


col2.write('### Customer Gender per Profession')
## --- INPUT SLIDER --- Age
input_slider_age = col2.slider(
    label='Select age range',
    min_value=customer_merge['age'].min(),
    max_value=customer_merge['age'].max(),
    value=[20,50]
)

min_slider_age = input_slider_age[0]
max_slider_age = input_slider_age[1]


## Barplot Customer Gender per Profession
### Data Customer Gender per Profession
customer_age = customer_merge[customer_merge['age'].between(left=min_slider_age, right=max_slider_age)]

### plot Customer Gender per Profession

customer_gender_prof_plot = px.bar(customer_age.groupby(['Profession', 'gender']).size().reset_index(name='count').sort_values(by='count'),
             x='count', y='Profession', color='gender', barmode='group',
             labels={'count': 'Customer Count'},
             category_orders={'gender': ['Male', 'Female']},
             color_discrete_map={'Male': 'green', 'Female': 'lightgreen'})

col2.plotly_chart(customer_gender_prof_plot, use_container_width=True)

st.divider()

# --- ROW 4 ---

col3, col4 = st.columns(2)

col3.write('### Spending Score per Province')
## --- INPUT SELECT --- Gender
input_select_gender = col3.selectbox(
    label='Select Gender',
    options=customer_merge['gender'].unique().sort_values()
)

## Barplot Spending Score per Province
### Data Spending Score per Province
cust_gender = customer_merge[customer_merge['gender'] == input_select_gender]
average_spending_per_generation = cust_gender.groupby('province')['Spending_Score'].mean().sort_values().reset_index().tail(10)

### plot Spending Score per Province
spending_per_province_plot = px.bar(average_spending_per_generation, 
                                    x='Spending_Score', 
                                    y='province',
                                    color_discrete_sequence=['green'])

spending_per_province_plot.update_layout(
    xaxis_title='Average Spending Score',
    yaxis_title='Province')

col3.plotly_chart(spending_per_province_plot, use_container_width=True)

col4.write('### Customer Count per Generation')
### plot Customer Count per Generation
customer_per_generation_plot = px.bar(customer_merge['generation'].value_counts().reset_index().sort_values(by='count'),
                                      x='count', 
                                      y='generation', 
                                      labels={'index': 'Generation', 'generation': 'Customer Count'}, 
                                      color_discrete_sequence=['green'])
customer_per_generation_plot.update_layout(
    yaxis_title='Generation',
    xaxis_title='Customer Count')

col4.plotly_chart(customer_per_generation_plot, use_container_width=True)