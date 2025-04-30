# 🐳 **Docker Containers for AI and Data Science Developers**

Docker is a powerful tool that allows you to package your applications and their dependencies into a single container. 
- This makes it easy to deploy and run your applications in any environment, whether it's on your local machine, in the cloud, or on a server.
- Docker is especially useful for AI and data science developers, as it allows you to create reproducible environments for your projects. This means that you can share your code with others and be sure that it will run the same way on their machines as it does on yours.
- Docker is also importat for MLOps, as it allows you to create containers for your machine learning models. This makes it easy to deploy your models in production and scale them as needed.

- [🐳 **Docker Containers for AI and Data Science Developers**](#-docker-containers-for-ai-and-data-science-developers)
  - [🐳 Dockerizing Your Streamlit App: Beginner Friendly Guide](#-dockerizing-your-streamlit-app-beginner-friendly-guide)
  - [✅ Step 0: Prerequisites](#-step-0-prerequisites)
    - [🐍 Install Python](#-install-python)
    - [📦 Install pip (comes with Python)](#-install-pip-comes-with-python)
      - [Update pip (optional):](#update-pip-optional)
  - [📦 Step 1: Set Up Your Project](#-step-1-set-up-your-project)
  - [🐍 Step 2: Set Up Virtual Environment (venv)](#-step-2-set-up-virtual-environment-venv)
  - [📦 Step 3: Install Streamlit \& Freeze Requirements](#-step-3-install-streamlit--freeze-requirements)
  - [🐳 Step 4: Create a Dockerfile](#-step-4-create-a-dockerfile)
  - [🚫 Step 5: Create a .dockerignore file](#-step-5-create-a-dockerignore-file)
  - [🧱 Step 6: Install Docker](#-step-6-install-docker)
    - [6.1 Install Docker in lunux](#61-install-docker-in-lunux)
  - [🔨 Step 7: Build the Docker Image](#-step-7-build-the-docker-image)
  - [▶️ Step 8: Run the Docker Container](#️-step-8-run-the-docker-container)
    - [To run the container in detached mode (background):](#to-run-the-container-in-detached-mode-background)
  - [🧠 Summary](#-summary)
  - [**Docker-Hub**](#docker-hub)
  - [🚀 Push Your Image to Docker Hub](#-push-your-image-to-docker-hub)
    - [1. Log in to Docker Hub](#1-log-in-to-docker-hub)
      - [1.1 Create a Docker Hub repository](#11-create-a-docker-hub-repository)
    - [2. Tag Your Image](#2-tag-your-image)
    - [3. Push the Image](#3-push-the-image)
  - [Docker Cheatsheet](#docker-cheatsheet)
  - [🛠️ Troubleshooting](#️-troubleshooting)
    - [Common Issues](#common-issues)


## 🐳 Dockerizing Your Streamlit App: Beginner Friendly Guide

This guide walks you through converting your local **Streamlit app using virtual environment (venv)** into a **Docker container**, so it can run anywhere, even without Python installed!

---

## ✅ Step 0: Prerequisites

Make sure you have the following installed:

### 🐍 Install Python
- Download from: https://www.python.org/downloads/
- Make sure to select **"Add Python to PATH"** during installation.

### 📦 Install pip (comes with Python)

Check it:

```bash
pip --version
# or
pip3 --version # for macOS/Linux
```
#### Update pip (optional):

```bash
# for windows
python -m pip install --upgrade pip
# for macos/linux
python3 -m pip install --upgrade pip
```

---

## 📦 Step 1: Set Up Your Project

Create your app folder:

```bash
mkdir my-streamlit-app
cd my-streamlit-app
```

Add your Streamlit app code:

```bash
touch app.py
```

Paste a sample app:

```python
# app.py
# write in terminal
cat >> app.py

import streamlit as st

st.title("My First Dockerized Streamlit App with [codanics](www.codanics.com)")
st.write("Hello from inside Docker!")
```
> Press `CTRL+D` to save and exit.
> You can also use any text editor to create `app.py` and paste the code.
---

## 🐍 Step 2: Set Up Virtual Environment (venv)

```bash
python -m venv .venv
```

Activate the environment:

- On macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```
- On Windows:
  ```bash
  .venv\Scripts\activate
  ```

---

## 📦 Step 3: Install Streamlit & Freeze Requirements

```bash
pip install streamlit
pip freeze > requirements.txt
```

This creates a file `requirements.txt`.

---

## 🐳 Step 4: Create a Dockerfile

Create a file called `Dockerfile` in your project folder:

```bash
touch Dockerfile
```
Add the following content:

```Dockerfile
# Use official Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy app code to container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 🚫 Step 5: Create a .dockerignore file

Ignore unnecessary files by creating a `.dockerignore` file:
```bash
touch .dockerignore
```
Add the following content:

```
__pycache__/
*.pyc
.venv/
.env
```

---

## 🧱 Step 6: Install Docker

> Docker CLI is free and open-source, but Docker Desktop is a paid product (based on the number of users and usage).
> - For personal use, Docker Desktop is free.
> - For commercial use, Docker Desktop is paid.
> - For educational use, Docker Desktop is free.
> - For open-source projects, Docker Desktop is free.
> - For non-profit organizations, Docker Desktop is free.

Download Docker Desktop from:  
👉 https://www.docker.com/products/docker-desktop

> You need to create a Docker account to download.
> Follow the installation instructions for your OS (Windows, macOS, or Linux).

### 6.1 Install Docker in linux

```bash
# for ubuntu
sudo apt-get update
sudo apt-get install docker.io
# after installation
sudo systemctl start docker
sudo systemctl enable docker
# check docker version
docker --version
```
> - For other Linux distributions, refer to the official Docker documentation.

### 6.2 Install Docker in macos

```bash
# for macos
brew install --cask docker
# after installation
open /Applications/Docker.app
# check docker version
docker --version
```
> - For other macOS distributions, refer to the official Docker documentation.
### 6.3 Install Docker in windows

```bash
# for windows
choco install docker-desktop
# after installation
docker-desktop
# check docker version
docker --version
```


Once installed, verify:

```bash
docker --version
```
`Docker version 28.0.4, build b8034c0`
> If you see a version number, Docker is installed correctly.
 
**Trouble Shooting:**
> - If you see an error, restart your computer and try again.
> - If you still see an error, check Docker Desktop is running.
> - If you see a message about "WSL 2 backend", follow the instructions to enable it.
> - If you see a message about "Docker Desktop is starting", wait for it to finish.
> - If you see a message about "Docker Desktop is running", you're good to go!
---

## 🔨 Step 7: Build the Docker Image

In your project folder (with Dockerfile):

> 1. Run Docker Desktop. 
> 2. **Make sure Docker Desktop is running.**
> 3. Open a terminal or command prompt.
> 4. Navigate to your project folder.
> 5. Run the following command to build the Docker image:

```bash
docker build -t my-streamlit-app .
```
> - `-t my-streamlit-app` gives your image a name.
> - `.` specifies the current directory as the build context.

> you can also create a docker image which suits your choice of platform such as linux /arm64 or linux/amd64 or windows/amd64  or windows/arm64 or linux/arm/v7 or linux/arm/v6 etc.  
```bash
# check docker image
docker buildx ls
# for ubuntu x86_64 
docker buildx build --platform linux/amd64 -t my-streamlit-app .
```

**remove images**

```bash
# list my docker images
docker images
# remove my docker image
docker rmi my-streamlit-app:latest
# remove my docker image by id
docker rmi e518336f912b -f 
```

```
Do check your platform version using the following commands:
```bash
# for linux
uname -m
# for windows
wmic os get osarchitecture
# for macos
uname -m
```

---
> **Note:** Allow vscode to use other apps if asked.
> - If you see a message like `Sending build context to Docker daemon  3.072kB`, it means Docker is building the image.
---
> - This command may take a few minutes to complete, depending on your internet speed and system performance.
> - You will see a lot of output as Docker builds the image.
> - If you see a message like `Successfully built <image_id>`, your image is ready!

Check if image is available in Docker:

```bash
docker images
```
> You should see `my-streamlit-app` in the list of images.

---

## ▶️ Step 8: Run the Docker Container

```bash
docker run -p 8501:8501 my-streamlit-app
```
> - `-p 8501:8501` maps port 8501 on your host to port 8501 in the container.
> - `my-streamlit-app` is the name of your image.
> - This command runs the container in the foreground, so you can see the logs.
> - If you see a message like `Starting up server`, your app is running!

Visit:  
👉 http://localhost:8501

🎉 Your Streamlit app is now running inside a Docker container!

### To run the container in detached mode (background):

```bash
docker run --name MAtufail -d -p 8501:8501 my-streamlit-app
```
> - `-d` runs the container in detached mode (in the background).
> - `--name MAtufail` gives your container a name (optional).
> - You can check running containers with:
```bash
docker ps
```
> - To stop the container, use:
```bash
docker stop MAtufail
```
> - To remove the container, use:
```bash
docker rm MAtufail
```

---

## 🧠 Summary

| Task                  | Command |
|-----------------------|---------|
| Create venv           | `python -m venv .venv` |
| Activate venv         | `source .venv/bin/activate` or `.venv\Scripts\activate` |
| Install Streamlit     | `pip install streamlit` |
| Save requirements     | `pip freeze > requirements.txt` |
| Build Docker image    | `docker build -t my-streamlit-app .` |
| Run Docker container  | `docker run -p 8501:8501 my-streamlit-app` |

---

📬 **Need help?**  
Ask your questions at: [github.com/aammartufail](https://github.com/AammarTufail/DSAAMP_2025/blob/main/03_docker_containers_mlops/docker_readme..md)


## **Docker-Hub**
- [Docker Hub](https://hub.docker.com/) is a cloud-based repository for Docker images.
- You can push your images to Docker Hub to share them with others or use them on different machines.
- To push your image to Docker Hub, you need to create an account and log in to Docker Hub from your terminal.
- You can then use the `docker push` command to upload your image.


---

## 🚀 Push Your Image to Docker Hub

Let's push your image to the Docker Hub repository `maammartufail/test_app`.

### 1. Log in to Docker Hub

```bash
docker login
```
> Enter your Docker Hub username and password when prompted.

#### 1.1 Create a Docker Hub repository
- Go to [Docker Hub](https://hub.docker.com/).
- Click on **Create Repository**.
- Enter the name of your repository (e.g., `test_app`).
- Choose **Public** or **Private**. I prefer **Public**.
- Click on **Create**.
> You can also create a repository from the command line using the Docker CLI.
```bash
docker create repository maammartufail/test_app
```
> - This command creates a new repository named `test_app` under your Docker Hub account `maammartufail`.
> - You can also create a repository from the Docker Hub website.


### 2. Tag Your Image

Tag your local image (`my-streamlit-app`) to match your Docker Hub repo:

```bash
# Check your image ID
docker images
# Tag your image
docker tag my-streamlit-app maammartufail/test_app:latest
```

### 3. Push the Image

```bash
docker push maammartufail/test_app:latest
```

> After the push completes, your image will be available at:  
> https://hub.docker.com/r/maammartufail/test_app

---

**Tip:**  
You can now pull and run this image from any machine with Docker installed:

```bash
docker pull maammartufail/test_app:latest
docker run -p 8501:8501 maammartufail/test_app:latest
```

> Run in background:
```bash
# run in background even if you restart your computer
docker run --name MAtufail -d -p 8501:8501 maammartufail/test_app:latest
# check running containers
docker ps
# check logs
docker logs MAtufail
# stop the container
docker stop MAtufail
# remove the container
docker rm MAtufail
# remove the image
docker rmi maammartufail/test_app:latest
```

## Docker Cheatsheet
 Docker cheatsheet for common commands is available at:
👉 [Docker Cheatsheet](https://docs.docker.com/get-started/docker_cheatsheet.pdf)

> - This command downloads the image from Docker Hub and runs it locally.
> - You can also use this image in cloud platforms like AWS, Azure, or Google Cloud.
> - You can also use this image in CI/CD pipelines to automate your deployment process.
> - You can also use this image in Kubernetes to deploy your app in a container orchestration platform.
---
## 🛠️ Troubleshooting
### Common Issues
- **Docker Daemon Not Running**: Make sure Docker Desktop is running.
- **Permission Denied**: Run Docker commands with `sudo` on Linux.
- **Image Not Found**: Check the image name and tag.
- **Port Already in Use**: Change the port mapping in the `docker run` command.
- **Container Not Starting**: Check the logs with `docker logs <container_id>`.
- **Streamlit Not Found**: Make sure you have `streamlit` in your `requirements.txt`.
- **Network Issues**: Check your internet connection and firewall settings.
- **Dockerfile Errors**: Check the syntax and paths in your Dockerfile.
- **Slow Build**: Use `--no-cache` to speed up the build process.
- **Image Size**: Use `docker system prune` to clean up unused images and containers.
- **Docker Desktop Issues**: Restart Docker Desktop or your computer.
- **Docker Hub Issues**: Check Docker Hub status page for outages.

---