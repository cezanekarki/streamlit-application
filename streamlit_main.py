import snowflake.connector
import streamlit
import pandas as pd
import requests
from urllib.error import URLError
streamlit.title('Healthy Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected= streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_food_data(food_choice_name):
   fruity_vice_response = requests.get('https://fruityvice.com/api/fruit/'+food_choice_name)

    # write your own comment -what does the next line do? 
   fruityvice_normalized = pd.json_normalize(fruity_vice_response.json())
   return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
   
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please enter fruit name to get its information')
  else:
   get_food = get_food_data(fruit_choice)
   # write your own comment - what does this do?
   streamlit.dataframe(get_food)
    
except URLError as e:
  streamlit.error()


streamlit.header('The fruit list contains:')

def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * from fruit_load_list")
      return my_cur.fetchall()
     
if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_row = get_fruit_load_list()
   streamlit.dataframe(my_data_row)
   
def insert_fruit_load_list(insert_value):
   with my_cnx.cursor() as my_cur:
      my_cur.execute(f"insert into fruit_load_list values({insert_value})")
      return 'Thanks for adding '+ insert_value
   
fruit_choice_insert = streamlit.text_input('Name a fruit to add:')
if streamlit.button('Insert Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_row = insert_fruit_load_list(fruit_choice_insert)
   streamlit.dataframe(my_data_row)

