---
title: "so... how to create a skill that works?"
description: "A practical process for creating skill files by finding model failures, patching knowledge gaps, and benchmarking the result."
slug: how-to-create-a-skill-that-works
published_at: "2026-02-23T17:36:58Z"
modified_at: "2026-05-01T00:00:00Z"
date_display: "February 23, 2026"
section: "Claude skills"
tags:
  - Claude skills
  - AI agents
  - SkillBench
keywords:
  - Claude skills
  - AI agents
  - SkillBench
  - skill files
cover:
  src: assets/articles/how-to-create-a-skill-that-works/cover.jpg
  alt: "Cover image for so... how to create a skill that works?"
  og_alt: "Skill file article cover"
originally_published:
  platform: X
  url: "https://x.com/port_dev/status/2025988266525102525"
devto_id: 3687666
---

![Cover image for so... how to create a skill that works?](assets/articles/how-to-create-a-skill-that-works/cover.jpg)

In my previous article, I argued that skills don't work the way most people expect.

> Related: [Skills don't work the way we think they do](skills-dont-work-the-way-we-think-they-do.html)

The data from SkillBench supports this. Attaching skills doesn't automatically guarantee better performance.

So the real question becomes:

If skills don't magically fix models... How do you engineer them properly?

To answer that, we need to understand how knowledge itself works.

I think human knowledge is like a block of cheese.

![A block of cheese representing human knowledge](assets/articles/how-to-create-a-skill-that-works/human-knowledge-cheese.png "human knowledge or a block of cheese")

It grows over time, with holes ever-present.

When we hit something we don't know, we:

- look it up
- learn it
- apply it
- patch the hole and move forward

LLMs don't do this.

When they hit a hole, they don't say "I don't know."

They hallucinate. They lazily fill the gap with plausible-sounding but incorrect information.

Aaand that's where things break, and we, being the superior entity, come in to help.

## The Two Types of Holes

Through trial and error, I've noticed there are two kinds.

### 1. Knowledge gaps

Example:

My OpenClaw agent tries to open a browser extension. It fails.

I tell it:

> "You already have a browser. Open that."

Suddenly the dumdum understands the task and opens the freaking browser.

It wasn't incapable.

It just didn't reason through the environment correctly.

That's a hole.

### 2. Moldy knowledge

Sometimes it does know something, but it's outdated.

Examples:

- Using `useScaffoldContractRead` instead of `useScaffoldReadContract` in Scaffold-ETH
- Manually defining Monad mainnet instead of importing from `viem/chains`

That's stale info on the LLM's side. I call it mold.

And mold spreads silently. If you don't correct it once, it keeps reappearing in future runs. And you might never notice it.

## How I Create Skill Files

Here's my actual process.

### 1. I let the model fail

For example, when I was building the monad-development skill, I simply said:

> "Create a token on Monad."

That's it. Then I watched it fail.

I didn't over-direct it.

I wanted to see where the holes were.

### 2. I take notes on every failure

This sounds weird but yes I watch it and take notes/let it takes notes afterwards. after the LLM completes its run. I ask it "What did you have problems with?", "What did you fail to do on the first try?", and I go and check if the thing I asked for is built the way I wanted it to be.

### 3. I create the skill.md file

The skill file contains the patches to fill in the gaps of the LLMs knowledge and remove mold+fill in the gap that is created by removing the moldy part.

The file is concise, specific, and clear.

### 4. I re-run and benchmark

I run the same prompt again with the skill attached. If it still struggles, I refine the skill.

I repeat until:

- First-attempt success rate is high
- Hallucinations drop(mostly)
- Tool usage becomes clean and consistent

## What This Really Is

This is systematic failure harvesting. Treat the LLM as a system with blind spots and engineer around them.

Prompt. Let it fail. Take notes. Create a skill file out of your notes. Rinse and repeat until you are at a desired success rate.

This is how you create a skill that actually works.

## Further reading

SkillBench paper:

> Skills Don't Always Improve Performance<br>
> [https://arxiv.org/pdf/2602.12670](https://arxiv.org/pdf/2602.12670)

My previous article:

> [Skills don't work the way we think they do](skills-dont-work-the-way-we-think-they-do.html)

Vercel's agents.md versus skills.md article:

> AGENTS.md outperforms skills in our agent evals<br>
> [https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
