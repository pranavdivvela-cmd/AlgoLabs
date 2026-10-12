# AlgoLabs: Linux terminal labs in your browser

**[▶ Open AlgoLabs in Codespaces](https://codespaces.new/xDarkPhoneix/AlgoLabs?quickstart=1)**

All labs are graded on the class **lab server**. You log in to it with the private SSH key from your personal access ZIP.

- **Lab 5:** connect straight from your own laptop's terminal with `ssh -i` (see [Lab 5](#lab-5-connect-directly-with-your-key)).
- **Lab 4:** use a Linux terminal that runs in your browser (a GitHub Codespace), because the lab copies files between two machines.

Your access ZIP comes from your instructor's email, for example `Lab_4_student07_Access.zip`. One ZIP works for **every** lab. Keep it private: the file `access/ssh_key` inside it is your private key, and anyone who has it can log in as you.

## Labs

| Lab | Topic | Instructions |
|-----|-------|--------------|
| `lab4` | File permissions, SSH and remote file transfer | [labs/lab4/Experiment_Book_4_Draft.md](labs/lab4/Experiment_Book_4_Draft.md) |
| `lab5` | Bash automation and terminal workflows | [labs/lab5/Lab_Book.md](labs/lab5/Lab_Book.md) |

---

## Lab 5: connect directly with your key

Lab 5 needs no Codespace. You need a terminal with `ssh`: **Terminal** on Mac/Linux, **PowerShell** on Windows 10/11.

1. **Unzip your access ZIP** and open your terminal in the unzipped folder (for example `Lab_4_student07_Access`).
2. **Protect your key** (once). SSH refuses a private key that other users can read.

   ```bash
   chmod 600 access/ssh_key                                                  # Mac / Linux
   ```

   ```powershell
   icacls access\ssh_key /inheritance:r /grant:r "$($env:USERNAME):R"      # Windows PowerShell
   ```

3. **Log in** (replace `studentNN` with your account, shown in the ZIP's `README.md`):

   ```bash
   ssh -i access/ssh_key studentNN@98.70.53.61
   ```

   The first time, SSH shows the server's fingerprint and asks whether to continue. Type `yes` only if it matches the fingerprint in your ZIP's `README.md`.

4. **Do the lab on the server:**

   ```bash
   cd ~/lab-work/lab5          # your Lab 5 folder: sample data and README.md are here
   check_lab lab5              # see your score at any time
   ```

Follow [labs/lab5/Lab_Book.md](labs/lab5/Lab_Book.md). The same instructions are also in `README.md` in your server folder. Each part ends with a **✅ Check** box that tells you which evidence files to save. Type `exit` to disconnect; your files stay on the server. Next time, repeat step 3 only.

---

## Lab 4: first time, set up a Codespace (about 2 minutes)

You need:

- your own GitHub account
- your personal access ZIP (see above)

Steps:

1. **Open the Codespace.** Click the link at the top, sign in to GitHub and choose **Create codespace**. Wait until the editor and terminal appear.
2. **Upload your ZIP.** In the file Explorer on the left, right-click the **`.uploads`** folder and choose **Upload…**, then pick your ZIP. Do **not** unzip it.
3. **Start a lab.** In the terminal at the bottom (or **Terminal → New Terminal**), type the lab you are doing:

   ```bash
   bash start_lab.sh lab4
   ```

4. **Roll number.** If asked, type the roll number registered with your instructor. It is asked only once.

When setup finishes, the prompt changes to something like:

```text
[Lab 4 Codespace] vscode@codespaces-abc123:~$
```

This is your **lab terminal**. In it, `ssh`, `scp` and `check_lab` already know your account and key.

---

## Lab 4: every time, do the lab

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
| How to get there | Lab 4: `bash start_lab.sh lab4` | Lab 5: `ssh -i access/ssh_key studentNN@98.70.53.61` from your laptop. Lab 4: `ssh lab-server` from the lab terminal |
| Prompt starts with | `[Lab 4 Codespace]` | `studentNN@students-lab` |
| Your lab folder | `lab-work/…` in the repository | `~/lab-work/lab4`, `~/lab-work/lab5`, … |
| To leave | `exit` closes the lab terminal | `exit` takes you back to where you connected from |

When unsure, run `hostname`, `whoami` and `pwd`.

---

## Check your score

```bash
check_lab lab5      # on the server: name the lab
check_lab           # in the Lab 4 Codespace terminal: checks the lab it was opened for
```

- Grading runs on the server, and the tests are hidden.
- You can check as often as you like. Every attempt is recorded for your instructor.
- Checking never changes your files.
- Read the **FAIL** lines: each one names the ✅ Check it belongs to.

---

## Coming back later

- **Lab 5:** log in again with the same `ssh -i …` command. Your work is on the server.
- **Lab 4, same Codespace:** open it from [github.com/codespaces](https://github.com/codespaces), then run `bash start_lab.sh LAB` again. Your saved work is still there, on both machines.
- **Switching labs:** run `exit` until you are back at the normal terminal, then `bash start_lab.sh` with the other lab.
- **A new lab was announced:** run `git pull` in the repository root to get it.
- **New or rebuilt Codespace:** upload the same ZIP from your email again. Your work on the server is kept.

---

## If something goes wrong

| Problem | What to do |
|---|---|
| `UNPROTECTED PRIVATE KEY FILE` or `bad permissions` (Lab 5) | Protect the key with `chmod 600` or `icacls` (step 2 of Lab 5), then log in again. |
| `Identity file access/ssh_key not accessible` (Lab 5) | Your terminal is not in the unzipped folder. `cd` into it, or give the full path after `-i`. |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | Stop. Do not type `yes` or delete anything. Send the exact message to your instructor. |
| `No access ZIP found` (Lab 4) | Upload your ZIP into `.uploads` (keep it zipped), then run the start command again. |
| `More than one access ZIP` or `different access` | Keep only **your own** ZIP in `.uploads`. If you uploaded someone else's, ask your instructor. |
| `Unknown lab` | Run `git pull` in the repository root, then try again. |
| `Could not resolve hostname lab-server` or `check_lab: command not found` | You are not in the lab terminal. Run `bash start_lab.sh LAB` from the repository root. |
| Connection lost / frozen terminal | Open a new terminal and connect again (Lab 5: the `ssh -i …` command; Lab 4: `bash start_lab.sh lab4`, then `ssh lab-server`). Saved files are kept. |
| `Host key verification failed` or `Permission denied (publickey)` | Do not change any SSH settings. Send the exact error to your instructor (**never** send your key or ZIP). |
| A file already exists, or a check says "extra line" | Look at the file first (`cat FILE`). Appending (`>>`) twice adds lines twice. Recreate the file, then try again. |
| Lab 4: "original file changed" | Keep your attempt and ask your instructor. Setup never restores changed files. |

---

## Rules

- Use only **your own** ZIP, account and roll number.
- Never commit, share or post your ZIP or key. Uploads and keys are already kept out of Git.
- Work only on your own lab files. Do not use `sudo`.
- Lab 4: when you are done, **stop your Codespace** to save your free hours: [github.com/codespaces](https://github.com/codespaces) → **⋯** → **Stop codespace**. Keep it until you have submitted your work.
