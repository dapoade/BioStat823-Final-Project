import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


st.markdown(""" # Covid-19 Dashboard """ )

st.markdown(""" ### Covid Deaths, Hospitalizations, and ICU admittances by Month""")
covid = pd.read_csv('./covidv2.csv')

covid.replace({'icu_yn': {'Yes': 1,'No': 0}}, inplace = True)
covid.replace({'hosp_yn': {'Yes': 1,'No': 0}}, inplace = True)


#Line Chart of Deaths over time
death_month = covid.groupby(['case_month'])['death_yn', 'hosp_yn', 'icu_yn'].sum().reset_index()
death_month.columns = ['Month', 'Deaths', 'Hospitalizations', "ICU"]
death_month.set_index('Month', inplace = True)

st.line_chart(death_month)


st.markdown('## Percentage of Deaths by Race')

covid1 = covid.query('death_yn == 1' )
kpi1, kpi2, kpi3 = st.columns(3)

white_death_perc = covid1.race.value_counts()[0] / (covid1.race.value_counts()[0] + covid1.race.value_counts()[1] + covid1.race.value_counts()[2] + covid1.race.value_counts()[3] )
white_death_perc = white_death_perc * 100

black_death_perc = covid1.race.value_counts()[1] / (covid1.race.value_counts()[0] + covid1.race.value_counts()[1] + covid1.race.value_counts()[2] + covid1.race.value_counts()[3] )
black_death_perc = black_death_perc * 100

asian_death_perc = covid1.race.value_counts()[2] / (covid1.race.value_counts()[0] + covid1.race.value_counts()[1] + covid1.race.value_counts()[2] + covid1.race.value_counts()[3] )
asian_death_perc = asian_death_perc *100

kpi1.metric(label = 'Percentage of Covid Deaths that are White People',
            value = '%.2f' %white_death_perc + ' %')

kpi2.metric(label = 'Percentage of Covid Deaths that are Black People',
            value = '%.2f' %black_death_perc + ' %')

kpi3.metric(label = 'Percentage of Covid Deaths that are Asian People',
            value = '%.2f' %asian_death_perc + ' %')




st.markdown('## Number of Deaths by Month and State')
months = list(covid['case_month'].unique())
months = sorted(months)
states = list(covid.res_state.unique())

selected_months = st.multiselect("Month(s):", months)

all_months = st.checkbox("Select all months")
if all_months:
    selected_months = months


selected_states = st.multiselect("State(s):", states)
all_states = st.checkbox("Select all States")
if all_states:
    selected_states = states


covid1 = covid1.query('res_state == (@selected_states) & case_month == (@selected_months)')

fig = px.bar(covid1, x='res_state', y='death_yn', title= "Covid Deaths by State and Year",
    labels={
    "death_yn": "Number of Deaths",
    "res_state": "State"} )
fig.update_traces(marker_color='Dark Red')
st.plotly_chart(fig, use_container_width = True)
# st.bar_chart(data = covid1['res_state', 'death_yn'])
