import streamlit as st
#from streamlit import session_state
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import bcrypt
import base64

st.set_page_config(
        page_title="IoT Power Saver",
        page_icon="💡",
    )
# Initialize st.session_state if it doesn't exist
if "authentication_status" not in st.session_state:
    st.session_state.authentication_status = None
#st.rerun()

# -- USER AUTHENTICATION --

credentials = {
        "usernames":{
            "Bhav":{
                "name":"Bhavadev",
                "password":"$2b$12$C7Na1nAvLrCZPmvb8lT9s.4s6dF3wHV50p9xBH8UEUjSzjsOsM4nW"
                },
            "Such":{
                "name":"Suchir",
                "password":"$2b$12$j13TEhBOAVjjsu9L5lSDv.YwKsIz07okKxEEXA6EV7twmVcK9KZeC"
                }            
            }
        }
#Authentication Object
authenticator = stauth.Authenticate(credentials, "IoT_Power_Saver","auth", cookie_expiry_days=30)

print("authentication_status before login:", st.session_state.authentication_status)
name, authentication_status, username = authenticator.login("main", fields ={'Form  name': 'Login'})
print("authentication_status after login:", st.session_state.authentication_status)

if authentication_status is True:
    #Text part in the app
    st.write("# Welcome to The Power Saver! 💡")

    file_ = open("smart-home-app.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
    )
    st.write("The future of Smart Home Savings!")
    st.write("----------")
    st.subheader("App features: ")
    st.markdown(
    """
    - Hourly Consumption Chart
    - Cost Calculator
    """    
    )
    st.write("----------")
    # Create the SQL connection as specified in your secrets file.
    conn = st.connection("mysql", type='sql')
    # Perform query.
    df = conn.query('SELECT * from mytable;', ttl = 600)

    df['Time'] = df['Time'].astype(str)

    # Query and display the data you inserted
    st.header("🖥️ Your Devices")
    st.dataframe(df)

    st.markdown(
            """
            
        # 💸 Price Calculator 
        - We calculate the prices per KWh of usage and display the price in the country's local currency
        """
        )

    #Displaying Cost Data.
    df_2 = conn.query('SELECT * FROM electricity_cost;', ttl = 600)
    st.dataframe(df_2)

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")

    st.markdown(
        """

        My GitHub 😊 [Aaryan's GitHuB](https://github.com/AaryanTheLaughingGas)
"""
    )
else:
    if authentication_status is False:
        st.error("Username/ password is incorrect")
    else:
        st.warning("Please enter your Username and password to proceed")
