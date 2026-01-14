# 🚀 Deployment Guide (GCP VM + Minikube + Kubernetes)

## 1️⃣ Initial Setup

- Push Code to GitHub 
  - Ensure your complete project code is pushed to a GitHub repository.

- Create a Dockerfile 
  - Add a Dockerfile in the root directory to containerize the application.

- Create Kubernetes Deployment File 
  - Make a file named 'llmops-k8s.yaml'

- Create a VM Instance on Google Cloud 
  - Go to Compute Engine → VM Instances 
  - Click Create Instance 
  - Configuration:
    - Machine Series: E2 
    - Machine Type: Standard 
    - Memory: 16 GB RAM 
    - Boot Disk Size: 256 GB 
    - OS Image: Ubuntu 24.04 LTS 
    - Networking: Enable HTTP and HTTPS traffic

- Create the VM instance

- Connect to the VM 
  - Use the SSH (browser-based) option from GCP Console

## 2️⃣ Configure VM Instance

- Clone your GitHub repo
```bash
git clone https://github.com/saadtariq-ds/e-commerce-product-recommender.git
ls
cd e-commerce-product-recommender
ls
```

- Install Docker
  - Search: "Install Docker on Ubuntu"
  - Open the first official Docker website (docs.docker.com)
  - Scroll down and copy the first big command block and paste into your VM terminal
  - Then copy and paste the second command block
  - Then run the third command to test Docker:
  ```bash
  docker run hello-world
  ```

- Run Docker without sudo 
  - On the same page, scroll to: "Post-installation steps for Linux"
  - Paste all 4 commands one by one to allow Docker without sudo 
  - Last command is for testing

- Enable Docker to start on boot 
  - On the same page, scroll down to: "Configure Docker to start on boot"
  - Copy and paste the command block (2 commands):
  ```bash 
  sudo systemctl enable docker.service
  sudo systemctl enable containerd.service
  ```
  
- Verify Docker Setup
  ```bash 
  systemctl status docker       # You should see "active (running)"
  docker ps                     # No container should be running
  docker ps -a                 # Should show "hello-world" exited container
  ```
  
## 3️⃣ Configure Minikube inside VM

- Install Minikube 
  - Open browser and search: Install Minikube 
  - Open the first official site (minikube.sigs.k8s.io) with minikube start on it 
  - Choose:
    - OS: Linux 
    - Architecture: x86 
    - Select Binary download
    
- Install Minikube Binary on VM 
  - Copy and paste the installation commands from the website into your VM terminal
  
- Start Minikube Cluster
  ```bash
  minikube start
  ```
  
- Install kubectl 
  - Search: Install kubectl 
  - Run the first command with curl from the official Kubernetes docs 
  - Run the second command to validate the download 
  - Instead of installing manually, go to the Snap section (below on the same page)
  ```bash
  sudo snap install kubectl --classic
  ```
  - Verify installation:
  ```bash
  kubectl version --client
  ```
  - Check Minikube Status
  ```bash
  minikube status         # Should show all components running
  kubectl get nodes       # Should show minikube node
  kubectl cluster-info    # Cluster info
  docker ps               # Minikube container should be running
  ```
  
## 4️⃣ Interlink your Github on VSCode and on VM
```bash
git config --global user.email "your_email"
git config --global user.name "your_github_username"

git add .
git commit -m "commit"
git push origin main
```

- When prompted
  - Username: Your Github Username
  - Password: Github Token

## 5️⃣ Build and Deploy your APP on VM
```bash
## Point Docker to Minikube
eval $(minikube docker-env)

docker build -t flask-app:latest .

kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY="" \
  --from-literal=ASTRA_DB_APPLICATION_TOKEN="" \
  --from-literal=ASTRA_DB_KEYSPACE="default_keyspace" \
  --from-literal=ASTRA_DB_API_ENDPOINT="" \
  --from-literal=HF_TOKEN="" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN=""

kubectl apply -f kubernetes-deployment.yaml


kubectl get pods

### U will see pods runiing


# Open another terminal

kubectl port-forward svc/flask-service 5000:80 --address 0.0.0.0

## Now copy external ip and :8501 and see ur app there....
```

## 6️⃣ Prometheus and Grafana Cloud Monitoring
```bash
## Open another VM terminal for Grfana cloud

kubectl create namespace monitoring

kubectl get ns

kubectl apply -f prometheus/prometheus-configmap.yaml

kubectl apply -f prometheus/prometheus-deployment.yaml

kubectl apply -f grafana/grafana-deployment.yaml

## Check target health also..
## On IP:9090
kubectl port-forward --address 0.0.0.0 svc/prometheus-service -n monitoring 9090:9090

## Username:Pass --> admin:admin
kubectl port-forward --address 0.0.0.0 svc/grafana-service -n monitoring 3000:3000

Configure Grafana
Go to Settings > Data Sources > Add Data Source


Choose Prometheus

URL: http://prometheus-service.monitoring.svc.cluster.local:9090

Click Save & Test

Now make a dashboard for different visualization 

```
