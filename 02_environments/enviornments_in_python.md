# Conda/mamba/python Environments
The way to isolate, manage, and supercharge your AI/dev workflows.

## What are environments?
Environments are isolated spaces where you can install packages and dependencies without affecting the global Python installation or other environments. 
- This is particularly useful when working on multiple projects that may require different versions of libraries or Python itself.
- Environments help avoid version conflicts and ensure that each project has the exact dependencies it needs to run smoothly.

---
## Complete lecture on environments and package management

<a href="https://youtu.be/OnCr8XmIiX0">
  <img src="https://img.youtube.com/vi/OnCr8XmIiX0/0.jpg" alt="conda/pip/venv/mamba  environments | A complete Guide" width="500"/>
</a>

---

## Pros and Cons of Environments
| Category              | Pros                                                                 | Cons                                                                                   |
|-----------------------|----------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| Isolation             | Each environment is independent, preventing conflicts between projects. | Each environment can take up significant disk space, especially if you have many environments. |
| Version Control       | You can specify exact versions of packages, ensuring reproducibility. | Managing multiple environments can be complex and may require additional tools.         |
| Ease of Management    | You can quickly create and delete environments as needed.            | New users may find it challenging to understand how to manage environments effectively. |
| Environment Variables | You can set environment variables specific to each environment.      | You need to remember to activate/deactivate environments when switching projects.       |
| Customization         | You can customize each environment with different Python versions and packages. | Some packages may not work well in isolated environments.                              |


## Use Cases of Environments

- **Data Science**: Different projects may require different versions of libraries like NumPy, Pandas, or TensorFlow.
- **Machine Learning**: Different models may require different versions of libraries like scikit-learn or Keras.
- **Deep Learning**: Different neural networks may require different versions of libraries like PyTorch or TensorFlow.
- **AI Workflow**: Different AI workflows may require different versions of libraries like OpenAI Gym or Hugging Face Transformers.
- **Web Development**: Different web applications may require different versions of frameworks like Flask or Django.
- **Scripting**: Different scripts may require different versions of libraries like Requests or BeautifulSoup.
- **Automation**: Different automation tasks may require different versions of libraries like Selenium or PyAutoGUI.
- **Testing**: Different test suites may require different versions of libraries like pytest or unittest.
- **Deployment**: Different deployment environments may require different versions of libraries like Flask or Django.
- **Game Development**: Different games may require different versions of libraries like Pygame or Panda3D.

## Software to Manage Environments

### conda/mamba/miniconda/micromamba
- **Description**: Conda is a package manager that can create and manage environments. 
- Mamba is a faster alternative to conda.

> It is preferable to use mamba over conda for package management due to its speed and efficiency. But the choice is yours.
> 
> You can use either conda or mamba to create and manage environments.

#### Installation
> To install conda (miniconda) on your system, follow the instructions on the [official website](https://www.anaconda.com/docs/getting-started/miniconda/install).
> You can follow the following tutorials to Install conda, git and GitBash in windows:

<a href="https://www.youtube.com/watch?v=nA2_5BrOHwQ">
  <img src="https://img.youtube.com/vi/nA2_5BrOHwQ/0.jpg" alt="YouTube video: Install conda, git and GitBash in Windows" width="300"/>
</a>
<a href="https://youtu.be/UyVPHNeEka0">
  <img src="https://img.youtube.com/vi/UyVPHNeEka0/0.jpg" alt="YouTube video: GitBash and miniconda | Integration | Solutions" width="300"/>
</a>
<a href="https://youtu.be/AzS8gEdiRWc">
  <img src="https://img.youtube.com/vi/AzS8gEdiRWc/0.jpg" alt="YouTube video: miniConda | Environments and Installations | A complete Guide" width="300"/>
</a>

### venv or virtualenv
- **Description**: A built-in module in Python 3.3 and later that allows you to create isolated environments.
- It is a lightweight alternative to `virtualenv` and is included with Python installations.
- It is particularly useful for creating isolated environments for Python projects.
- It is also a good choice for projects that require a specific version of Python and dependencies.

#### **Creating a Virtual Environment**: 
```bash
python -m venv myenv
```
#### **Activating the Environment**: 
```bash
# On Windows
myenv\Scripts\activate
# On macOS/Linux
source myenv/bin/activate
```
#### **Deactivating the Environment**: 
```bash
deactivate
```
#### **Deleting the Environment**: 
```bash
# On Windows
rmdir /S /Q myenv
# On macOS/Linux
rm -rf myenv
```
### pipenv
- **Description**: A tool that combines `pip` and `virtualenv` to create isolated environments and manage dependencies.
- It automatically creates a `Pipfile` and `Pipfile.lock` to manage dependencies.
- It is particularly useful for managing dependencies in Python projects.
- It is a good choice for projects that require a specific set of dependencies and versions.
- It is also a good choice for projects that require a specific version of Python.

#### **Installation**: 
```bash
pip install pipenv
```
#### **Creating a Virtual Environment**: 
```bash
pipenv install
```
#### **Activating the Environment**: 
```bash
pipenv shell
```
#### **Deactivating the Environment**: 
```bash
exit
```
#### **Deleting the Environment**: 
```bash
pipenv --rm
```
### pyenv
- **Description**: A tool to manage multiple Python versions on your system.
- It allows you to switch between different Python versions easily.
- It is particularly useful for projects that require a specific version of Python.
- It is also a good choice for projects that require a specific version of Python and dependencies.

#### **Installation**: 
```bash
curl https://pyenv.run | bash
```
#### **Installing Python Versions**: 
```bash
pyenv install 3.8.10
pyenv install 3.9.5
```
#### **Setting Global Python Version**: 
```bash
pyenv global 3.8.10
```
#### **Setting Local Python Version**: 
```bash
pyenv local 3.9.5
```
#### **Uninstalling Python Versions**: 
```bash
pyenv uninstall 3.8.10
pyenv uninstall 3.9.5
```

### Docker
- **Description**: A platform that allows you to create, deploy, and manage applications in containers.
- It allows you to create isolated environments for your applications, including all dependencies and configurations.

- It is particularly useful for deploying applications in different environments, such as development, testing, and production.
- It is also a good choice for projects that require a specific version of Python and dependencies.

#### **Installation**: 
```bash
# Follow the instructions on the official website
# https://docs.docker.com/get-docker/
```
> Details coming soon...


