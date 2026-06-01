# GitHub Setup and Submission Instructions

Dear Participant,

You have been invited to join the GitHub organization for the training program. This GitHub repository will be used for submitting assignments, weekly projects, and the final capstone project.

Please follow the steps below carefully.

---

## 1. Accept the GitHub Invitation

You will receive an invitation email from GitHub.

Please do the following:

1. Open the invitation email from GitHub.
2. Click on **Join @Agile-Ventures-Pvt-LTD** or **View invitation**.
3. Log in using your GitHub account.
4. Accept the invitation.

If you do not already have a GitHub account, create one using the same email address on which you received the invite.

Once you accept the invite, you will be added to the training team and will get access to the training repository.

---

## 2. Repository Details

The training repository is:

```text
Agile-Ventures-Pvt-LTD / AI_Training_Batch_May_2026
```

Repository URL:

```text
https://github.com/Agile-Ventures-Pvt-LTD/AI_Training_Batch_May_2026
```

You will use this repository for:

* Daily assignments
* Weekly projects
* Monthly capstone work
* Code submissions
* Review and feedback

---

## 3. Install Git on Your System

Before cloning the repository, make sure Git is installed.

To check whether Git is installed, open your terminal or command prompt and run:

```bash
git --version
```

If Git is installed, you will see a version number.

Example:

```bash
git version 2.43.0
```

If Git is not installed, please install it from:

```text
https://git-scm.com/downloads
```

---

## 4. Clone the Repository

After accepting the GitHub invitation, open your terminal or command prompt.

Go to the folder where you want to keep your training code.

Example:

```bash
cd Documents
```

Now clone the repository:

```bash
git clone https://github.com/Agile-Ventures-Pvt-LTD/AI_Training_Batch_May_2026.git
```

Go inside the repository folder:

```bash
cd AI_Training_Batch_May_2026
```

---

## 5. Create Your Own Branch

Each participant must work only in their own branch.

Please do not work directly on the `main` branch.

Use this branch naming format:

```text
participant-firstname-lastname
```

Example:

```text
participant-ashish-sinha
participant-neha-sharma
participant-ravi-kumar
```

To create your branch, run:

```bash
git checkout -b participant-yourname
```

Example:

```bash
git checkout -b participant-ashish-sinha
```

To check your current branch, run:

```bash
git branch
```

The branch with `*` next to it is your current branch.

Example:

```text
* participant-ashish-sinha
  main
```

---

## 6. Folder Structure for Submissions

All work must be submitted inside the `submissions` folder.

The structure will be like this:

```text
submissions/
├── assignments/
│   ├── assignment-01/
│   ├── assignment-02/
│   └── assignment-03/
│
├── project-build/
│   ├── llm-application/
│   ├── langchain-application/
│   └── langgraph-application/
│
└── capstone/
```

Inside each activity folder, create your own folder using your name.

Use this format:

```text
firstname-lastname
```

Example:

```text
ashish-sinha
neha-sharma
ravi-kumar
```

---

## 7. How to Submit an Assignment

Suppose you are submitting Assignment 01.

Create your folder here:

```text
submissions/assignments/assignment-01/your-name/
```

Example:

```text
submissions/assignments/assignment-01/ashish-sinha/
```

Place all your Assignment 01 files inside your folder.

Example:

```text
submissions/assignments/assignment-01/ashish-sinha/
├── solution.py
├── README.md
└── requirements.txt
```

If you are using Jupyter Notebook, your folder may look like this:

```text
submissions/assignments/assignment-01/ashish-sinha/
├── assignment_01_solution.ipynb
├── README.md
└── requirements.txt
```

---

## 8. How to Submit a Weekly Project

Suppose you are submitting the Week 01 project.

Create your folder here:

```text
submissions/project-build/llm-application/your-name/
```

Example:

```text
submissions/project-build/llm-application/ashish-sinha/
```

Place your project files inside that folder.

Example:

```text
submissions/project-build/llm-application/ashish-sinha/
├── app.py
├── notebook.ipynb
├── README.md
├── requirements.txt
└── screenshots/
```

---

## 9. How to Submit the Capstone Project

For the capstone project, create your folder here:

```text
submissions/capstone/your-name/
```

Example:

```text
submissions/capstone/ashish-sinha/
```

Recommended capstone folder structure:

```text
submissions/capstone/ashish-sinha/
├── README.md
├── app.py
├── requirements.txt
├── architecture.md
├── demo-notes.md
├── notebooks/
├── src/
├── data-sample/
└── screenshots/
```

Do not upload large datasets, model files, or confidential data.

---

## 10. Required README.md in Every Submission

Every assignment, weekly project, and capstone submission must include a `README.md` file.

Your `README.md` should include:

```text
1. Name
2. Assignment or project title
3. Short description of what you have built
4. Steps to run the code
5. Libraries or packages required
6. Any assumptions made
7. Output screenshots or explanation, if required
```

Example:

````markdown
# Assignment 01 - Prompt Engineering

## Participant Name
Ashish Sinha

## Description
This assignment demonstrates zero-shot and few-shot prompting using the Groq API.

## How to Run

```bash
pip install -r requirements.txt
python solution.py
````

## Files Included

* solution.py
* requirements.txt
* README.md

## Notes

The API key is not included in the code. Please set it using an environment variable.

````

---

## 11. How to Save and Push Your Work

After adding your files, run the following commands.

First check the status:

```bash
git status
````

Add your files:

```bash
git add .
```

Commit your work:

```bash
git commit -m "Added assignment 01 submission"
```

Push your branch:

```bash
git push -u origin participant-yourname
```

Example:

```bash
git push -u origin participant-ashish-sinha
```

For future submissions, you can simply use:

```bash
git add .
git commit -m "Added assignment 02 submission"
git push
```

---

## 12. How to Create a Pull Request

After pushing your branch, go to the GitHub repository in your browser.

You may see a button like:

```text
Compare & pull request
```

Click it.

Make sure the pull request shows:

```text
base: main
compare: participant-yourname
```

Example:

```text
base: main
compare: participant-ashish-sinha
```

Use this pull request title format:

```text
Training Submissions - Your Name
```

Example:

```text
Training Submissions - Ashish Sinha
```

In the pull request description, mention what you have submitted.

Example:

```text
Submitted:
- Assignment 01
- Assignment 02
- Week 01 Project
```

Then click:

```text
Create pull request
```

You do not need to create a new pull request for every assignment unless the trainer specifically asks you to do so. You can keep updating the same pull request by pushing new commits to your branch.

---

## 13. Daily Workflow

Whenever you work on a new assignment or project, follow this process:

```text
1. Make sure you are on your own branch.
2. Create the correct folder for the assignment or project.
3. Add your code and README.md file.
4. Run and test your code locally.
5. Commit your changes.
6. Push your changes to GitHub.
7. Update your pull request if required.
```

Commands:

```bash
git branch
git status
git add .
git commit -m "Added latest submission"
git push
```

---

## 14. Important Rules

Please follow these rules carefully:

* Work only in your own branch.
* Do not push code directly to the `main` branch.
* Do not edit or delete another participant’s folder.
* Do not rename common folders unless instructed.
* Do not upload passwords, API keys, tokens, or `.env` files.
* Do not upload large datasets, model files, videos, or unnecessary files.
* Keep your code clean and readable.
* Add a `README.md` file for every submission.
* Commit your work regularly.
* Use meaningful commit messages.

---

## 15. Files You Should Not Upload

Do not upload the following files or folders:

```text
.env
.venv/
venv/
__pycache__/
.ipynb_checkpoints/
*.pyc
*.pkl
*.joblib
large datasets
API keys
password files
model weights
```

If your code needs an API key, mention it in your README file and use environment variables.

Example:

```bash
export GROQ_API_KEY="your-api-key"
```

For Windows Command Prompt:

```cmd
set GROQ_API_KEY=your-api-key
```

Do not write the actual API key inside your code.

---

## 16. Before Submitting, Check This

Before pushing your work, make sure:

```text
Your code is inside the correct folder.
Your folder name is correct.
Your code runs without errors.
Your README.md file is included.
No API key or password is present in the code.
You are working on your own branch.
```

Useful commands:

```bash
git branch
git status
```

---

## 17. Common Git Commands

Check current branch:

```bash
git branch
```

Check changed files:

```bash
git status
```

Add all files:

```bash
git add .
```

Commit changes:

```bash
git commit -m "your message"
```

Push changes:

```bash
git push
```

Pull latest changes from main:

```bash
git checkout main
git pull origin main
git checkout participant-yourname
git merge main
```

---

## 18. If You Face Any Issue

If you face any issue, please share the following details with the trainer:

```text
1. Screenshot of the error
2. Command you ran
3. Your branch name
4. Your folder path
5. Short explanation of what you were trying to do
```

Example:

```text
I was trying to push Assignment 01 from branch participant-ashish-sinha.
The command I ran was git push.
I received the attached error.
```

This will help us resolve your issue quickly.

---

## 19. Summary

You only need to remember this:

```text
Accept GitHub invite
Clone the repository
Create your own branch
Create your own folder for each assignment or project
Add code and README.md
Commit and push
Create or update your pull request
```

Please complete the GitHub setup before the hands-on session starts.

Regards,
Ankur Saxena

