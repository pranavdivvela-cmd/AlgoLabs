# AlgoLabs: Linux terminal labs

All labs are graded on the class **lab server**. You log in to it with the private SSH key from your personal access ZIP, straight from your own laptop's terminal with `ssh -i` (see [Lab 5](#lab-5-connect-directly-with-your-key)).

Your access ZIP comes from your instructor's email, for example `Lab_4_student07_Access.zip`. One ZIP works for **every** lab. Keep it private: the file `access/ssh_key` inside it is your private key, and anyone who has it can log in as you.

## Labs

| Lab | Topic | Instructions |
|-----|-------|--------------|
| `lab4` | File permissions, SSH and remote file transfer | [labs/lab4/Experiment_Book_4_Draft.md](labs/lab4/Experiment_Book_4_Draft.md) |
| `lab5` | Bash automation and terminal workflows | [labs/lab5/Lab_Book.md](labs/lab5/Lab_Book.md) |

---

## Lab 5: connect directly with your key

Lab 5 needs just a terminal on your own computer: **Terminal** on Mac or Linux.

> **Your private key is a file:** `access/ssh_key` inside your access ZIP. You give SSH the file's **location** with `-i`. Do **not** open the key and paste its text into the terminal: that fails and exposes your key.

**1. Unzip your access ZIP.** You get a folder such as `Lab_4_student07_Access` that contains `README.md` and an `access` folder with your key `ssh_key`.

**2. Open a terminal inside that folder.**

- **Mac:** open Terminal, type `cd ` (with a space), drag the folder into the window, press Enter.
- **Linux:** right-click the folder and choose **Open in Terminal**.

Check that you are in the right place: `ls access` must list `ssh_key`.

**3. Protect your key** (first time only). SSH refuses a key that other users of your computer can read.

```bash
chmod 600 access/ssh_key                                                  # Mac / Linux
```

**4. Connect.** Replace `studentNN` with your account (it is in your ZIP's `README.md`, which also has this exact command):

```bash
ssh -i access/ssh_key studentNN@98.70.53.61
```

The first time, SSH asks `Are you sure you want to continue connecting?`. Type `yes` only if the fingerprint shown matches the one in your ZIP's `README.md`. You are connected when the prompt shows `studentNN@students-lab:~$`.

**5. Do the lab on the server:**

```bash
cd ~/lab-work/lab5          # your Lab 5 folder: sample data and README.md are here
check_lab lab5              # see your score at any time
```

Follow [labs/lab5/Lab_Book.md](labs/lab5/Lab_Book.md). The same instructions are also in `README.md` in your server folder. Each part ends with a **✅ Check** box that tells you which evidence files to save. Type `exit` to disconnect; your files stay on the server.

**Next time:** open a terminal in the same folder (step 2) and run the step 4 command.

---

## Check your score

```bash
check_lab lab5      # on the server: name the lab
```

- Grading runs on the server, and the tests are hidden.
- You can check as often as you like. Every attempt is recorded for your instructor.
- Checking never changes your files.
- Read the **FAIL** lines: each one names the ✅ Check it belongs to.

---

## Coming back later

- Log in again with the same `ssh -i …` command. Your work is on the server.

---

## If something goes wrong

| Problem | What to do |
|---|---|
| `UNPROTECTED PRIVATE KEY FILE` or `bad permissions` (Lab 5) | Protect the key with `chmod 600` (step 3 of Lab 5), then log in again. |
| `Identity file access/ssh_key not accessible` (Lab 5) | Your terminal is not in the unzipped folder: redo step 2, or give the key's full path, e.g. `ssh -i ~/Downloads/Lab_4_student07_Access/access/ssh_key student07@98.70.53.61`. |
| `Identity file b3BlbnNzaC1rZXkt… not accessible` (or `-----BEGIN…`), or bash says `command not found` for lines of letters (Lab 5) | You pasted the key's **text**. Use the file path `access/ssh_key` instead, and tell your instructor so they can give you a new key. |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | Stop. Do not type `yes` or delete anything. Send the exact message to your instructor. |
| Connection lost / frozen terminal | Open a new terminal and connect again (the `ssh -i …` command). Saved files are kept. |
| `Host key verification failed` or `Permission denied (publickey)` | Do not change any SSH settings. Send the exact error to your instructor (**never** send your key or ZIP). |
| A file already exists, or a check says "extra line" | Look at the file first (`cat FILE`). Appending (`>>`) twice adds lines twice. Recreate the file, then try again. |

---

## Rules

- Use only **your own** ZIP, account and roll number.
- Never commit, share or post your ZIP or key. Uploads and keys are already kept out of Git.
- Work only on your own lab files. Do not use `sudo`.
