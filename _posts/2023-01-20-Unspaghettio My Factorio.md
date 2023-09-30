---
layout: post
title:  "Un-Spaghettio My Factorio!"
tags: fun
---

# Un-Spaghettio My Factorio!
So some time ago I picked up Factorio on steam some time ago. The goal of the game is to gather resources and build tools, transportation, production and automation to bootstrap your way eventually to construct a rocket. There isn't one single playstyle or winning strategy so there's really good replay value... so naturally I *played it for a bit*.

![play time](/assets/posts/2023-01-20/01_play_time.png)


## Spaghetti
In the official website, you'll find some images of *spaghetti*. Here's an example:

![spaghetti](/assets/posts/2023-01-20/02_spaghetti.jpg)

It's really easy to make a spaghetti! As the game progresses, just connect all the inputs to the consumers and outputs to their downstream consumers with the shortest path possible. Do that for a couple of production lines and you've made yourself an instant spaghetti. Some say a spaghetti is beautiful, others say it's a the bane of their existence... but hey, everyone has made one before.


## What's wrong with it? 
A sprawling mess is hard to manage - once you've made a spaghetti, you can't unmake it without destroying everything. If a part of it needs to be changed, there's very little working room to do so. Changing one part of the spaghetti often takes out more parts than expected and doing so comes with a high likelihood of killing your factory.

Basically, spaghettis are nice to look at but bad to touch because...
- Complex dependencies - Where do inputs come from? Where do outputs go? Everything's lost in the ether of the spaghetti.
- Wasted resources - It was already enough trouble making the machinery to produce a new item fit into the spaghett. Nobody has time to make sure that it's functioning efficiently.
- Hard to scale - What if I need more electronic circuits? How can I make sure more inputs are available and how can I put down additional assemblers to create more outputs? 

There must be a better way!

![must be a better way](/assets/posts/2023-01-20/03_must_be_a_better_way.jpg)


## What's an anti-spaghetti?
Organizing the spaghetti is the key to being able to grow the factory. But what exactly is organizing? It's making sure that functionality is **self-contained** and **simplified** in a given area of the factory. This process is also known as compartmentalization or encapsulation but since **blueprints** in Factorio perfectly embody this concept, we'll just call them **blueprints** going forth.

**Blueprints** should be:
- Self-contained: Everything necessary to perform a function is included in the area. No manual intervention is required to maintain production, so long as a stream of inputs is maintained.
- Simplified: It's easy to provide inputs and receive outputs to the production area. Production reduces complexity - this means that often multiple inputs are combined to create a few outputs (often resulting in a reduction in total item quantity). 


## Steps to create a blueprint
Since electronic circuits are one of the most used intermediate components in Factorio, let's use that as an example. We'll be creating a blueprint to create electronic circuits.

Let's reconsider what a electronic circuit production requires:

![electronic circuit flowchart](/assets/posts/2023-01-20/04a_eg_dag.png)

Some notable features of this recipe are:
1. Only 2 inputs are required (iron plates and copper plates)
2. There's a single intermediate component, copper coils.
3. Multiple copper coils are produced from a single copper plate.

Next, we'll go through these steps to set up a **blueprint** for electronic circuits.
1. Define infrastructure to distribute inputs and aggregate outputs
2. Design an efficient way to do transform the inputs and outputs


### Define the inputs and outputs
A belt each for copper and iron should work as inputs in early game since we're unlikely to saturate the belts. Even though we'll need to switch to trains as inputs at some point in scaling, this belt-based approach can still be reused since trains still need to unload to belts. A single belt for outputs would also suffice.

Some designs put inputs on the same side as outputs while others have them on opposite sides. We'll look at an example from [here](https://factorioprints.com/view/-KjZIX7kOZQkjNigDi9o).

Same-side approach with 3 input lanes and a single output lane on the same side.

![same side](/assets/posts/2023-01-20/05b_same_side.png)

Opposite-side approach with 3 input lanes on the left and a single output lane on the right (in the middle vertically).

![opposite side](/assets/posts/2023-01-20/05a_opposite_side.png)

They differ on the following aspects:
- Extensible: For same side approach, production can be extended by adding more to the opposite end. 
- Simple: For opposite side approach, the inputs and outputs are less likely to overlap.
- Less impact on surroundings: Managing inputs and outputs for opposite-side approach requires infrastructure on both ends.

Summary of the approaches:

| Input and output sides | Extensible | Simple | Less impact on surroundings | 
| ---- | ---- | ---- | --- |
| Same side | ✅ | ❌ | ✅ | 
| Opposite side | ❌ | ✅ | ❌ |


### Efficient transformation
We want our setup to have as few bottlenecks as possible. Bottlenecks indicate wasted material and assemblers. Most importantly, it's a waste of space, which is a limiting factor in Factorio.

We'll start with [this great resource](https://kirkmcdonald.github.io/calc.html#tab=graph&data=1-1-19&items=electronic-circuit:f:1) to visualize the rates required to produce 60 electronic circuits per minute.

![circuit rates](/assets/posts/2023-01-20/04b_eg_rates.png)

Let's bear in mind these ratios:
- For every iron plate, we need 1.5 copper plates - the optimal ratio of copper to iron inputs is therefore 3:2. We can start with just 1:1 ratio and then add more copper and iron inputs later as we expand production.
- 2x copper coils are produced for each copper plate inputs - we should be using copper coils as soon as they're produced since dumping the coils into logistics will be a massive waste of space and introduce bottlenecks.
- 1.5 assemblers are required for copper coil production for each assembler for electronic circuit. The optimal ratio for copper coil production to electronic circuit production is thus 3:2. We should stick to this ratio at all times. 

An optimal setup looks like the following:

![circuit assemblers](/assets/posts/2023-01-20/06_circuit_assemblers.png)

Top two input lanes are copper and the bottom input is iron. The bottom-most lane carries the output electronic circuits. The source blueprint is available [here](https://www.factorio.school/view/-ND8sYSaE9kfSGD-6Hzd).


## Buses vs Trains
Once we've created a efficient blueprint for production, we'll need to connect them up together. Connecting things together is the main goal of the mid to late game, when the macro-logisitics dominate gameplay. Busses and trains are the primary tools to solve this problem.

A bus is a collection of lanes (or belts in Factorio). Here's how it looks like:

![bus](/assets/posts/2023-01-20/07_bus.png)

The bus primary refers to the parallel collection of lanes carrying inputs and outputs. The example starts with a 5-lane input on the left with the addition of a new lane (electronic circuits) on the right, creating a 6-lane bus. Lanes are split off to lead into a production area and outputs are merged back into the bus.

Trains are the best way to transport bulk items over long distances. You'll have to load and unload items to and from trains though, which makes it not a free lunch. Busses and trains differ in some significant ways that we'll discuss below.

![train](/assets/posts/2023-01-20/07_train.png)


#### Ease of integration
It's much easier to put things into and out of busses. Loading and offloading for trains takes up much more space compared to the bus example above. Here's an example on loading a train, which requires balancing (splitters) and buffers (inserters and chests).

![train load](/assets/posts/2023-01-20/07a_train.png)


#### Space efficiency
If you just need to move things in bulk from one location to another, it's much more efficient to use trains. They shrink the intermediate bus lanes which can get really wide into a couple of tiles wide (i.e. the width of a train track). Here's an example of replacing a 5-lane wide bus with a 5-carriage long train:

![bus to train](/assets/posts/2023-01-20/07b_bus_to_train.png)


#### Complexity
Trains need fuel and can be blocked by limited throughput of the rail network caused by signaling and rail network design. Also, with more and more train stations, your factory space starts to become more train than factory. After a while you're playing Train Tycoon instead of Factorio, but that can be fun too.

![train network](/assets/posts/2023-01-20/07c_train_network.png)

We'll end it here with this really cool [train guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2737259470).
