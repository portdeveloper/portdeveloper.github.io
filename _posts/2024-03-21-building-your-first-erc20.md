---
layout: post
title: "Building Your First ERC20 and Understanding How it Really Works"
date: 2024-12-21 6:00:00 +0300
categories: blockchain solidity
---

![ERC20 Token Header Image]({{ site.baseurl }}/assets/images/erc20/header.png)

## Table of contents

- [What's up with the name?](#whats-up-with-the-name)
- [What is an erc20 token?](#what-is-an-erc20-token)
- [Looking at it from above](#looking-at-it-from-above)
- [Understanding the interface first](#understanding-the-interface-first)
- [Building our erc20 token step by step](#building-our-erc20-token-step-by-step)
  - [Step 1: setting up the basic structure](#step-1-setting-up-the-basic-structure)
  - [Step 2: adding balance tracking](#step-2-adding-balance-tracking)
  - [Step 3: implementing token transfers](#step-3-implementing-token-transfers)
  - [Step 4: adding the approval system](#step-4-adding-the-approval-system)
- [Where are the values stored?](#where-are-the-values-stored)
- [Events](#events)
- [Deploying our contract](#deploying-our-contract)
- [What we've built](#what-weve-built)
- [Common gotchas & security considerations](#common-gotchas--security-considerations)
- [Where to go from here](#where-to-go-from-here)

You have probably traded lots of meme coins, made some money and lost some money, and almost everyone knows how ERC20s work on a basic level. They have a transfer function and stuff. But let's dive deeper to understand how it really works under the hood.

## What's up with the name?

ERC stands for "Ethereum Request for Comments", and an ERC is a proposal for Ethereum Standards to ensure interoperability across the ecosystem. [ERC20](https://eips.ethereum.org/EIPS/eip-20) was the 20th of such proposals, and it defined a standard for fungible tokens. Since every other fungible token out there supports the ERC20 standards, we know how to interact with any token.

## What is an erc20 token?

An ERC20 token is just a ✨glorified✨ Excel spreadsheet that keeps token balances and updates them when asked to. When you are sending some tokens to someone else, you're just asking the contract to subtract some amount of tokens from your balance, and add that amount to theirs, if you have the balance to be able to do so. The key difference from a ✨glorified✨ spreadsheet is that these balance updates happen on the blockchain, which means they are permanent and can't be tampered with once they're recorded. In addition, anyone can check these balances and verify them any time.

## Looking at it from above

[Here is the most widely-used ERC20 smart contract implementation ever from the OpenZeppelin team.](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol) I suggest you stop reading this article here, go to OpenZeppelin's implementation of ERC20, and read it slowly. Take your time. We will use almost all of those. And don't get scared if it's a bit overwhelming and long! Even if you skim it, you will get a good idea of how an ERC20 works. We will be building our own ERC20 step by step below.

## Understanding the interface first

Before we start coding, let's understand what functions an ERC20 token must implement. Think of this as our blueprint:

![ERC20 Token Architecture Diagram]({{ site.baseurl }}/assets/images/erc20/erc20-diagram.svg)

Here's the interface our token needs to implement:

```solidity
// Get the name of the token
function name() public view returns (string)

// Get the symbol of the token
function symbol() public view returns (string)

// Get the number of decimals the token uses
function decimals() public view returns (uint8)

// Get the total supply of the token
function totalSupply() public view returns (uint256)

// Get the balance of an address
function balanceOf(address _owner) public view returns (uint256 balance)

// Transfer tokens from one address to another as the caller
function transfer(address _to, uint256 _value) public returns (bool success)

// Transfer tokens from one address to another, but only if the caller has been approved to do so
function transferFrom(address _from, address _to, uint256 _value) public returns (bool success)

// Approve another address to transfer tokens on behalf of the caller
function approve(address _spender, uint256 _value) public returns (bool success)

// Get the remaining number of tokens that an address is allowed to transfer on behalf of another address
function allowance(address _owner, address _spender) public view returns (uint256 remaining)
```

> **💡 Note:** You are probably wondering about the difference between `transfer` and `transferFrom`:
>
> - `transfer`: Used when YOU are directly sending your own tokens
> - `transferFrom`: Used when you're moving tokens on behalf of someone else who has approved you to do so (like when a DEX moves your tokens after you approve it)

## Building our erc20 token step by step

Now let's build our token piece by piece. We'll use Remix - a browser-based IDE that's perfect for writing and testing Ethereum smart contracts.

> **💡 Quick Setup:** Head over to [remix.ethereum.org](https://remix.ethereum.org/#), create a new file called `ERC20.sol` in the contracts section, and let's start coding!

### Step 1: setting up the basic structure

First, let's create the basic structure with our token's identity:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MyExtremelySimpleToken {
    string public name = "MyExtremelySimpleToken";
    string public symbol = "MEST";
    uint8 public decimals = 18;
}
```

Here we have defined the name, symbol, and decimals of our token. Notice the different types of variables we are using. We have used `string` for the name and symbol, and `uint8` for the decimals.

Next, let's add the core functionality - tracking token balances.

### Step 2: adding balance tracking

```solidity
contract MyExtremelySimpleToken {
    // ... previous code ...

    uint256 private _totalSupply;
    mapping(address => uint256) private _balances;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor() {
        _totalSupply = 1000000 * 10**18;  // 1 million tokens
        _balances[msg.sender] = _totalSupply;
        emit Transfer(address(0), msg.sender, _totalSupply);
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }
}
```

Now we have added a private variable `_totalSupply` to track the total supply of the token, which we initialize to 1 million tokens in the constructor. We also added a mapping `_balances` to track the balance of each address. Also we have an event `Transfer` that we will emit when a transfer happens. Inside the constructor, we have initialized the total supply and given all the tokens to the creator(which is the deployer of the contract). And that happens to be me. I am rich now.💸💸💸 In the constructor, we have also emitted a `Transfer` event to indicate that the total supply has been transferred to the creator. Also we have implemented `totalSupply()` and `balanceOf()` functions to get the total supply and the balance of any address respectively.

Now our little ERC20 token is able to keep track of the total supply and the balance of any address. But it doesn't have the ability to transfer tokens yet. Let's add that now.

### Step 3: implementing token transfers

```solidity
contract MyExtremelySimpleToken {
    // ... previous code ...

    function transfer(address to, uint256 amount) public returns (bool) {
        require(_balances[msg.sender] >= amount, "Insufficient balance");

        _balances[msg.sender] -= amount;
        _balances[to] += amount;

        emit Transfer(msg.sender, to, amount);
        return true;
    }
}
```

This `transfer` function is used to transfer tokens from the caller to another address. It takes two arguments: the address to transfer the tokens to, and the amount of tokens to transfer. It returns a boolean to indicate the success of the transfer. We also have a `TransferFrom` function that is used to transfer tokens from one address to another, but only if the caller has been approved to do so. And `TransferFrom` is what enables decentralized exchanges to move tokens from one address to another.

Let's move on to implementing the approval system.

### Step 4: adding the approval system

```solidity
contract MyExtremelySimpleToken {
    // ... previous code ...

    mapping(address => mapping(address => uint256)) private _allowances;
    event Approval(address indexed owner, address indexed spender, uint256 value);

    function approve(address spender, uint256 amount) public returns (bool) {
        _allowances[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowances[owner][spender];
    }

    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        require(_allowances[from][msg.sender] >= amount, "Insufficient allowance");
        require(_balances[from] >= amount, "Insufficient balance");

        _allowances[from][msg.sender] -= amount;
        _balances[from] -= amount;
        _balances[to] += amount;

        emit Transfer(from, to, amount);
        return true;
    }
}
```

### Getting the full picture

Now here is the full code with all the comments.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MyExtremelySimpleToken {
    // This is the name of our token, a public variable of type string - OPTIONAL
    string public name = "MyExtremelySimpleToken";
    // This is the symbol of our token, a public variable of type string - OPTIONAL
    string public symbol = "MEST";
    // This is the number of decimals our token uses, a public variable of type uint8 - OPTIONAL
    uint8 public decimals = 18;

    // Track total supply
    uint256 private _totalSupply;

    // Track all balances
    mapping(address => uint256) private _balances;
    // Track all allowances
    mapping(address => mapping(address => uint256)) private _allowances;

    // Transfer event is emitted when tokens are transferred from one address to another
    event Transfer(address indexed from, address indexed to, uint256 value);
    // Approval event is emitted when an allowance is set for an address
    event Approval(address indexed owner, address indexed spender, uint256 value);
    // More on events below!

    constructor() {
        _totalSupply = 1000000 * 10**18;  // 1 million tokens with 18 decimals
        _balances[msg.sender] = _totalSupply; // Give all the tokens to the creator
        emit Transfer(address(0), msg.sender, _totalSupply); // Emit a Transfer event
    }

    // Returns the total supply of the token
    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    // Returns the balance of an account
    // Notice that this is a public function, and it is view, which means it doesn't modify the state of the contract. Also the return type is uint256, which is the type of the balance.
    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }

    // Transfers tokens from the caller to another address
    // This is a public function, and it returns a boolean. It also modifies the state of the contract, so it is not marked as view.
    // The function takes two arguments: the address to transfer the tokens to, and the amount of tokens to transfer.
    // The arguments are of type address and uint256.
    function transfer(address to, uint256 amount) public returns (bool) {
        // Require the msg.sender has more tokens than the amount they are trying to transfer
        require(_balances[msg.sender] >= amount, "Insufficient balance");
        // Subtract the amount from the msg.sender's balance
        _balances[msg.sender] -= amount;
        // Add the amount to the recipient's balance
        _balances[to] += amount;
        // Emit a Transfer event
        emit Transfer(msg.sender, to, amount);
        // Return true to indicate the transfer was successful
        return true;
    }

    // Approves another address to transfer tokens on behalf of the caller
    // This is a public function, and it returns a boolean. It also modifies the state of the contract, so it is not marked as view.
    // The function takes two arguments: the address to approve, and the amount of tokens to approve.
    // The arguments are of type address and uint256.
    function approve(address spender, uint256 amount) public returns (bool) {
        _allowances[msg.sender][spender] = amount; // Set the allowance
        emit Approval(msg.sender, spender, amount); // Emit an Approval event
        return true; // Return true to indicate the approval was successful
    }

    // Returns the remaining number of tokens that an address is allowed to transfer on behalf of another address
    // This is a public function, and it is marked as view, which means it doesn't modify the state of the contract.
    // The function takes two arguments: the address of the owner, and the address of the spender.
    // The return type is uint256, which is the type of the allowance.
    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowances[owner][spender];
    }

    // Transfers tokens from one address to another, but only if the caller has been approved to do so
    // This is a public function, and it returns a boolean. It also modifies the state of the contract, so it is not marked as view.
    // The function takes three arguments: the address of the sender, the address of the recipient, and the amount of tokens to transfer.
    // The arguments are of type address and uint256.
    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        // Require the caller has been approved to transfer the amount
        require(_allowances[from][msg.sender] >= amount, "Insufficient allowance");
        // Require the sender has enough tokens to transfer
        require(_balances[from] >= amount, "Insufficient balance");

        _allowances[from][msg.sender] -= amount; // Subtract the amount from the caller's allowance
        _balances[from] -= amount; // Subtract the amount from the sender's balance
        _balances[to] += amount; // Add the amount to the recipient's balance

        emit Transfer(from, to, amount); // Emit a Transfer event
        return true; // Return true to indicate the transfer was successful
    }
}
```

## Where are the values stored?

`name`, `symbol`, and `decimals` are stored in the contract's storage. `name` is stored in slot 0, `symbol` is stored in slot 1, and `decimals` is stored in slot 2.

Let's inspect the contract's storage using [Storagoor v2](https://storagoorv2.vercel.app/) to see the values of `name`, `symbol`, and `decimals`. I have already [deployed the contract we wrote to the Sepolia testnet.](https://sepolia.etherscan.io/address/0x668058852F2083c699b01fBD503Dd3Dba9F56b69)

You can select Sepolia as the network and the contract address as `0x668058852F2083c699b01fBD503Dd3Dba9F56b69`.
Then, if you put in 0 for the storage slot position, and click "Read Storage Slot", you get 4 interpretations of the value of `name`, since it is stored in the position 0. You can do the same for other variables except for mappings.

Mappings work quite differently. Let's look at our two mappings:

```solidity
mapping(address => uint256) private _balances;
mapping(address => mapping(address => uint256)) private _allowances;
```

For the `_balances` mapping:

- If the mapping is at slot `p`, then the value for key `k` is stored at: `keccak256(h(k) . p)`
- Where `.` represents concatenation and `h(k)` is the key padded to 32 bytes
- So if `_balances` is at slot 3, the balance for address `0x123...` would be at: `keccak256(0x123...000...000 . 0x0000...0003)`

For the nested `_allowances` mapping:

- For a nested mapping at slot `p`, the value for keys `k1` and `k2` is at: `keccak256(h(k2) . keccak256(h(k1) . p))`
- So if `_allowances` is at slot 4, the allowance that address `0x456...` can spend on behalf of `0x123...` would be at: `keccak256(0x456...000...000 . keccak256(0x123...000...000 . 0x0000...0004))`

This complex storage pattern is why:

1. Mappings can't be iterated over - values are scattered across storage in a deterministic but non-sequential way
2. Mappings are incredibly storage-efficient - only used slots take up space
3. It's impossible to get a list of all keys in a mapping

Let's verify this:

1. Go to [Storagoor v2](https://storagoorv2.vercel.app/) and enter our contract address `0x668058852F2083c699b01fBD503Dd3Dba9F56b69`
2. The `_balances` mapping is at slot 4, so, to find the balance of the deployer address `0x9A3C34EB976C13D721BDbcea5cb922b0cb2A6E1E`, turn on the mapping mode and enter the deployer address as the mapping key. Click read to read the value in the slot. You should see `1000000000000000000000000` in the Decimal part
3. Compare the value you see in the Decimal part with what you see when calling `balanceOf(0x9A3C34EB976C13D721BDbcea5cb922b0cb2A6E1E)` on [abi.ninja](https://abi.ninja/0x668058852F2083c699b01fBD503Dd3Dba9F56b69/11155111?methods=balanceOf)

You should see the same value in both places. [Below](#deploying-our-contract), we are deploying the contract to the Sepolia testnet so that you can send the tokens around and test different storage slots!

## Events

Events are a way to log information about what's happening in a smart contract. We can define any event we want, and we can emit it in any function we want. In this tutorial, we've defined two events: `Transfer` and `Approval`. `Transfer` is emitted when a token is transferred from one address to another, and `Approval` is emitted when an allowance is set for an address.

## Deploying our contract

Let's deploy our contract to the Sepolia testnet. Let's go to [Google's Sepolia testnet faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia) and get some testnet ETH.

Once you have some ETH, you can deploy your contract to the Sepolia testnet using Remix.

![Remix IDE Compiler Tab Screenshot]({{ site.baseurl }}/assets/images/erc20/remix-compiler.png)
Go to Solidity Compiler, compile the contract.

![Remix IDE Deploy Tab Screenshot]({{ site.baseurl }}/assets/images/erc20/remix-deploy.png)
Then go to the Deploy & Run Transactions tab. Choose "Injected Provider - MetaMask" as your environment and deploy the contract.

If successful, you should see something like this:
![Successful Contract Deployment Screenshot]({{ site.baseurl }}/assets/images/erc20/deployment-success.png)

Expand the contract to see the functions you can call.

![Contract Functions Interface Screenshot]({{ site.baseurl }}/assets/images/erc20/contract-functions.png)

## What we've built

Let's take a step back and appreciate what we've created. Our ✨glorified spreadsheet✨ ecan now:

- Keep track of everyone's balances
- Let people send tokens to each other
- Allow other contracts (like decentralized exchanges) to move tokens on someone's behalf
- Keep a permanent record of all transfers

Most importantly, all of this happens on the blockchain, making it transparent and tamper-proof.

## Common gotchas & security considerations

When working with ERC20 tokens, watch out for these common issues:

1. **Decimal Handling**: Remember that `18` decimals means 1 token is represented as 1000000000000000000. Always account for this when working with token amounts!

2. **Approval Racing**: The standard `approve` function has a potential racing condition. That's why many tokens also implement `increaseAllowance` and `decreaseAllowance`. You can read more about it [here](https://ethereum.stackexchange.com/questions/93717/how-can-we-stop-front-running-for-approve).

3. **msg.sender vs tx.origin**: `msg.sender` is the address of the account that called the function. `tx.origin` is the address of the account that initiated the transaction. Always use `msg.sender` to ensure you're working with the immediate caller of your function.

## Where to go from here

Now that you understand the basics, you might want to explore:

- Adding `increaseAllowance` and `decreaseAllowance` functions
- Implementing token burning or minting
- Adding ownership and access control
- Making your token pausable for emergencies

Note: this is a simplified implementation. For production use, always use audited code like OpenZeppelin's implementation we looked at earlier.
