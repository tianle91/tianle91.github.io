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

## Ad opportunities are diverse
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

## What do advertisers need to do?
The main character in Mad Men is a creative directive at an advertising agency whose job is to create advertisement campaigns. He appeals to the collective consciousness and leverages human desires to drive sales. It's a story of intrigue, excitement and personal growth which makes for excellent TV. 

![advertisers](/assets/posts/2023-11-03/advertisers.png)

These days, online advertisers still need to answer the same questions:
- **What do I want to show to users**? Do I want to show a video, static image or just text? 
- **What kind of users do I want?** There are 5 billion internet users and even more internet-capable devices. Which ones are humans and what do we know about them? Do I want to target by demographics or do I want to target a specific set of individual users (e.g. those who have visited my site before, have items in a cart)?
- **Where do I want to show my ad?** There are 1 billion websites in the world and even more if websites vary by user (e.g. facebook or instagram home feeds). Do I want to show the ad on the top, bottom, left or right side on a page? 

On top of that, the modern internet advertising landscape has become a lot more metrics driven. Let's look at a couple of metrics which measure the success of an advertising campaign. 
- **Cost Per Mille (Impressions) (CPM)** The average amount spent per 1000 (i.e. mille) ads shown (i.e. impressions). 
- **Cost Per Click (CPC)** The average amount spent per click on an ad. Usually the ad sends a user to a website upon clicking on it.  
- **Cost Per Lead (CPL)** The average amount spent per "lead". A "lead" can vary by advertiser but is usually associated with user actions that correlate highly with revenue (e.g. number of orders made by users after seeing an ad). 

These core metrics all depends on the amount paid for an impression. This is therefore arguably the most important question:

> How much should I pay for an ad? 

## What about sellers? 

![websites](/assets/posts/2023-11-03/websites.png)

Sellers also have priorities:
- What kind of ads can I show that can improve or not worsen user engagement? 
- How do I maximize revenue generated by ads? 

## What does an ad exchange do? 
- Ask for bids from multiple buyers 
- Collect bids and send to sellers
