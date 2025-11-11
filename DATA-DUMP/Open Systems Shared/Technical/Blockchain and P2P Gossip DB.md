The idea is to only store critical data in blockchain, and to store non
critical in p2p services, then hash the non critical data, and save the
hash as critical data on the blockchain.

# Conclusion summary

A post will be stored on gossip with the content hash as the id.
Eventually any edits made can link to and from the original post id as a
linked list. All votes will be reset for the new/edit post, but a record
of all the old votes will be kept in the original post.

# Original Concern

This issue is that if a hash is to be stored on a blockchain, then it
will cost money to create a post. It should be accessible to all.

Maybe a post that can earn experience must be part of the blockchain,
and this can be sponsored. So all posts initially will not be part of
the blockchain, but maybe when it passes a threshold it must be part of
the blockchain.

That means any vote, since it writes to the blockchain must also cost
money.

# Case poor expert

1.  Make valuable post

2.  Get sponsored

3.  Earn a great deal of experience

4.  Unable to vote because no money to make a vote.

# What if people can sponsor votes?

That way people with experience can vote and use the money from the
fund. Can this be exploited if someone moves money out of their account
to not pay for a vote? No, because the cost of moving funds should be
more than the vote.

What if there is a pool of funds for posting and voting, but if you pay
for it yourself you get bonus experience?

Maybe if you fund your own vote, it\'s what allows you to earn it back
if it passes?

A user can then post to p2p only, but can not start earning exp until it
is funded and posted on the blockchain also!

Although when someone votes, the cost of vote will account for the
experience gained by others, since the routine will run when voting in
the smart contract.

Maybe then the post content hash is the id of the post.

If someone tries to change the content in p2p, and tries to propagate
it, it will not match the hash and thus id. They will have essentially
created a new post. In p2p only posts with matching hash can be
accepted.

Then voting on the blockchain can be made against that hash.

Should a post lose all of its votes because of a spelling mistake? No,
just don\'t correct the spelling mistake, don\'t lose the votes.

The concept of floating an idea or post is emerging, to loosely put
something out there, without having to commit resources to it. Once it
is ready, by some means, it is "published" to the block, where ite takes
resources to do so, but can earn resources also.

Users can follow for free. Maybe users should be able to vote for free
also, without being able to earn experience. This could just be to
categorize a post. Maybe when the post gets published to the block,
users who have already voted can get notified, and they can turn their
votes into real block votes. Or can set this to happen ahead of time.

## Problems with public draft

Being able to post publically without earning exeprience has some draw
backs.

If somone posts something offensive they can do it consequence free,
since they can not get negative experience, or downvotes.

## Will replies ever need to be on the block?

No. content does not need to be on the blockchain

## When will a post need to get published to the block?

Posts do not get published to the block.

This might be the same question as should an author get experience for a
post they made that is not published?

A pulish will link the user id, the post id, and the content hash on the
blockchain.

Maybe a post never needs to be sent to the blockchain, and only votes
need to be recorded on the blockchain.

## Can voters cast non-block votes?

No, there are no non block votes, votes are on the block.

If a post is on the block, should users be able to cast non block votes?
What would be the value in this feature?

There is no value I can see at this point.

## Is there any value to non-block votes in general?

No. adds complexity to having different types of votes.

## Linked list of content hash

[[Edits are not
permited]{.underline}](#should-votes-be-reset-or-kept-for-a-post-edit)

When a post is made, the content hash will be the id. When an edit is
made, the new content hash will be linked from the old content hash.

## Should votes be reset or kept for a post edit?

The problem with edits is that it costs money to vote, if a poster can
edit or delete without consequnce there will be wasted funds on voting.
This argument supports keeping the votes, so that users do not waste
their vote.

If the votes are kept, then this can be exploited by keeping the votes
of voters who will not cast revotes, therefore votes should be reset.
Since it is the action of the poster that causes a revote, it should be
the poster who is responsible for the consequences, not the voter. This
is potentially the same issue as deleting, since the content might
change, the vote might need to be changed, therefore costing the voter
for the edit.

**Therefore editing and deleting should not be possible after posting**

Options:

-No deleting or editing after posting

-no deleting after posting, but editing is permitted

## Where should the hash be generated?

If it is generated on the client, it is not guaranteed that it will not
be a duplicate. Someone could maliciously use the id of an existing
post. So i would still need to be checked for duplicates. If its
generated on blockchain, it guarantees that its a unique id and no check
is required. If its generated in a blockchain that means that the
content needs to be sent to the blockchain.

## Case Post

1.  Client creates hash as ID of content

2.  Data is sent to gossip network

## Case Vote

1.  Upvote of post tag is submitted to the block and to gossip

2.  User pays fee for voting

## Case List Posts

1.  List of posts from gossip network

    a.  Includes vote counts per tag

    b.  

## Case Edit

Editing is not allowed

1.  Edit is posted

2.  Original post gets a link to the edit post as its edit property

3.  New post gets a link to the old post in its old property

4.  Original post no longer will show up in post list since it has an
    edit property

5.  When a voter logs in, an app can check all the posts they voted on
    to see if they have an edit property, if they do, they can be
    notified that a post they voted on was edited and a link provided to
    the new post.

## Case Post and vote

1.  Content hash is created and set as post ID

2.  Viewers will get post from post list

3.  A vote is made and logged against the post id on the block

## Case Poster Experience

1.  A day passes after posting and 10 upvotes total

2.  The poster executes the smart contract that checks their posts for
    earned exp

    a.  Upvote totals are calculated and experienced is issued

3.  Any upvote past a day will result in immediate experience update

## Can Posts be deleted?

[[Posts can not be deleted after
posting.]{.underline}](#should-votes-be-reset-or-kept-for-a-post-edit)

##  What happens when a poster has already earned experience and they would like to edit?

[[Posts can not be deleted after
posting.]{.underline}](#should-votes-be-reset-or-kept-for-a-post-edit)

Maybe edits can not be made after a day of posting or voting.

Maybe the exp can be returned to the voters if the edit is deemed
important enough

## Should voting cost?

In order to write to the blockchain, it must cost. But if voting costs,
it will not be available to everyone.

A solution is to create separate tokens for each experience type. And in
order to earn double experience on voting or posting, a user must have
the block running on their system. This way voting and posting should
cost nothing and be fully operated by those staking their experience.

Should voting block miners be rewarded with extra voting power because
they run a node? **No**, experience and voting power should be directly
proportional to value created.

Also scaling is an issue, since voting power can not scale with the
amount of power mining the block, there will be no incentive to scale
mining power, and thus no guarantee that the network can keep up with
voting demand.

A radical idea is to have a currency for each tag, that way mining power
is independent of voting power. But since this currency can be exchanged
for any other currency, it currently appears to make no difference than
using a standard currency. If though the currency could not be
exchanged, this might create an option worth exploring further.

The other option is the have a fund that covers the cost of voting.

Another option is that users can earn funding by creating content in
tags that are sponsored, so each upvote a user receives in a tag, will
result in funding being funneled to them from those sponsoring those
tags. This will allow them to earn credits that they can use to pay for
voting.

What if experience is what earns passive income, that way voting is a
value decision, By spending experience on voting, one reduces their
income generating stream. This means this vote is important to the user
voting.

Therefore overtime, someone that is able to vote because they have
experience, will also be able to fund voting since they are earning
passive income on that experience.

Therefore sponsorship is a key component to the functionality of the
open platform.

## Philosophical Problem

Voting should be free to all, but writing to the blockchain will always
have a cost. At the same time there is also a time and resource cost to
making it to a current voting poll and submitting your vote.
