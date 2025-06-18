# Working Genius Team Model Deployment Bundle (Python Web App using Streamlit)

# app.py

import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
import json

st.set_page_config(page_title="Working Genius Team Model", layout="wide")
st.title("Working Genius Team Model")

# Define the team profiles with full WG profile (Genius, Competency, Frustration)
team = {
    "Anne": {"Genius": ["G", "T"], "Competency": ["I", "D"], "Frustration": ["W", "E"]},
    "Molly": {"Genius": ["I", "D"], "Competency": ["G", "E"], "Frustration": ["W", "T"]},
    "Allison": {"Genius": ["I", "D"], "Competency": ["G", "T"], "Frustration": ["W", "E"]},
    "Kris": {"Genius": ["W", "E"], "Competency": ["D", "I"], "Frustration": ["G", "T"]}
}

# Allow user to modify team interactively
st.sidebar.header("Modify Team Members")
for member in team.keys():
    st.sidebar.subheader(f"{member}")
    genius_selection = st.sidebar.multiselect(f"{member}'s Geniuses", ["W", "I", "D", "G", "E", "T"], default=team[member]["Genius"], key=member+"_Genius")
    competency_selection = st.sidebar.multiselect(f"{member}'s Competencies", ["W", "I", "D", "G", "E", "T"], default=team[member]["Competency"], key=member+"_Competency")
    frustration_selection = st.sidebar.multiselect(f"{member}'s Frustrations", ["W", "I", "D", "G", "E", "T"], default=team[member]["Frustration"], key=member+"_Frustration")
    team[member] = {"Genius": genius_selection, "Competency": competency_selection, "Frustration": frustration_selection}

# Flatten geniuses, competencies, and frustrations for distribution
all_geniuses = [genius for member in team.values() for genius in member["Genius"]]
all_competencies = [comp for member in team.values() for comp in member["Competency"]]
all_frustrations = [frust for member in team.values() for frust in member["Frustration"]]

# Count occurrences
genius_counts = Counter(all_geniuses)
competency_counts = Counter(all_competencies)
frustration_counts = Counter(all_frustrations)

# Bar chart of full distribution
st.subheader("Team Distribution: Genius, Competency, Frustration")
labels = sorted(set(all_geniuses + all_competencies + all_frustrations))
g_counts = [genius_counts[label] for label in labels]
c_counts = [competency_counts[label] for label in labels]
f_counts = [frustration_counts[label] for label in labels]

fig, ax = plt.subplots(figsize=(10, 5))
bar_width = 0.25
index = range(len(labels))
ax.bar(index, g_counts, bar_width, label='Genius', color=(0/255, 160/255, 73/255))
ax.bar([i + bar_width for i in index], c_counts, bar_width, label='Competency', color=(251/255, 195/255, 49/255))
ax.bar([i + 2*bar_width for i in index], f_counts, bar_width, label='Frustration', color=(203/255, 105/255, 91/255))

ax.set_xlabel("Working Genius Type")
ax.set_ylabel("Count")
ax.set_title("Current Distribution of Working Genius Profiles")
ax.set_xticks([i + bar_width for i in index])
ax.set_xticklabels(labels)
ax.legend()
st.pyplot(fig)

# Project Phase Simulation based on Genius only
project_phases = {
    "Ideation": ["W", "I"],
    "Vetting": ["D"],
    "Launch Planning": ["G"],
    "Execution": ["G", "T"],
    "Stabilization": ["E", "T"]
}

coverage_report = {}
for phase, needed in project_phases.items():
    coverage_score = sum(genius_counts[genius] for genius in needed)
    coverage_report[phase] = coverage_score

# Show phase coverage as bar chart
st.subheader("Team Coverage per Project Phase (Genius Only)")
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.bar(coverage_report.keys(), coverage_report.values(), color='salmon')
ax2.set_xlabel("Project Phase")
ax2.set_ylabel("Coverage Score")
ax2.set_title("Coverage of Geniuses per Project Phase")
plt.xticks(rotation=15)
st.pyplot(fig2)

# Network Graph of Team Geniuses
st.subheader("Team Genius Relationship Map")
G = nx.Graph()
for member, profile in team.items():
    for genius in profile["Genius"]:
        G.add_edge(member, genius)

fig3, ax3 = plt.subplots(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=1200, font_size=10, ax=ax3, edge_color='gray')
ax3.set_title("Visual Map of Team Geniuses")
st.pyplot(fig3)

# Export full team profile as JSON
if st.sidebar.button("Export Current Team Profile"):
    st.sidebar.download_button(
        label="Download Team Profile",
        data=json.dumps(team, indent=2),
        file_name="working_genius_full_profile.json",
        mime="application/json"
    )

st.sidebar.markdown("---")
st.sidebar.markdown("Developed as a Working Genius Visual Tool")

# requirements.txt

# streamlit
# matplotlib
# networkx
