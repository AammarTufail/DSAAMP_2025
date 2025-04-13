
# 📚 How to Create and Deploy a MkDocs Project on GitHub Pages (A to Z Guide)

This guide walks you through creating a professional documentation site using **MkDocs** and deploying it to **GitHub Pages** — perfect for portfolios, project docs, or personal knowledge bases.

---

## ✅ What is MkDocs?

MkDocs is a static site generator that's great for building **beautiful documentation** using Markdown. It’s fast, simple, and looks great!

---

## 🧰 Prerequisites

Make sure you have the following:

- ✅ Conda installed
- ✅ Basic knowledge of Markdown
  - You can learn Markdown from here is urdu/hindi [Markdown for Data Scientists and AI experts in 72 minutes](https://youtu.be/qJqAXjz-Rh4?si=1yJaj4my-bRPe5vR)
- ✅ Basic knowledge of Git & GitHub
  - You can learn Git from here is urdu/hindi [git & GitHub for Data Scientists and AI experts](https://www.youtube.com/live/iJAGwErBFrU?si=zs-k076Lj1DHLRbS&t=100)
- ✅ Python installed
  - You can learn Python from here is urdu/hindi [Python for Data Scientists and AI experts](https://youtu.be/glFfZcxwhtE)
- ✅ GitHub account
- ✅ Git installed
  - You can Install Git from [here](https://git-scm.com/downloads)

---

## 📦 Step 1: Install MkDocs

Open your terminal or command prompt:

```bash
conda create -n mkdocs python=3.12 -y
conda activate mkdocs
pip install mkdocs
pip install mkdocs-material # Optional: Material theme
pip install mkdocs-git-revision-date-localized-plugin mkdocs-material mkdocs-material-extensions mkdocs-git-authors-plugin
```

---

## 🏗️ Step 2: Create a New MkDocs Project

```bash
mkdocs new mera_portfolio
cd mera_portfolio
```

Project structure:

```
mera_portfolio/
├── docs/
│   └── index.md
└── mkdocs.yml
```

---

## 📝 Step 3: Customize Your Docs

- Edit the default `docs/index.md`:
- Edit `mkdocs.yml` to change the site name:

---

## 🚀 Step 4: Preview the Docs Locally

```bash
mkdocs serve
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

> This is how you can specify the port and host
```bash
mkdocs serve -a 127.0.0.1:8501
```
> This will start a local server to preview your documentation on 8501 [http://127.0.0.1:8501](http://127.0.0.1:8501).

---

## 🌍 Step 5: Create a GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click **New Repository**
3. Name it something like `mera_portfolio`
4. Set it to **Public**
5. Add a description (optional)
5. Don't initialize with README or .gitignore

---

## 🛠️ Step 6: Initialize Git & Push

> Make sure you are in the `mera_portfolio` directory.
> If you are not, navigate to it using:
```bash
cd path/to/mera_portfolio
```
Initialize Git and push your project:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/mera_portfolio.git # replace the link to your repo
git push -u origin main
```

---

## 🧪 Step 7: Install GitHub Deploy Tool

Install the deploy helper, follow the instructions given in [Step-1](#-step-1-install-mkdocs) to install the `mkdocs` package.


And update `mkdocs.yml` if you need to customize anything:

```yaml
theme:
  name: material
```

---

## 🚢 Step 8: Deploy to GitHub Pages

```bash
mkdocs gh-deploy
```
> This command will deploy your site to the `gh-pages` branch of your repository.
> If you want to deploy to a different branch, you can specify it using the `--remote-branch` option.

This:
- Builds your site
- Pushes it to the `gh-pages` branch
- Makes it live on GitHub Pages 🚀

---

## 🌐 Step 9: Access Your Live Site

> The site is live on GitHub Pages at: `https://your-username.github.io/mera_portfolio/`
> Replace `your-username` with your GitHub username and `mera_portfolio` with your repository name.
> You can also specify a custom domain by adding a `CNAME` file to the `docs/` directory.
> This file should contain your custom domain name (e.g., `www.yourdomain.com`).

---

## 🧼 Optional: Add More Pages & Navigation

Add `.md` files to `docs/` and update `mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - About: about.md
```

---

## 📌 Summary Table

| Task                   | Command / Description                        |
|------------------------|-----------------------------------------------|
| Install MkDocs         | `pip install mkdocs`                         |
| Create Project         | `mkdocs new mera_portfolio`                  |
| Preview Locally        | `mkdocs serve`                               |
| Create GitHub Repo     | [GitHub](https://github.com)                 |
| Initialize Git         | `git init`                                   |
| Push to GitHub         | `git push -u origin main`                    |
| Deploy to GitHub Pages | `mkdocs gh-deploy`                           |
| Access Live Site       | `https://your-username.github.io/mera_portfolio/` |
| Add More Pages         | Edit `mkdocs.yml` and add `.md` files        |
| Customize Theme        | Edit `mkdocs.yml` under `theme:`             |
| Add Custom Domain      | Create `CNAME` file in `docs/` directory      |

---

Enjoy building clean, responsive documentation with MkDocs! 🎉

---
<h1 style="font-family: 'poppins'; font-weight: bold; color: Green;">👨‍💻Author: Dr. Muhammad Aammar Tufail</h1>

[![GitHub](https://img.shields.io/badge/GitHub-Profile-blue?style=for-the-badge&logo=github)](https://github.com/AammarTufail) 
[![Kaggle](https://img.shields.io/badge/Kaggle-Profile-blue?style=for-the-badge&logo=kaggle)](https://www.kaggle.com/muhammadaammartufail) 
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/dr-muhammad-aammar-tufail-02471213b/)  

[![YouTube](https://img.shields.io/badge/YouTube-Profile-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/@codanics) 
[![Facebook](https://img.shields.io/badge/Facebook-Profile-blue?style=for-the-badge&logo=facebook)](https://www.facebook.com/aammar.tufail) 
[![TikTok](https://img.shields.io/badge/TikTok-Profile-black?style=for-the-badge&logo=tiktok)](https://www.tiktok.com/@draammar)  

[![Twitter/X](https://img.shields.io/badge/Twitter-Profile-blue?style=for-the-badge&logo=twitter)](https://twitter.com/aammar_tufail) 
[![Instagram](https://img.shields.io/badge/Instagram-Profile-blue?style=for-the-badge&logo=instagram)](https://www.instagram.com/aammartufail/) 
[![Email](https://img.shields.io/badge/Email-Contact%20Me-red?style=for-the-badge&logo=email)](mailto:aammar@codanics.com)

---