import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title ('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
streamlit.text ('what is cookin? ')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruites_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruites_to_show=my_fruit_list.loc[fruites_selected]

# Display the table on the page.
streamlit.dataframe(fruites_to_show)

streamlit.header("Fruityvice Fruit Advice!")
#try:
#    fruit_choice = streamlit.text_input('What fruit would you like information about?')
#    if not fruit_choice:
#        streamlit.error ("please select a fruit to get information.")
#    else :
#        streamlit.write('The user entered ', fruit_choice)
#        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#        # streamlit.text(fruityvice_response.json())
#        
#        # Use pandas to normalize the json
#       fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#       # display the data frame
#       streamlit.dataframe(fruityvice_normalized)
# create the repetable code block ( called a function)
def get_fruityvice_data(this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized
#New section to display fruityvice api response
streamlit.header('FruityVice Fruite Advice!')
try:
    fruit_choice=streamlit.text_input('What fruite would you like information about?')
    if not fruit_choice:
            streamlit.error("Please select a fruit to get information")
    else:
        back_from_function=get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()

#streamlit.stop()

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
#my_data_rows = my_cur.fetchall()
#streamlit.header("The Fruit Load list Contains :")
#streamlit.dataframe(my_data_rows)

streamlit.header("This fruit load list contains")
#Snowflake-relates functions
def get_fruit_load_list():
        with  my_cnx.cursor() as my_cur:
                my_cur.execute("SELECT * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
                return my_cur.fetchall()
# Add a button to load the fruit
if streamlit.button('Get fruit load list'):
        my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
        my_data_rows=get_fruit_load_list()
        my_cnx.close()
        strealit.dataframe(my_data_rows)
                
#Allow end user to add fruit to list
def insert_row_snowflake(new_fruit):
        with my_cnx.cursor() as my_cur:
                my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('"+new_fruit+"')")
                return "Thanks for adding" + new_fruit
add_my_fruit = streamlit.text_input('View our fruit list - add your favorites!')
if streamlit.button('get fruit list'):
        my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
        back_from_function=insert_row_snowflake(add_my_fruit)
        streamlit.text(back_from_function)
                
streamlit.stop()
# Allow user to add a fruit to the list
#add_my_fruit = streamlit.text_input('What fruit would you like to add?','manga')
#my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('"+add_my_fruit+"')")
#streamlit.write('thank you for adding ', add_my_fruit)
#my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('From Streamlit')")


