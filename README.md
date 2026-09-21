# Python labs for EC3318/MN3101 Corporate Finance

<img src=".pics/01-foundation-black-text.png" alt="University of St Andrews" width="320" />

**Open Codespaces → open the notebook → run the first cell.** No AI subscription is needed for either lab.

## Start here: Codespaces (recommended)

These are **formative, ungraded labs**. Use the Classroom 50 assignment link supplied on Moodle to create **your own private course copy**. It contains both labs, so you only need to accept the assignment once. Accept any GitHub organisation invitation when prompted. If you cannot access your copy or create a Codespace, ask your lecturer for help.

1. On your copy's GitHub page, choose **Code → Codespaces → Create codespace**. To return to existing work, reopen your existing Codespace instead.
2. Wait for the automatic setup to finish. It installs the lab environment for you.
3. Open **`lab1-notebook.ipynb`** (or **`lab2-notebook.ipynb`** for Lab 2). Run the first code cell with its **▶** button, then work down the notebook in order.

If asked to choose a kernel, select **Corporate Finance Labs (.venv)**, or **Python Environments → cflabs (3.12.14)** with the `.venv` path. A kernel is the Python environment that runs your notebook.

## If something goes wrong

Open **Terminal → Run Task** to find the named tasks below.

| Problem | What to do |
| --- | --- |
| Setup failed, or a package cannot be found | **Run Setup again:** choose **Setup lab environment**. If it fails again, show your lecturer the failed step in the terminal. |
| The notebook cannot run, or uses a different Python | **Select the lab environment:** click **Select Kernel** at the top right of the notebook and choose **Corporate Finance Labs (.venv)**. If it is not listed, choose **Select Another Kernel → Python Environments → .venv**. |
| Unsure whether your work reached GitHub | Save the notebook, then run **Check whether your work has synced**. Follow the message shown. |

## Saving and finishing

Files save automatically while you work. Saving either lab notebook also attempts to record and upload your notebook changes to your GitHub copy. **A saved file is not proof that the upload succeeded.**

Before finishing, save the notebook and run **Check whether your work has synced**. You can also open the notebook on GitHub to check your latest changes. If an upload fails, details appear under **View → Output → Run On Save**; a later notebook save retries it. Ask your lecturer for help with an access or conflict error.

**Syncing is not a formal submission.** Follow any separate submission instructions on Moodle. Return to this same private repository and Codespace for Lab 2.

After checking your work has synced, stop the Codespace using **Codespaces: Stop Current Codespace** in the Command Palette. Open the palette with **Cmd+Shift+P** on Mac or **Ctrl+Shift+P** on Windows/Linux.

## Getting help

The [lecture resources](.assistant-resources/README.md) include PDFs for Lectures 0–3 and the available key concepts and terms decks, alongside their editable sources. Check Moodle for later updates.

Start with the notebook explanations and ask your lecturer when you get stuck. **GitHub Copilot is optional**: if you have access, open its chat and ask for an explanation of a small piece of code or an error message.

Try: “Explain this error and give me one hint. Do not solve the exercise for me.” Predict what the code should do, inspect any suggested change, run it, and explain the result in your own words. You can complete every exercise without Copilot.

## Local VS Code (optional)

1. Install [VS Code](https://code.visualstudio.com/) and [Git](https://git-scm.com/downloads), then use **Git: Clone** in VS Code's Command Palette to open your writable course copy. Sign in to GitHub when required to sync your work.
2. Install the repository's recommended extensions when prompted: Python, Jupyter, Run On Save and optional Copilot.
3. Choose **Terminal → Run Task → Setup lab environment** and wait for success. No Docker installation is needed.
4. Open the lab notebook, select **Corporate Finance Labs (.venv)**, and run the first code cell.

## Other optional AI tools

Codex and Claude are additional options for students who already want to use them. Their extensions and the Copilot, Codex and Claude command-line tools are installed during Codespaces setup without signing you in. An optional installation failure does not prevent you from running the labs.

Locally, choose **Terminal → Run Task → Install optional AI tools** to install these extras. Their own account and access requirements apply; you do not need to sign in or buy access to complete the labs.

[Optional reference: environments, Git and further reading](docs/reference.md)
