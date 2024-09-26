# importing Libraries

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
st.set_page_config(page_title="Covid_19 Dashboard",page_icon=None,layout="wide",initial_sidebar_state="auto",menu_items=None)
# Load Data
df1 = pd.read_csv("country_wise_latest.csv")
df2 = pd.read_csv("covid_19_clean_complete.csv")
df3 = pd.read_csv("day_wise.csv")
df4 = pd.read_csv("full_grouped.csv")
df5 = pd.read_csv("usa_county_wise.csv")
df6 = pd.read_csv("worldometer_data.csv")

# Sidebar
st.sidebar.header("Covid 19 Dashboard")
st.sidebar.image("covid.jpg")
st.sidebar.write("Coronavirus disease 2019 (COVID-19) is a contagious disease caused by the coronavirus SARS-CoV-2...")
st.sidebar.markdown("Made with:heart_eyes: By : Dr.Eng.[Marwa Elsherif](https://www.linkedin.com/in/dr-marwa-elsherif-1396a0113/)")

st.sidebar.write("")
st.sidebar.write("FilteryourData:")
# Sidebar filter
cat_filter = st.sidebar.selectbox("Categorical", ['Confirmed', 'Recovered', 'Deaths'])
cat_filter2=st.sidebar.selectbox("Categorical2", ['Confirmed', 'Deaths'])
# Displaying the selected category
#st.write(f"You selected: {cat_filter}")
#st.write(f"You selected: {cat_filter2}")
# Body - Row A
a1, a2, a3, a4 = st.columns(4)
a1.metric("Total Cases", df6['TotalCases'].sum())
a2.metric("Total Deaths", df6['TotalDeaths'].sum())
a3.metric("Total Recovered", df6['TotalRecovered'].sum())
a4.metric("Total Tests", df6['TotalTests'].sum())

# Row B - Top 10 Countries by Deaths
country_deaths = df4.groupby('Country/Region')['Deaths'].sum().sort_values(ascending=False).head(10)  # Top 10 countries
country_deaths_reset = country_deaths.reset_index()

colors = cm.viridis(np.linspace(0, 1, len(country_deaths_reset)))

# Plotting the Data
hh = plt.figure(figsize=(10, 6))
plt.bar(country_deaths_reset['Country/Region'], country_deaths_reset['Deaths'], color=colors)
plt.title('Top 10 Countries by Total Deaths')
plt.ylabel('Total Deaths')
plt.xlabel('Country/Region')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(hh)

import matplotlib.pyplot as plt

# Line plot of confirmed cases over time
data = {
    'Date': df3['Date'],
    'Confirmed': df3['Confirmed'],
    'Recovered': df3['Recovered'],
    'Deaths': df3['Deaths']
}
df = pd.DataFrame(data)

# Convert Date column to datetime if not already
df['Date'] = pd.to_datetime(df['Date'])

# Limiting the date range (e.g., show only the last 30 days)
df_limited = df.tail(30)  # Shows the last 30 days; change 30 to any other value if needed

# Creating the figure for the plot
# Line plot of confirmed cases over time with a custom color
ss = plt.figure(figsize=(10, 6))

# Use a custom color for the line (e.g., '#FF5733') and markers
plt.plot(df_limited['Date'], df_limited[cat_filter], marker='o', label=f'Last 30 Days {cat_filter} Cases', color='#FF5733')

# Customizing the x-axis ticks to show fewer dates
plt.xticks(rotation=45)

# Adding titles and labels with custom colors
plt.title(f'Daily {cat_filter} Cases Over Last 30 Days', color='#3357FF')  # Title in custom blue
plt.xlabel('Date', color='#3357FF')  # X-axis label in custom blue
plt.ylabel(f'{cat_filter} Cases', color='#3357FF')  # Y-axis label in custom blue

# Adding a legend with a custom background color
plt.legend(facecolor='#EAEAEA', edgecolor='#FF5733')  # Custom legend colors

# Adjust the layout and display the plot
plt.tight_layout()
plt.show()

# Display the plot in Streamlit
st.pyplot(ss)
#st.write("Unique values in Province_State:", df5['Province_State'].unique())
# Filter USA Data for States (remove 'USA' from Province_State if exists)
df5_filtered = df5[df5['Province_State'] != 'USA']  # Filter out 'USA' if present

# Scatter plot for USA Data (Confirmed Cases vs Deaths by State)
data2 = {
    'Province_State': df5_filtered['Province_State'],
    'Confirmed': df5_filtered['Confirmed'],
    'Deaths': df5_filtered['Deaths']
}
dfx = pd.DataFrame(data2)

# Sort the data by 'Confirmed' and limit to the top 30 states
df_limited2 = dfx.groupby('Province_State').sum().sort_values(by='Confirmed', ascending=False).head(30).reset_index()

# Scatter plot for Confirmed vs Deaths in the USA (Top 30 States)
st.subheader("Confirmed Cases vs. Deaths in USA (Top 30 States)")
# Scatter plot with categorical color sequence
fig = px.scatter(data_frame=df_limited2, 
                 x='Province_State', 
                 y=cat_filter2, 
                 color=cat_filter2, 
                 size=cat_filter2, 
                 hover_name='Province_State',
                 color_discrete_sequence=px.colors.qualitative.Set1)  # Custom color sequence for categorical data

st.plotly_chart(fig, use_container_width=True)

st.subheader( "Ratio of racovered cases world wide")

df_limited3 = df2.groupby('Country/Region').sum().sort_values(by='Recovered', ascending=False).head(10).reset_index()

# Create a pie chart using the limited DataFrame
fig = px.pie(data_frame=df_limited3, 
             names='Country/Region',  # Column for country names
             values='Recovered',      # Column for the pie chart values
             color='Country/Region')  # Optional: Color by country

# Display the pie chart in Streamlit
st.plotly_chart(fig, use_container_width=True)