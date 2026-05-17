---
title: "Skills don't work the way we think they do"
description: "Notes on the SkillBench paper and what it says about curated skills, self-generated skills, and agent performance."
slug: skills-dont-work-the-way-we-think-they-do
published_at: "2026-02-20T18:39:10Z"
modified_at: "2026-05-01T00:00:00Z"
date_display: "February 20, 2026"
section: "Claude skills"
tags:
  - Claude skills
  - SkillBench
  - AI agents
keywords:
  - Claude skills
  - SkillBench
  - AI agents
  - agent performance
cover:
  src: assets/articles/skills-dont-work-the-way-we-think-they-do/cover.jpg
  alt: "Cover image for Skills don't work the way we think they do"
  og_alt: "SkillBench chart article cover"
originally_published:
  platform: X
  url: "https://x.com/port_dev/status/2024916757337571605"
devto_id: 3687663
---

![Cover image for Skills don't work the way we think they do](assets/articles/skills-dont-work-the-way-we-think-they-do/cover.jpg)

I just finished reading SkillBench paper: [https://arxiv.org/pdf/2602.12670](https://arxiv.org/pdf/2602.12670)

And the results are definitely not what most people expect.

## What researchers did

![SkillBench research setup screenshot](assets/articles/skills-dont-work-the-way-we-think-they-do/researchers-did.jpg)

They did 86 real-work tasks across 11 domains and executed 7,308 runs.

Each task was tested in three modes:

1. Baseline (no skills)
2. Curated skills (human-written)
3. Self-generated skills by the model

![SkillBench result comparing smaller models with skills to larger models without skills](assets/articles/skills-dont-work-the-way-we-think-they-do/haiku-skills-opus.jpg "haiku with good skills is better than vanilla opus")

Without further ado, below are some conclusions that I found interesting in the paper.

## Self-generated skills don't help

One of the most hyped ideas in agent research is:

> "Let the model write its own tools / skills."

But it is mostly a wasted effort. In this research, self-generated skills produced no meaningful improvement over baseline.

In some cases, they made performance worse.

Today's models simply cannot reliably create useful reusable procedural abstractions.

This matters because a huge part of current agent research assumes models can recursively improve by generating better skills/tools. This benchmark suggests that assumption is premature.

![SkillBench chart showing self-generated skills did not meaningfully improve performance](assets/articles/skills-dont-work-the-way-we-think-they-do/self-generated-skills.jpg)

## Human-made skills work A LOT better

When Skills were carefully written by humans, performance jumped +16.2 percentage points on average.

But here's what's even more surprising:

**Domain variance was extreme**

- Some domains saw small gains (~4-5 pp)
- Others saw enormous gains (~50+ pp)

![SkillBench chart showing high domain variance for human-made skills](assets/articles/skills-dont-work-the-way-we-think-they-do/human-skills-domain-variance.jpg)

Skills don't help the same in different fields.. They disproportionately help in structured, procedural domains.

## Smaller models + skills ≈ bigger models without skills

A smaller model with curated Skills matched or exceeded a larger model without Skills.

This is huge for cost optimization:

- Local agents
- Edge deployment
- Open-source models

## Too many skills can hurt

Overly broad or verbose skill libraries degraded performance. Focused, minimal skill modules performed better.

![SkillBench result showing too many skills can degrade performance](assets/articles/skills-dont-work-the-way-we-think-they-do/too-many-skills.jpg)

Pick your skills carefully. 2-3 skills work better than 4+ skills.

## Here is my takeaway

If this paper is right (and i think it is, mostly because of my personal experiences with skill files):

- Scaling alone isn't enough
- Autonomy narratives are premature
- Skill architecture design is now a first-class research problem

Read the full paper: [https://arxiv.org/pdf/2602.12670](https://arxiv.org/pdf/2602.12670)
