---
title: "rent geniuses, own workhorses"
description: "I run AI two opposite ways inside one app: Whisper transcription on a dead GTX 1050 laptop, and Claude in the cloud for the judgment calls. That split is the whole answer to 'should I run AI locally?'. You rent geniuses and you own workhorses, and I built a calculator (shouldirunthis.xyz) that proves owning the genius isn't worth it."
slug: "rent-geniuses-own-workhorses"
published_at: "2026-06-25T12:00:00Z"
modified_at: "2026-06-25T12:00:00Z"
date_display: "June 25, 2026"
section: "AI coding"
tags:
  - AI
  - local models
  - agents
keywords:
  - local ai
  - whisper
  - shouldirunthis
  - extractoor
  - raspberry pi agent
  - claude
cover:
  src: "assets/articles/rent-geniuses-own-workhorses/cover.png"
  alt: "rent geniuses, own workhorses"
  og_alt: "rent geniuses, own workhorses"
---

![rent geniuses, own workhorses](assets/articles/rent-geniuses-own-workhorses/cover.png "the line from the talk that the whole thing hangs on")

I put together a lightning talk for ClawCon Ankara around one question I keep getting asked: should I run AI locally? People want a yes or a no. The honest answer is that it depends on the job, and I only really got that after building one app where the same program leans on AI two completely opposite ways.

For anything broad and smart you rent it from the cloud. For one narrow, repetitive job you can own the hardware and run it for free until it dies. You rent geniuses, you own workhorses.

## the same app gave me two opposite answers

I built a thing called [extractoor](https://extractoor.com). You hand it a long video and it pulls out the clips worth posting. Under the hood it reaches for AI twice, and the two jobs taught me opposite lessons.

The first job is transcription, turning the audio into text. It's narrow and well defined, and a specialized model like Whisper is genuinely great at it. I run Whisper locally on a janky old laptop with a GTX 1050 in it. I can leave hours of audio grinding through it and the only bill is the electricity.

The second job is deciding which moments are actually any good. I send that to Claude in the cloud, because nothing I can run at home comes anywhere close.

## when you do want the genius at home

Sometimes you genuinely want a strong general model in your house, for privacy or just because you can. So I built a calculator for exactly that question: [shouldirunthis.xyz](https://shouldirunthis.xyz). It lists actual models with real GPU build prices and your own electricity rate, and tells you whether buying the rig beats paying for a subscription or an API.

The short version is that putting a real general model in your house runs from about $1,100 for a small one on a laptop up past nineteen grand for a serious rig, and for normal usage the verdict reads the same the whole way down the table: just subscribe. If you're wiring up an agent it can't use your $200 monthly plan anyway, so you flip the "I use the API" toggle and the verdict turns into just use the API. The rig only starts winning once you're burning more than a subscription can hold, which most people never get near.

Which loops right back to extractoor: **my transcription workhorse isn't even on that chart.** A GTX 1050 can't run a single general model the calculator lists. A narrow job runs fine on the hardware everyone else is throwing out.

## the rent is subsidized, for now

There's a reason the calculator keeps telling you to subscribe: right now the labs are selling the genius for far less than it costs them to run. [SemiAnalysis](https://x.com/SemiAnalysis_/status/2064815044085318040) bought every Anthropic and OpenAI plan in June and hammered them with coding tasks until the weekly limits cut out:

> Recently, we purchased one of each Anthropic/OpenAI subscription plan and randomly ran long horizon coding tasks until we exhausted the weekly limit. It's widely believed that a $200/month plan maxes out at ~$2000/month worth of tokens (assuming API pricing). However, we found...

The real number was nowhere near $2,000: a maxed-out Claude Max plan came out around $8,000 of API-priced tokens, and ChatGPT's top tier landed near $14,000. For a heavy user the subscription runs something like 40 to 70 times cheaper than paying the API rate for the same work.

So when shouldirunthis tells you to subscribe, that's the math talking, and the math only works because someone else is eating the bill. Subsidies get repriced once the people writing the checks want their margins back, and when the rent goes up some of those home rigs start to pencil out.

None of this touches the workhorse half. The narrow job on my dead 1050 won't care what a Claude plan costs next year, because it was never renting anything to begin with.

## wiring it into one personal agent

So how do you build a personal agent with all of this in your head? You split it by job. I put the always-on brain on a Raspberry Pi, the part that keeps my context and answers me whenever, because it has to run forever and barely touches the power bill. The heavy reasoning it can't do itself, it hands to the cloud. The boring repetitive grunt work can go to that dead 1050 sitting next to it.

I stood up an OpenClaw agent on the Pi as that brain and pointed it at deepseek-v4-pro. To be clear, that model is not running on the Pi and it never could, it wants something like thirteen thousand dollars of GPUs and two and a half kilowatts to even boot, so the Pi is really just placing a cloud call. Which is the whole thesis happening to me by accident: I never even tried to run the genius at home, because I'd already built the thing that told me not to.

I had this running on my own scrappy orchestrator, Hermes, before I swapped OpenClaw in, and honestly the orchestrator barely matters. The split is what matters, and it holds up no matter which orchestrator you drop in.

## so, should you run it locally?

That's the wrong question to lead with. Ask which job you're actually looking at and let that decide where it runs. Almost every agent worth building needs both at once, wired together anyway.

You rent geniuses. You own workhorses.

[extractoor.com](https://extractoor.com) if you want the app. [shouldirunthis.xyz](https://shouldirunthis.xyz) if you want to run the math for your own setup before you spend a cent.
