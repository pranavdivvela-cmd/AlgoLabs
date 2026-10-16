# Lab 7: Introduction to Git

**Environment:** the class lab server, reached from the terminal of your GitHub Codespace. Your account is `studentNNN` and your roll number is `RollNo`: replace them with your own account (in your ZIP's name, e.g. `student07`) and roll number (e.g. `2026001`) everywhere below.

## Objective

This lab introduces Git as a **local** version control system: you will track changes, inspect history and undo mistakes. Everything stays on your own machine (no GitHub, no `push`/`pull`). The lab ends with `git reset` and `git revert`.

By the end of the lab, you should be able to:

- Create and initialise a local Git repository (`git init`).
- Explain the three places a change can live: the **working tree**, the **staging area** and the **repository**.
- Track files and stage modifications (`git add`).
- Create meaningful commit snapshots (`git commit`).
- Compare changes in the working tree and the staging area (`git diff`, `git diff --staged`).
- Inspect history and individual commits (`git log`, `git show`).
- Discard unstaged changes in the working tree (`git restore`).
- Unstage changes and rewrite local history (`git reset --soft | --mixed | --hard`).
- Safely undo a commit that others already have (`git revert`).

---

## Setup: connect to the lab server

This is the same as in Lab 5 and Lab Test 1. The repository's `README.md` explains each step in more detail. Your access ZIP (`Lab_4_studentNNN_Access.zip`) is the one from your instructor's email; the same ZIP works for every lab.

1. Open your Codespace from the AlgoLabs repository (**Code → Codespaces**, or the link in the repository's `README.md`). Wait until a terminal appears at the bottom; if there is none, use **Terminal → New Terminal**.
2. If `~/Lab_4_studentNN_Access` does not exist yet in this Codespace, upload your ZIP into the `.uploads` folder (right-click it in the Explorer, **Upload…**) and unzip it:

   ```bash
   unzip -o .uploads/Lab_4_studentNN_Access.zip -d ~
   ```

3. Protect the key and connect:

   ```bash
   cd ~/Lab_4_studentNN_Access
   chmod 600 access/ssh_key
   ssh -i access/ssh_key studentNN@98.70.53.61
   ```

4. You are connected when the prompt shows `studentNN@students-lab`. Go to your lab folder and check that grading works:

   ```bash
   cd ~/lab-work/lab7
   check_lab lab7                                # 0/100 before you start; run it any time
   ```

> **Work on the server, not in the Codespace.** The Codespace also has Git, so commands will "work" there too, but only `~/lab-work/lab7` **on the server** is graded. Always check that your prompt shows `studentNN@students-lab`.

> **If you get stuck** with a repository in a bad state, you can start that repository again: `cd ~/lab-work/lab7 && rm -rf git-lab` (or `quickcart`) and redo its experiments. Nothing else is affected.

---

## Prerequisites

Check that Git is installed on the server:

```bash
git --version
```

Configure your Git identity **before your first commit**. Use your own name, and use exactly this e-mail address with **your roll number** in place of `RollNo` (for example `2026001@algolab.local`); it is how the grader knows the commits are yours:

```bash
git config --global user.name "Your Name"
git config --global user.email "RollNo@algolab.local"
```

Check the configuration:

```bash
git config --global --list
```

You should see `user.email=RollNo@algolab.local`.

> Git may print a hint about the default branch name when you run `git init`. You can ignore it: `master` and `main` both work for this lab.

---

# Experiment 1 — Create a Git Repository

## Goal

Create a new project directory and initialise it as a Git repository.

## Task

Create the directory `git-lab` inside your lab folder and enter it:

```bash
cd ~/lab-work/lab7
mkdir git-lab
cd git-lab
```

Initialise Git:

```bash
git init
```

Inspect the repository (`-a` also shows hidden entries):

```bash
ls -a
git status
```

Confirm that you are inside a Git working tree:

```bash
git rev-parse --is-inside-work-tree
```

Expected output:

```text
true
```

## Questions

1. What directory is created by `git init`?
2. Does `git status` show any files to commit?
3. What is the purpose of the `.git` directory? What would happen if you deleted it?

> ✅ **Check:** `git-lab` contains a Git repository. (Marks are given once it also has commits, after Experiment 3.)

---

# Experiment 2 — Create and Track Files

## Goal

Understand the difference between an **untracked** file and a **staged** file.

## Task

Create two files in `git-lab`:

- `README.md` containing the single line `Git Lab`
- `notes.txt` containing **at least three lines** of your own notes about Git

```bash
echo "Git Lab" > README.md
nano notes.txt          # write at least three lines, save with Ctrl+O, exit with Ctrl+X
```

Check the repository. Both files are listed under **Untracked files**:

```bash
git status
```

Add `README.md` to the staging area and check again:

```bash
git add README.md
git status
```

Now add `notes.txt` and check once more:

```bash
git add notes.txt
git status
```

Both files now appear under **Changes to be committed**.

## Questions

1. What changed in the `git status` output after `git add README.md`?
2. What is the difference between an untracked file and a staged file?
3. Has either file been committed yet?

> ✅ **Check:** nothing to save yet. Both files must be staged before you start Experiment 3.

---

# Experiment 3 — Create Your First Commit

## Goal

Create a permanent snapshot of the staged changes.

## Task

Commit the staged files:

```bash
git commit -m "Add initial project files"
```

Check the repository and inspect the commit:

```bash
git status
git log
```

## Questions

1. What information does `git log` display for each commit?
2. What is a commit?
3. Why should a commit message describe the change?

> ✅ **Check:** `git-lab` has at least one commit, and it contains `README.md` (with `Git Lab`) and `notes.txt`.

---

# Experiment 4 — Modify Files and Inspect Changes

## Goal

Learn how Git detects changes after a commit, and where each kind of `git diff` looks.

## Task

Add **two more lines** to `notes.txt` (so it has at least five lines).

Before staging the change, run:

```bash
git status
git diff
```

Stage the change:

```bash
git add notes.txt
```

Now compare both kinds of diff:

```bash
git diff
git diff --staged
```

Do **not** commit yet: you will commit this change in Experiment 5.

## Questions

1. What does `git diff` show before staging?
2. Why does `git diff` show nothing after staging?
3. What does `git diff --staged` show?
4. In your own words, what is the difference between the **working tree**, the **staging area** and the **repository**?

| Command             | Compares                            |
| :------------------ | :---------------------------------- |
| `git diff`          | working tree ↔ staging area         |
| `git diff --staged` | staging area ↔ last commit (`HEAD`) |
| `git diff HEAD`     | working tree ↔ last commit (`HEAD`) |

> ✅ **Check:** the committed `notes.txt` must end up with at least five non-empty lines (after Experiment 5).

---

# Experiment 5 — Create Multiple Commits

## Goal

Understand how a project grows through a sequence of small commits.

## Task

First commit the change you staged in Experiment 4, with a message that describes it, for example:

```bash
git commit -m "Add notes about git diff"
```

Then make **at least one more** meaningful change (for example, add a line to `README.md` describing the project) and commit it. For each change:

1. Modify a file.
2. Inspect the change (`git diff`).
3. Stage the change (`git add`).
4. Create a commit with a meaningful message.

```bash
git add .
git commit -m "Describe the project in README"
```

Inspect the history:

```bash
git log --oneline
```

You should now have at least **three** commits.

Every commit message must describe the change in at least two words. Avoid messages such as:

```text
update
changes
test
final
abc
```

> ✅ **Check:** at the end of the lab, `git-lab` has at least 5 commits (Experiment 8 adds two more) and **every** commit message has at least two words and is not one of the vague messages above.

---

# Experiment 6 — View Repository History

## Goal

Learn how to inspect previous versions of a project.

## Task

Run each of these and compare the output:

```bash
git log
git log --oneline
git log --oneline --graph
```

Inspect a particular commit, using a real commit ID from your `git log --oneline` output:

```bash
git show <commit-id>
```

You can also name commits relative to `HEAD`:

```bash
git show HEAD        # the latest commit
git show HEAD~1      # the commit before it
```

## Questions

1. What information is stored in a commit?
2. What is the advantage of `--oneline`?
3. What does `git show` display?

> ✅ **Check:** nothing new to save; this experiment only reads history.

---

# Experiment 7 — Restore Changes

## Goal

Learn how to discard changes that have not been committed.

## Task

Modify `notes.txt` (add any line), then look at the change:

```bash
git status
git diff
```

Discard the modification and check again:

```bash
git restore notes.txt
git status
```

`git status` reports `nothing to commit, working tree clean`.

## Questions

1. What does `git restore <file>` do to unstaged modifications in the working tree? Can you get them back?
2. What is the difference between `git restore <file>` and `git restore --staged <file>`?

> ✅ **Check:** at the end of the lab, both repositories have nothing staged and no modified tracked files (`git status` says _working tree clean_).

---

# Experiment 8 — Undo and Revert Commits (`git reset` and `git revert`)

## Goal

Undo commits in two different ways:

- `git reset` moves `HEAD` back and **rewrites** local history (`--soft`, `--mixed`, `--hard`).
- `git revert` **adds a new commit** that undoes an earlier one, without rewriting history.

---

## Part A — Reset Commit History (`git reset`)

`git reset` moves `HEAD` (your current branch) to another commit. Its three modes differ in what happens to the staging area (index) and the working tree:

| Mode                  | Moves `HEAD`? | Resets staging area?     | Changes working tree?           | Data safety     |
| :-------------------- | :------------ | :----------------------- | :------------------------------ | :-------------- |
| `--soft`              | Yes           | No (changes stay staged) | No (files untouched)            | Safe            |
| `--mixed` _(default)_ | Yes           | Yes (changes unstaged)   | No (files untouched)            | Safe            |
| `--hard`              | Yes           | Yes                      | Yes (discards uncommitted work) | **Destructive** |

You will practise all three modes on a throw-away **practice commit**, so that none of your real work is lost.

### 0. Create the practice commit

```bash
echo "Reset practice line" >> notes.txt
git add notes.txt
git commit -m "Practice commit for reset"
git log --oneline -n 3
```

### 1. Soft reset (`git reset --soft`)

Move `HEAD` back one commit but keep the change **staged**:

```bash
git reset --soft HEAD~1
git status            # the change is listed under "Changes to be committed"
git log --oneline -n 3
```

The commit is gone from the log, but its change is still staged. Commit it again directly (no `git add` needed):

```bash
git commit -m "Practice commit for reset (after soft reset)"
```

### 2. Mixed reset (`git reset --mixed`, the default)

Move `HEAD` back and **unstage** the change, but keep it in the working tree:

```bash
git reset --mixed HEAD~1
git status            # the change is listed under "Changes not staged for commit"
```

This time you must stage the change again before committing:

```bash
git add notes.txt
git commit -m "Practice commit for reset (after mixed reset)"
```

### 3. Hard reset (`git reset --hard`)

Move `HEAD` back, reset the staging area **and** discard the change from the working tree:

```bash
# WARNING: --hard permanently discards uncommitted work
git reset --hard HEAD~1
git status            # working tree clean
git log --oneline -n 3
cat notes.txt         # "Reset practice line" is gone
```

The practice commit has disappeared from `git log`. Git still remembers every move of `HEAD` in the **reflog**:

```bash
git reflog -n 8
```

You will see your three `reset: moving to HEAD~1` entries there.

---

## Part B — Safely Revert Commits (`git revert`)

`git reset` rewrites history, which is dangerous once others have your commits. `git revert` instead creates a **new commit** that applies the exact inverse of an existing commit.

### 1. Revert a specific commit

Create a commit to undo:

```bash
echo "Temporary feature line" >> notes.txt
git add notes.txt
git commit -m "Add temporary feature"
```

Revert it, keeping Git's default message:

```bash
git revert HEAD --no-edit
git log --oneline -n 3        # a new commit: Revert "Add temporary feature"
cat notes.txt                 # "Temporary feature line" is gone
git show HEAD                 # the revert removes exactly the line the feature added
```

### 2. Reading: resolving revert conflicts

You do not need to do this part; read it so you know what to do when it happens. If the commit you revert conflicts with later changes, Git stops and asks you to resolve the conflict:

```bash
git status                     # lists the conflicted file(s)
nano <file>                    # edit the file and remove the <<<<<<< ======= >>>>>>> markers
git add <file>                 # mark the conflict as resolved
git revert --continue          # finish the revert commit
```

To cancel and return to the state before the revert started:

```bash
git revert --abort
```

## Questions

1. What is the fundamental difference between `git reset` and `git revert`?
2. What are the three modes of `git reset`, and how does each one affect the staging area and the working tree?
3. Why is `git reset --hard` considered dangerous?
4. On a shared team branch, why is `git revert` preferred over `git reset`?
5. Which command aborts a `git revert` that stopped with a conflict?

> ✅ **Check (Part A):** the reflog shows at least three resets and your two commits _after soft reset_ and _after mixed reset_; no commit starting with `Practice commit` is left in the history, and `notes.txt` no longer contains `Reset practice line`.
>
> ✅ **Check (Part B):** the history contains `Add temporary feature` directly followed by its revert commit made by `git revert` (`Revert "Add temporary feature"`), and `notes.txt` no longer contains `Temporary feature line`.

---

# Experiment 9 — Final Challenge: The Friday Night Incident

## The Story

You have just joined **QuickCart**, a small online-shopping startup, as a developer. The team is building the user module of the app, which has three features:

| Feature     | Developer     |
| :---------- | :------------ |
| `login`     | You           |
| `logout`    | You           |
| `dashboard` | Riya (intern) |

QuickCart has one important rule:

> **Every commit is deployed straight to production.** Real customers use it within minutes.

It is **Friday, 6:00 PM**. Your `login` and `logout` features are live and working. Riya commits her `dashboard` feature and leaves for the weekend.

Five minutes later, the support channel explodes:

```text
[18:05] Customer: I can't log in!
[18:05] Customer: The logout button is broken.
[18:06] Customer: The dashboard won't open.
[18:07] CTO: EVERYTHING is down. Fix it now.
```

One new feature has taken down **all three**. You are on call. Your job is to find the bad commit, bring production back, and keep the team's history clean.

## How This Challenge Works

To keep the focus on Git, the "app" is a single text file named `app.txt`. Each line describes the state of one feature:

```text
login: working
logout: working
```

To "check production", you simply read the file:

```bash
cat app.txt
```

You will build features with `echo`. Remember the difference between the two redirection operators:

| Operator | Meaning                                         |
| :------- | :---------------------------------------------- |
| `>`      | **Overwrites** the file with the new line       |
| `>>`     | **Appends** the new line to the end of the file |

> Type every `echo` line and commit message **exactly** as shown: the grader compares them.

## Your Mission

| Act | What happens                                            | Git skill             |
| :-- | :------------------------------------------------------ | :-------------------- |
| 1   | Build `login` and `logout`                              | `add`, `commit`       |
| 2   | Riya commits `dashboard` and production crashes         | `diff`, `commit`      |
| 3   | Find the bad commit                                     | `log`, `show`, `diff` |
| 4   | Remove the dashboard from production                    | **`git revert`**      |
| 5   | Ship an improved `login`                                | `diff`, `commit`      |
| 6   | On Monday, Riya breaks it again, but only on her laptop | **`git reset`**       |
| 7   | Ship the dashboard properly                             | `status`, `add`       |

---

## Setup

Create a **new** repository for this challenge, next to `git-lab` (not inside it):

```bash
cd ~/lab-work/lab7
mkdir quickcart
cd quickcart
git init
```

---

## Act 1 — Build Login and Logout

### Step 1: The login feature

```bash
echo "login: working" > app.txt
cat app.txt
git add app.txt
git commit -m "Add login feature"
```

### Step 2: The logout feature

Append the logout feature with `>>`:

```bash
echo "logout: working" >> app.txt
```

Before committing, check exactly what changed:

```bash
git diff
```

Check production and commit:

```bash
cat app.txt
git add app.txt
git commit -m "Add logout feature"
```

**Production status:**

```text
login: working
logout: working
```

All good.

---

## Act 2 — The Dashboard Commit

Now you play **Riya**. She is in a hurry to leave for the weekend. Her dashboard needs a config file that she has on her own laptop but never added to the repository. She also makes a second mistake: she types `>` instead of `>>`.

```bash
echo "dashboard: CRASHED (config file missing)" > app.txt
```

She doesn't check `git diff` or test anything. She commits and leaves:

```bash
git add app.txt
git commit -m "Add user dashboard"
```

### Production is down

Switch back to being **you**, the on-call developer. Check production:

```bash
cat app.txt
```

```text
dashboard: CRASHED (config file missing)
```

`login` and `logout` are gone, and `dashboard` is crashing. **All three features are down.**

---

## Act 3 — Investigate: Find the Culprit

Good engineers don't guess. They read the history.

View the timeline:

```bash
git log --oneline
```

```text
c3c3c3c Add user dashboard        <-- deployed at 18:00, crashed at 18:05
b2b2b2b Add logout feature
a1a1a1a Add login feature
```

_(Your commit IDs will be different.)_

Inspect the suspect commit:

```bash
git show HEAD
```

Compare the last working version with the broken one:

```bash
git diff HEAD~1 HEAD
```

```diff
-login: working
-logout: working
+dashboard: CRASHED (config file missing)
```

The diff tells the whole story. The dashboard commit **deleted** the `login` and `logout` lines and added a broken `dashboard` line.

### Think About It

1. Riya only wanted to add a dashboard. Why did `login` and `logout` disappear?
2. Which commit is the **last known good** version?
3. Which command, run before `git commit`, would have shown Riya her mistake?

---

## Act 4 — Remove the Dashboard from Production (`git revert`)

### Why not use `git reset`?

You might be tempted to run `git reset --hard HEAD~1` and make the dashboard commit disappear. **Don't.**

The dashboard commit is already **in production**, and the rest of the team already has it. If you rewrite history:

- Your history no longer matches everyone else's.
- Your teammates get confusing conflicts the next time they sync.
- The record of what went wrong disappears, so the team cannot learn from it.

> **Rule:** once a commit has been shared, undo it with a **new** commit instead of erasing it. That is exactly what `git revert` does.

### Do It

Revert the dashboard commit:

```bash
git revert HEAD --no-edit
```

_(You can also revert by commit ID: `git revert <dashboard-commit-id> --no-edit`.)_

Check production:

```bash
cat app.txt
```

```text
login: working
logout: working
```

`login` and `logout` are back, and the broken dashboard is gone.

Now look at the history:

```bash
git log --oneline
```

```text
d4d4d4d Revert "Add user dashboard"   <-- the fix (a NEW commit)
c3c3c3c Add user dashboard            <-- still in the history
b2b2b2b Add logout feature
a1a1a1a Add login feature
```

**Nothing was deleted.** The history tells the full truth: the dashboard was added, it broke production, and it was reverted.

Inspect the revert commit and compare it with the dashboard commit:

```bash
git show HEAD
```

The revert commit is the exact **opposite** of the dashboard commit: every line that was removed is added back, and every line that was added is removed. Its message also records which commit it reverts (`This reverts commit …`).

```text
[18:21] You: Production is restored. The dashboard was rolled back with git revert.
[18:22] CTO: Great work.
```

---

## Act 5 — Improve Login

With production stable again, the CTO passes on a customer complaint:

> _"Users who type `Alice` instead of `alice` can't log in, and an empty password gives a confusing error. Can you fix that before Monday?"_

Ship the improvement **on top of** the revert. Rewrite the file with the improved login and keep logout unchanged:

```bash
echo "login: working (case-insensitive username, blocks empty password)" > app.txt
echo "logout: working" >> app.txt
```

> This time you are using `>` **on purpose**, because you are rewriting the whole file. Always check `git diff` afterwards to make sure you changed only what you meant to.

```bash
git diff
```

Only the `login` line should have changed. Check production and commit:

```bash
cat app.txt
git add app.txt
git commit -m "Improve login: case-insensitive username and empty-password check"
```

---

## Act 6 — Monday Morning (`git reset`)

On Monday, Riya feels terrible about Friday and tries the dashboard again. This time she correctly uses `>>`, but she **still** hasn't added the config file, so the dashboard still crashes.

There is one big difference from Friday:

> **She has NOT shared this commit.** It exists only on her laptop. Nobody else has it, and it has not reached production.

Play Riya again:

```bash
echo "dashboard: CRASHED (config file missing)" >> app.txt
git add app.txt
git commit -m "Add user dashboard (attempt 2)"
```

This time she checks before sharing:

```bash
cat app.txt
```

```text
login: working (case-insensitive username, blocks empty password)
logout: working
dashboard: CRASHED (config file missing)
```

The dashboard is still broken. Because the commit is **local and unshared**, she does not need a public "undo" commit. She can erase it as if it never happened. This is the job for `git reset`:

```bash
git reset --hard HEAD~1
```

Verify:

```bash
git status
git log --oneline
cat app.txt
```

Expected history:

```text
e5e5e5e Improve login: case-insensitive username and empty-password check
d4d4d4d Revert "Add user dashboard"
c3c3c3c Add user dashboard
b2b2b2b Add logout feature
a1a1a1a Add login feature
```

The "attempt 2" commit is gone, the working tree is clean, and production is unaffected.

> **Why `--hard`?** Riya wants to throw the broken attempt away completely. If she wanted to **keep her work and fix it**, she would use `git reset --soft HEAD~1` (changes stay staged) or `git reset --mixed HEAD~1` (changes stay in the working tree, unstaged).

---

## Act 7 — Ship the Dashboard Properly

Help Riya ship her feature the right way.

1. Create the missing config file:

   ```bash
   echo "widgets: Recent Orders, Wishlist, Recommended For You" > dashboard.config
   ```

2. Add the working dashboard to the app:

   ```bash
   echo "dashboard: working" >> app.txt
   ```

3. Run `git status`. `dashboard.config` appears as **untracked**. This is the warning Riya missed on Friday.

4. Review the changes:

   ```bash
   git diff
   cat app.txt
   ```

5. Stage **both** files and commit them together:

   ```bash
   git add app.txt dashboard.config
   git commit -m "Add user dashboard with widget config"
   ```

Final production status:

```text
login: working (case-insensitive username, blocks empty password)
logout: working
dashboard: working
```

---

## What Did We Learn?

| Situation                                 | Was the commit shared? | Right tool   | Why                                                                          |
| :---------------------------------------- | :--------------------- | :----------- | :--------------------------------------------------------------------------- |
| Friday: the dashboard broke production    | Yes                    | `git revert` | Adds a new "undo" commit, so history stays intact and the team stays in sync |
| Monday: the dashboard broke Riya's laptop | No                     | `git reset`  | Rewriting private history is safe and keeps the log clean                    |

**Golden rule:**

> **Revert** what others have already seen. **Reset** what only you have seen.

Lessons for the team:

1. **Run `git diff` before you commit.** It would have shown Riya that she was deleting `login` and `logout`.
2. **Run `git status` before you commit.** It shows files you forgot to add, such as a missing config file.
3. **Commit everything a feature needs together.** The code and its config belong in the same commit.
4. **Test before you share.** Riya's Monday mistake never reached production because she checked first.

---

## Questions

1. Why did `login` and `logout` disappear when Riya only added a dashboard?
2. After the `git revert` in Act 4, how many commits were in the history? Why did the number go **up** instead of down?
3. Why was `git reset` the wrong choice on Friday but the right choice on Monday?
4. In Act 6, what would `git status` show if Riya had used `git reset --soft HEAD~1` instead of `--hard`? What about `--mixed`?
5. Which two commands, run before `git commit` on Friday, could have prevented the whole incident?

## Finish

Run the grader and read any **FAIL** lines; each names the experiment it belongs to:

```bash
cd ~/lab-work/lab7
check_lab lab7
```

Type `exit` to disconnect. Your repositories stay on the server.
