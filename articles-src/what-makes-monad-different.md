---
title: "What makes Monad different"
description: "You already ship on Base or Arbitrum and someone told you to try Monad. Here is what is actually different underneath the same Solidity, what it lets you build, and what will bite you on day one."
slug: "what-makes-monad-different"
published_at: "2026-09-21T12:00:00Z"
modified_at: "2026-09-21T12:00:00Z"
date_display: "September 21, 2026"
section: "Monad"
tags:
  - Monad
  - EVM
  - Solidity
keywords:
  - Monad
  - what makes Monad different
  - Monad vs L2
  - parallel EVM
  - MonadBFT
  - Monad finality
cover:
  src: "assets/articles/what-makes-monad-different/cover.svg"
  alt: "What makes Monad different"
  og_alt: "What makes Monad different, for devs who already ship on an EVM chain"
---

I keep getting the following question from people on every Blitz I do: "What makes Monad different?"  and I want to answer it in this article. 

I work at Monad, grain of salt and all that. Read along.


## Same code, so what changed

I understand why people ask this question. When you deploy a contract on Monad, everything is the same. You use the same foundry, the same viem/wagmi, and you deploy the same bytecode. So from a higher level nothing is really different, and from that viewpoint i understand the validity of this question.

What changed is the machine running that bytecode. The Monad client was written from scratch. It executes transactions in parallel and you don't even need to know it. It just watches what each transaction reads and re-runs the ones that conflicted. The state is stored in MonadDb. Most Ethereum clients keep the Merkle Patricia trie inside a generic key-value database such as LevelDB or RocksDB, so one data structure ends up embedded in another; MonadDb implements the Patricia trie directly, both on disk and in memory. And the consensus finalizes a block in two 300ms slots with around 200 validators voting on it. And the best thing here is that you don't need to know what's happening behind the scenes.

A note: I will be linking as many terms as I can out of this article to the relevant pages that explain them, so do not expect a linear read, feel free to jump between pages.

## whymonad.com

I made a site for this question a while ago: [whymonad.com](https://whymonad.com/). I was tired of saying "parallel EVM, 10k TPS, 300ms blocks". As far as I can tell, numbers by themselves don't make anyone switch chains; people switch when they try to build something and it doesn't work where they are. So the site takes three situations like that and plays them out on Ethereum, Solana, Arbitrum and Monad at the same time, with the same users.

<figure class="embed">
<iframe src="https://whymonad.com/embed/this-is-monad" title="Monad validators proposing live mainnet blocks, from whymonad.com" loading="lazy" scrolling="no" style="width:100%;height:640px;border:0;border-radius:6px;overflow:hidden" referrerpolicy="no-referrer-when-downgrade"></iframe>
<figcaption>live from whymonad.com, or <a href="https://whymonad.com/#this-is-monad">open this section on the site</a></figcaption>
</figure>

The site shows what happens in each case. The reasons are in the docs, and I've linked the pages as I go.

## A stablecoin breaks its peg

Suppose a stablecoin drops to $0.97. Half a million people now want out before it drops further, and the animation shows the first 70 of them trying on each chain.

<figure class="embed">
<iframe src="https://whymonad.com/embed/race" title="A stablecoin depeg simulated on four chains, from whymonad.com" loading="lazy" scrolling="no" style="width:100%;height:640px;border:0;border-radius:6px;overflow:hidden" referrerpolicy="no-referrer-when-downgrade"></iframe>
<figcaption>live from whymonad.com, or <a href="https://whymonad.com/#race">open this section on the site</a></figcaption>
</figure>

On Ethereum they queue and fees go up, because sequential execution and a generic state database cap the chain at about 15 transactions a second, and better hardware doesn't change that. On Solana execution is fast, but the exit you built for the EVM doesn't exist there. Solana has also gone down under this kind of load before, 17 hours in 2021 from a bot flood. On Arbitrum things are cheap and you get a soft confirmation in about 2 seconds. But it all goes through one sequencer, and if you want to actually leave to L1 that takes about 7 days.

On Monad everyone is out in under a second. Monad's consensus is [MonadBFT](https://docs.monad.xyz/monad-arch/consensus/monad-bft). A block gets voted on in the slot after it is proposed and becomes final in the slot after that. Slots are 300ms, so a transaction is final about 600ms after it enters a block, and that is guaranteed by the protocol. On an optimistic L2 the 200ms confirmation you show your user is the sequencer telling you what it plans to do, and the L1 settlement that actually locks it in is about a week away. On Monad there is no sequencer, so there is nothing upstream that can reorder or undo the transaction once it's final. And there are about 200 validators voting on it, which an L2 with one sequencer doesn't have.

The cost of this is hardware. A Monad full node wants 16 cores, 32 GB of RAM and two 2 TB NVMe drives, about four times the CPU and bandwidth of an Ethereum full node. I'd rather tell you here than have you find it on the hardware requirements page.

## A consumer app goes viral

Now consider the opposite situation, which is the day every consumer app is hoping for. A claim or a ticket drop or a game item blows up on social and wallets start signing all at once. Which chain lets most of those users actually finish the claim?

<figure class="embed">
<iframe src="https://whymonad.com/embed/launch" title="A viral consumer launch simulated on four chains, from whymonad.com" loading="lazy" scrolling="no" style="width:100%;height:640px;border:0;border-radius:6px;overflow:hidden" referrerpolicy="no-referrer-when-downgrade"></iframe>
<figcaption>live from whymonad.com, or <a href="https://whymonad.com/#launch">open this section on the site</a></figcaption>
</figure>

On Ethereum the launch gets expensive.  Some people wait it out. A lot of new users look at the fee, decide the claim is not worth it and close the tab, and those were the people the launch was for. On Solana fees are fine, but you can't bring your contracts, so first you port. On a rollup the claim is cheap and fast, and then the user asks how to move their thing somewhere else and you're explaining bridges.

On Monad the demand clears without leaving the EVM, mainly because there is a lot more room. The chain does 500M gas per second (150M per block, every 300ms) where Ethereum does 2.5M. A single transaction can spend 30M gas, which is an entire Ethereum block. A transfer is about 0.0021 MON, a swap about 0.02 MON. The base fee rises slowly and falls fast, so a spike raises fees gradually. And the contract taking all this is the same bytecode you already had, so the people who come back tomorrow find the same contract at the same address.

Consumer apps are also the ones that run out of room in the contract. On Monad contracts can be 128 KB instead of 24 KB, so the diamond proxy you built to fit under EIP-170 is optional now. Memory is priced linearly up to 8 MB. A 1 MB allocation is about 16k gas on Monad and about 2.2M on Ethereum. I measured one of these for [mipland](https://mipland.com/): a storage scratchpad rewritten to use memory instead went from 2,420,884 gas to 57,003 on mainnet, and the transaction hash is on the site if you want to check.

## A market moves before everyone can react

This has the same shape as the depeg, except there is money on both sides of it. The price breaks lower, liquidations fire around eight seconds in, arb spreads open up around twenty, and liquidators, arbitrageurs and market makers all hit the chain at once. Blockspace in those twenty seconds is worth more than at any other time, and transaction ordering decides who gets paid for it.

<figure class="embed">
<iframe src="https://whymonad.com/embed/market" title="A market shock simulated on four chains, from whymonad.com" loading="lazy" scrolling="no" style="width:100%;height:640px;border:0;border-radius:6px;overflow:hidden" referrerpolicy="no-referrer-when-downgrade"></iframe>
<figcaption>live from whymonad.com, or <a href="https://whymonad.com/#market">open this section on the site</a></figcaption>
</figure>

On Ethereum the liquidity is deep but it waits for blockspace. On Solana it's fast, but it's not the EVM liquidity that needs rebalancing. On a rollup execution is cheap, but ordering goes through the sequencer, so whoever runs the sequencer is in the trade.

On Monad two things matter here. The first is parallel execution, which means the liquidator and the arbitrageur don't wait on each other unless they actually touch the same state, and if they do, the client notices and re-runs the later one. The second is ordering: inside a block it is the leader's call, with a priority gas auction as the default, and there is no third-party block builder in the path. The consensus also has tail-fork resistance, meaning a leader cannot fork away the previous block to grab what was in it.

Fastlane just shipped the best example of this I've seen. [Moose](https://moose.trade) is a DEX aggregator that picks the route onchain, at execution time, based on the price each route actually fills at. The simulated quote doesn't enter into it. Their words: it "doesn't place a server between you and the blockchain," so there's no offchain quote for a market maker to spoof. You need the memory and contract limits from the last section and the execution from this one to write that.

## The matrix

The bottom of the site is a table with six rows: EVM compatible, decentralized validator set, high sustained throughput, sub-second finality, low fees as activity rises, self-sufficient base chain. For any one row you can find a chain that passes it; the claim is that Monad passes all six. The site says this looks like marketing until you see the mechanisms, and I agree, so here they are.

<figure class="embed">
<iframe src="https://whymonad.com/embed/matrix" title="Chain property comparison matrix, from whymonad.com" loading="lazy" scrolling="no" style="width:100%;height:640px;border:0;border-radius:6px;overflow:hidden" referrerpolicy="no-referrer-when-downgrade"></iframe>
<figcaption>live from whymonad.com, or <a href="https://whymonad.com/#matrix">open this section on the site</a></figcaption>
</figure>

<script>
window.addEventListener("message", function (e) {
  if (!e.data || e.data.type !== "whymonad-embed-height") return;
  var frames = document.querySelectorAll("figure.embed iframe");
  for (var i = 0; i < frames.length; i++) {
    if (frames[i].contentWindow === e.source) {
      frames[i].style.height = Math.ceil(e.data.height) + "px";
    }
  }
});
</script>

First, parallel EVM execution on unchanged bytecode. Second, MonadDb, from above, which also uses async I/O so parallel reads don't block each other. Third, pipelined consensus, so the slow steps overlap instead of running one after another. Fourth, finality two 300ms slots after proposal with a couple hundred validators, instead of one operator.

None of those can be added to an existing client later, which is why the site's "why this matters" section comes down to two lines: existing apps move without a rewrite, and more things become buildable.

## What will bite you on day one

If you port a working dapp to Monad, there are four things that break, and I'll take them in the order you'll hit them.

**Gas is charged on the limit, not on usage.** Consensus happens before execution, so when the chain charges you it doesn't know yet how much gas you'll use, and charging on usage would let someone set a huge limit while using almost none of it, which is a denial of service vector. So you pay `gas_limit * price`. This is fine until MetaMask sees a reverting `eth_estimateGas` and sets the limit to something absurd, and your user pays for it. The fix is to set explicit gas limits in your app and never ship a wallet-estimated limit on a path that can revert.

**There is no global mempool.** Transactions go to the next three leaders, not to everyone. If your product watches pending transactions, to index them or to front-run them, that doesn't port. Use the `monadNewHeads` and `monadLogs` feeds instead, which tell you what consensus did with each block you've seen, so you don't guess at reorgs.

**Every account keeps a 10 MON reserve.** A transaction that would take an EOA below 10 MON reverts. If the EOA is EIP-7702 delegated it reverts no matter what. Session key wallets and anything that sweeps an account to zero need a floor. No L2 has this and it's the one I see people hit at hackathons.

**Freshly funded accounts wait three blocks.** Execution runs a few blocks behind consensus, so an account that just went from zero to funded can't send until the funding transaction is three blocks deep. Your faucet-then-deploy script needs to wait about 1.2 seconds after the receipt, or one contract that funds and acts in the same call.

Also, full nodes don't keep arbitrary historical state. Blocks, receipts, logs and traces are all there, but `eth_getStorageAt` on a block from last month needs the historical RPC. If your analytics need an archive node, budget for it.

## The chain moves

Monad ships its own client and its own consensus, so protocol changes come as Monad Improvement Proposals every few months, and some change the gas schedule under you. MIP-8 went live in September and grouped storage into pages of 128 slots. A repeated write to a slot in a page you already touched is 100 gas now instead of 11,000. Arrays and structs get this for free; mappings don't, because each key lands on its own page. L2s don't have this, so read the spec before your next storage layout.

If you already ship on an EVM chain, run the three situations on [whymonad.com](https://whymonad.com/) with your own chain swapped in, then come back to the list of what breaks. Deploy the thing you already have and tell me how it went in the [Monad developer Discord](https://discord.gg/monaddev) or on [Telegram](https://t.me/portdev).
