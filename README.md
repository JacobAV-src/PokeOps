# 🎴 PokeOps – Mint a Pokémon Card for Your DevOps Task!

> “There’s a time and place for everything — but not now.”  
> — Professor Oak, probably after seeing your YAML syntax

---

Welcome to **PokeOps**, where **doing DevOps gets you Pokémon cards**.

This GitHub Action mints a **unique trading card** each time a user closes an issue marked as **[TASK COMPLETED]** in a project repo.  
Cards are added to a live **Pokémon Binder** webpage hosted via GitHub Pages.

> DevOps meets nostalgia. Who says CI/CD can't be fun?

---

## 🚀 How it Works

1. A user creates an issue with their task.
2. They close it using the title prefix: **`[TASK COMPLETED]`**
3. This triggers the GitHub Action:
   - Mints a unique Pokémon card via the backend API
   - Injects the card into the `docs/index.html` binder
   - Commits the update and pushes to GitHub Pages
   - Comments on the issue to confirm

You earn a new Pokémon card every time you complete a task.  
Your binder grows. Your DevOps karma ascends.

---

## 📸 **Check out My Binder!**

👉 [View the Pokémon Binder](https://yourusername.github.io/your-repo-name/)
---

## 🛠️ Setup Instructions

1. **Visit this repo**
   https://github.com/JacobAV-src/PokeOps-User
   
2. Use the repo as a template  
   Click “Use this template” to create your own project using this setup.

3. **Enable GitHub Pages**  
   - Go to your repo → Settings → Pages  
   - Source: `docs/` folder on `main` branch

4. **Use the Issue Format**  
   - An Issue Template will be available to use.
   - Input your Devops related tasks (or Quests?) into the issue.
   - After you have finished your tasks, Close the Issue.

5. **Receive your card**
   - The Closing of the Issue will trigger a Github Action which will send the request to a hosted backend.
   - In around 1-2 minutes, you will receive a card in your docs/index.yaml file.

6. **View your binder**
   - You can view the index.yaml file via browser, Github Pages or other options.
