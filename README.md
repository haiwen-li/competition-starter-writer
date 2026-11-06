# Writing Agents for Community Notes: participant setup guide

## Contents

- [Overview](#overview)
  - [What you need before you start](#what-you-need-before-you-start)
- [Part 1. Create your X account and register](#part-1-create-your-x-account-and-register)
  - [1.1 Create the X account for your writer](#11-create-the-x-account-for-your-writer)
  - [1.2 Register for the competition](#12-register-for-the-competition)
- [Part 2. Sign up for the X API and the AI Note Writer API](#part-2-sign-up-for-the-x-api-and-the-ai-note-writer-api)
  - [2.1 Create an X developer app](#21-create-an-x-developer-app)
  - [2.2 Enroll as an AI Note Writer](#22-enroll-as-an-ai-note-writer)
- [(Optional) Part 3. Get an xAI API key](#optional-part-3-get-an-xai-api-key)
- [(Optional) Part 4. Fork the starter writer and run it](#optional-part-4-fork-the-starter-writer-and-run-it)
  - [4.1 Fork and clone](#41-fork-and-clone)
  - [4.2 Choose how to run your writer](#42-choose-how-to-run-your-writer)
  - [Option A. Run on your computer](#option-a-run-on-your-computer)
    - [A.1 Install xurl and log in](#a1-install-xurl-and-log-in)
    - [A.2 Install the writer](#a2-install-the-writer)
    - [A.3 Do a dry run](#a3-do-a-dry-run)
    - [A.4 Submit test notes](#a4-submit-test-notes)
    - [A.5 Check your scores](#a5-check-your-scores)
  - [Option B. Run on GitHub Actions](#option-b-run-on-github-actions)
- [Improve your writer and earn admission!](#improve-your-writer-and-earn-admission)
  - [Earning admission](#earning-admission)
  - [Limits to plan around](#limits-to-plan-around)
  - [Start improving](#start-improving)
- [Rules, costs and help](#rules-costs-and-help)
- [About the starter writer](#about-the-starter-writer)
  - [How it works](#how-it-works)
  - [Project layout](#project-layout)

## Overview

The setup has four parts. You only need to finish the first two parts to be eligible to participate.

1. Register for the competition and create an X account for your writer.
2. Sign up for the X API, enroll as an AI Note Writer, and generate your X keys.
3. (Optional) Get an xAI API key for the language model.
4. (Optional) Fork the starter writer, run it, and submit your first test notes.

### What you need before you start

- **An X account that meets the following requirements:**
  - Must NOT already be signed up as a Community Notes contributor
  - Must have a verified phone number from a trusted carrier
    - Phone number can be associated with only one AI Note Writer.
    - Phone number can be associated with a maximum of one non-AI Community Notes contributor account.
  - Must have a verified email address
    - This email address does not need to be the email you use for competition registration
- **A GitHub account**, to share your writer setup with us.

## Part 1. Create your X account and register

### 1.1 Create the X account for your writer

Your AI Note Writer acts through an X account. The account must never have been a Community Notes contributor.

1. Create a new account at [x.com](https://x.com) or use an existing account.
2. Add and verify an email address in the account settings. This email address does not need to be the email you use for competition registration
3. Add and verify a phone number from a trusted carrier in the account settings.

Stay logged in to this account in your browser. Parts 2 and 3 use it.

**Check.** The account settings show both the email address and the phone number as verified.

### 1.2 Register for the competition

1. Register your team with the [registration form](https://docs.google.com/forms/d/1PDBXcCVGVoqdc_qdUXEqJzQ0xLoTWYkW2CgKLvi5cTk/viewform).
2. To receive announcements and rule updates, sign up with the [updates form](https://docs.google.com/forms/d/1CAvnAkMPyOnqwlQZnFe4kanUenNEuVZe62XI9LJ0HqA/viewform). Teammates who want updates can each sign up.

## Part 2. Sign up for the X API and the AI Note Writer API

### 2.1 Create an X developer app

1. Go to the [X Developer Console](https://console.x.com) and sign in with your writer account.
2. Accept the Developer Agreement and Policy, and fill in the short profile about how you will use the API.
3. Click on "Apps" on the left side bar under "Access". You will see an app with name ends with your X account name. Click on it, then click on "Settings" next to the app name.
4. Select "Read and write" under "App permissions". Select "Web App, Automated App or Bot" under "Type of App". For "App Info", callback URL may be anything e.g. <http://localhost:8080>, and website URL could be <http://x.com>.
5. Save changes.

### 2.2 Enroll as an AI Note Writer

1. **Sign up for the [AI Note Writer API](https://x.com/i/flow/cn-api-signup).**
2. Go back to your app page in the Developer Console and check that the app is connected to **Community Notes** in "Project Access - Manage"
3. Under "Keys & Tokens", find "Consumer Key"  under OAuth 1.0 Keys. Click “regenerate” -> “Yes, regenerate”
   - Store “Consumer Key”, with the name: `X_API_KEY`
   - Store "Consumer Key Secret”, with the name: `X_API_KEY_SECRET`
4. Under "Keys & Tokens", find "Access Token"  under OAuth 1.0 Keys. Click “regenerate” -> “Yes, regenerate”
   - Store “Access Token”, with the name: `X_ACCESS_TOKEN`
   - Store “Access Token Secret”, with the name: `X_ACCESS_TOKEN_SECRET`

| Where on the page | Value | Name used in Part 4 |
| --- | --- | --- |
| Consumer Keys | API Key | `X_API_KEY` |
| Consumer Keys | API Key Secret | `X_API_KEY_SECRET` |
| Authentication Tokens | Access Token | `X_ACCESS_TOKEN` |
| Authentication Tokens | Access Token Secret | `X_ACCESS_TOKEN_SECRET` |

Generate the access token only after you have set Read and write in step 2.1. If you lose a key, regenerate it. The old one stops working. Never commit these keys to GitHub or share them in public.

## (Optional) Part 3. Get an xAI API key

The starter writer uses Grok through the xAI API. You can switch the writer to another model provider later.

1. Sign in at [console.x.ai](https://console.x.ai).
2. Create an API key and save it as `XAI_API_KEY`.

## (Optional) Part 4. Fork the starter writer and run it

### 4.1 Fork and clone

1. Open the [starter writer repo](https://github.com/haiwen-li/competition-starter-writer) and click **Fork**.
2. Clone your fork and move into it.

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/competition-starter-writer.git
cd competition-starter-writer
```

A fork of a public repo is public. Your keys stay private because they live only on your computer (Option A) or in your repo's Actions secrets (Option B), and the repo's `.gitignore` keeps `.env` out of commits.

### 4.2 Choose how to run your writer

You can run the writer on your own computer (Option A) or on GitHub's servers with GitHub Actions (Option B). You only need one of them.

|  | Option A. Your computer | Option B. GitHub Actions |
| --- | --- | --- |
| Setup | Install xurl and uv, put your xAI key in `.env` | Add five secrets to your GitHub repo |
| Changing the writer | Edit and rerun right away | Commit and push, then run the workflow |
| Scheduled runs | Only while your computer is on | Run on GitHub's servers |
| Checking scores | `check_scores.py` (step A.5) | Not included |

We recommend Option A while you develop your writer, and Option B once you want it to run on a schedule.

### Option A. Run on your computer

#### A.1 Install xurl and log in

The writer talks to the X API through [xurl](https://github.com/xdevplatform/xurl), X's command line tool. Install it with any one of these commands.

```bash
brew install --cask xdevplatform/tap/xurl      # macOS with Homebrew
npm install -g @xdevplatform/xurl              # any OS with Node.js
curl -fsSL https://raw.githubusercontent.com/xdevplatform/xurl/main/install.sh | bash   # no sudo, installs to ~/.local/bin
```

If you used the `curl` command and your terminal then says `xurl: command not found`, the folder it installed to is not on your PATH yet. Add it and open a new terminal.

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc    # use ~/.bashrc if your shell is bash
```

Log in with the four values from step 2.2.

```bash
xurl auth oauth1 --consumer-key API_KEY --consumer-secret API_KEY_SECRET \
  --access-token ACCESS_TOKEN --token-secret ACCESS_TOKEN_SECRET
```

Check the login.

```bash
xurl auth status    # should show "OAuth1: Configured"
```

#### A.2 Install the writer

1. Install [uv](https://docs.astral.sh/uv/), the Python package manager the repo uses. It installs Python 3.12 for you if needed.
2. From the repo folder, install the dependencies and create your `.env` file.

```bash
uv sync
cp .env.example .env
```

3. Open `.env` in a text editor and paste your xAI key after `XAI_API_KEY=`. Leave `TEST_MODE=true`.

#### A.3 Do a dry run

A dry run fetches real posts and writes draft notes, but does not call the X API to submit the note. Use it to confirm everything is connected.

```bash
uv run src/main.py --num-posts 5 --dry-run
```

#### A.4 Submit test notes

When the dry run works, run the writer without `--dry-run`.

```bash
uv run src/main.py --num-posts 10
```

Each submitted note prints **SUCCESSFULLY SUBMITTED NOTE**. Add `--concurrency 4` to process four posts at a time.

Your writer is in test mode, so these notes are not submitting on X.

#### A.5 Check your scores

```bash
uv run src/check_scores.py          # readable report
uv run src/check_scores.py --json   # raw data
```

The report lists every test note with its score on each evaluator, then a summary count. Scores can take a while to appear after you submit, so check back if a note shows no results yet.

### Option B. Run on GitHub Actions

The repo includes a GitHub Actions workflow, `.github/workflows/community_note_writer.yaml`, that runs the writer on GitHub's servers. It does the same thing as steps A.3 and A.4, but it can also run on a schedule while your computer is off. You do not need to install anything from Option A.

1. **Add your keys as repository secrets.** In your fork on GitHub, open **Settings > Secrets and variables > Actions**. On the **Secrets** tab, click **New repository secret** and add these five, with the names spelled exactly as shown.
   - `X_API_KEY`
   - `X_API_KEY_SECRET`
   - `X_ACCESS_TOKEN`
   - `X_ACCESS_TOKEN_SECRET`
   - `XAI_API_KEY`
2. **Turn on Actions for your fork.** Open the **Actions** tab and click the button to enable them.
3. **Run it once by hand.** Open **Actions > Starter AI Note Writer > Run workflow**. You can set the number of posts, the concurrency, and whether to do a dry run. Check **dry run** the first time.
4. **Read the output.** Click the run, then the **write\_notes** job, then the **Run the writer** step. The output is the same as in step A.3.
5. **(Optional) Run on a schedule.** In `.github/workflows/community_note_writer.yaml`, remove the `#` in front of the two `schedule` lines, then commit and push. The example runs every 6 hours.

The workflow always runs in test mode unless you add a repository variable named `TEST_MODE` with the value `false`, on the **Variables** tab of the same settings page. Add it only after X admits your writer.

## Improve your writer and earn admission!

### Earning admission

X admits a writer once its test notes score well enough. [AI Note Writer guide](https://communitynotes.x.com/guide/en/api/overview) sets these criteria over the writer's 50 most recent test notes.

| Evaluator score | What it measures | Requirement |
| --- | --- | --- |
| `ClaimOpinion` | whether the note addresses the post's claims without opinion or speculation | at least 30% `high`, and at most 30% `low` |
| `UrlValidity` | whether every link in the note returns HTTP 200 | at least 95% `high` |
| `HarassmentAbuse` | whether contributors are likely to see the note as harassment or abuse | at least 98% `high` |

After admission, you can change `TEST_MODE=true` to `TEST_MODE=false` in `.env`. From then on your notes are submitted on the platform, go to human raters, and they can appear on X if people from different perspectives rate them helpful.

### Limits to plan around

- A writer can submit only one note per post.
- A note is 1 to 280 characters and must include a source URL.

### Start improving

The starter is deliberately simple, with one Grok call per post and a single prompt. You can use different LLMs or design different note writing prompts, strategies, and pipelines.

The API also offers features the starter does not use yet. For example, `POST /2/evaluate_note` returns the ClaimOpinion score for a note; `DELETE /2/notes/{id}` allows you to delete a community note.

## Rules, costs and help

- **Data use.** By signing up for the X API you agree to X's [Developer Policy and agreements](https://developer.x.com/en/developer-terms). Community Notes API data may be used only for writing Community Notes, and the X API and X content may not be used to fine-tune or train a foundation or frontier model.
- **Questions about the starter writer or the API.** You can email us, ask questions in our Discord, or open an issue on the starter writer repo.

---

## About the starter writer

This is a working starter bot for the WSDM Cup competition **Writing Agents for Community Notes**. It is meant to be forked and improved.

The starter is deliberately simple. It makes **one LLM call per post**. In that call, `grok-4.3` searches the web and X (including images and video), decides whether the post needs a note, and writes the note if it does. The rest of the code fetches posts, submits notes and shows you how the automated evaluator scored them.

### How it works

Each run of `src/main.py` does three things.

1. Calls `GET /2/notes/search/posts_eligible_for_notes` to get posts that people have requested notes on, along with any quoted or replied-to posts.
2. Makes one Grok call per post (`src/note_writer/write_note.py`). Grok answers with one of three decisions.
   - `WRITE NOTE`, with the note text and at least one misleading tag
   - `NO NOTE NEEDED`
   - `NOT ENOUGH EVIDENCE`
3. Submits each note with `POST /2/notes`, unless you passed `--dry-run`.

### Project layout

```
.github/workflows/
  community_note_writer.yaml     GitHub Actions workflow (Option B)
.env.example                     template for your .env file (Option A)
src/
  main.py                        fetch posts, write a note for each, submit
  check_scores.py                list test-mode notes and their evaluator scores
  data_models.py                 pydantic models for posts, media and notes
  cnapi/
    xurl_util.py                 run xurl and parse its JSON output
    get_api_eligible_posts.py    fetch and parse posts eligible for notes
    submit_note.py               submit a note
  note_writer/
    write_note.py                the prompt, the JSON schema, and the per-post logic  <- start here
    llm_util.py                  the xAI Responses API call with web and X search
```
