# n8n

n8n is an open-source workflow automation tool that allows you to connect various applications and services to automate tasks and processes.

## Features
- **Visual Workflow Editor**: Create workflows using a drag-and-drop interface.
- **Extensive Integrations**: Connect with over 200 applications and services.
- **Custom Nodes**: Build custom nodes to extend functionality.
- **Triggers and Actions**: Set up workflows that respond to events or run actions based on conditions.
- **Self-Hosted**: Run n8n on your own server for full control over your data.

## Installation

You can install n8n using conda with nodejs and npm, and/or Docker. Here are the steps for each method:

### Using Conda

```bash
conda create -n n8n -c conda-forge nodejs
conda activate n8n
npm install n8n -g
```

After installation, you can start n8n by running:

```bash
n8n
```
This will start the n8n server, and you can access it by navigating to `http://localhost:5678` in your web browser.

### Using Docker

1. Make sure you have Docker installed on your machine.
2. go to docker hub and pull the n8n image:
```bash
docker pull n8nio/n8n
```
3. Run the n8n container with the following command:
```bash
# make dir
mkdir ~/home/node/
docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```
4. Access n8n by navigating to `http://localhost:5678` in your web browser.


