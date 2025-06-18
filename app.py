# Working Genius Team Model Deployment Bundle (Python Web App using Streamlit)

# Enhanced Gear Version with Full Profile Mapping and Phase Member Display

import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
import json

st.set_page_config(page_title="Working Genius Team Model", layout="wide")
st.title("Working Genius Team Model — Gear Enhanced")

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

# Flatten profiles for distribution
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

phase_members = {}
for phase, needed in project_phases.items():
    members_in_phase = []
    for member, profile in team.items():
        if any(genius in profile["Genius"] for genius in needed):
            members_in_phase.append(member)
    phase_members[phase] = members_in_phase

# Display individual members per phase with colors
st.subheader("Team Coverage per Project Phase (Individuals)")
colors = [(0/255, 160/255, 73/255), (251/255, 195/255, 49/255), (203/255, 105/255, 91/255), (100/255, 149/255, 237/255), (255/255, 140/255, 0/255)]
fig2, ax2 = plt.subplots(figsize=(10, 6))

for idx, (phase, members) in enumerate(phase_members.items()):
    for i, member in enumerate(members):
        ax2.bar(phase, 1, bottom=i, color=colors[i % len(colors)], label=member if i == 0 else "")

ax2.set_ylabel("Number of Team Members")
ax2.set_title("Team Member Participation in Each Phase")
plt.xticks(rotation=15)
# Only add legend for first occurrence
handles, labels_unique = [], []
for i, member in enumerate(set(m for members in phase_members.values() for m in members)):
    handles.append(plt.Rectangle((0,0),1,1,color=colors[i % len(colors)]))
    labels_unique.append(member)
ax2.legend(handles, labels_unique, title="Members")
st.pyplot(fig2)

# Enhanced Network Graph of Team Profiles
st.subheader("Enhanced Team Genius Relationship Map")
G = nx.Graph()

# Add relationships for all 3 types
for member, profile in team.items():
    for genius in profile["Genius"]:
        G.add_edge(member, genius, relation='Genius')
    for comp in profile["Competency"]:
        G.add_edge(member, comp, relation='Competency')
    for frust in profile["Frustration"]:
        G.add_edge(member, frust, relation='Frustration')

pos = nx.spring_layout(G, seed=42)
fig3, ax3 = plt.subplots(figsize=(10, 7))

# Draw edges by type
edge_colors = []
edge_styles = []
for (u, v, d) in G.edges(data=True):
    if d['relation'] == 'Genius':
        edge_colors.append((0/255,160/255,73/255))
        edge_styles.append('solid')
    elif d['relation'] == 'Competency':
        edge_colors.append((251/255,195/255,49/255))
        edge_styles.append('solid')
    else:
        edge_colors.append((203/255,105/255,91/255))
        edge_styles.append('dashed')

for style in set(edge_styles):
    idx = [i for i, s in enumerate(edge_styles) if s == style]
    edges = [list(G.edges())[i] for i in idx]
    ec = [edge_colors[i] for i in idx]
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=ec, style=style, width=2, ax=ax3)

# Draw nodes with gear shape simulated (star)
nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_shape='*', node_size=1500, ax=ax3)
nx.draw_networkx_labels(G, pos, font_size=10, ax=ax3)

plt.title("Gear-Shaped Team Relationship Map")
st.pyplot(fig3)

st.sidebar.markdown("---")
st.sidebar.markdown("Developed as a Working Genius Visual Tool — Gear Enhanced")

# Export full team profile as JSON
if st.sidebar.button("Export Current Team Profile"):
    st.sidebar.download_button(
        label="Download Team Profile",
        data=json.dumps(team, indent=2),
        file_name="working_genius_full_profile.json",
        mime="application/json"
    )

# requirements.txt

# streamlit
# matplotlib
# networkx
