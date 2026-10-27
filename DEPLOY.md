# Deployment Guide: Autobiography and Portfolio Streamlit App

Follow these steps to deploy your Streamlit application to Streamlit Community Cloud:

## 1. Push to a Public GitHub Repository
1. Initialize git in your project directory (if not already initialized):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Autobiography and Portfolio app"
   ```
2. Create a new **public** repository on [GitHub](https://github.com/new).
3. Link your local repository to GitHub and push your code:
   ```bash
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git branch -M main
   git push -u origin main
   ```

## 2. Sign In to Streamlit Community Cloud
1. Navigate to [https://share.streamlit.io](https://share.streamlit.io) in your web browser.
2. Sign in using your GitHub account authorized to access your repositories.

## 3. Deploy `app.py`
1. Click the **"New app"** (or **"Create app"**) button.
2. Select your repository: `<your-username>/<your-repo-name>`.
3. Set the branch to `main`.
4. Set the main file path to `app.py`.
5. (Optional) Customize your app URL under Advanced settings.
6. Click **"Deploy!"**.

## 4. Verify the Deployment
1. Once deployment succeeds, copy your published app URL (e.g., `https://<your-app-name>.streamlit.app`).
2. Open a **Private / Incognito** window in your browser.
3. Paste the URL and verify that the page loads completely, themes render properly, images show up, and interactive widgets function without any errors or missing dependencies.
