# Tags & Visibility

Each tag will have its own visibility. When we get the messages from the
blockchain, we also need to get the list of tags (names) and the up and
down votes of each for the message. The front end will then calculate
visibility and state of the message with up and down votes.

Node can handle the heavy lifting of serving and synching of this.

When a message is posted to the blockchain, it must contain atleast one
tag, but what if a user wants to provide many tags? This is not possible
since solidity does not support sending arrays or strings. Maybe have a
maximum of 3 tags, and users can vote more after. This would also limit
the amount of tag farming someone can do.

The message post event will then sync node, and it will have the initial
list of tags. When someone votes a tag, node will also sync the tag and
vote.

### Problem

Cant store array of struct inside a struct currently, so saving votes
inside comments will not work. A work around is to store a separate
votes array, and link to the comment id.

# Experience

How do we make sure that only the right contract can update the user
account experience points?

When a user interacts with the system in a way that could give them
experience, such as posting a comment. The campaign contract address of
the comment is stored on the user account contract.

Another option is to make the campaign factory the only authority that
can update exp. Then campaigns send the request to the factory, the
factory then updates the account.

If an account contract is made, what will authorize campaigns being
added to it?

We will need to keep track of all accounts that vote to award
experience.

Each comment tag can keep a list of accounts that voted. But we also
need to know if they voted up or down. So maybe the comment tag can have
a list of accounts for upvotes and downvotes, the length will give the
count of each.

When the threshold is passed, we can iterate through all of the accounts
and update the exp.

If the length keeps track of the votes, then someone waging 10 votes,
will have to be on the list 10 times, vs storing a value

Campaign-\>comment-\>tag-\>voterAddress\[0\] = address

Campaign-\>comment-\>tag-\>voterAddressValues\[address\] = 10

The problem with this is, if a voter has already voted, we need to first
check that, then just modify their existing vote.

### What if the vote is done through the accounts contract?

this is counterintuitive, why is voting on a campaign comment done from
an account contract and not the campaign contract?

But by doing it this way, the account would store the campaign address,
and then can verify that the update exp call is coming from the campaign
address. The problem is, that the user can pass their own address as the
campaign address, which could store it as a trusted campaign, and then
they can manipulate their exp. Not sure if this is actually possible but
is a concern.

Ideally, the account contract would check with the campaignFactory to
see if the address that is requesting the exp update is actually a
campaign.

In order to make sure the call to increase experience is authorized, we
need to make sure its coming from an authorized campaign. Therefore we
need to check against some list to see if its the address is an
authorized campaign.

This list could be in account or campaignfactory, or its own contract
campaigns.

Campaigns in campaignFactory.

Account checks factory to see if campaign is authorized. If so, then
update exp. So then account would just contain experience. As well as
other account meta data.

Accountfactory would maintain the campaign lists.

# Tokens

How will tokens be created, distributed, redeemed? How will the platform
or owner know what limit to set for them, or what exchange value to
initiate with?

## Use Cases

1.  Selling chair, sells 1 token first goal 1 eth for 1 token

2.  Another token 2nd goal, 2 eth for 1 token

3.  Two tokens can be redeemed, meaning the user only wants to make two
    chairs? Or maybe two at a time, or at first.

4.  Both tokens are redeemed.

5.  The owner decides to put both backup for sale with a new goal, maybe
    adding 3 now that they are comfortable.

<!-- -->

1.  Continuing from previous #4

2.  One of the backers decides to sell his token for twice what he paid
    for it on an exchange

3.  The back doubles up

4.  The new token holder redeems the token and gets the chair

So good so far. When a user funds the goal, the minimal buy in is 1 eth,
this will give them one chair token. The campaign token creates(?) an
erc20 token and sends it to the buyer.

So we know how they are created and distributed (kinda).

We also know the owner decides the value of each item, roughly \$250, so
1 eth, at the time. They decide this based on how much time and money
upfront it takes them, and what profit they want to make, or how much
their time is worth.

And since the owner wants to incentivise early buyers, he offers the
chair token at a discount for the first goal. So we know what the intial
exhange will go for.

The owner also decides that he doesn\'t want to make more than two
chairs to start with, for whatever reason, maybe he doesn\'t want risk,
has time limitations. So he limits the sale to two tokens. Once he is
done with those, he can add a new goal and resell the two redeemed
tokens or more. So we know how the limit is set.

What we don\'t know is how the tokens will actually be redeemed. This
will probably be the owners responsibility, but the platform can provide
a template to help.

Redeeming for items will involve sending the token to the owners address
along with the required meta data, such as address, name etc.

Once the token and meta data is revived, the owner can send the item.

Delivery details will be fully the owners and backers responsibly. The
owner should specify all these details including free shipping
limitations, extra shipping costs, country limitations, and if they are
manufactured the item before they ship, or they already have stock they
are asking out instantly.

How will this work for service tokens?

## Bike Rental Use Case

A company wants to develop a bike rental company with hubs throughout
the city. Maybe 1 token would be equal to 1 minute of use. So the moment
a bike is unlocked from the hub rack, a timer starts, and when it locked
at a different hub the timer ends.

How does the company determine the initial value of the token, and token
quantity, limits?

Also if the token is tied down to 1 minute, then the value of the token
would fluctuate all that much, since the real world value of such a
service wont fluctuate much. The only way it might actually increase
greatly is for the heavily discounted initial token sales. Is this
desired? It would add stability to the token, but investment attraction
beyond the initial investors would be minimal. This seems desirable?

Though this might result in token hoarders, since there is stable, they
can hold on to them and not risk losing value. Although what benefit
would this be to them, it would lockup their value to just one service,
the idea is to have fluid value amongst many tokens.

So far it does seem desirable.

So then the initial value of the token, beyond the discount, would
reflect competitor pricing with reasonable margins. So maybe for a 30
minute ride it would be 5 dollars. So then 5 / 250(value of eth) = 50.
50 \* 30 minutes = 1500 minutes or 1500 ride tokens.

Now what about a token quantity and decimal point (can the tokens be
divisible?)

Since there is no physical item or effort that needs to be delivered for
tokens, then why does there need to be a limit? A limit could come from
the community. To limit the sale until trust with the service grows.
Goals will naturally do this. So then the owner could create trillions
of tokens created, and only so many sold at a time through ever
increasing goals.

What about divisibility? What decimals should these have?

If a user takes out a bike, then 30 seconds later realises they didn\'t
want it. They would pay 1 token. Or they could pay .5 token, or its a \<
1 minute grace period, where u get it for free. In this situation there
probably shouldn\'t be any divisions.

## Use case

1.  Uber like ride share service, first goal is 1000 ride tokens for 1
    eth.

2.  Next goal is 500 ride tokens for 1 eth.

Brainstorm:

Why is it not 1 ride token for 1 eth? What goes into that decision? If
you think of a ride now averaging 25 dollars, the cheapest it could be
is maybe 5 dollars.

The idea would be to not have a set price, but let riders and driver
establish a price. The service would simply match riders to drivers with
matching price ranges, trip parameters. In busy areas there could be
bidding.

In this case, some trips might cost more than other trips even though
they are the same distance. The value of a trip would be fluid, even
though the token value could be stable. By locking 1 token to 1km, busy
rider areas would pay 2 tokens for 1 km, and busy driver areas would pay
.5 token for 1km. In a balanced supply and demand area, 1 token would be
1km.

The other option is not to lock the token to a utility measure. To let
that value define itself organically. By selling 10 million tokens at an
initial sale price. The going rate would be the initial sale price (set
by competing value with discount), until all tokens are sold. At that
point the price could climb or drop. Does this become a security token
at this point? Since you still pay drivers in ride token, it should
still be a utility token.

# Creating tokens

When should tokens be created? As soon as people are able to contribute,
so at the time of publishing the campaign. The owner should have no
special privilege over the erc 20 token contract. The campaign contract
address should be stored on so that it authenticates issuing.

# Token Default Options (ease of use)

It needs to be easy for owners to create a campaign, so there should be
no custom options exposed by default, but an advanced they section they
can setup optionally for advanced users. The questions is then, what
should the default settings be for the erc 20 token and what are the
exposed settings?

Name and symbol are required and easy to set. Decimal should be 0 by
default and hidden. Totalsupply is a tricky one.

# Contract Architecture

The accounts contract can be created with the campaign factory. It can
have a list of published campaigns. It can actually contain all the
campaign lists currently found in the campaign factory. The
campaignFactory therefore wont have a state any longer, which i think is
ideal.

Should publishing still be done through the factory? No i think the only
thing the factory should do is create campaigns. But then its just a
contract with a create campaign function, whats the point? Essentially
the campaignFactory can become the account contract. Since creating and
managing campaigns could be done under an account. Although managing
campaigns is a democratic process and not really for the account to
handle, so maybe not?

So then what if we just keep one contract, whatever its called, that
handles both campaigns and accounts. Testing becomes a problem if its
not split. Since campaignfactory creates campaigns, but then campaigns
depends on campaignfactory for exp, then its a circular dependency; hard
to test or maintain.

# Accounts

Should user need to create accounts?

Benefits

1.  Can save username

2.  Can save exp and published contracts instead of in a singleton
    account contract

Downside

1.  Have to create an account instead of just starting to interact with
    the system right away

2.  Contracts will have to reference account addresses and account
    contract addresses ( gets confusing)

# Draft Campaigns

Hold on a sweet second, why are draft campaigns on the blockchain
anyways? No one but the owner gets to see them so it serves no benefit
but to add complexity.

Ideally, a draft campaign should be in non blockchain storage.
Localstorage on the browser can work, but then the user cannot work in
the cloud. Ideally it should be on node.

On the other hand, a draft campaign is still just a campaign, so even
when its published, its the same contract, just on a different list. So
then is having a blockchain list of all the draft campaigns really an
issue? It also is needed because it is used to setup goals, the campaign
must exist for the goals to be added to it, this needs to be done in a
draft state.

Conclusion: draft campaigns need to be on the blockchain.

# Master Owner

If the open funder contract maintains a reference of all the sub
contracts, then a master owner would be needed to update the references
whenever a contract gets updated. If for some reason the master owner
secret is lost. The main open funder contract would not be able to
update references, and since the sub systems only trust the main
contract, control off all contracts would be lost. The only way to
recover would be to redeploy a new main contract.

Eventually the master owner can be replaced by a democratized system for
approving and updating contracts.
