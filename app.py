import streamlit as st
import requests
import yaml
import time

st.set_page_config(page_title="🚀 GitOps Agent Dashboard", page_icon="🚀", layout="wide")

# -------------------- Sidebar --------------------
st.sidebar.title("GitOps Agent Control Panel")

# YAML URL
repo_url = st.sidebar.text_input(
    "Deployment YAML URL",
    "https://raw.githubusercontent.com/revanthjoshua/gitops-agents/main/deployment.yaml"
)

# Deployment interval
interval = st.sidebar.number_input(
    "Check interval (seconds)",
    min_value=5,
    max_value=60,
    value=10
)

# Simulated clusters
clusters = [
    {"name": "Cluster-A", "provider": "GKE", "status": "Idle"},
    {"name": "Cluster-B", "provider": "EKS", "status": "Idle"},
    {"name": "Cluster-C", "provider": "AKS", "status": "Idle"},
]

selected_clusters = st.sidebar.multiselect(
    "Select clusters to deploy",
    [c["name"] for c in clusters],
    default=[c["name"] for c in clusters]
)

st.title("🚀 GitOps Agent Simulator")
st.markdown("""
This app simulates a GitOps agent deploying a Kubernetes manifest to multiple clusters.
It detects changes in your YAML file and triggers simulated deployments with live logs.
""")

# -------------------- Helper Functions --------------------
def fetch_manifest(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return yaml.safe_load(response.text)
    except Exception as e:
        st.error(f"Error fetching YAML: {e}")
        return None

def simulate_deploy(cluster, manifest):
    cluster_name = cluster["name"]
    st.info(f"⏳ Deploying **{manifest['metadata']['name']}** to **{cluster_name} ({cluster['provider']})**")
    # Simulate deployment delay
    for i in range(1, 4):
        st.write(f"{cluster_name}: Step {i}/3 - Running...")
        time.sleep(0.5)
    st.success(f"✅ Deployment to {cluster_name} simulated successfully!")

# -------------------- Session State --------------------
if "last_manifest" not in st.session_state:
    st.session_state.last_manifest = None

# -------------------- Main Loop --------------------
placeholder = st.empty()
with placeholder.container():
    while True:
        manifest = fetch_manifest(repo_url)
        if manifest is None:
            st.warning("Waiting for a valid deployment YAML...")
            time.sleep(interval)
            continue

        # Detect changes
        if st.session_state.last_manifest != manifest:
            st.subheader("💡 Change detected! Triggering GitOps sync...")
            for cluster in clusters:
                if cluster["name"] in selected_clusters:
                    simulate_deploy(cluster, manifest)
                    cluster["status"] = "Deployed"
            st.session_state.last_manifest = manifest
        else:
            st.info("No changes detected. Clusters are up-to-date.")

        # Display clusters table
        st.table([{ "Cluster": c["name"], "Provider": c["provider"], "Status": c["status"] } for c in clusters])

        st.markdown(f"Next check in **{interval} seconds**...")
        time.sleep(interval)
        placeholder.empty()