Lab 5: upload only your own emailed access ZIP (for example
`Lab_4_studentNN_Access.zip`) into this folder. Right-click this folder in the
Codespaces Explorer and choose Upload, or drag the ZIP into it. Keep it zipped.

Then run in the terminal (replace `studentNN` with your account):

```bash
unzip -o .uploads/Lab_4_studentNN_Access.zip -d ~
cd ~/Lab_4_studentNN_Access
chmod 600 access/ssh_key
ssh -i access/ssh_key studentNN@98.70.53.61
```

Full steps are in `labs/lab5/Lab_Book.md`. Keep your email attachment so you
can set up again after rebuilding or creating a new Codespace.
