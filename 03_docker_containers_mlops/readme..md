# 🐳 Dockerizing Your Streamlit App: Beginner Friendly Guide

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

Download Docker Desktop from:  
👉 https://www.docker.com/products/docker-desktop

> You need to create a Docker account to download.
> Follow the installation instructions for your OS (Windows, macOS, or Linux).

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