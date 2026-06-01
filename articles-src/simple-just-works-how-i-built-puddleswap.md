---
title: "Simple just works: how i built puddleswap"
description: "How I built puddleswap on Monad testnet, why I almost overengineered the routing, and the case for solving the narrow problem you actually have instead of the general one you imagine."
slug: simple-just-works-how-i-built-puddleswap
published_at: "2026-05-17T12:00:00Z"
modified_at: "2026-05-17T12:00:00Z"
date_display: "May 17, 2026"
section: "Developer tools"
tags:
  - puddleswap
  - Monad
  - DEX
keywords:
  - puddleswap
  - Monad
  - DEX
  - routing
  - over-engineering
cover:
  src: assets/articles/simple-just-works-how-i-built-puddleswap/cover.svg
  alt: "Cover image for Simple just works: how i built puddleswap"
  og_alt: "puddleswap article cover"
originally_published:
  platform: X
  url: "https://x.com/port_dev"
devto_id: 3708879
---

![Cover image for Simple just works: how i built puddleswap](assets/articles/simple-just-works-how-i-built-puddleswap/cover.svg)

Any problem yields to enough complexity.

I caught myself almost doing exactly that on puddleswap. Here's how that went, plus the gut-check I run now before writing anything clever. If you ever feel yourself overengineering things, this is for you.

I was at a [Monad Blitz](https://blitz.devnads.com) event, if I am not mistaken it was the one in Ankara, and I was watching everyone around me hack on cool stuff while I sat in the corner answering their questions. I mean that's my job but it felt weird not building stuff while everyone else is trying their best.

So at some point I figured I should just build something(while not ignoring people at the same time lol). Something simple enough that the brag would be how little it took.

That's how puddleswap happened. A testnet dex on Monad testnet

Going in, I wanted the fewest moving parts I could get away with. The thing I'd be most proud of would be how little there was to maintain. (If possible, i wanted nothing to maintain at all.)

Most of the actual work was done by an AI agent. It wrote the React frontend and deployed the contracts; the swap UI came together as it went. The contracts are stock Uniswap V2, audited a thousand times over the years(centuries in web3). The frontend is Vite + React with no backend. The swap accepts real Circle USDC, a mock USDT we deployed for testnet liquidity, and WMON. A small rebalancer service on railway keeps the price pegs roughly honest.

It's live at [app.puddleswap.org](https://app.puddleswap.org/).

The build was mostly uneventful. The agent did its thing, I reviewed diffs, we iterated. What I want to talk about is the one decision I almost got wrong: the routing.

## The thing I almost overengineered

Standard answer for "how does a DEX UI route swaps" is a graph algorithm. You have N tokens and M pools, build the liquidity graph, run shortest-path weighted by output amount, return the best route. 1inch and Matcha both work this way and every aggregator article online tells you to do the same, so I started writing it.

Then I looked at my actual data.

Three "core" tokens: USDC, USDT, WMON. Maybe ten pools, every one of them touching at least one core. I was writing a graph algorithm to solve a problem I didn't have.

![Star routing diagram with A on the left, B on the right, and three core hubs USDC, USDT and WMON in the middle](assets/articles/simple-just-works-how-i-built-puddleswap/star-routing.svg "the whole graph: A and B connect through three core hubs, plus a direct edge when one exists")

So I deleted it and wrote the following instead (s/o to @danielvf for the idea + the initial PRD).

## The enumeration

For any swap A → B, enumerate every plausible route through the hubs:

- Direct: `A → B`
- Through one hub: `A → USDC → B`, `A → USDT → B`, `A → WMON → B`
- Through two hubs: `A → USDC → USDT → B`, `A → USDC → WMON → B`, `A → USDT → WMON → B`, and reverses

That's at most ten candidate paths. Send all ten quote requests in one multicall, pick the path with the highest output, swap on that.

```typescript
const routes = buildCandidateRoutes(tokenIn, tokenOut, cores);

const results = await publicClient.multicall({
  contracts: routes.map((path) => ({
    address: router,
    abi: routerAbi,
    functionName: "getAmountsOut",
    args: [amountIn, path],
  })),
  allowFailure: true,
});

const best = selectBestQuote(results);
```

The whole router is around 50 lines. It builds the candidate list (deduped) and returns whichever path the multicall said had the highest quote.

## Why this matters beyond DEXes

I'm not saying graph routing is wrong. For a mainnet aggregator routing across thousands of pools and dozens of DEXes, it's the right tool. But I wasn't building that.

Here's the lesson: **a lot of code over-solves its problem.**

You see it everywhere once you start looking. A sorting algorithm where the data is always ten items or fewer, when plain insertion sort would have done. A caching layer sitting in front of a database that gets hit twice a day, as if the database weren't already a cache. Or my favorite, pub/sub wired up for exactly one publisher and one subscriber, where you could have called the function. Another example you might have noticed is claude suggesting using redis for caching instead of using a simple in-memory cache for tiny apps that would not get restarted enough times to justify it.

The smart-looking solution is usually someone solving the *general* problem, because that's what they were trained on. The general problem is harder, more interesting, and absolutely useless to you if your constraints are narrower.

On puddleswap, my constraints are:

- One chain, one DEX
- Three hub tokens I control (or my agent controls)
- Operator-maintained liquidity
- UI being so simple that my grandma can use it(rip grandma)

Within those constraints, enumeration is provably correct (every meaningful route gets checked) and faster than graph traversal, since it's one batched RPC instead of N round-trips. It's also a fraction of the code. The day any of those constraints stops holding is the day I'll bother writing the graph router.

## When this breaks

I'd be lying if I said this scales. Obvious failure modes are:

- Exotic-to-exotic pools that bypass the hubs entirely. Enumeration misses them.
- A hub runs dry of liquidity on one side. Router still checks routes through it and eats a bad quote.

## The end

If you're building on Monad testnet and need swaps for your tests, puddleswap is live at [app.puddleswap.org](https://app.puddleswap.org/). The router is at [puddleswap/web/src/lib/routing.ts](https://github.com/portdeveloper/puddleswap/blob/main/web/src/lib/routing.ts).

And next time you reach for the complex solution, check whether your problem actually needs it. It probably doesn't. 

And maybe ask your agent if there are any easier solutions to the problem you are trying to solve.

> Related: [How to find ideas worth building](how-a-button-i-built-for-one-docs-site-ended-up-on-twenty.html) - the same heuristic applied to a different problem.

Questions?
