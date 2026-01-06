---
layout: post
title:  "No such thing as an ad!"
tags: ads
excerpt_separator: <!--more-->
---

???
<!--more-->

# No such thing as an ad
*Disclaimer: these opinions do not reflect those of my employer and are mine alone*

The most popular content platforms that we see today have ads. As users, it's rather frustrating to have ads or sponsored content show up on your content feed. However, these ads are what incentivizes these platforms to host the content that you want to see as well as train recommendation algorithms that identify the content that is most suited to you. 

So how do these platforms decide what kind of ads to show you? And are personalized ads actually good for you (privacy concerns aside)? 

We'll start by taking a look at how the basic business model of current content platforms is formed, then at how Youtubers take on sponsored content as a microcosm of the decisions a content platform has to make. Finally, we'll take a peek into Google's (now defunct) plans to decentralize online ads as well as an quick intro to how you can have privacy-preserving personalization. 

But first let's explore how most content providers ended up with advertising as their main business model.


# How ads took over the world
Newspapers used to be how most people got their "content". They had either a subscription or pay-per-view model but all of them had advertisements or "classified ads", usually in the less browsed half of the papers.

![newspaper stands](https://inhabitat.com/wp-content/blogs.dir/1/files/2023/05/1336747_81_118551_mbaoiLBrD-889x593.jpg)

Some time in the 2000s though, "free" newspapers started gaining traction. They differed in that it didn't cost the readers anything but were instead supported primarily by the advertisers. Of course, that meant that ads took up much more space in the papers, often up to 50% and no longer being relegated to the back half. 

## Online advertising 
As mobile phones and cellular plans dug their claws into society, newspapers started losing more ground to websites, which operate on a similar model to the free newspapers. The easiest way for these websites to start earning revenue is to introduce ads. 

Some less scrupulous sites also had pop-up ads and misleading buttons, which turned users away from those sites but not before charging advertisers for the click. However, even the sites that are most severely lacking in scruples would need some way of getting users to even visit their sites in the first place. There was a period of time when the answer is just SEO (i.e. gaming the search engine algorithms) but Google's [PageRank](https://en.wikipedia.org/wiki/PageRank)and its successors made this significantly more difficult (they have user retention problems of their own, back when they had competition anyways). 

![internet ads](https://miro.medium.com/v2/resize:fit:1300/0*jnk0_FJWQf_7Z4j4.jpg)

*Aside: Online advertising also had the extra benefit of being attributable to purchase decisions, which old school billboards weren't able to accomplish. Ever heard of the old saying about marketing dollars, that "half of my marketing budget is wasted, but the problem is that I don't know which half"? Online advertising sold the promise that you can now tell which half is wasted... or can you? We'll talk about this in another post...*


## Users v advertisers
Ad-supported content platforms need to balance the needs of these two parties in their ads system: 
1. Users - content and recommendation algorithms must be able to consistently attract enough users to the platform. The attention from these users (i.e. viewership) can then be resold to third parties (i.e. advertisers) through third party content (i.e. ads). 
2. Advertisers - ads should be reach users who are most likely to buy their products or services (or other activities upstream of purchases). 

Leaning too much towards users can lead to insufficient income to keep employees paid whereas too much ads can result in a loss of users and therefore less valuable attention to be resold for advertisers. 

The platform therefore needs to perform a balancing act, which basically boils down to the following decisions:
1. How much of user attention should be resold?
2. What kind of third party content should fill the monetized attention? Not all ads that are valuable to advertisers are also valuable to users (and by extension, the long term health of the platform).
3. How much should third parties pay for the privilege of showing their content? This should come naturally as a function of the two prior decisions in conjunction with the amount of value advertisers place on the ad itself. 

I like to call this the "Fundamental Problems of (ad-supported) Content Platforms" aka FPCP, with the assumption that ad-supported being pretty much the defacto business model of content platforms these days. 

*Aside: User and advertiser retention can be measured as a measure of success for the balancing act described above. For example, user and advertiser churn (i.e. inactivity after X days) are typically bad outcomes whereas increased user time spent on the platform, increased weekly/monthly user counts as well as advertiser budgets can be perceived as positive outcomes.*

How platforms reach these decisions are a closely-guarded secret, but we can take a look at Youtubers, who are in some ways a microcosm of ad-supported content platforms, even if some of them are a one-person show. 


# Youtubers and sponsored content
Youtubers tend to run ads on their videos on top of the platform inserted ads. They are a proxy of content platform because of these similarities:
1. They need to maintain viewership with some core audience segment in order to establish consistent and valuable viewership. 
2. They often resell some of the attention they get from their content to third parties (i.e. ads) as ads spliced into their videos. 

We'll try to answer some of these questions below by looking at a few Youtubers.  
1. How much of user attention should be resold?
2. What kind of third party content should fill the monetized attention? 
3. How much should third parties pay for the privilege of showing their content? 


## Does LinusTechTips have too many ads?
[@LinusTechTips](https://www.youtube.com/@LinusTechTips) is one of the top tech Youtubers who runs a multi-million dollar company primarily built on his Youtube channels. However, a [recent post](https://www.reddit.com/r/LinusTechTips/comments/1pztlu0/3_ad_segments_in_a_12_minute_video_is_insane/) on [r/LinusTechTips](https://www.reddit.com/r/LinusTechTips/) complained about too many ads (3 ad segments in a 13 minute video). I believe they're referring to [this video about RAM prices](https://www.youtube.com/watch?v=iRvyRo5Fk0o) posted on Dec 30th 2025. Looking at the [SponsorBlock](https://sponsor.ajay.app) view, we can see that those ads took up about 23% of the video.

![LTT 3ads sponsorblock view](/assets/posts/2026-01-06/LTT_3ads_sponsorblock.jpg)

But what's [@LinusTechTips](https://www.youtube.com/@LinusTechTips)'s view on this ad load? In their [revenue breakdowns video](https://www.youtube.com/watch?v=GeCP-0nuziE), we see that Youtube ads (i.e. AdSense) only makes up about 14% of their revenue and that most of their revenue comes from their "merch" (i.e. products from their team, making up 55% of the revenue) and sponsorships (i.e. third party products or services, making up 21%). 

Breaking down the 3 ad spots (not including Youtube injected ones i.e. AdSense, 14% of revenue), we find the top 2 revenue sources: 
1. DBrand, their channel sponsor (sponsorships, 21% of revenue)
2. Clear LTT screwdrivers (merch, 55% of revenue)
3. Private Internet Access (sponsorships, 21% of revenue)

From LTT's perspective, these 3 ad slots make absolute sense. From viewers' perspective though, perhaps even one ad may seem too much for some (hence the existence of ad blockers like [AdGuard](https://adguard.com/en/welcome.html) and services such as [SponsorBlock](https://sponsor.ajay.app)), so the question for us regarding user needs is really "how harmful is having 3 ad slots for users"? 

The evidence we can find here (other than the [post ranting about 3 ads in 12 minutes](https://www.reddit.com/r/LinusTechTips/comments/1pztlu0/3_ad_segments_in_a_12_minute_video_is_insane/)) is minimal. For example, there are no signs that the channel subscriber counts have been negatively affected by that video posted on Dec 30th 2025 according to [SocialBlade.com](https://socialblade.com/youtube/handle/linustechtips).

![LTT Total subs increasing consistently](/assets/posts/2026-01-06/LTT_total_subs.png)

So the answer seems to be no! However, this comes with some caveats:
1. Positioning of these ads - clustering these ads after the "hook" (when interest in the main content is high) and after the main content is a common strategy to balance watch times and ad load. 
2. Relevance of the ads to the viewer - are users ok with seeing these ads? LTT viewers are typically tech enthusiasts and are already likely to be in interested in related topics such as DBrand phone cases (with phone circuit board skins), LTT screwdrivers (marketed as being built for PC builders) and PIA (vpn for the privacy conscious). Ads which are less relevant to the audience can reduce the ad volume however. For example, [this dyson sponsored video being one of the most disliked](https://www.reddit.com/r/LinusTechTips/comments/15i23rk/what_is_ltts_most_disliked_video/#:~:text=They%20didn't%20put%20it,would%20be%20nothing%20but%20Dyson.).

The ideal ad is one that is so relevant to viewers' interests so as to be indistinguishable from organic content. However, in this case, an advertiser wouldn't even need to pay for the content. So what gives?


# Goldilocks zone of advertising
We'll look at the relevance of third-party content from the advertiser's side.
I'll be using advertiser and 3P (third-party) interchangeably since they're the third-party from the perspective of the content creator and viewer relationship.
As such we can see ads as third party content which may be shown along with first party content (i.e. the video that users want to see) at the discretion of the content generator.

There's an equilibrium in terms of 3P content relevance as we'll break down later:
![Goldilocks zone of advertising](/assets/posts/2026-01-06/goldilocks_zone_of_advertising.png)

On the right side is what we discussed earlier.
Advertisers generally do not need to pay for 3P content that may be indistinguishable from organic content (e.g. new camera gear releases for a Youtube channel focusing on camera gear reviews).
In these cases, there may be concerns other than content relevance which dominates this segment of content (e.g. limited access to new product, company imposes embargo timelines due to testing variations).
Of note here is that what can be relevant organic content in on channel might be irrelevant content on another channel (e.g. content about dyson vacuums in a tech channel vs in a robovacs channel).


## Setting a baseline for 3P content 
From the content provider's perspective, it's much more reasonable to set a baseline for third party content. One such example comes from an indie tech Youtuber I enjoy, [@BeccaFarsace](https://www.youtube.com/@BeccaFarsace), who describes trust as being ["more valuable than any brand deal"](http://www.youtube.com/watch?v=PME4LZMDtK0&t=308). This observation is true regardless of whether you trust her as a person or that this just makes good business sense, since the amount of ad dollars you can command is directly influenced by the users who wants to watch the content. 

![An honest conversation about sponsorships from Becca](https://www.youtube.com/watch?v=PME4LZMDtK0) 


## Audience-based Relevance 
The base of relevance stems from what the viewers want to (or are okay with) watch.
As such, there are more forms of relevance than just the niche that the channel is focusing on.
TODO chart about multi-dimensional relevance
 