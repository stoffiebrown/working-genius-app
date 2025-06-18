{\rtf1\ansi\ansicpg1252\cocoartf2856
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Working Genius Team Model (Python Web App Version using Streamlit)\
\
import streamlit as st\
import matplotlib.pyplot as plt\
import networkx as nx\
from collections import Counter\
\
st.set_page_config(page_title="Working Genius Team Model", layout="wide")\
st.title("Working Genius Team Model")\
\
# Define the team profiles\
team = \{\
    "Anne": ["G", "T"],\
    "Molly": ["I", "D"],\
    "Allison": ["I", "D"],\
    "You": ["W", "E"]\
\}\
\
# Allow user to modify team interactively\
st.sidebar.header("Modify Team Members")\
for member in team.keys():\
    selections = st.sidebar.multiselect(f"\{member\}'s Geniuses", ["W", "I", "D", "G", "E", "T"], default=team[member], key=member)\
    team[member] = selections\
\
# Flatten to get full list of all Genius types\
all_geniuses = [genius for geniuses in team.values() for genius in geniuses]\
genius_counts = Counter(all_geniuses)\
\
# Bar chart of team distribution\
st.subheader("Team Genius Distribution")\
fig1, ax1 = plt.subplots(figsize=(8, 4))\
ax1.bar(genius_counts.keys(), genius_counts.values(), color='skyblue')\
ax1.set_xlabel("Genius Type")\
ax1.set_ylabel("Count")\
ax1.set_title("Current Distribution of Geniuses")\
st.pyplot(fig1)\
\
# Project Phase Simulation\
project_phases = \{\
    "Ideation": ["W", "I"],\
    "Vetting": ["D"],\
    "Launch Planning": ["G"],\
    "Execution": ["G", "T"],\
    "Stabilization": ["E", "T"]\
\}\
\
coverage_report = \{\}\
for phase, needed in project_phases.items():\
    coverage_score = sum(genius_counts[genius] for genius in needed)\
    coverage_report[phase] = coverage_score\
\
# Show phase coverage as bar chart\
st.subheader("Team Coverage per Project Phase")\
fig2, ax2 = plt.subplots(figsize=(10, 4))\
ax2.bar(coverage_report.keys(), coverage_report.values(), color='salmon')\
ax2.set_xlabel("Project Phase")\
ax2.set_ylabel("Coverage Score")\
ax2.set_title("Coverage of Geniuses per Project Phase")\
plt.xticks(rotation=15)\
st.pyplot(fig2)\
\
# Network Graph of Team Geniuses\
st.subheader("Team Genius Relationship Map")\
G = nx.Graph()\
for member, geniuses in team.items():\
    for genius in geniuses:\
        G.add_edge(member, genius)\
\
fig3, ax3 = plt.subplots(figsize=(8, 6))\
pos = nx.spring_layout(G, seed=42)\
nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=1200, font_size=10, ax=ax3, edge_color='gray')\
ax3.set_title("Visual Map of Team Geniuses")\
st.pyplot(fig3)\
\
# Export team profile as JSON\
import json\
if st.sidebar.button("Export Current Team Profile"):\
    st.sidebar.download_button(\
        label="Download Team Profile",\
        data=json.dumps(team, indent=2),\
        file_name="working_genius_team.json",\
        mime="application/json"\
    )\
\
st.sidebar.markdown("---")\
st.sidebar.markdown("Developed as a Working Genius Visual Tool")\
}