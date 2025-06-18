# MM Leadership - Working Genius Team Model (Python Web App using Streamlit)

# Weighted Version with Intuitive Relationship Map and Harmonized Member Colors

import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
import json

st.set_page_config(page_title="MM Leadership - Working Genius Team Model", layout="wide")
st.title("MM Leadership - Working Genius Team Model — Weighted & Simplified Relationship Map")

# Define the team profiles with full WG profile (Genius, Competency, Frustration)
team = {
    "Anne": {"Genius": ["G", "T"], "Competency": ["I", "D"], "Frustration": ["W", "E"]},
    "Molly": {"Genius": ["I", "D"], "Competency": ["G", "E"], "Frustration": ["W", "T"]},
    "Allison": {"Genius": ["I", "D"], "Competency": ["G", "T"], "Frustration": ["W", "E"]},
    "Kris": {"Genius": ["W", "E"], "Competency": ["D", "I"], "Frustration": ["G", "T"]}
}

# Assign harmonized colors to each team member
member_colors = {
    "Anne": (255/255, 127/255, 80/255),    # Coral
    "Molly": (135/255, 206/255, 235/255),  # Sky Blue
    "Allison": (221/255, 160/255, 221/255), # Plum
    "Kris": (144/255, 238/255, 144/255)    # Light Green
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
labels = sorted(set(all_geniuses + all_competencies + all_frustrations))
genius_counts = Counter(all_geniuses)
competency_counts = Counter(all_competencies)
frustration_counts = Counter(all_frustrations)

g_counts = [genius_counts[label] for label in labels]
c_counts = [competency_counts[label] for label in labels]
f_counts = [frustration_counts[label] for label in labels]

st.subheader("Team Distribution: Genius, Competency, Frustration")
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

# Weighted Project Phase Simulation
project_phases = {
    "Ideation": ["W", "I"],
    "Vetting": ["D"],
    "Launch Planning": ["G"],
    "Execution": ["G", "T"],
    "Stabilization": ["E", "T"]
}

st.subheader("Team Coverage per Project Phase (Weighted Individuals)")
fig2, ax2 = plt.subplots(figsize=(10, 6))

for idx, (phase, needed) in enumerate(project_phases.items()):
    bottom = 0
    for member in team.keys():
        weight = 0
        for genius in needed:
            if genius in team[member]["Genius"]:
                weight += 1.0
            elif genius in team[member]["Competency"]:
                weight += 0.5
        if weight > 0:
            ax2.bar(phase, weight, bottom=bottom, color=member_colors[member], edgecolor='black')
            bottom += weight

ax2.set_ylabel("Weighted Contribution")
ax2.set_title("Weighted Team Member Participation per Phase")
plt.xticks(rotation=15)

handles = [plt.Rectangle((0,0),1,1,color=member_colors[member]) for member in team.keys()]
labels_unique = list(team.keys())
ax2.legend(handles, labels_unique, title="Members")
st.pyplot(fig2)

# Simplified Network Graph
st.subheader("Simplified Team Relationship Map")
G = nx.Graph()

# Add nodes for team members and types
for member in team.keys():
    G.add_node(member, type='member')
for genius_type in ["W", "I", "D", "G", "E", "T"]:
    G.add_node(genius_type, type='genius')

# Add edges with relation type
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
for (u, v, d) in G.edges(data=True):
    if d['relation'] == 'Genius':
        nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], edge_color=(0/255,160/255,73/255), width=2, ax=ax3)
    elif d['relation'] == 'Competency':
        nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], edge_color=(251/255,195/255,49/255), width=2, ax=ax3)
    else:
        nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], edge_color=(203/255,105/255,91/255), style='dashed', width=2, ax=ax3)

# Draw nodes with distinct shapes
node_shapes = {'member': 'o', 'genius': 's'}
for ntype in node_shapes:
    nodelist = [n for n in G.nodes if G.nodes[n]['type'] == ntype]
    color_list = [member_colors[n] if n in member_colors else 'lightgray' for n in nodelist]
    nx.draw_networkx_nodes(G, pos, nodelist=nodelist, node_shape=node_shapes[ntype], node_color=color_list, node_size=1500, ax=ax3)

nx.draw_networkx_labels(G, pos, font_size=10, ax=ax3)
plt.title("Simplified Team Relationship Map")
st.pyplot(fig3)

st.sidebar.markdown("---")
st.sidebar.markdown("Developed as MM Leadership Working Genius Visual Tool")

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
