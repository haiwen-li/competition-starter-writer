# Starter API Note Writer

A working starter bot for the WSDM Cup competition, Writing Agents for Community Notes. It is adapted from the Community Notes [Template API Note Writer](https://github.com/twitter/communitynotes/tree/main/template-api-note-writer). This starter bot:

1. **Uses only one LLM call per post.** As a simple starting point, it retrieves information, makes note writing decision, and (if needed) writes a note in a single xAI API call. 
2. **Uses xAI API.** The starter bot uses `grok-4.3` with `web_search` and `x_search` and image and video understanding.

This starter kit also contains a `TEST_MODE` setting and a `check_scores.py` script to see how your test notes were scored.

## What it does

For each run, `src/main.py`:

1. Calls `GET /2/notes/search/posts_eligible_for_notes` to get posts that people have requested notes on, plus any quoted or replied-to posts.
2. For each post, makes one Grok call (`src/note_writer/write_note.py`). The answer is one of:
   - `WRITE NOTE`, with the note text and at least one misleading tag
   - `NO NOTE NEEDED`
   - `NOT ENOUGH EVIDENCE`
3. Submits each note with `POST /2/notes` (skipped with `--dry-run`).

## Setup

### 1. Prepare an X account

You need an X account with a verified email address and a verified phone number from a trusted carrier. Check the [AI Note Writer guide](https://communitynotes.x.com/guide/en/api/overview) for the current account requirements, since they may change.

### 2. Create an X developer app

1. Sign up at [developer.x.com](https://developer.x.com) with that account.
2. Create a Project and an App.
3. In the app's **User authentication settings**, set permissions to **Read and Write**.
4. On the app's **Keys and tokens** page, generate the **API Key and Secret** and the **Access Token and Secret**. Generate the access token *after* setting Read and Write. 


### 3. Register as an AI Note Writer

Follow the enrollment steps in the [AI Note Writer guide](https://communitynotes.x.com/guide/en/api/overview). 


### 4. Get an LLM API key

To run this writer, use your xAI API key or create a key at [console.x.ai](https://console.x.ai).

### 5. Install and log in to `xurl`

Like the template, this writer calls the X API through [`xurl`](https://github.com/xdevplatform/xurl), X's command line tool. Install it with one of:

```bash
brew install --cask xdevplatform/tap/xurl
npm install -g @xdevplatform/xurl
curl -fsSL https://raw.githubusercontent.com/xdevplatform/xurl/main/install.sh | bash
```

Then log in with the four OAuth 1.0a keys from step 2:

```bash
xurl auth oauth1 --consumer-key API_KEY --consumer-secret API_KEY_SECRET \
  --access-token ACCESS_TOKEN --token-secret ACCESS_TOKEN_SECRET
```

`xurl auth status` should now show `OAuth1: Configured`. If you have also set up OAuth2 accounts in `xurl`, make sure requests are made as your note-writer account.

### 6. Install and run

Install [uv](https://docs.astral.sh/uv/). It installs Python 3.12 for you if needed. Then, from this folder:

```bash
uv sync
cp .env.example .env    # then fill in XAI_API_KEY
uv run src/main.py --num-posts 5 --dry-run
```

`.env` holds your xAI key and is listed in `.gitignore`, so it is not committed.

`--dry-run` does everything except submit, so it is the safe way to check your keys and read the drafts. When the drafts look reasonable, drop the flag to submit:

```bash
uv run src/main.py --num-posts 10
```

Use `--concurrency N` to process N posts at a time.


## Test mode and admission

All notes start in test mode (`TEST_MODE=true`, the default). Test notes are not shown publicly. An automated evaluator scores them. To see the scores for every test note you have written, run:

```bash
uv run src/check_scores.py          # readable report
uv run src/check_scores.py --json   # raw data
```

Once your writer's test notes score well enough, X admits the writer and notifies you. After admission, set `TEST_MODE=false` in `.env` so your notes go to human raters. See the [guide](https://communitynotes.x.com/guide/en/api/overview) for the current admission rules.

## Project layout

```
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

## License

Apache 2.0, same as [twitter/communitynotes](https://github.com/twitter/communitynotes). Most of the code is from that repo's `template-api-note-writer`.
