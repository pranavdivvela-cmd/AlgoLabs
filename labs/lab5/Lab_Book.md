# Bash Automation & Terminal Workflows

Welcome to the **Bash Automation & Terminal Workflows Lab**.

In this lab, you will move from running individual Linux commands to building a **reusable Bash automation script**.

You will learn how Bash stores values, finds commands, reports success or failure, handles output and errors, and finally how to combine these concepts into a useful automation workflow.

---

## Learning Objectives

By the end of this lab, you should be able to:

- Create and use Bash variables.
- Use variables as command arguments.
- Understand why quoting matters in Bash.
- Understand how `$PATH` is used to locate commands.
- Use `command -v` to find commands.
- Understand command exit status.
- Use `$?` to inspect the previous command's status.
- Use `&&` and `||` for conditional execution.
- Understand `stdout` and `stderr`.
- Redirect output using:
  - `>`
  - `>>`
  - `2>`
  - `2>&1`
- Create and execute Bash scripts.
- Pass arguments to scripts using `$1`.
- Validate directories and files.
- Use arrays.
- Use `for` loops.
- Build a reusable automation script.
- Handle errors instead of assuming commands always succeed.

---

# Lab Scenario

Imagine that you are working as a junior engineer for an event-management team.

Every event has its own directory containing important information:

```text
events/
├── campus-day/
│   ├── notes.txt
│   ├── registrations.txt
│   └── budget.txt
│
├── sports-day/
│   ├── notes.txt
│   ├── registrations.txt
│   └── budget.txt
│
└── tech-fest/
    ├── notes.txt
    ├── registrations.txt
    └── budget.txt
```

The team currently performs several commands manually:

```bash
ls events/campus-day
wc -l events/campus-day/registrations.txt
wc -l events/campus-day/budget.txt
```

This works once.

But what happens when there are:

- 10 events?
- 50 events?
- Different folder names?
- Missing files?
- Incorrect input?

Instead of repeating commands manually, we will build a **reusable Bash automation script**.

---

# Lab Roadmap

You will complete the lab in the following stages:

```text
Variables
   ↓
Quoting
   ↓
PATH
   ↓
Exit Status
   ↓
&& / ||
   ↓
stdout / stderr
   ↓
Redirection
   ↓
First Bash Script
   ↓
Script Arguments
   ↓
Input Validation
   ↓
Arrays
   ↓
Loops
   ↓
Complete Automation Script
   ↓
Final Challenge
```

---

# Getting Started

## 1. Check Bash

Run:

```bash
bash --version
```

You should see the installed Bash version.

---

## 2. Check your current directory

Run:

```bash
pwd
```

Then:

```bash
ls
```

Make sure you are inside the lab directory.

---

## 3. Go to your lab folder

Do **all** work for this lab inside your lab folder:

```bash
cd ~/lab-work/lab5
mkdir -p evidence
```

---

## How checking works

Run this at any time to see your progress:

```bash
check_lab lab5
```

Each part below ends with a **✅ Check** box. It tells you which files to save and what `check_lab` looks at.

Important rules:

- `check_lab` only looks at **files** in `~/lab-work/lab5`. It does not see your terminal history.
- Later parts change `report.sh` and `handover.txt`. That is why some checks ask you to **copy a snapshot** into `evidence/`. Take the snapshot at the end of that part, not later.
- Save evidence with the exact commands shown. Do not edit evidence files by hand.
- If you redo a part, rerun **all** of its evidence commands so files are not appended twice.

### ✅ Check 0 — Getting started

```bash
bash --version | head -n 1 > evidence/00-bash-version.txt
pwd > evidence/00-pwd.txt
```

`check_lab` verifies:

- `evidence/00-bash-version.txt` starts with `GNU bash, version`.
- `evidence/00-pwd.txt` is exactly your lab folder: `/home/<your-account>/lab-work/lab5`.

---

# Part 1 — Bash Variables

A Bash variable is a name that stores a value in the current shell.

Example:

```bash
folder="campus-day"
```

Read the value using:

```bash
echo "$folder"
```

The important syntax is:

```text
variable="value"
```

There must be **no spaces around `=`**.

### Task 1

Create:

```bash
folder="campus-day"
```

Then run:

```bash
echo "$folder"
```

Expected output:

```text
campus-day
```

Now change the variable:

```bash
folder="sports-day"
```

and run:

```bash
echo "$folder"
```

### Questions

1. What value is stored in `folder`?
2. What happens when you change the variable?
3. Does changing the variable rename or create a directory?

### ✅ Check 1 — Variables

```bash
folder="campus-day"
echo "$folder" > evidence/01-variable.txt
folder="sports-day"
echo "$folder" >> evidence/01-variable.txt
```

`check_lab` verifies:

- `evidence/01-variable.txt` contains exactly two lines: `campus-day`, then `sports-day`.

---

# Part 2 — Using Variables in Commands

Variables become useful when they are passed to commands.

Example:

```bash
folder="campus-day"

ls "$folder"
```

You can also use a variable as part of a path:

```bash
wc -l "$folder/registrations.txt"
```

This allows the same commands to work with different folders.

The lecture demonstrates this idea by changing the value of `folder` while keeping the commands unchanged.

### Task 2

Create two event directories:

```bash
mkdir -p campus-day
mkdir -p sports-day
```

Create files:

```bash
touch campus-day/registrations.txt
touch sports-day/registrations.txt
```

Now run:

```bash
folder="campus-day"
ls "$folder"
```

Change:

```bash
folder="sports-day"
```

and run:

```bash
ls "$folder"
```

### Think

Why is using a variable better than writing:

```bash
ls campus-day
```

everywhere?

### ✅ Check 2 — Variables in commands

```bash
folder="campus-day"
ls "$folder" > evidence/02-ls.txt
folder="sports-day"
ls "$folder" >> evidence/02-ls.txt
```

`check_lab` verifies:

- `campus-day/` and `sports-day/` are folders.
- `campus-day/registrations.txt` and `sports-day/registrations.txt` exist.
- `evidence/02-ls.txt` contains `registrations.txt` twice (one line per folder).

---

# Part 3 — Why Quoting Matters

Consider a folder containing a space:

```text
campus day
```

Create it:

```bash
mkdir -p "campus day"
```

Now:

```bash
folder="campus day"
```

Compare:

```bash
ls "$folder"
```

with:

```bash
ls $folder
```

and:

```bash
ls '$folder'
```

### Important

Double quotes:

```bash
"$folder"
```

expand the variable while keeping the value together as one argument.

Single quotes:

```bash
'$folder'
```

prevent variable expansion.

The lecture specifically uses this example to demonstrate why quoting matters.

### Task 3

For each command, predict the result **before running it**.

```bash
folder="campus day"

ls "$folder"
ls $folder
ls '$folder'
```

Record your observations.

### ✅ Check 3 — Quoting

First put a file inside the folder so `ls` has something to show:

```bash
touch "campus day/agenda.txt"
```

Then save the output (and errors) of all three forms:

```bash
folder="campus day"
ls "$folder" > evidence/03-double-quotes.txt 2>&1
ls $folder   > evidence/03-no-quotes.txt 2>&1
ls '$folder' > evidence/03-single-quotes.txt 2>&1
```

`check_lab` verifies:

- `campus day/` (with a space) is a folder containing `agenda.txt`.
- `evidence/03-double-quotes.txt` is exactly `agenda.txt`.
- `evidence/03-no-quotes.txt` shows that `ls` looked for **two** names, `campus` and `day`, and could not find them.
- `evidence/03-single-quotes.txt` shows that `ls` looked for the literal name `$folder`.

---

# Part 4 — Understanding `$PATH`

Bash needs to know where executable commands are located.

Run:

```bash
echo "$PATH"
```

You may see something similar to:

```text
/usr/local/bin:/usr/bin:/bin
```

The directories are separated using `:`.

Bash searches these directories in order.

---

## Finding a Command

Use:

```bash
command -v python3
```

You can also check:

```bash
command -v bash
command -v ls
command -v grep
```

The lecture uses `command -v` to demonstrate how Bash resolves command names.

---

## Task 4 — Create Your Own Command

Inside your lab folder, create:

```bash
mkdir -p bin
```

Create:

```bash
nano bin/hello.sh
```

Add:

```bash
#!/usr/bin/env bash

echo "Hello from my custom command!"
```

Save the file.

Make it executable:

```bash
chmod +x bin/hello.sh
```

Now run:

```bash
./bin/hello.sh
```

Then add your directory to `PATH` (run this from `~/lab-work/lab5`):

```bash
export PATH="$PWD/bin:$PATH"
```

Now run:

```bash
command -v hello.sh
```

Finally:

```bash
hello.sh
```

### Question

Why does:

```bash
hello.sh
```

work after modifying `PATH`?

### ✅ Check 4 — PATH and your own command

In the same terminal where you ran `export PATH=...`:

```bash
command -v bash     > evidence/04-bash-path.txt
command -v hello.sh > evidence/04-hello-path.txt
hello.sh            > evidence/04-hello-output.txt
```

`check_lab` verifies:

- `bin/hello.sh` is executable (made with `chmod +x`), starts with `#!/usr/bin/env bash` and prints the greeting.
- `evidence/04-bash-path.txt` is a full path to `bash`, such as `/usr/bin/bash`.
- `evidence/04-hello-path.txt` is exactly `/home/<your-account>/lab-work/lab5/bin/hello.sh`.
- `evidence/04-hello-output.txt` is exactly `Hello from my custom command!`.

> If `command -v hello.sh` prints nothing, your `PATH` change was lost (for example, you opened a new terminal). Run the `export` command again.

---

# Part 5 — Exit Status

Every command returns a numeric exit status.

Generally:

```text
0       → success
non-zero → another outcome/failure
```

Example:

```bash
ls /etc
echo "$?"
```

Now:

```bash
ls /does-not-exist
echo "$?"
```

The special variable:

```bash
$?
```

contains the exit status of the **previous command**.

This distinction is important because every subsequent command can replace `$?`.

---

## Task 5

Run:

```bash
ls /etc
echo "$?"
```

Then:

```bash
ls /does-not-exist
echo "$?"
```

Then:

```bash
echo "Hello"
echo "$?"
```

### Question

What happened to the previous exit status after running another command?

### ✅ Check 5 — Exit status

Save only the status numbers (the normal output is thrown away with `/dev/null`):

```bash
ls /etc > /dev/null;                echo "$?" >  evidence/05-status.txt
ls /does-not-exist 2> /dev/null;    echo "$?" >> evidence/05-status.txt
echo "Hello" > /dev/null;           echo "$?" >> evidence/05-status.txt
```

`check_lab` verifies:

- `evidence/05-status.txt` has exactly three lines: `0`, a non-zero number (`2` for `ls`), then `0` again.

---

# Part 6 — `&&`

The `&&` operator runs the second command **only when the first command succeeds**.

Example:

```bash
mkdir handover && echo "Directory created"
```

Conceptually:

```text
command succeeds?
       |
      yes
       ↓
run next command
```

If the first command fails, the second command does not execute.

The lecture demonstrates this behavior using `mkdir` and `cp`.

### Task 6

Try:

```bash
mkdir test && echo "Success"
```

Then run it again:

```bash
mkdir test && echo "Success"
```

Observe what happens.

### ✅ Check 6 — `&&`

Remove the folder from your experiment, then repeat it with the message saved to a file:

```bash
rmdir test      # skip this line if test/ does not exist yet
mkdir test && echo "Success" >> evidence/06-and.txt
mkdir test && echo "Success" >> evidence/06-and.txt
```

The second `mkdir` fails, so its `echo` must not run.

`check_lab` verifies:

- `test/` is a folder.
- `evidence/06-and.txt` contains `Success` exactly **once**.

---

# Part 7 — `||`

The `||` operator runs the second command when the first command returns a non-zero status.

Example:

```bash
cat missing.txt || echo "Could not read the file"
```

Conceptually:

```text
command succeeds?
       |
      no
       ↓
run fallback command
```

### Task 7

Run:

```bash
cat missing.txt || echo "File could not be read"
```

Then:

```bash
cat /etc/hosts || echo "Could not read hosts file"
```

### Question

Why does the second command execute in the first example but not necessarily the second?

### ✅ Check 7 — `||`

```bash
cat missing.txt              || echo "File could not be read"    >> evidence/07-or.txt
cat /etc/hosts > /dev/null   || echo "Could not read hosts file" >> evidence/07-or.txt
```

`check_lab` verifies:

- `missing.txt` does not exist in your lab folder.
- `evidence/07-or.txt` contains exactly one line: `File could not be read`.

---

# Part 8 — stdout and stderr

Commands can produce two important types of output.

### stdout

Normal program output.

Stream number:

```text
1
```

### stderr

Error and diagnostic messages.

Stream number:

```text
2
```

The lecture demonstrates this using a command that receives both an existing and a missing file.

---

## Task 8

Create:

```bash
touch notes.txt
```

Then run:

```bash
ls notes.txt missing.txt
```

Observe the output.

Ask yourself:

> Which output is normal output and which is an error?

### ✅ Check 8 — stdout and stderr

There is nothing extra to save here; Parts 9–11 capture these two streams into files.

`check_lab` verifies:

- `notes.txt` exists in your lab folder and is empty.
- `missing.txt` still does not exist.

---

# Part 9 — Redirect stdout

Use:

```bash
>
```

Example:

```bash
ls notes.txt missing.txt > listing.txt
```

Now:

```bash
cat listing.txt
```

The normal output was redirected to:

```text
listing.txt
```

But what happened to the error?

### ✅ Check 9 — Redirect stdout

`listing.txt` is reused in Part 10, so keep a snapshot:

```bash
cp listing.txt evidence/09-listing.txt
```

`check_lab` verifies:

- `evidence/09-listing.txt` is exactly `notes.txt` (the error message is **not** in it).

---

# Part 10 — Redirect stderr

Use:

```bash
2>
```

Example:

```bash
ls notes.txt missing.txt > listing.txt 2> errors.txt
```

Now inspect:

```bash
cat listing.txt
```

and:

```bash
cat errors.txt
```

You have separated:

```text
stdout → listing.txt
stderr → errors.txt
```

This is an important technique for automation and logging.

### ✅ Check 10 — Redirect stderr

The files from the example are the evidence. Leave them in place.

`check_lab` verifies:

- `listing.txt` is exactly `notes.txt`.
- `errors.txt` is one line: the `ls` error about `missing.txt` (`No such file or directory`).
- `errors.txt` does **not** contain the normal output.

---

# Part 11 — Combine stdout and stderr

Use:

```bash
2>&1
```

Example:

```bash
ls notes.txt missing.txt > run.log 2>&1
```

Now:

```bash
cat run.log
```

Both normal output and errors are stored in:

```text
run.log
```

The order matters:

```bash
> run.log 2>&1
```

first redirects stdout, then sends stderr to stdout's current destination.

### ✅ Check 11 — Combine stdout and stderr

Also try the **wrong** order, to see why the order matters:

```bash
ls notes.txt missing.txt 2>&1 > wrong-order.log
```

The error appears on your screen, and `wrong-order.log` only gets the normal output.

`check_lab` verifies:

- `run.log` has exactly two lines: one containing `notes.txt` and one containing the `missing.txt` error.
- `wrong-order.log` is exactly `notes.txt`.

---

# Part 12 — Your First Bash Script

Create:

```bash
report.sh
```

Start with:

```bash
#!/usr/bin/env bash
```

This is called the **shebang**.

Add:

```bash
folder="campus-day"

ls "$folder" > handover.txt
wc -l "$folder/registrations.txt" >> handover.txt
```

Make it executable:

```bash
chmod +x report.sh
```

Run:

```bash
./report.sh
```

Inspect:

```bash
cat handover.txt
```

The lecture introduces this as the first reusable shell script.

### ✅ Check 12 — First script

You will change `report.sh` in the next parts, so take snapshots now:

```bash
cp report.sh    evidence/12-report.sh
cp handover.txt evidence/12-handover.txt
```

`check_lab` verifies:

- `report.sh` is in your lab folder and executable (`chmod +x`).
- `evidence/12-report.sh` starts with `#!/usr/bin/env bash` and uses `>` and `>>` to write `handover.txt`.
- `evidence/12-handover.txt` is exactly:

```text
registrations.txt
0 campus-day/registrations.txt
```

---

# Part 13 — Script Arguments

Hard-coding:

```bash
folder="campus-day"
```

makes the script less reusable.

Instead use:

```bash
folder="$1"
```

Now the user provides the folder.

Run:

```bash
./report.sh campus-day
```

or:

```bash
./report.sh sports-day
```

The first argument supplied to the script is available through:

```bash
$1
```

The lecture demonstrates the same script with multiple event folders.

### ✅ Check 13 — Script arguments

```bash
./report.sh sports-day
cp report.sh    evidence/13-report.sh
cp handover.txt evidence/13-handover.txt
```

`check_lab` verifies:

- `evidence/13-report.sh` sets `folder="$1"` (with the quotes) and no longer hard-codes `campus-day`.
- `evidence/13-handover.txt` is exactly:

```text
registrations.txt
0 sports-day/registrations.txt
```

---

# Part 14 — Validate Input

What happens if someone runs:

```bash
./report.sh
```

or:

```bash
./report.sh missing-event
```

A good script should not blindly continue.

Use:

```bash
if [ ! -d "$folder" ]; then
    echo "Provide an existing event folder." >&2
    exit 1
fi
```

Important concepts:

```text
-d     check whether something is a directory
!      reverse the condition
>&2    send output to stderr
exit 1 return a failure status
fi     end the if block
```

The lecture introduces this validation pattern explicitly.

### ✅ Check 14 — Validate input

Add the `if` block to `report.sh`, right after `folder="$1"`. Then test both bad inputs, saving stderr and the exit status:

```bash
./report.sh 2> evidence/14-noarg.err;                echo "$?" > evidence/14-noarg.status
./report.sh missing-event 2> evidence/14-missing.err; echo "$?" > evidence/14-missing.status
cp report.sh evidence/14-report.sh
```

`check_lab` verifies:

- `evidence/14-noarg.status` and `evidence/14-missing.status` are both exactly `1`.
- `evidence/14-noarg.err` and `evidence/14-missing.err` each contain `Provide an existing event folder.` (so the message went to **stderr**).
- `evidence/14-report.sh` contains `-d`, `>&2` and `exit 1`.
- No folder named `missing-event` was created.

---

# Part 15 — Arrays

Suppose every event contains:

```text
notes.txt
registrations.txt
budget.txt
```

Instead of repeating commands:

```bash
wc -l "$folder/notes.txt"
wc -l "$folder/registrations.txt"
wc -l "$folder/budget.txt"
```

we can store the files in an array.

```bash
files=(
    "$folder/notes.txt"
    "$folder/registrations.txt"
    "$folder/budget.txt"
)
```

> ✅ Arrays are checked together with loops in **Check 16**.

---

# Part 16 — For Loops

Now process every file:

```bash
for file in "${files[@]}"; do
    wc -l "$file"
done
```

The loop means:

```text
Take each file
     ↓
store it in $file
     ↓
run wc -l
     ↓
move to next file
```

The lecture uses this exact array-and-loop pattern to process multiple files.

---

# Task 16

Give `campus-day` all three files, with this exact content:

```bash
printf 'Venue: main hall\nStart: 10:00\n'             > campus-day/notes.txt
printf 'Asha\nBilal\nChen\n'                          > campus-day/registrations.txt
printf 'Stage: 5000\nFood: 8000\nPrint: 1200\nMisc: 800\n' > campus-day/budget.txt
```

Then modify your script so it processes:

```text
notes.txt
registrations.txt
budget.txt
```

using an array and loop. Keep the first line `ls "$folder" > handover.txt`, and replace the single `wc -l ... >> handover.txt` line with the loop, appending each `wc -l "$file"` to `handover.txt`.

### ✅ Check 16 — Arrays and loops

```bash
./report.sh campus-day
cp report.sh    evidence/16-report.sh
cp handover.txt evidence/16-handover.txt
```

`check_lab` verifies:

- `campus-day/notes.txt`, `registrations.txt` and `budget.txt` hold exactly the text above (2, 3 and 4 lines).
- `evidence/16-report.sh` defines an array (`files=(`) and loops over it with `for file in "${files[@]}"`.
- `evidence/16-report.sh` contains `wc -l` only **once** (the loop does the repeating, not copy-paste).
- `evidence/16-handover.txt` is exactly:

```text
budget.txt
notes.txt
registrations.txt
2 campus-day/notes.txt
3 campus-day/registrations.txt
4 campus-day/budget.txt
```

---

# Part 17 — Build the Complete Automation Script

Now combine everything.

Your script should be:

```text
report.sh
```

and should accept:

```bash
./report.sh <event-folder>
```

Example:

```bash
./report.sh campus-day
```

---

## Requirements

Your script must:

### 1. Accept an event directory

Use:

```bash
$1
```

---

### 2. Validate the directory

If the directory does not exist:

- Print an error.
- Send the error to stderr.
- Exit with status `1`.

---

### 3. Validate required files

Required files:

```text
notes.txt
registrations.txt
budget.txt
```

If any file is missing:

```text
Missing file: <filename>
```

must be printed to stderr.

---

### 4. Generate a handover report

Create:

```text
handover.txt
```

The report should contain:

```text
EVENT HANDOVER REPORT
=====================

Event: campus-day

FILES
-----
notes.txt
registrations.txt
budget.txt

COUNTS
------
notes.txt: ...
registrations.txt: ...
budget.txt: ...
```

---

### 5. Use an array

Store the required files in an array.

---

### 6. Use a loop

Process the files using a `for` loop.

---

### 7. Handle errors

The script should return:

```text
0 → success
1 → failure
```

### ✅ Check 17 — Complete automation script

Make an incomplete event folder to test the missing-file path:

```bash
mkdir -p draft-day
touch draft-day/notes.txt draft-day/budget.txt     # registrations.txt left out on purpose
```

Run the failure cases first and the success case last:

```bash
./report.sh 2> evidence/17-noarg.err;             echo "$?" > evidence/17-noarg.status
./report.sh draft-day 2> evidence/17-draft.err;   echo "$?" > evidence/17-draft.status
./report.sh campus-day;                           echo "$?" > evidence/17-ok.status
cp report.sh    evidence/17-report.sh
cp handover.txt evidence/17-handover.txt
```

> Tip: `wc -l < "$folder/$name"` prints just the number, without the filename.

`check_lab` verifies:

- `evidence/17-noarg.status` and `evidence/17-draft.status` are `1`; `evidence/17-ok.status` is `0`.
- `evidence/17-draft.err` contains `Missing file: registrations.txt`, and does **not** mention `notes.txt` or `budget.txt`.
- `evidence/17-report.sh` uses `$1`, `-d`, an array, a `for ... in "${array[@]}"` loop, `>&2` and `exit 1`.
- `evidence/17-handover.txt` matches this exactly (extra spaces at line ends are ignored):

```text
EVENT HANDOVER REPORT
=====================

Event: campus-day

FILES
-----
notes.txt
registrations.txt
budget.txt

COUNTS
------
notes.txt: 2
registrations.txt: 3
budget.txt: 4
```

---

# FINAL CHALLENGE LAB

## Production Handover System

You are now given a real-world task.

Your manager wants you to build a reusable **Event Handover System**.

You are given:

```text
events/
├── campus-day/
│   ├── notes.txt
│   ├── registrations.txt
│   └── budget.txt
│
├── sports-day/
│   ├── notes.txt
│   ├── registrations.txt
│   └── budget.txt
│
└── tech-fest/
    ├── notes.txt
    ├── registrations.txt
    └── budget.txt
```

This `events/` folder is already in your lab folder (`~/lab-work/lab5/events`). Do not edit the files inside it; `check_lab` checks that they are unchanged and compares your report against their real line counts.

Your job is to create, in `~/lab-work/lab5`:

```text
handover.sh
```

It writes `handover.txt` and appends to `errors.log` in the folder you run it from.

---

## Challenge Command

The script must work like:

```bash
./handover.sh events/campus-day
```

It should also work with:

```bash
./handover.sh events/sports-day
```

and:

```bash
./handover.sh events/tech-fest
```

You should **not** need to modify the script for different events.

---

# Challenge Requirements

## Requirement 1 — Input Validation

Handle:

```bash
./handover.sh
```

and:

```bash
./handover.sh events/missing
```

correctly.

---

## Requirement 2 — File Validation

Check that:

```text
notes.txt
registrations.txt
budget.txt
```

exist.

Use an appropriate Bash file test.

---

## Requirement 3 — Generate Report

Create:

```text
handover.txt
```

containing useful information about the event.

---

## Requirement 4 — Count Files

Use:

```bash
wc -l
```

to count the lines in each required file.

---

## Requirement 5 — Use Arrays

The required files must be stored in an array.

---

## Requirement 6 — Use a Loop

Use a `for` loop to process the files.

---

## Requirement 7 — Error Handling

Errors should go to stderr.

For example:

```bash
echo "Missing file: $file" >&2
```

---

## Requirement 8 — Exit Codes

Your script must return:

```text
0 → success
1 → failure
```

---

## Requirement 9 — Logging

Create:

```text
errors.log
```

for errors.

A successful execution should generate:

```text
handover.txt
```

---

## Bonus Challenge

Add a timestamp to the report.

For example:

```text
Generated: Sat Oct 10 11:30:00 IST 2026
```

You can investigate:

```bash
date
```

to accomplish this.

---

# Required Test Cases

Before submitting, test your script with all of these:

### Test 1 — Valid event

```bash
./handover.sh events/campus-day
```

Expected:

```text
Success
```

Exit status:

```text
0
```

---

### Test 2 — Another valid event

```bash
./handover.sh events/sports-day
```

Expected:

```text
Success
```

Exit status:

```text
0
```

---

### Test 3 — No argument

```bash
./handover.sh
```

Expected:

```text
Error
```

Exit status:

```text
1
```

---

### Test 4 — Invalid directory

```bash
./handover.sh events/missing-event
```

Expected:

```text
Error
```

Exit status:

```text
1
```

---

### Test 5 — Missing file

Create:

```text
events/incomplete-event/
```

with `notes.txt` and `budget.txt`, but intentionally leave out:

```text
registrations.txt
```

```bash
mkdir -p events/incomplete-event
touch events/incomplete-event/notes.txt events/incomplete-event/budget.txt
```

Then run:

```bash
./handover.sh events/incomplete-event
```

Expected: an error on stderr that names the missing file, for example:

```text
Missing file: registrations.txt
```

Exit status:

```text
1
```

---

### ✅ Check — Final challenge

Start from a clean log, then run every test case, saving stderr, exit status and the report after each success:

```bash
mkdir -p evidence/challenge
rm -f errors.log

./handover.sh events/campus-day 2> evidence/challenge/t1.err;    echo "$?" > evidence/challenge/t1.status
cp handover.txt evidence/challenge/t1-handover.txt

./handover.sh events/sports-day 2> evidence/challenge/t2.err;    echo "$?" > evidence/challenge/t2.status
cp handover.txt evidence/challenge/t2-handover.txt

./handover.sh 2> evidence/challenge/t3.err;                      echo "$?" > evidence/challenge/t3.status
./handover.sh events/missing-event 2> evidence/challenge/t4.err; echo "$?" > evidence/challenge/t4.status
./handover.sh events/incomplete-event 2> evidence/challenge/t5.err; echo "$?" > evidence/challenge/t5.status

./handover.sh events/tech-fest;                                   echo "$?" > evidence/challenge/t6.status
```

The last run leaves `handover.txt` for `tech-fest` in your lab folder.

`check_lab` verifies:

| Area | What is checked |
| --- | --- |
| Script | `handover.sh` is executable (made with `chmod +x`), starts with `#!/usr/bin/env bash`, uses `$1`, an array, a `for ... in "${array[@]}"` loop, `wc -l`, a file test (`-f` or `-e`), `>&2` and `exit 1`. It does **not** hard-code `campus-day`, `sports-day` or `tech-fest`. |
| Starter data | Every file in `events/campus-day`, `events/sports-day` and `events/tech-fest` is unchanged. |
| Test 1, 2, 6 | Status files are `0`; `t1.err` and `t2.err` are empty. |
| Test 3, 4 | Status files are `1`; `t3.err` and `t4.err` are not empty. |
| Test 5 | `events/incomplete-event/` has `notes.txt` and `budget.txt` but no `registrations.txt`; `t5.status` is `1`; `t5.err` mentions `registrations.txt`. |
| Reports | `t1-handover.txt`, `t2-handover.txt` and `handover.txt` each name their own event (`campus-day`, `sports-day`, `tech-fest`), list all three files, and show the correct line count on the same line as each filename. |
| Logging | `errors.log` exists and records the errors from tests 3–5, including the missing `registrations.txt`. |
| Bonus | `handover.txt` has a line starting with `Generated: ` (2 bonus points; the other checks add up to 98). |

---

# Submission Checklist

Before considering the lab complete, verify:

- [ ] I can create Bash variables.
- [ ] I understand `$variable`.
- [ ] I understand why quotes matter.
- [ ] I understand `$PATH`.
- [ ] I can use `command -v`.
- [ ] I understand exit status.
- [ ] I can use `$?`.
- [ ] I understand `&&`.
- [ ] I understand `||`.
- [ ] I understand stdout.
- [ ] I understand stderr.
- [ ] I can redirect stdout.
- [ ] I can redirect stderr.
- [ ] I understand `2>&1`.
- [ ] I can create a Bash script.
- [ ] I can make a script executable.
- [ ] I can pass `$1`.
- [ ] I can validate directories.
- [ ] I can validate files.
- [ ] I can use arrays.
- [ ] I can use loops.
- [ ] I can handle errors.
- [ ] I completed the final challenge.
- [ ] I saved every evidence file under `evidence/` with the commands in the ✅ Check boxes.
- [ ] `check_lab lab5` shows PASS for every check.

---

# Reflection Questions

Answer these after completing the lab.

### Q1

Why are variables useful in shell scripts?

### Q2

Why should variables containing paths usually be quoted?

### Q3

What is `$PATH`?

### Q4

What does exit status `0` normally indicate?

### Q5

What does `$?` represent?

### Q6

What is the difference between:

```bash
>
```

and:

```bash
>>
```

### Q7

What is the difference between stdout and stderr?

### Q8

What does:

```bash
2>&1
```

do?

### Q9

What does `$1` represent?

### Q10

Why should a production script validate its inputs?

### Q11

Why are arrays and loops useful?

### Q12

What makes your final script reusable?

---

# Key Takeaways

At the beginning of this lab, you manually executed commands:

```bash
ls
wc
cat
```

By the end, you should be able to build an automated workflow:

```text
Input
  ↓
Validate
  ↓
Process
  ↓
Handle errors
  ↓
Generate output
  ↓
Return status
```

This is one of the fundamental ideas behind shell automation.

The goal is not simply to memorize Bash commands.

The goal is to learn how to turn a sequence of manual terminal operations into a **reliable, reusable automation workflow**.

---

# What You Should Be Able to Do After This Lab

Given a repetitive terminal task, you should now be able to ask:

> "Can I automate this?"

And then think in terms of:

```text
Variables
    ↓
Inputs
    ↓
Commands
    ↓
Exit Status
    ↓
Conditions
    ↓
Output/Error Handling
    ↓
Loops
    ↓
Script
```

**Congratulations — you have built your first Bash automation workflow! **
