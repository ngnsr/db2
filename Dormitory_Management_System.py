#!/usr/bin/env python

#  streamlit run Dormitory_Management_System.py

import streamlit as st

page_icon = ":hotel:"
page_name = "Dormitory Management System"
layout = "centered"
st.set_page_config(page_title=page_name, page_icon=page_icon, layout=layout)

st.header(page_name + " " + page_icon)
st.sidebar.success("Select a page above.")
st.markdown("This multi-page application is a Streamlit dashboard that can be used to analyze data from Dormitory Management System💥")
st.markdown("🔵     Author: **Vlad Risenhin**")
