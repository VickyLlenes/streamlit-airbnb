import streamlit as st
st.title('¡Mi First App with Streamlit!') 
st.write("¡Hola, world from me Mac!")
st.text("Hola")
st.header("Header")
st.subheader("Subheader")
st.text_input("Esribir nombre:")
age = st.number_input("Age?:")

st.write(f"Your age is {age}")

if age >= 18:
    st.write(f"You are allow in panda")
else:
    st.title(f"You are not allow")
    
city = st.multiselect("What city are you from?",["Madrid","Barcelona","Malaga"])
st.selectbox("What city are you from?",["Madrid","Barcelona","Malaga"])

st.write(city)

result = st.checkbox("Are you in class?")
st.write(result)

result = st.checkbox("Are you in class?", key="Check2")
st.write(result)

import pandas as pd

df = pd.DataFrame(
    {
        "web":["Google", "Youtube","Facebook"],
        "url":["google.com","youtuble.com","facebook.com"],
        "Rating":[4,5,4]
    })

#https://docs.streamlit.io/develop/api-reference/data/st.column_config

st.write(df)

st.dataframe(df,
             column_config={
             "web": st.column_config.TextColumn("Website"),
             "url": st.column_config.LinkColumn("link")
             })

import numpy as np
import matplotlib.pyplot as plt
x = np.linspace (0, 10, 100)
viz_size_x_axis = st.number_input("What is the size of the chart?")
fig, ax = plt.subplots(figsize=(viz_size_x_axis, 8))
ax.plot(x= x,
        y=x/10)

st.pyplot(fig)

