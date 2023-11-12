---
layout: post
title:  "Are Ad Exchanges similar to Stock Exchanges?"
tags: hardware
---

# Are Ad Exchanges similar to Stock Exchanges?
Ad exchanges sit between people who want to buy ads (advertisers) and those who wish to sell their ad spots (publishers). They help publishers maximize the value of each ad spot by collecting bids and ads from advertisers. 

![ad exchange role](/assets/posts/2023-11-03/ad_exchange_role.png)

Online ad exchanges *feel like* stock exchanges. After all, they're fast, automated, have huge daily volumes and have "exchanges" in their name. 

![ad exchanges logos](/assets/posts/2023-11-03/ad_exchanges_logos.jpeg)

Similarly there are also large cap "stocks" made up by prime internet properties such as youtube, facebook, instagram, twitter wherein one can find users who might be interested in something you'd like to sell.
In the follow sections, we'll look at a couple of features which make ad exchanges a uniquely different beast compared to stock exchanges.  

# What's different? 
Quantity has a quality of its own and we can really see that in ad markets.

## Ad opportunities are diverse and cheap
Here are some numbers to set a baseline for the size of a market:
- Nasdaq has about 2,500 stocks 
- There are about 300 million companies in the world (120,000x Nasdaq)
- eBay has about 1 billion active listings (420,000x Nasdaq)

Now, how many ads are there in a day? We don't have specific numbers but let's try to think about the problem with a few key numbers: 
- There are 400 million internet users in North America in 2022
- The average person in the US views over 100 page views in a day
- There's probably about 10 ads on a page

Multiplying the above brings us to about 400 billion ads per day, easily dominating all the other markets we looked at above.

This quantity of ads is spread across the total number of active internet users (400 million) and the pages they viewed in a day (~100). Even though page views are likely to be concentrated around a few popular websites, the total cross product of users and pages is likely to still be on the scale of 40 billion (i.e. 400 million users x 100 pages / user).

> There are about 400 billion ads / day over 40 billion user, page pairs. 

To contextualize this figure, there are only 33 million trades on Nasdaq on 2023-11-09 over less than 2,500 stocks. The ratio of the number of trades to the number assets is 13200:1 for Nasdaq compared to 10:1 for ads (on the scale of number of ads per page), indicating that the diversity of ad trades is at least compared 1000x higher compared to stocks.

## They're also cheap
On the other hand, advertising revenue in the US is $300 billion in 2021. This figure is reached in a single day on Nasdaq, where the trading volume for 2023-11-09 is already 240 billion usd.

> Ad opportunities are 1000x more diverse, but brings in 400x less revenue.

## And vanish faster than the latest internet fad
Stock delistings are rare and usually makes the news but internet fads come and go every week. Ad opportunities vanish faster you can say "Mississipi" five times. 

Pages need to load quickly to avoid losing users. Pages that take more than 5 seconds to load can lose more than 50% of users ([source](https://www.browserstack.com/guide/how-fast-should-a-website-load)). Therefore, publishers are incentivized to minimize the time spent on loading ads (for revenue) to maximize the time allocated to generating content (for retention).

For real-time bidding, the response deadline is about 100ms ([source](https://developers.google.com/authorized-buyers/rtb/peer-guide)), which is on the same scale of high-frequency stock trading. However, there's generally no need to sell a stock within milliseconds (as is the case for ads) and sell orders can be active for days on the stock exchange.

## TLDR
Compared to stock trades:
1. Ad opportunities are 1000x more diverse
2. But brings in 400x less revenue
3. And ads have to sell within milliseconds compared to hours or days.

# What does it mean for bidding?
It immediately follows from the above that pricing such a large number of ads quickly and cheaply is not a easy problem to solve. 

As such, the online ad industry has converged on the following solutions: 
- Standardization of bid requests [openrtb](https://iabtechlab.com/standards/openrtb/) allow for algorithms to bid on important attributes related to web page, ad opportunity (on the page) as well as user information.
- Simple and fast automatic bidding algorithms (<100ms). Humans simply cannot react fast enough to the diversity of ad opportunities.

Let's explore a bit these broad categories of bidding-related attributes:
- Which page showing the ad? There are 1 billion websites in the world so it’s not feasible to look at each page which can feature your ad. Even in the scenario that you decide to go with one platform (e.g.  Facebook or Instagram), each user would also see a different home feed. 
- How is the ad being shown on the page?  
- Who's viewing the ad? There are 5 billion internet users and it’s not always possible to figure out if users are actually the same person, just using a different device. 
- What's the ad about? 

# What does the ad exchange do? 
???

# Privacy is coming for your lunch
Cookieless - centralizing the supply and demand framework. 
