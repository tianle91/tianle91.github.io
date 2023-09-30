# A market 
A market is made up by participants. Participants have a pre-determined set of trades. A trade is fully determined by the quantity of a particular good that is given up in return for a quantity of another good.

Each participant wants to achieve the following competing objectives:
1. Minimize the time spent finding a counterparty for their trades (i.e. minimizing overhead).
2. Maximize the quantity of the desired good (i.e. maximizing return).

# Fully connected market
For the sake of simplicity let's assume that the number of parties is always much larger than the variety of goods in the market. Consider the simplest case of having only two goods in the market, then any party can trade a good for any other good directly in a single barter trade. But what if there are more than two goods? 

## Direct trades are inefficient but Indirect trades are costly
If there are `N` goods in a system, the first good `g_1` needs parties willing to trade `g_2, g_3, ... g_N` for it (`N-1` pairs). Likewise for `g_2`, we need `N-2` pairs since everything else is the same except that the `(g_1, g_2)` pair is already accounted for. The number of trading pairs required is thus `O(N^2)` - so this is increasingly less likely to be the case as the number of goods in the market increases. 

> Trades can be split up using any number of intermediate goods. 

This significantly reduces the number of pairwise trades necessary. The market therefore only need the pairs `(g_1, g_2), (g_2, g_3), ... (g_{N-1}, g_N)`, which is `O(N)`, which is much more likely to occur than if we're restricted to direct trades. However, the tradeoff here is that instead of completing the trade directly in 1 transaction, we need `O(N)` number of transactions in the worst case to completing the trade. Furthermore, demand for well-connected goods also increases. 

# Money increases liquidity and competition
> Intermediate goods don't need to be actual goods.

Intermediate goods that are required by indirect trades don't necessarily have to be real goods. That's where money comes in. Suppose each good is immediately exchangeable for a pre-defined quantity of money (e.g. by a central authority). 

## Reduction in number of transactions
In such a scenario, instead of having to complete `O(N)` trades, one can only perform `O(1)` trades since we only need to sell a good for money and then buy the desired good with money. This is identical to the case of direct trades where only `O(1)` number of trades is required for a fully connected market. 

The total number of trading pairs has also decreased, resulting in the increase in participants for each trading pair. Instead of there being a market for each pair, there is now only a market wherein one trades a good for money. 

## Increase in market size 
Given goods `g_1, g_2, ..., g_N`, the size of the direct trade market without money is defined by trading pairs `{(g_1, g_2), (g_1, g_3), ..., (g_1, g_N)}, {(g_2, g_3), ...}, ... {(g_{N-1}, g_N)}`,  which is `O(N^2)`. With money, it is now just `(g_1, money), (g_2, money), ..., (g_N, money)`, which is `O(N)`, a significant consolidation of previously disjoint markets. 

If there were previously `M >> N^2` participants, then the market size has increased from roughly `M/N^2` participants per market to `M/N`  participants. The order of increase is significant, at `(M/N)/(M/N^2) ~ N^2/N ~ O(N)`. 

Since the market changes in time, this also equals to less waiting time. 

## Markets are liquid and prices are stable 
Of course, the ratio at which goods are exchangeable for money is defined by the market and thus varies according to the buy and sell orders available. However, the increase in the size of the market makes "immediately exchangeable" (i.e. liquidity) and "pre-defined" (i.e. price-stability) quantity of money more practically achievable. 

# Money is options 
Traditionally, any form of physical money issued by the central authority money has the following properties
- It doesn't degrade easily and can be reused from trade to trade. 
- Costs of transporting money is much smaller than transporting goods. 
- It's fungible so its use cannot be restricted. 

If the goods that money can exchange for stays relatively the same over time, parties may be willing to exchange goods for money right now with the expectation that money can be used to exchanged for other goods in the future. Even though agreements can be made between willing parties to that effect, the use of money enables anyone to enter into such an arrangement and standardizes such agreements. 

When a sale of a good for money occurs today, what happens is a tradeoff wherein, the seller obtains:
- The value of a good today, in exchange for the value of the same good in the future.
- Optionality in the goods they want to buy in the future, in exchange for the amount of goods they can buy in the future. 
Both tradeoffs depend on the market conditions today and the future but the future is much more uncertain than that today.

Value is determined by an ordered and weighed basket of goods a party desires. This may vary across parties. However the main determinant of trade outcomes is the goods produced by each party. 
