# app.py
import streamlit as st
import yaml
import requests
import time

# -------------------------
# Your existing agent logic
# -------------------------
def fetch_manifest(url):
    st.info("Fetching manifest from GitHub...")
    response = requests.get(url)
    return yaml.safe_load(response.text)

def deploy(cluster, manifest):
    st.write(f"Deploying to {cluster['name']} ({cluster['provider']})")
    st.write(f"Application: {manifest['metadata']['name']}")
    st.write(f"Replicas: {manifest['spec']['replicas']}")
    st.success(f"Deployment to {cluster['name']} simulated successfully!")

# -------------------------
# Streamlit UI
# -------------------------
st.title("Multi-Cloud GitOps Agent Demo")
st.markdown("""
This demo simulates a GitOps control plane that detects changes in a Kubernetes manifest on GitHub 
and deploys it to multiple clusters (simulated).
""")

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

st.subheader("Connected Clusters")
for cluster in config["clusters"]:
    st.write(f"- {cluster['name']} ({cluster['provider']})")

# GitHub repo input
repo_url = st.text_input("GitHub manifest URL:", config.get("repo_url", ""))

# Button to trigger sync
if st.button("Run GitOps Sync"):
    if not repo_url:
        st.error("Please provide the GitHub manifest URL!")
    else:
        manifest = fetch_manifest(repo_url)
        st.code(manifest, language="yaml")

        # Load last_state.yaml to detect changes
        try:
            with open("last_state.yaml") as f:
                old_manifest = yaml.safe_load(f)
        except:
            old_manifest = None

        if old_manifest != manifest:
            st.success("Change detected! Triggering GitOps sync...")
            for cluster in config["clusters"]:
                deploy(cluster, manifest)
            with open("last_state.yaml", "w") as f:
                yaml.dump(manifest, f)
        else:
            st.info("No changes detected. Clusters are up-to-date.")