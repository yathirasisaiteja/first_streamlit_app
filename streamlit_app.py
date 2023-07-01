import streamlit
import pandas
import requests

import snowflake.connector
from urllib.error import URLError


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

def get_fruityvice_data(this_fruit_choice):
 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
 streamlit.text(fruityvice_response.json())
 fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
 return fruityvice_normalized
 

for x in fruits_selected:
 streamlit.text(x)
 try:
  fruityvice_normalized = get_fruityvice_data(x)
  try:
   fruityvice_normalized = fruityvice_normalized.set_index('name')
   streamlit.dataframe(fruityvice_normalized)
  except:
   streamlit.text('fruit '+x+' not present at the server')
 except URLError as e:
  streamlit.error()

streamlit.header("🍇 Fruityvice Fruit Advice!  🍇")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)
if not fruit_choice:
 streamlit.error("Please select a fruit to get information")
else:
 fruityvice_normalized = get_fruityvice_data(fruit_choice)
 try:
  fruityvice_normalized = fruityvice_normalized.set_index('name')
  streamlit.dataframe(fruityvice_normalized)
 except:
  streamlit.text('fruit '+x+' not present at the server')


#snow connector usage
streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
 with my_cnx.cursor() as my_cur:
  my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
  return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_row = get_fruit_load_list()
 streamlit.dataframe(my_data_row)

# don't run anything past here while we troubleshoot 
#streamlit.stop()

def insetr_row_snowflake(new_fruit):
 with my_cnx.cursor() as my_cur:
  my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ("+new_fruit+") ")
  return "thanks for adding "+new_fruit


fruit_choice = streamlit.text_input('What fruit would you like to add?')
if not fruit_choice:
 streamlit.error("Please add fruit which need to be inserted")
else:
 if streamlit.button('add the fruit'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insetr_row_snowflake(fruit_choice)
  streamlit.text(back_from_function)
  streamlit.write('Thanks for adding ', fruit_choice)
#my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit') ")





