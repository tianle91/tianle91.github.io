---
layout: post
title:  "Tech Debt is Fun in Factorio"
tags: fun coding
hidden: true
excerpt_separator: <!--more-->
---

Tech debt at work is a chore. Tech debt in Factorio is the whole game. Same problem, opposite feeling - and the difference is worth poking at.
<!--more-->


## The same problem, twice
At work, tech debt is the stuff you took a shortcut on that now slows everyone down. A schema nobody wants to touch, a service with three owners and no docs, a "temporary" script that's been load-bearing for two years. You know it should be fixed. You also know that fixing it means touching something that's currently serving real traffic, and that's exactly why nobody does.

Factorio is the same situation, just made of belts. You wire up a quick production line to unblock yourself, then another, then ten more, and a few hours later you've got a sprawl you can't change without breaking something downstream. I wrote a whole post about [un-spaghettifying a Factorio base](/2023/01/20/Unspaghettio-My-Factorio.html) - that *is* paying down tech debt, I just didn't call it that.

![spaghetti base next to an organized blueprinted base](/assets/posts/2026-06-24/01_spaghetti_vs_organized.png)
*The same problem you avoid at work, except here you signed up for it on purpose.*

So why is one a slog and the other a Saturday well spent?


## Your service never goes down, and that's the point
The thing that makes work tech debt scary is that the service is live. You can't pause production to refactor it. People are depending on it *right now*, and a mistake is an incident.

Factorio has exactly this constraint, and it turns out to be the source of the fun rather than the stress. Your factory never stops. While you're ripping out a section and rebuilding it, the rest of the base keeps consuming inputs and expecting outputs. If you starve a downstream consumer, you watch it happen - the belts run dry, the assemblers idle, the whole line stalls. It's a live migration with a progress bar.

The difference is that in Factorio the live system is *legible*. You can see the entire thing at once. The blast radius of a change is visible before you commit to it. At work the same migration is happening behind dashboards and across teams you've never met, and you're mostly guessing at what's downstream.

![zoomed-out map view of the whole factory](/assets/posts/2026-06-24/02_whole_base_map_view.png)
*The entire production system in one frame - the view you never get of a real service.*


## Bottlenecks announce themselves
The best Factorio mechanic, the one I wish every production system had, is that a backed-up belt is just *visible*. Items pile up behind the slow step. You don't need a tracing system or a week of profiling - you walk down the line until you find where the items stop moving, and that's your bottleneck.

![a belt backed up with items piled behind a slow assembler](/assets/posts/2026-06-24/03_backed_up_belt.png)
*Items pile up right behind the slow step. This is your p99 latency, and you didn't have to instrument anything to see it.*

This is observability that you get for free, and it completely changes how it feels to maintain the thing. Most of the dread around touching a live service is uncertainty: you don't know what'll break, so every change feels like a coin flip. When you can *see* the constraint, paying down debt stops being scary and starts being a puzzle. The factory is telling you exactly what to fix next.

Most of the work tech debt I've hated wasn't hard to fix. It was hard to *see*. The fix was easy once I understood the system; understanding the system was the whole job.


## Rebuilding is cheap, so you actually do it
The other half of why it's fun: the cost of a redo is almost nothing. You select the bad section, deconstruct it, and bots haul the parts away while you stamp down the better version from a blueprint. No migration plan, no rollback runbook, no asking three teams for sign-off. If the new version is worse, you undo it.

![a red deconstruction selection over a section with bots hauling parts away](/assets/posts/2026-06-24/04_deconstruction_blueprint.png)
*Select the bad part, stamp down the better one, let the bots sort it out. No rollback runbook.*

That cheap feedback loop is what makes refactoring enjoyable. You try a layout, see it's wrong, and try another - the same loop that makes any good toolchain feel good. The reason refactoring at work drags is that the loop is expensive: a change takes a deploy, a bake, a careful watch of the metrics. When the loop is slow, you batch up risk and dread the big-bang rewrite. When the loop is fast, you pay the debt down continuously and barely notice.

A lot of the difference between "fun" and "chore" is just the length of that loop.


## Rebuilding while it's running is the actual game
Once you've played for a while, the game stops being about reaching the rocket and becomes about reshaping a running factory without taking it down. You wall off a section, reroute its inputs to a temporary feed, rebuild it, then cut back over - and the rest of the base never noticed. That's a zero-downtime migration, and it's *the fun part*, not the price of admission.

![construction bots rebuilding one section while the rest of the base keeps running](/assets/posts/2026-06-24/05_live_rebuild_in_progress.png)
*A section being rebuilt mid-flight while everything downstream keeps getting fed. A zero-downtime migration you can actually watch.*

I think that reframe is the takeaway. At work I treat tech debt as the tax I pay for having shipped something. In Factorio I treat the exact same activity as the thing I sat down to do. The activity didn't change - reshape a live system that you can't turn off. What changed is that the system is legible, the bottlenecks are visible, and the redo is cheap.

You can't fully buy those properties for a real service. But you can chase them: make the system observable enough that the bottleneck shows itself, make the deploy loop fast enough that a redo isn't a big deal, and keep the thing legible enough that you can see the blast radius before you commit. Get close enough and the chore starts to feel a little like the game.
