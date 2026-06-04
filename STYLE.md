# Article style guide

How articles on portdeveloper.github.io are written. Derived from the existing posts (puddleswap, vibe-code, skills, GPT 5.5, how-to-create-a-skill). If you are drafting something for this site, follow this. If a rule below contradicts what's in an existing article, the article wins and this file is wrong.

## Hard rules (do not violate)

1. **No em-dashes.** Not "—", not "–". Use a regular hyphen "-", a comma, parentheses, or two sentences. This is the #1 AI-slop tell.
2. **Straight quotes only.** `"` and `'`, never `"` `"` `'` `'`.
3. **No "delve", "leverage", "robust", "seamless", "ecosystem" (when used as filler), "landscape", "journey", "unpack", "deep dive", "navigate" (when figurative).**
4. **No "It's worth noting that", "Moreover", "Furthermore", "Additionally", "In conclusion", "In today's world", "Whether you're X or Y".**
5. **No tricolon symmetry as a stylistic crutch.** "Fast, reliable, and scalable" reads as marketing copy. Pick one and say why.
6. **No hedge stacking.** "Perhaps it could potentially be argued that..." gets cut to the claim.
7. **No closing summary that restates the article.** End on the punch, the CTA, or the link. Not a recap.
8. **No headings like "Introduction", "Conclusion", "Background".** Headings name the actual thing in that section ("The thing I almost overengineered", "Too many skills can hurt").
9. **No antithesis-as-emphasis ("X, not Y").** Banned: "This is X, not Y", "It's not X, it's Y", "not just X but Y", and bare "X, not Y" clauses dropped in for emphasis. It's a copywriter reflex and one of the loudest AI tells. Delete it or state the point flat. "This is a courtesy heads-up, not a blocker." becomes "No rush on it." "It's not about speed, it's about correctness." becomes "Correctness is the point." If a contrast is genuinely load-bearing (a real correction the reader needs), split it into two sentences instead of hinging on a comma. Write "it's under `linux-arm64`. The `linux-aarch64` path 404s." rather than "it's under `linux-arm64`, not `linux-aarch64`."
10. **No standalone punch-sentences.** Short declarative beats dropped in for emphasis are an AI terseness tic: "That's the whole fix.", "That's it.", "That's the point.", "It's a separate commit.", "It's that simple.", "This isn't theoretical.", "Wrong." Cut them, or fold the point into the surrounding line. The same goes for meta-narration that announces what the writing does ("so the guide leads with the distinction", "this section will cover") instead of just doing it. A normal relative clause inside a longer sentence ("that's the field you add") is fine; the tic is the standalone punchy one.
11. **No fronted participial or absolute-phrase openers.** A sentence that leads with a detached `-ing`/`-ed` clause or an absolute phrase before the subject is a top-tier AI-essay tell. Banned: "Left to its defaults, an agent reaches for the textbook answer.", "Having shipped it, I moved on.", "Armed with the data, the choice was obvious.", "Faced with ten pools, a graph was overkill.", "Trained on the general case, the model reaches for it." Start on the subject instead: "An agent reaches for the textbook answer by default." Paul Graham's prose is ~95% subject-initial (in "Write Simply," 24 of 25 sentences open on the subject); match that. The trailing version is the same tell and also out: "..., having met the general case years before the specific one" becomes a clause that stands on its own subject ("we meet the general case years before the specific one"). This does NOT ban short adverbial or prepositional openers, which are in-voice and common here: "Then I looked at my actual data.", "On puddleswap, my constraints are", "So I deleted it." The tell is specifically a participle or absolute phrase doing scene-setting work in front of the subject. A short idiomatic participial that port already reaches for is voice, not slop, and stays ("Going in, I wanted the fewest moving parts"); the ban is for the longer constructed kind ("Left to its defaults,", "Having met the general case,").

## Voice

- First person, direct. "I built", "I deleted it", "I caught myself".
- Default opener is a personal-narrative arc, not a detached observation. "One day I saw that...", "I was at a Monad Blitz...", "I just finished reading the SkillBench paper". Not "There's a button on most docs sites now" (that's a third-person reporter voice — wrong).
- Self-deprecating is fine and encouraged where it's honest. ("I sat in the corner answering their questions. I mean that's my job but it felt weird not building stuff.")
- Talk to the reader like a person who already does this work. No throat-clearing about what AI is or what Docusaurus is.
- Strong direct judgments are allowed and preferred over hedged ones. "That just won't work." "Don't do that." "Stop." "The general problem is harder, more interesting, and absolutely useless to you if your constraints are narrower."
- Rhetorical questions are in-style, used sparingly. "Have you ever tried doing this natively?", "If this is a problem for me, it is a problem for other people as well, right?". They invite the reader in. Don't stack more than one per section.
- Casual interjections OK in moderation: `btw`, `lol`, `s/o`, `kinda`, `honestly`, `aaand`, `alright`. Don't stack them.
- Specific named people / projects > generic references. "@Simek's RN-PR review" not "feedback from a contributor".
- **When the outcome is uncertain, hedge and put yourself in the sentence — don't predict with fake confidence.** AI writes "Some will land this month. Some will sit for ages." (third-person reporter, confident future tense, parallel structure). The voice version is "Some might never get merged in but some might get in, I try my best!" (hedged "might", joined with "but", personal aside that admits you're the one trying). The point isn't the hedging itself — it's that you, the person doing the work, are visible in the sentence.

## Punctuation and microstyle

- Use `&` occasionally for tight pairings (`faster&better`, `prompt+test+fix`). Don't force it.
- Parenthetical asides are fine, often informal: `(btw the full examples are at the end)`, `(centuries in web3)`, `(s/o to @danielvf)`.
- Stretched words for emphasis are allowed and on-brand: `aaaand`, `aaand`, `dumdum`. Use sparingly.
- Emoji and emoji shortcodes are allowed for self-deprecating callouts only. 😭 is the workhorse (`Enough boasting 😭`, `I don't 😭`). Cap: one per section, max two per article. Never use emoji for decoration, never use them where bold would do the job. Write emoji as actual unicode characters (`😭`), not shortcodes (`:sob:`), since the site is plain markdown.
- Exclamation marks are fine if they're earned by real enthusiasm or surprise. "It was great!" earns one. "Here's the article!" doesn't.
- Lowercase `i` is the default in **titles** ("how i built puddleswap"). Body text uses `I` in normal sentences, but port lets `i` go lowercase inside casual parenthetical asides ("(If possible, i wanted nothing to maintain at all.)"). Don't auto-correct those, and don't worry if a casual proper noun shows up lowercase in body text either (`dex`, `claude`, `railway`).
- Sentence-case titles, no Title Case.
- Sentence fragments are fine. So are one-word sentences. Use them for rhythm.
- Code blocks for code, not for emphasis. Don't put a one-liner observation in a code block.

## Structure

- Hook in the first 1-3 sentences. Either a scene, a strong claim, or the punchline-of-the-article.
- The intro often compresses the whole arc up-front, then the body sections add depth and color, not retelling. Don't save the reveal for the end.
- Most articles have 3-5 H2 sections. Don't pad with more.
- Lead each section by saying the thing, then unpacking it. Don't bury the lede.
- Brags get punctured. If a sentence makes you sound good, the next line pops the balloon. ("My little plugin is now used by over twenty docs sites... Enough boasting 😭.", "The plugin has a contributor base now. I don't 😭."). This is what keeps the article likable.
- Numbered lists are good for the "look how far this has come" reveal — list a handful of name-drops, then punch out.
- A short "the end" / call-to-action paragraph closes the piece. Examples that work:
  - puddleswap: "If you're building on Monad testnet and need swaps for your tests, puddleswap is live at..."
  - GPT 5.5: "if you take one thing from this: before you reach for that Extra High button, rewrite the prompt..."
- Pull-quote (`>`) is used for: external quotes, links to related posts, paper citations, sample prompts. Not for emphasizing your own sentences (use bold for that).
- Bold a *pivot* sentence inside a paragraph when the article turns on it. "Here's the lesson: **a lot of code over-solves its problem.**"
- Lists are fine when the items are genuinely parallel (constraints, failure modes, prompts to try). Don't list things just to make the page scannable.

## Things that are *not* AI-slop but read like it if overdone

These are tools, not sins. Use them, but notice when you've used them three times in one article:

- "Here's what changed."
- "The fix is..."
- "Two things:"
- "Don't do that."
- Cold-open sentences ("So I deleted it.").

If every section opens this way, the rhythm collapses into a tic. Vary it.

## The "punchy claim + parallel sentence list + punchy closer" pattern

This is the single most AI-shaped cadence and it sneaks in constantly. It has two common variants.

**Variant A (SVO list + "by the time" closer):**

> It's awful. Selection grabs the nav and the sidebar. Code blocks lose their fences. Inline links turn into raw text. Tables collapse. By the time you've cleaned it up in your prompt window, you've forgotten what you were trying to ask.

**Variant B (imperative-fragment list + terse double closer):**

> So I asked Claude to build a custom button for the Monad site. Find the article container, walk the DOM, convert it to clean markdown, drop the result in the clipboard. Maybe 200 lines. Took an afternoon.

Why both read as slop:

1. Four list items in a row with identical grammar and near-identical length. Whether they're SVO sentences ("X verbs Y. X verbs Y.") or imperative fragments ("Verb X. Verb Y."), the rhythm is monotone.
2. The closer is templated. Either a too-tidy "By the time you've X, you've Y" construction, or a stack of two 2-4 word punchy fragments ("Maybe 200 lines. Took an afternoon." / "Couple hundred lines. Done.").
3. The whole paragraph reads as "engineered for scannability" rather than written by a person talking.

Fix in order of preference:

1. **Fold the list into a parenthetical or comma chain** instead of one-sentence-per-item. ("You always get more than you wanted (the sidebar, the navbar, three layers of breadcrumb) and the formatting always breaks in transit.")
2. **Vary sentence length aggressively.** A 4-word sentence, a 25-word sentence, a one-word sentence. Mix.
3. **Integrate the punchy closer into a full sentence.** ("The whole thing came out to maybe 200 lines and I shipped it the same afternoon." beats "Maybe 200 lines. Took an afternoon.")
4. **Replace the "by the time" construction with a personal consequence.** ("I'd spend more time massaging the paste than writing the question." beats "By the time you've cleaned it up, you've forgotten what you were asking.")
5. **Cut the inventory entirely** if you can describe the *feeling* in one sentence. The reader rarely needs a checklist.

Two specific micro-tells to never write:

- **Three or more parallel items in a row, in any punctuation form.** Doesn't matter whether they're full sentences (`Find X. Walk Y. Convert Z.`), comma-separated phrases inside one sentence (`find X, walk Y, convert Z`), colon-introduced clauses (`The logic is dumb: find X, walk Y, convert Z`), or bullet points. The slop is the parallel-rule-of-three itself, not the punctuation around it. AI loves rule-of-three because it sounds rhetorical; humans naturally write two-item or four-item lists more often than three-item ones, and rarely with perfect grammatical symmetry. If you have to enumerate three things, break the parallel structure (different verb tenses, different lengths, an aside in the middle) or drop the list entirely and state the gist.
- **A paragraph ending with two consecutive 2-4 word sentence fragments.** ("Done. Took an hour." / "Maybe 50 lines. Worked first try.") One short closer is fine; stacking two reads as AI trying to sound terse.

If you catch yourself stacking parallel sentences or three-item lists, stop and rewrite the paragraph.

## Headings

- Sentence case. No trailing punctuation except `?` if it's actually a question.
- Name the content. "The thing I almost overengineered" beats "Overengineering". "Too many skills can hurt" beats "Limitations".
- Numbered headings (`## 1. Lead with the outcome`) are fine for how-to articles where the order matters. Don't number for the sake of it.

## Code, links, images

- Inline code for identifiers, file paths, package names, flags.
- Fenced blocks with language tag (` ```typescript `, ` ```js `) for snippets.
- Link to specific files / lines on GitHub when referencing your own code.
- Images get an alt and a caption (the caption is the third arg in the markdown: `![alt](src "caption")`). Captions are lowercase, conversational. ("the whole graph: A and B connect through three core hubs"). They are not redundant restatements of the alt.

## What an opening looks like

Good (puddleswap):
> Any problem yields to enough complexity.
>
> I caught myself almost doing exactly that on puddleswap. Here's how that went, plus the gut-check I run now before writing anything clever.

Good (skills):
> I just finished reading SkillBench paper: [link]
>
> And the results are definitely not what most people expect.

Good (copy-page-button — story-arc opening that compresses the whole article):
> One day I saw that every company was adding a copy page button to their docs. I wanted to add one to Monad docs as well. So I built something with Claude, and then I thought, well why don't I make this a plugin so that other people use it too? If this is a problem for me, it is a problem for other people as well, right?
>
> I quickly published an initial version and I have been maintaining it for months now.
>
> My little plugin is now used by over twenty docs sites, most notably:
>
> 1. Sui
> 2. Ethereum execution-apis
> 3. Arbitrum
>
> Enough boasting 😭. Now I will explain how I built it, why, and how you can do the same!

Bad (would never appear here):
> In the rapidly evolving landscape of AI-assisted development, it's worth noting that prompting techniques have become increasingly important. This article will delve into the nuances of...

## What a closing looks like

Good (puddleswap):
> And next time you reach for the complex solution, check whether your problem actually needs it. It probably doesn't.
>
> And maybe ask your agent if there are any easier solutions to the problem you are trying to solve.
>
> Questions?

Good (vibe-code):
> Now, go.
>
> And do magic, for we live in a magical era.

Bad:
> In conclusion, we have explored the various aspects of X. By following these best practices, you can ensure your workflow remains efficient and your output remains high-quality.

## The frontmatter

Copy an existing article's frontmatter as the template. Don't try to remember the shape. Required fields: `title`, `description`, `slug`, `published_at`, `modified_at`, `date_display`, `section`, `tags`, `keywords`, `cover`. `originally_published` and `devto_id` get added if/when cross-posted.

## Calibration from port's own edits

Port revised a draft by hand. The pattern in those edits, recorded so the same things stop getting reintroduced:

- **Cut the writerly closer-clause.** "A no-bs DEX on Monad testnet, the kind a weekend buys you." became "A testnet dex on Monad testnet". The clause that makes a sentence sound well-crafted is usually the first one to delete. Plainer wins.
- **Keep humanizing asides even when they don't advance the argument.** Port added "while everyone else is trying their best", "(rip grandma)", "(or my agent controls)", "(If possible, i wanted nothing to maintain at all.)". These exist to sound like a person typed them. Don't strip them as redundant, and don't be afraid to add them.
- **Name the concrete thing.** "A small rebalancer service" gained "on railway". Say the host, the tool, the place when you know it.
- **Reach for a lived, current example over a textbook one.** To the list of over-engineering examples port appended "claude suggesting using redis for caching instead of a simple in-memory cache for tiny apps that would not get restarted enough times to justify it." Specific, agent-era, from experience. It's also a fourth item, longer and shaped differently than the three before it, which breaks the rhythm instead of padding a rule-of-three. A good model for how to add an example without making the list more symmetric.
- **Trim dead intensifiers and spare clauses.** "with no backend anywhere" lost "anywhere". "audited a thousand times over the years (centuries in web3) and not something I wanted to fork" lost the trailing clause. "Vite plus React" became "Vite + React" (use `+` for tight pairs).
- **Don't echo your own framing verb.** "it's the right tool. I'm saying I wasn't building that." became "...the right tool. But I wasn't building that." The repeated "I'm saying" was the tell; a plain "But" carries it.
- **Dropping "X, not Y" usually means deleting Y, not rephrasing it.** "how little it took, not how clever it was" just became "how little it took". Port cut the antithesis rather than splitting it into two sentences. When in doubt, delete the contrast clause.

## More slop tells (caught while drafting, 2026-06)

These kept reappearing even in a piece that was about avoiding slop. Watch for them.

- **Don't telegraph the question, just ask it.** "The question I wanted answered was simple:" or "what I really wanted to know was" is throat-clearing. Cut to "I had a question in mind:" or ask the question in the first person and move on.
- **Don't announce the result before you give it.** "the part I expected it to fail, it nailed:" and "here's the surprising part" pre-chew the reader's reaction. Show what happened and let them have the reaction themselves.
- **Say a motif once.** A good setup line ("I never told it which chain it was for") loses all its weight if you repeat it three times across the piece. State the premise once, pay it off once, don't restate it in between.
- **The rule-of-three keeps coming back in disguise.** It isn't only "fast, reliable, and scalable." Verb lists ("run it, fine-tune it, and ship it"), noun lists ("a pot, a short timer, every click, and whoever clicks last"), and clause lists ("imported Hardhat, declared two constructors, used a fake modifier, and called a dead helper") are the same tell. Cut to one vivid item, or break the parallel hard.
- **No standalone punch-sentences for drama.** "Then I watched.", "It didn't.", "Credit where it's due." Each is a tic. Fold the point into the sentence next to it.
- **Don't inflate the stakes for effect.** "the bug that emptied the DAO in 2016 and split Ethereum in two" is two clauses of drama where one plain fact carries it: "the bug behind the 2016 DAO hack". State it flat.

## When in doubt

Read the puddleswap article. If your draft sounds different in voice, fix the draft.
