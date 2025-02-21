import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from streamlit_extras.dataframe_explorer import dataframe_explorer
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt
import time

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
        return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
        if make_hashes(password) == hashed_text:
                return hashed_text
        return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
        c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
        c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
        conn.commit()

def login_user(username,password):
        c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
        data = c.fetchall()
        return data


def view_all_users():
        c.execute('SELECT * FROM userstable')
        data = c.fetchall()
        return data

def test():

        st.subheader("Predicts your data in an accurate manner")

        with st.container():
                st.write("---")
                selected = option_menu(
                        menu_title=None,
                        options=["Home", "Crime Rate Analysis", "Prediction"],
                        icons=["house", "award-fill", "calendar"],
                        menu_icon="cast",
                        default_index=0,
                        orientation="horizontal",
                )
                st.subheader('Upload the dataset either in excel/csv format:')
                uploaded_file = st.file_uploader(" ", type=['csv', 'xlsx'])

                if uploaded_file:
                        st.markdown('---')
                        try:
                                df = pd.read_csv(uploaded_file)  # Assuming it's a CSV
                        except pd.errors.ParserError:
                                df = pd.read_excel(uploaded_file) # Or it could be an Excel file

                        if selected == "Home":
                                
                                st.subheader('Process of predicting the crime rate')
                                st.image("img2.jpg")
                                st.write(
                                        "Crime analysis and prediction is a systematic approach for identifying the crime."
                                        " This system can predict regions which have high probability for crime occurrences and visualize crime "
                                        "prone areas."
                                        " Using the concept of data mining we can extract previously unknown, useful information from an "
                                        "unstructured data."
                                        " We propose a system which can analyze, detect, and predict various crime probability in a given region."
                                )
                                st.dataframe(df)
                                st.write(
                                        "[Reference](https://www.kaggle.com/code/sugandhkhobragade/caste-crimes-crimes-against-sc-2001-2013)"
                                )

                        elif selected == "Crime Rate Analysis":
                                filtered_df = dataframe_explorer(df)
                                st.dataframe(filtered_df, use_container_width=True)
                                st.write("---")
                                st.subheader("State Wise Total IPC Crimes:")
                                st.dataframe(df.groupby(by=["STATE/UT"]).sum()[["TOTAL IPC CRIMES"]])

                                fig = px.box(df, x="YEAR", y="DISTRICT", title="District Analysis by Year")  # more meaningful title
                                st.plotly_chart(fig)

                                st.subheader("Analysis of Datasets by Graphs:")
                                if st.button('Analysis'):
                                        st.subheader('Bar Chart:')
                                        st.bar_chart(df.groupby("YEAR")["MURDER"].sum()) # or a different aggregate based on what makes sense

                                        st.subheader('Plotly Chart:')
                                        fig_plotly = px.line(df.groupby("YEAR")["MURDER"].sum(), title="Murder Rate Over Years") # line chart may make more sense.
                                        st.plotly_chart(fig_plotly)

                                        st.subheader('Area Chart:')
                                        st.area_chart(df.groupby("YEAR")["MURDER"].sum())

                                if st.checkbox("Area graph with different factors"):
                                        all_columns = df.columns.to_list()
                                        feat_choices = st.multiselect("Choose a Feature", all_columns)
                                        if feat_choices:
                                                new_df = df[feat_choices]
                                                st.area_chart(new_df)
                                        else:
                                                st.warning("Please select at least one feature for the Area Chart.")

                        elif selected == "Prediction":
                                st.dataframe(df)
            
                                st.subheader('District Prediction:')
                                row1 = st.selectbox('Select the district:', df['DISTRICT'].unique()) #unique() so you have distict select options
                                row2 = st.selectbox('Select the state:', df['STATE/UT'].unique())

                                selected_rows = df[(df['DISTRICT'] == row1) & (df['STATE/UT'] == row2)]

                                if st.button('Predict'):
                                        if not selected_rows.empty:
                                                result = selected_rows['MURDER'].sum()
                                                st.write("The total predicted murders: " + str(result))
                                                if result > 1000:
                                                        st.subheader('This area might have a high Crime Rate')
                                                else:
                                                        st.subheader('This area has a lower Crime Rate')
                                        else:
                                                st.error("No data found for the selected District and State. Please select other values.")
                                if st.checkbox("Area graph with different factors for predictions"):
                                        all_columns = df.columns.to_list()
                                        feat_choices = st.multiselect("Choose a Feature", all_columns)
                                        if feat_choices:
                                                new_df = df[feat_choices]
                                                st.subheader('Area Chart:')
                                                st.area_chart(new_df)
                                        else:
                                                st.warning("Please select at least one feature for the Area Chart.")


def main():

        st.markdown("<h1 style='text-align: center; color: green;'>Crime Rate Prediction System</h1>", unsafe_allow_html=True)
        menu = ["HOME","ADMIN LOGIN","USER LOGIN","SIGN UP","ABOUT US"]
        choice = st.sidebar.selectbox("Menu",menu)


        if choice == "HOME":
                st.markdown("<h1 style='text-align: center;'>HOMEPAGE</h1>", unsafe_allow_html=True)
                st.image("img.jpg")
                time.sleep(3)
                st.warning("Goto Menu Section To Login !")



        elif choice == "ADMIN LOGIN":
                 st.markdown("<h1 style='text-align: center;'>Admin Login Section</h1>", unsafe_allow_html=True)
                 user = st.sidebar.text_input('Username')
                 passwd = st.sidebar.text_input('Password',type='password')
                 if st.sidebar.checkbox("LOGIN"):

                         if user == "Admin" and passwd == 'admin123':

                                                st.success("Logged In as {}".format(user))
                                                test()
                                                st.subheader("User Profiles")
                                                user_result = view_all_users()
                                                clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                                                st.dataframe(clean_db)
                                                
                         else:
                                st.warning("Incorrect Admin Username/Password")
          
                         
                        

        elif choice == "USER LOGIN":
                st.markdown("<h1 style='text-align: center;'>User Login Section</h1>", unsafe_allow_html=True)
                username = st.sidebar.text_input("User Name")
                password = st.sidebar.text_input("Password",type='password')
                if st.sidebar.checkbox("LOGIN"):
                        # if password == '12345':
                        create_usertable()
                        hashed_pswd = make_hashes(password)

                        result = login_user(username,check_hashes(password,hashed_pswd))
                        if result:

                                st.success("Logged In as {}".format(username))
                                test()
                        else:
                                st.warning("Incorrect Username/Password")
                                st.warning("Please Create an Account if not Created")





        elif choice == "SIGN UP":
                st.subheader("Create New Account")
                new_user = st.text_input("Username")
                new_password = st.text_input("Password",type='password')

                if st.button("SIGN UP"):
                        create_usertable()
                        add_userdata(new_user,make_hashes(new_password))
                        st.success("You have successfully created a valid Account")
                        st.info("Go to User Login Menu to login")

        elif choice == "ABOUT US":
                st.header("CREATED BY _**NAME**_")
                st.subheader("UNDER THE GUIDENCE OF _**GUIDE DETAILS**_")


if __name__ == '__main__':
        main()
