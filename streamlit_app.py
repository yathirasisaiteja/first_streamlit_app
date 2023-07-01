import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale , Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

streamlit.header('🍌🥭 list of fruites aviliable 🥝🍇')
my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')

# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

my_fruit_list = my_fruit_list.set_index('Fruit')
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Apple'])
#streamlit.text(fruits_selected)

streamlit.dataframe(my_fruit_list)

streamlit.header('🍌🥭 list of fruites selected 🥝🍇')
fruits_to_show = my_fruit_list.loc[fruits_selected]
#streamlit.text(len(fruits_to_show))
streamlit.dataframe(fruits_to_show)

streamlit.header("🥝 Fruityvice Fruit Advice! 🥝")

for x in fruits_selected:
 streamlit.text(x)
 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+x)
 streamlit.text(fruityvice_response.json())
 fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
 fruityvice_normalized = fruityvice_normalized.set_index('name')
 streamlit.dataframe(fruityvice_normalized)

streamlit.header("🍇 Fruityvice Fruit Advice!  🍇")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
streamlit.text(fruityvice_response.json())
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
fruityvice_normalized = fruityvice_normalized.set_index('name')
streamlit.dataframe(fruityvice_normalized)

#snow connector usage
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

fruit_choice = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', fruit_choice)






