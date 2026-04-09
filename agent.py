import requests
import yaml
import time

def fetch_manifest(url):
    print("Fetching manifest from GitHub...")
    response = requests.get(url)
    return yaml.safe_load(response.text)

def deploy(cluster, manifest):
    print(f"\nDeploying to {cluster['name']} ({cluster['provider']})")
    print(f"Application: {manifest['metadata']['name']}")
    print(f"Replicas: {manifest['spec']['replicas']}")
    print("Deployment simulated successfully!")

def main():
    while True:
        time.sleep(10)  # Check for changes every 10 seconds
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
            
            print("\nChecking again in 10 seconds...\n")
        time.sleep(10)

    manifest = fetch_manifest(config["repo_url"])
    try:
     with open("last_state.yaml", "r") as f:
        old_manifest = yaml.safe_load(f)
    except:
     old_manifest = None

    if old_manifest != manifest:
     print("\nChange detected! Triggering GitOps sync...\n")

     for cluster in config["clusters"]:
        deploy(cluster, manifest)

     with open("last_state.yaml", "w") as f:
        yaml.dump(manifest, f)

    else:
        
     print("\nNo changes detected. Clusters are up-to-date.")
    print("\nAll clusters synced (GitOps success)")

if __name__ == "__main__":
    main()