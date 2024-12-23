podman build . -t quay.io/prakashm88/ollama-sample-chat:latest

# oc new-app ollama-sample-chat --docker-image ollama-sample-chat

podman push  quay.io/prakashm88/ollama-sample-chat:latest

oc rollout restart deployments/ollama-sample-chat

#podman build -t quay.io/prakashm88/ollama-base:latest Containerfile-ollama

#podman push  quay.io/prakashm88/ollama-base:latest

#oc rollout restart deployments/ollama-base