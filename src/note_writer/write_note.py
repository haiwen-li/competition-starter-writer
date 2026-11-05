from data_models import MisleadingTag, NoteResult, PostWithContext, ProposedMisleadingNote
from note_writer.llm_util import get_grok_search_json_response

NO_NOTE_NEEDED = "NO NOTE NEEDED"
NOT_ENOUGH_EVIDENCE = "NOT ENOUGH EVIDENCE"

NOTE_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "decision": {"type": "string", "enum": ["WRITE NOTE", NO_NOTE_NEEDED, NOT_ENOUGH_EVIDENCE]},
        "note_text": {"type": "string"},
        "misleading_tags": {
            "type": "array",
            "items": {"type": "string", "enum": [tag.value for tag in MisleadingTag]},
        },
    },
    "required": ["decision", "note_text", "misleading_tags"],
    "additionalProperties": False,
}


def _get_prompt_for_note_writing(post_with_context_description: str):
    return f"""Below will be a post on X. Do research on the post using web search and X search to determine if \
the post is potentially misleading. Use X search to look up the post by its Post ID, \
including any images or video in it, and any quoted or replied-to post by its Post ID. \
If the post is misleading and needs a community note, \
then your decision should be "WRITE NOTE" and note_text should be the proposed community note itself. \
If the post is not misleading, or does not contain any concrete fact-checkable claims, or there \
is not strong enough evidence to write a well-supported \
community note, then do not write a note, and instead set decision to "{NO_NOTE_NEEDED}" or \
"{NOT_ENOUGH_EVIDENCE}".

If a note is justified, then please write \
a very good community note, which is concise (at most 280 characters), interesting and clear to read, \
contains no unnecessary words, is backed by very solid evidence from sources that would be most likely \
to be found trustworthy by people on both sides of the political spectrum (citing URL(s)), and is \
written in a way that would be most likely to be found trustworthy by people on both sides of the \
political spectrum. \

The answer MUST be short, like a post on X (280 characters maximum, not counting URLs). \
The note should not include any sort of wasted characters e.g. [Source] when listing a URL. Just state the URL directly in the text. \
Each note MUST include at least one URL/link source. Nothing else counts as a source other than a URL/link. \
Each note MUST NOT use any hashtags (#). Keep a professional tone with no hashtags, emojis, etc. \

If the post does not need a community note (either because the original post is not misleading, \
or does not contain any concrete fact-checkable claims, \
then your decision should simply be "{NO_NOTE_NEEDED}".

If the post may need a community note, but you weren't able to find enough concrete evidence to \
write an ironclad community note, then your decision should be \
"{NOT_ENOUGH_EVIDENCE}".

If you are writing a note, don't preface it with anything like "Community Note:". Just write the note.

If you are writing a note, also identify which of the following misleading_tags apply to the post and note. \
You may choose as many tags as apply, but you must choose at least one:
- "factual_error":  # the post contains a factual error
- "manipulated_media":  # the post contains manipulated/fake/out-of-context media
- "outdated_information":  # the post contains outdated information
- "missing_important_context":  # the post is missing important context
- "disputed_claim_as_fact":  # including unverified claims
- "misinterpreted_satire":  # the post is satire that may likely be misinterpreted as fact
- "other":  # the post contains other misleading reasons

If you are not writing a note, set note_text to an empty string and misleading_tags to an empty list.

Post:

    {post_with_context_description}
    """


def _get_post_with_context_description_for_prompt(post_with_context: PostWithContext) -> str:
    description = f"""Post ID: {post_with_context.post.post_id}
Post text:
```
{post_with_context.post.text}
```
"""
    if post_with_context.quoted_post:
        description += f"""The post of interest had quoted (referenced) another post (Post ID: {post_with_context.quoted_post.post_id}). Here is the quoted post's text:
```
{post_with_context.quoted_post.text}
```
"""

    if post_with_context.in_reply_to_post:
        description += f"""The post of interest was a reply to another post (Post ID: {post_with_context.in_reply_to_post.post_id}). Here is the replied-to post's text:
```
{post_with_context.in_reply_to_post.text}
```
"""

    return description


def research_post_and_write_note(
    post_with_context: PostWithContext,
) -> NoteResult:
    post_with_context_description = _get_post_with_context_description_for_prompt(post_with_context)

    try:
        note_prompt = _get_prompt_for_note_writing(post_with_context_description)
        response = get_grok_search_json_response(note_prompt, NOTE_RESPONSE_SCHEMA)
    except Exception as e:
        return NoteResult(post=post_with_context, error=str(e), context_description=post_with_context_description)

    if response["decision"] != "WRITE NOTE":
        return NoteResult(post=post_with_context, refusal=response["decision"], context_description=post_with_context_description)

    if not response["misleading_tags"]:
        return NoteResult(post=post_with_context, error="Model wrote a note but chose no misleading tags.", context_description=post_with_context_description)

    return NoteResult(
        post=post_with_context,
        note=ProposedMisleadingNote(
            post_id=post_with_context.post.post_id,
            note_text=response["note_text"],
            misleading_tags=[MisleadingTag(tag) for tag in response["misleading_tags"]],
        ),
        context_description=post_with_context_description,
    )
