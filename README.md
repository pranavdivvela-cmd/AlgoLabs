# AlgoLabs: Linux terminal labs in your browser

[Open AlgoLabs in Codespaces](https://codespaces.new/xDarkPhoneix/AlgoLabs?quickstart=1)

Use the class Codespaces link from your instructor's email. Sign in with **your own GitHub account** and create or resume your own Codespace. One Codespace works for every lab. The labs run in its Linux terminal on Windows, Mac and Linux laptops.

## Labs

| Lab | Topic | Instructions |
|-----|-------|--------------|
| `lab4` | File permissions, SSH and remote file transfer | [labs/lab4/Experiment_Book_4_Draft.md](labs/lab4/Experiment_Book_4_Draft.md) |
| `lab5` | Bash automation and terminal workflows | [labs/lab5/Lab_Book.md](labs/lab5/Lab_Book.md) |

New labs appear in the `labs/` folder. If your Codespace already exists, get them with `git pull` at the repository root.

## Start

1. Download your personal access ZIP from your email (for example `Lab_4_studentNN_Access.zip`). Keep it zipped and private. The same ZIP works for every lab.
2. In the Codespace Explorer, right-click the `.uploads` folder and choose **Upload**, or drag the ZIP into that folder. Upload only your own ZIP.
3. Choose **Terminal > New Terminal**. At the repository root, run the start script with the lab you are doing:

```bash
bash start_lab.sh lab5
```

Without a lab name, it lists the labs and asks which one to open.

4. If asked, enter your roll number. Only some labs ask for it, and only the first time.
5. Open the lab's instructions (see the table above) and begin.

Setup installs your key outside the repository, sets private file permissions and prepares your lab folder. It opens a lab Bash terminal with SSH/SCP already configured. Your email attachment fixes your server account (for example `student03`). On the server, each lab has its own folder: `~/lab-work/lab4/`, `~/lab-work/lab5/` and so on.

Use `ssh lab-server` to connect. `exit` returns you to the Codespace; another `exit` closes the lab Bash session. To open a new session or switch labs, return to the repository root and run `bash start_lab.sh LAB` again. Saved work is kept.

After setup succeeds, you may delete the uploaded ZIP from `.uploads`. Keep the email attachment: if you rebuild or create a new Codespace and private storage is missing, upload the same ZIP again. Uploads, connection profiles and generated work are excluded from Git. Do not add your key or ZIP to a commit or share it publicly.

## Two machines

- **Codespace / local terminal:** your starting Linux machine, opened in the browser. Files here belong to the Codespace, rather than your physical laptop.
- **Lab server / server terminal:** the remote Linux machine after `ssh lab-server`.

Use `hostname`, `whoami` and `pwd` to identify where you are. All commands in the lab instructions use Bash, regardless of your laptop's operating system. You do not need to install Python, SSH or PowerShell tools on your laptop.

## Check your work

In the lab Bash terminal, run:

```bash
check_lab
```

This checks the lab the terminal was opened for. You can also name a lab: `check_lab lab5`. The graded tests run only on the server; your score and each attempt are recorded for your instructor. Grading never changes your files. On the server itself, run `check_lab lab5` (or the lab you are doing).

### Lab 4 notes

Lab 4 uses both machines. The start script asks for your roll number and opens the terminal in `lab-work/lab4-YOUR-ROLL/`. Run `check_lab` from that folder: it first prints ungraded hints about your Codespace files, then asks the server to grade `~/lab-work/lab4`. Use the filenames in the booklet: `work/project.zip` or `work/project.tar.gz`, server folder `challenge-delivery`, and downloaded report `work/permissions-report.txt`.

To submit the report from your physical laptop, find it under `lab-work/lab4-YOUR-ROLL/work/` in the Codespace Explorer, right-click it and choose **Download**. Submit through your normal class submission channel.

### Lab 5 notes

All Lab 5 work happens on the server. After `bash start_lab.sh lab5`, run:

```bash
ssh lab-server
cd ~/lab-work/lab5
```

Your server folder already contains the `events/` sample data and a copy of the instructions (`README.md`).

## If something goes wrong

Check the machine you are using, your current directory and the exact error.

- **No access ZIP found:** upload your emailed access-only ZIP into `.uploads` and keep it zipped.
- **More than one ZIP / different access:** keep only your own ZIP in `.uploads`. Setup preserves installed access and refuses to replace it with another account. Ask your instructor if you uploaded the wrong one.
- **Unknown lab:** run `git pull` at the repository root to get new labs, then try again.
- **Connection lost:** reconnect and return to your server lab folder. Saved server files remain there.
- **Login or server identity error:** send the exact error to your instructor, without attaching your private key publicly. Keep host-key checking enabled.
- **Original file changed:** keep the attempt and ask your instructor for help. Setup does not restore changed files.
- **Output already exists:** inspect it and move it to an unused backup name before repeating the step. Extract archives into a new folder.
- **Checker reports an extra line:** inspect the file before repeating an append command.

Use permission commands on your own lab files, without sudo. Stop your Codespace when finished to avoid using more compute time; keep it until you have downloaded and submitted your work.
