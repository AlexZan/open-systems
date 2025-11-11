## Content Hash or Content

Should the title and body be saved on the blockchain? If it is, then the
gossip network is not required. This will make saving to the block more
expensive. If hash is saved, cost will not scale with content size.

## Log or State of Vote count

Update: state of vote count should be used

maybe blockchain should just keep a log of experience gains, but not the
state.

but who will compute the state after 1 day? on a gossip network any
viewer can, and the first to execute the timer condition can propigate
it. and it can be verified against the blockchain at any time.

but the blockchain will need to know the state to allow voting,
otherwise it will have to compute the total each time which is
inefficient.

\*\*therefore the computed state must be on the blockchain, and so then
who will compute it? it could be a timer contract, but what funds it?

what if the owner of the experience is the one that must collect the
experince, this is what sets the state.

## Content Hash

Update: content hash should be post id

The id of the post should not be the content hash since there could be
duplicate contents. Although having a built in safety for non duplicate
content might be good, but it would be easy to circumvent by just one
character defeating the purpose. The question is then, would there ever
be any utility in duplicate content? I think it is no. therefore the
content hash should be id, and if it already exists it should throw an
exemption.

## Should Blockchain generate hash or client?

Update: client should generate it

## 

Its a hash of the title + body. Whether the client or server does it the
result will be verifiable. If the client creates another hash, none of
the content of their post will work for it. If they try to duplicate the
hash of another post, this will result in a blockchain revert.

Even if the blockchain makes and issues the hash, the client still has
to propagate it to the gossip network, so they could always change it at
that point. Therefore the client should generate it.

## What if a client uses the hash of another post?

Then whenever a user upvotes their post, it will upvote another post.
Then every client must verify the hash before interacting with it. If
thats the case then maybe the hash should just be generated before each
blockchain write call?

## Experience

Update: Half Claim & double earn solution will allow for instant voting
without the issues below.

If experience is gained instantly through vote, then a user can just
keep revolting their own post and make it seem like they have many
upvotes from many people. A user can be stopped from voting on their own
post, but does this violate the rule that they should be able to do
anything with a single account that you could do with multiple accounts?

With two accounts, users could then upvote each of the posts back and
forth resulting in the same behavior that would no longer be allowed
with one account.

If a delay of one day occurs, then this would delay this. A user could
then upvote their own post with no issues, and would not have the
experience to do it until a day after posting. They can keep doing it,
it would just take a day each time.

## Experience from new tag

When is experience from a new vote available? It should be a day after
the first post was made to avoid the double voting issue explained
earlier.

A post is made, a user upvotes the post with a tag it did not have
originally. A day after posting a user can claim experience in that new
tag. Because they did not post that tag originally, they only get 1
experience, not two as they would with an original tag.

## Can a user continue to claim experience any time after 1 day of the original post?

Update: But should a user vote on your post be claimable immediately or
1 day after the vote was made? The point of the delay is to give anyone
globally time to review it/dispute it, but a vote cant really be
disputed, only downvoted, and downvoting can happen at any time. In this
case, do user votes even need to be claimed? They can be immediate.

Update: *the user can try to claim experience at any time, but can only
claim unclaimed default experience: made available 1 day after the
post.*

They should be able to at any time? Or should it be 1 day since the last
time it was done?

Maybe a claim availability resets every day.

And it simply checks a list of the votes made on tags, regardless of
posts, to see if it should provide the experience. Experience does not
care about posts, just tag votes.

So maybe just an unclaimed tag experience list is needed and not an
unclaimed posts

## If vote experience is given at vote time, how does halving work?

Because Half Claim & double earn solution needs the experience earned to
be half the equivalent vote, when someone votes only 1, what will
happen? It will need to be store in some remainder state. And when that
remainder state can provide experience when halved, it will do so, and
put the remainder in remainder for the next vote.

## Does a negative vote give half negative value experience, like a positive?

I dont think so, but then can it be exploited?

## Should a user be able to vote on their own post?

Update: yes, with an eventual Half Claim & double earn solution ( see
below).

Update: yes, they can self vote, possibly as promoting their post, but
it will cost half their experience.

The rule of multiple accounts shows that a user should be able to do
everything on one account that they can do on multiple. Therefore a user
should be able to to vote on their own post with the same account since
they could do it with another account. The problem then arises that they
can keep revoting on their post and keep bumping up the vote count. E.g.
If a user does this 10x, their post will have 10 upvotes.

The blockchain cost alone might be enough for most as a deterrent, but
not for all, therefore it is not a comprehensive solution.

If a user has 100 exp, then upvotes their own post 100x, that will cost
only one block wite, but then they can claim the exp and give themselves
another 100 votes.

If a user can only claim half the exp voted on their post, then the cost
to self voting will be very high. This would also half the growth rate
of experience in the system.

If there is a 24 hour claim limit on claiming voting experience, then
this would just delay it. A user with 100 exp can still self vote, and
24 hours later do it again. This would delay it, but not stop it. Making
only users with high exp able to pump posts.

If a count or log is made for self voting, then a user can just upvote
another of their accounts, then upvote their original post with that
amount, circumventing that count.

This also questions two users pumping each others posts. A is in cahoots
with B about their upcoming posts, and they agree when they post, each
will vote 1000 up on it, to promote it. They would not lose any
experience in doing so. The only solution to this is to half it on
claiming.

Another case is an influencer group; several key people with a great
deal of experience in top subjects that get paid to upvote posts of
paying users. The users would then have to return the experience through
another upvote. If this is very high profile, this can be done through a
spread across multiple shit posts. But even this can be easily
investigated and caught.

All of these issues would be solved by halving the experience. Maybe
trust or stake can increase the claim % to approach 100%. If you stake
100 exp, then 100 exp claimed will provide you a higher %. If a claim is
made against you for exploiting votes, then you lose the stake. But then
a user can just unstake after an exploit. Maybe staking is automatic.
Voting itself is staking. Or just by having experience it is at risk of
being lost if it is proven you exploited in a claim.

What if a degree of separation value is published. So if the poster
votes on their own post, then it will show x% of the posts have 0 degree
of separation. People will know it is self promotion.

If there is a reduction in experience each time self voting, it can be
summed as the cost of promotion. And since it cant be stopped, it should
be allowed, but it should have this cost.

This could never be done with decision votes, since no one gets decision
votes as experience.

### Half Claim & double earn solution 

by halving the votes to experience claim, but allowing users to earn
their votes back when votes are double the count of their vote, then
users could self vote as an investment in the value of their own post
and for promotion. E.g a user makes a post, votes 10 on the post, if the
post goes to 20 votes, then they get back their 10 votes, and now they
are able to claim 5, earning 5 experience from that. If the post does
not get any votes, they lose 5 experience since they can only claim 5
back from the 10 they voted.

## Should experience be earned from voting?

No, because then combined with self voting, a user can keep increasing
their experience.

## Should claimable exp only be stored in gossip?

Since it does not affect any block functionality, it should not be on
the block. There is no ready to claim exp state in the block. ClaimExp
function just checks if a post has matured to receive exp, but it is up
to the user to know when it should be time to call the function and use
gas.

## Blockchain, gossip network with frontend

A post will be made on the frontend app. Do we want to have the user pay
for blockchain writing right away? Or should that be only once it gets
the first vote?

In this case the first vote will always cost more, to pay for writing
the post and the vote.

Users can also subscribe/follow a post while it is on the gossip network
without it having to be on the blockchain.

If it is not on the blockchain, then the poster will not be able to
claim their experience. From the point someone votes, it will count as
posting to the blockchain, and 1 day after they are able to claim
experience.

In this case a new post:

1.  Submit post with app

2.  Gossip network propagates the post

3.  User is asked if they wish to pay for posting the blockchain

## Experience its own blockchain?

If exp is its own blockchain, then in order to claim experience you must
be running a node and must stake your existing experience automatically
when processing a block.

In this case voting and claiming experience is essentially free.

###  What about a brand new tag, no one will be processing it?

All tags will be processed. It is not a separate blockchain for each
experience.

## Crypto and app

Writing to the blockchain will require crypto to pay. A user must have
crypto in an account which they have access to. The easiest way is to
incorporate a wallet into the app which can store the credentials of an
existing or new crypto account.

The api that will interact with the blockchain will need access to
crypto somehow. Must find a suitable api for this.

## Mobile dapp?

Should the initial app be mobile? If the complexity of building it as a
mobile app is "too much" then the initial app should be a web app. The
advantage of a mobile app is that it would have much higher reach. Is
this advantage needed for the beta period?

Web will still allow all functionality.

After several days of assessment it seems the added complexity of trying
to get an etherium api/wallet into a mobile dapp is not worth the added
reach, for the time being.

I will then continue to develop with reactjs and web3

## App Stories

1.  Can view a list of posts

2.  Can create an account with identity that generates public/private
    keys and stores against the gossip password/id.

3.  New post as draft posts to the gossip network

4.  Posting posts to blockchain and gossip network

5.  Users can subscribe to a post

6.  Users will get notification when replies are made to a subscribed
    post, or when a draft post is finalized

7.  Finalizing a post sends it to the blockchain

8.  When a post is posted to blockchain, it will label the post
    acordingly

## User post without account

Does a person need an account to make a post? If they post, should it
create a blockchain key for them? Or only once they try to claim
experience? Would posting without needing to make an account lead to
spam? What will the identification be?

Maybe identification can be asked for before posting if not logged in,
users can select to remain anonymous by not setting an identification.

What will happen to posts if a user makes an account? They should remain
anonymous out of simplicity. Otherwise local token would have to be
tracked. Or they can be given a secret which they can use to make edits,
for each post.

## If a user posts anonymously then what happens to the experience from votes on their post?

People might not want to vote since the experience might be lost or is
not going to anyone. In this case should accounts without public keys be
posted.

Maybe votes dont cost anything? But u still need to experience to vote?

## Maybe anonymous posts are too complicated to have as an initial feature?

It seems the complication with wasted experience or claiming the exp
from a seed is a feature which only a small subset of users might want,
the rest will just create multiple accounts to be able to maintain
anonymity between them but also allow them to claim experience.

## What does making an account mean?

Update*: it means creating an account with a wallet service like
metamask. It will then use the public token to bind to all the user id
specific things in the gossip/blockchain network. There is no need to
create an account on the open system, this can be something for later
which will allow you to optionally put in public or private data, such
as name, etc.*

Does it mean they just create an identity? Does it mean they get a
blockchain secret? Or a wallet that manages the secret with a
passphrase.

If its stored just on the client, or phone, and unlocked with biometrics
or a password, then what happens if that device is lost? Then the secret
will be lost. In this case the secret needs to be stored remotely also,
to make it easy for new accounts this needs to happen by default. When
an account grows into something more valuable, the user can then remove
the secret from remote storage and self store in on a hardware wallet or
something.

Can the secret be stored on the gossip network encrypted by the
password?

If it can, then an account would involve making a gossip network
account, along with an ethereum account and storing both on the gossip
network.

## Should the public/private keys be generated when the account is made or only when they are needed?

If a user votes on a post, and at that point the content hash is saved
to the block, then at that point the owner account will be needed,
therefore the post should contain the block public key of the owner, so
that they are able to claim experience and funds.

## Should experience be its own blockchain?

Maybe in order to claim experience you must be running the block on a
device. This will make voting free, since all the users claiming
experience will have to process votes.

Will then funding just be on the mainnet? So sending funds to a fund
will cost gas on the main net? Or is it beneficial to do it on the exp
net? This can also bre processed by anyone claiming experience. Maybe
this can be kept on mainnet and answered later.

Maybe proof of stake with experience could be the process for earning
funds from that experience?

## TDD and App

E2e testing can be done with cypress, but it would be good to mock out
gunjs. What is the logic between the view and data that would be
testing?

Formatting could be tested?

Example data: \[{msg: 'blah', tags: \['tag'\]}\]

This data would need to be shown as a card, which is specific to the
view, and so would need e2e testing. There is really no behavior in
between data and view specific to the app that needs to be tested?

In this case this should be done with e2e testing, and just mock out the
service layer?

## E2E with gossip network: gunjs

Should the e2d tests be done with gunjs instead of a mock? Its fairly
easy to control gunjs to setup and initialize for testing, clear data,
etc. This way the full system minus blockchain can be tested through e2e
testing.

## Paging/streaming

When the post list gets too large, how should the application scale so
that it does not request the full set of posts. It can request x sorted
by something, then when the client naviages near the end it will request
the next batch.

## On Gossip Update

The client must subscribe to the on even of the gossip network to get
real time updates. The on event of gunjs gives the entire list and
updates. But how would this work with paging? Should the client just
auto display any new post?

Just like most social media, the feed should be fully in the users
control. And should not update automatically. In principal the only
things that should update auto are things which the user explicity
subscribed to. Maybe an extra feature can be added fore a manual update
button that shows how many updates there are, which update real time.
This would just have to trigger a post event, but not actually provide
the post.

## Should a post vote, save only to blockchain or to gossip also?

Update: Only blockchain. *Initially I think a post vote should only save
to the blockchain. Then later on once validation is implemented, it can
be synched with gossip. But is there an advantage to using gossip over
blockchain for reading? This might not be a real advantage and some
study must be done before validation is given value as an effort.*

Gossip is not secure, so a user could propagate a fake vote, which would
disagree with the blockchain. a method for validating a gossip
propagation against the blockchain is needed.

Next gossip update would be near immediate, where blockchain might have
a long delay. If it is delayed until there is a callback from a
successful block write, then the user must stay online with their client
to receive it. Or they can propagate a validate when the gossip post is
made. And each time a client views the post either (individual or in
post list) it will check to see the vote value from the blockchain. But,
it should do this anyways, so creating a validation list is pointless.
Maybe each client has x% to validate each post they view. Maybe that
they have experience in?

## How to Vote Intuitively in the client

Maybe clicking the tag in the post will show a +1 each time it is
clicked. Shift clicking will show -1 votes. A submit votes button will
show anytime there are votes to submit.

## Posting only to gossip

The advantage of only posting to gossip is that it will not cost
anything to post. The disadvantage is that there is no default
experience from the tags you post with.

Maybe if a poster does not put in tags, they will not get default
experience, and there is no point to put it on the blockchain, so it
will post only to gossip. A user can then vote on any tag they choose,
and at that point the post will get added to the blockchain.

Can this be exploited? Yes, since the hash does not exist on the
blockchain, then anyone can post it with a different owner. This can be
mitigated and eventually can come down to a claim if someone does
exploit it.

## Groups

If i make a post specific to a group, it will create value for no one
outside the group. Therefore should the experience gained from creating
value in a group be locked to just that group?

E.g. In a community group, a user posts that the rain water catcher is
starting to rip. This creates value for absolutely no one outside the
group who might be affected by the warning. Those inside the group are
likely to be affected by their source of water being damaged.

So the user might get upvoted in #rainwater catcher. But now the
experience should be locked to the group context. If the group was
called teenyfarms, the experience might be designed as
#teenyfarms.rainwater catcher.

### Type of groups

1.  Open, anyone can join leave

2.  Public, all data is viewable but requires membership vote by the
    other members to join. members can also vote to kick out a member by
    vote.

3.  Private, most data is not viewable, membership rules.a

Maybe groups can allow outside or parent experience in, but can not
transfer any experience out into the parent group. Eg. the canada group
does not allow experience into the global system, but the canada group
can take in experience from it (users can vote with their global
experience in the canada group). The Ontario group can take in
experience from both the canada group and the global group but can not
