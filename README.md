# AlgoLabs: Linux terminal labs in your browser

**[▶ Open AlgoLabs in Codespaces](https://codespaces.new/xDarkPhoneix/AlgoLabs?quickstart=1)**

You do these labs in a Linux terminal that runs in your browser (a GitHub Codespace). From there you connect to the class **lab server**, where your work is graded. It works the same on Windows, Mac and Linux. You do not need to install anything on your laptop.

## Labs

| Lab | Topic | Instructions |
|-----|-------|--------------|
| `lab4` | File permissions, SSH and remote file transfer | [labs/lab4/Experiment_Book_4_Draft.md](labs/lab4/Experiment_Book_4_Draft.md) |
| `lab5` | Bash automation and terminal workflows | [labs/lab5/Lab_Book.md](labs/lab5/Lab_Book.md) |

---

## First time: set up (about 2 minutes)

You need:

- your own GitHub account
- your personal access ZIP from your instructor's email, for example `Lab_4_student07_Access.zip`. One ZIP works for **every** lab. Keep it private.

Steps:

1. **Open the Codespace.** Click the link at the top, sign in to GitHub and choose **Create codespace**. Wait until the editor and terminal appear.
2. **Upload your ZIP.** In the file Explorer on the left, right-click the **`.uploads`** folder and choose **Upload…**, then pick your ZIP. Do **not** unzip it.
3. **Start a lab.** In the terminal at the bottom (or **Terminal → New Terminal**), type the lab you are doing:

   ```bash
   bash start_lab.sh lab5
   ```

   If you leave out the lab name, it shows the list of labs and asks you to choose.
4. **Roll number (Lab 4 only).** If asked, type the roll number registered with your instructor. It is asked only once.

When setup finishes, the prompt changes to something like:

```text
[Lab 5 Codespace] vscode@codespaces-abc123:~$
```

This is your **lab terminal**. In it, `ssh`, `scp` and `check_lab` already know your account and key.

---

## Every time: do the lab

### Lab 5: all work is on the server

```bash
bash start_lab.sh lab5      # open the lab terminal (from the repository root)
ssh lab-server              # log in to the lab server
cd ~/lab-work/lab5          # your Lab 5 folder: sample data and README.md are here
check_lab lab5              # see your score at any time
```

Follow [labs/lab5/Lab_Book.md](labs/lab5/Lab_Book.md). The same instructions are also in `README.md` in your server folder. Each part ends with a **✅ Check** box that tells you which evidence files to save.

### Lab 4: you use both machines

```bash
bash start_lab.sh lab4      # opens the lab terminal in lab-work/lab4-YOUR-ROLL/
```

Follow [labs/lab4/Experiment_Book_4_Draft.md](labs/lab4/Experiment_Book_4_Draft.md). Some steps happen in the Codespace and some on the server (`ssh lab-server`, folder `~/lab-work/lab4`). Use the exact file names from the booklet: `work/project.zip` or `work/project.tar.gz`, the server folder `challenge-delivery`, and `work/permissions-report.txt`.

Run `check_lab` from your Codespace Lab 4 folder. It first prints **hints** about your Codespace files (these are not graded), then the server grades your work.

To submit the report file, find it under `lab-work/lab4-YOUR-ROLL/work/` in the Explorer, right-click it and choose **Download**.

---

## Know which machine you are on

| | Codespace (your starting machine) | Lab server |
|---|---|---|
| How to get there | `bash start_lab.sh LAB` | `ssh lab-server` from the lab terminal |
| Prompt starts with | `[Lab 5 Codespace]` | `studentNN@students-lab` |
| Your lab folder | `lab-work/…` in the repository | `~/lab-work/lab4`, `~/lab-work/lab5`, … |
| To leave | `exit` closes the lab terminal | `exit` takes you back to the Codespace |

When unsure, run `hostname`, `whoami` and `pwd`.

---

## Check your score

```bash
check_lab           # checks the lab this terminal was opened for
check_lab lab5      # or name the lab (works on the server too)
```

- Grading runs on the server, and the tests are hidden.
- You can check as often as you like. Every attempt is recorded for your instructor.
- Checking never changes your files.
- Read the **FAIL** lines: each one names the ✅ Check it belongs to.

---

## Coming back later

- **Same Codespace:** open it from [github.com/codespaces](https://github.com/codespaces), then run `bash start_lab.sh LAB` again. Your saved work is still there, on both machines.
- **Switching labs:** run `exit` until you are back at the normal terminal, then `bash start_lab.sh` with the other lab.
- **A new lab was announced:** run `git pull` in the repository root to get it.
- **New or rebuilt Codespace:** upload the same ZIP from your email again. Your work on the server is kept.

---

## If something goes wrong

| Problem | What to do |
|---|---|
| `No access ZIP found` | Upload your ZIP into `.uploads` (keep it zipped), then run the start command again. |
| `More than one access ZIP` or `different access` | Keep only **your own** ZIP in `.uploads`. If you uploaded someone else's, ask your instructor. |
| `Unknown lab` | Run `git pull` in the repository root, then try again. |
| `Could not resolve hostname lab-server` or `check_lab: command not found` | You are not in the lab terminal. Run `bash start_lab.sh LAB` from the repository root. |
| Connection lost / frozen terminal | Open a new terminal and run `bash start_lab.sh LAB`, then `ssh lab-server` again. Saved files are kept. |
| `Host key verification failed` or `Permission denied (publickey)` | Do not change any SSH settings. Send the exact error to your instructor (**never** send your key or ZIP). |
| A file already exists, or a check says "extra line" | Look at the file first (`cat FILE`). Appending (`>>`) twice adds lines twice. Recreate the file, then try again. |
| Lab 4: "original file changed" | Keep your attempt and ask your instructor. Setup never restores changed files. |

---

## Rules

- Use only **your own** ZIP, account and roll number.
- Never commit, share or post your ZIP or key. Uploads and keys are already kept out of Git.
- Work only on your own lab files. Do not use `sudo`.
- When you are done, **stop your Codespace** to save your free hours: [github.com/codespaces](https://github.com/codespaces) → **⋯** → **Stop codespace**. Keep it until you have submitted your work.
