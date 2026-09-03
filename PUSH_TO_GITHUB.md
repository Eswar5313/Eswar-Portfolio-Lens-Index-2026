# Push this repository to GitHub

## 1. Replace the placeholder handle
Search the whole folder for `YOUR-USERNAME` and replace it with your GitHub username (VS Code: Ctrl+Shift+H).
```bash
grep -rl "YOUR-USERNAME" . | xargs sed -i 's/YOUR-USERNAME/<your-username>/g'
```

## 2. Create the repository on GitHub
Name: **Eswar-Master-Project-Portfolio-2026** — Description: copy from `REPO_NAME_AND_DESCRIPTION.txt` (≤350 chars). Public. Do **not** initialise with a README.

## 3. Push
```bash
cd Eswar-Master-Project-Portfolio-2026
git init
git add .
git commit -m "Master project portfolio: dashboard + 83 project folders"
git branch -M main
git remote add origin https://github.com/<your-username>/Eswar-Master-Project-Portfolio-2026.git
git push -u origin main
```
Or with the GitHub CLI: `gh repo create Eswar-Master-Project-Portfolio-2026 --public --source=. --push`

## 4. Enable GitHub Pages
Settings → Pages → Source: *Deploy from a branch* → Branch **main** / folder **/ (root)** → Save.
The dashboard goes live at `https://YOUR-USERNAME.github.io/Eswar-Master-Project-Portfolio-2026/` in ~1 minute (`.nojekyll` is already present).

## 5. Drop your files in
For each project folder, open `FILES_TO_ADD.md`, copy the PDFs / .xlsx / .pptx / code into the matching sub-folder, then commit:
```bash
git add . && git commit -m "Add deliverables: <track> <project>" && git push
```
Large files: keep any single file under 100 MB (GitHub hard limit). For files 50–100 MB use Git LFS: `git lfs track "*.mp4"`.

## 6. Fill the Cyber placeholders
Folders `04-Codec-Technologies-EV-and-Cyber/CYBER-xx-Project` are named generically where the original titles were not on record. Rename each to the folder name from your Codec cyber repo and update the title in `projects.json`, then run `python build/generate.py` (kept in `_build/`) to regenerate the pages — or just edit the README/index.html titles by hand.

## 7. Link it everywhere
- CV / LinkedIn Featured: `https://YOUR-USERNAME.github.io/Eswar-Master-Project-Portfolio-2026/`
- GitHub profile README: add the repo to the featured-projects table.
