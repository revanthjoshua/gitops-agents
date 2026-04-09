import streamlit as st
import requests
import yaml
import time

st.set_page_config(page_title="GitOps Agent", page_icon="🚀", layout="wide")

# -------------------- Sidebar --------------------
st.sidebar.title("GitOps Agent Control Panel")
repo_url = st.sidebar.text_input(
    "Deployment YAML URL",
    "https://raw.githubusercontent.com/revanthjoshua/gitops-agent/main/deployment.yaml"
)
interval = st.sidebar.number_input("Check interval (seconds)", min_value=5, max_value=60, value=10)

# Simulated clusters
clusters = [
    {"name": "Cluster-A", "provider": "GKE"},
    {"name": "Cluster-B", "provider": "EKS"},
    {"name": "Cluster-C", "provider": "AKS"},
]

selected_clusters = st.sidebar.multiselect(
    "Select clusters to deploy", [c["name"] for c in clusters], default=[c["name"] for c in clusters]
)

st.title("🚀 GitOps Agent Simulator")
st.markdown("""
This app simulates a GitOps agent deploying a Kubernetes manifest to multiple clusters.
It automatically detects changes in your YAML file and triggers deployments.
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

def deploy(cluster, manifest):
    st.info(f"Deploying **{manifest['metadata']['name']}** to **{cluster['name']} ({cluster['provider']})**")
    st.success(f"Deployment to {cluster['name']} simulated successfully!")

# -------------------- Main Logic --------------------
if "last_manifest" not in st.session_state:
    st.session_state.last_manifest = None

placeholder = st.empty()

with placeholder.container():
    while True:
        manifest = fetch_manifest(repo_url)
        if manifest is None:
            st.warning("Waiting for a valid deployment YAML...")
            time.sleep(interval)
            continue

        if st.session_state.last_manifest != manifest:
            st.subheader("💡 Change detected! Triggering GitOps sync...")
            for cluster in clusters:
                if cluster["name"] in selected_clusters:
                    deploy(cluster, manifest)
            st.session_state.last_manifest = manifest
        else:
            st.info("No changes detected. Clusters are up-to-date.")

        # Display clusters table
        st.table(clusters)

        st.markdown(f"Next check in {interval} seconds...")
        time.sleep(interval)
        placeholder.empty()