1.  Research Textile to see if it is a good option compared to github :
    No, does not have discussions

2.  Create anon email account, create github account

3.  Create markdown from intro document and publish

4.  Create markdown for task list

I propose that Git hub will be used as features are rolled out in open
systems, which can then gradually take over the responsibility from
github. e.g. Once open-forum can support discussions, then most of the
discussions can take place there as users can begin to earn experience,
once projects in open systems is ready, then project tracking can be
completed there instead, that way users can begin earning experience and
tokens.

# Public General Task List

1.  Consider using a project manager app/service like pivotal to track
    tasks, versus using github markdown.

# Open Forum Initial Release Tasks

Majority of the specifications of the open forum are tech agnostic,
therefore a discussion should be had about which technology stack would
be best to use currently to implement the open forum. Over the last 5
years I have implemented it with various technology stacks. The latest
is a proposed mix between a gossip network named gunjs and a solana
blockchain. This would allow posts to be made without any cost to the
user. The initial and current release only makes use of gunjs, and as
such implements the concept of a first admin (the first account made is
the admin). This allows some basic moderation actions such as removing
posts, which users can verify that the action is signed by the super
user. The removed posts go into a removed node, so they are never
actually deleted, just not displayed by default with all the posts in
the main post list. The initial release has no blockchain features for
simplicity.

1.  Consider using gossip network + blockchain, or purely blockchain,
    have discussion with solid conclusion.

2.  Finish Open Forum Initial Release, with the following key features:

    a.  Single Admin moderation, to remove accounts and posts

    b.  Single Admin invitation for new accounts

    c.  When a user makes an account, they can not make any posts until
        their account is activated.

    d.  The admin can see a list of pending accounts and activate them.

# Open Forum Community Token Moderation Release Tasks

The next proposed release will have the following features listed below
(these should be discussed before they are locked in). This will begin
to use the blockchain to handle tokens and token related actions. The
idea here is to allow the community to self-moderate by earning a
"utility token" every 24 hours. It will cost 1 utility token to make a
post. The post data can be stored in gunjs (gossip network), and a hash
of the content can be the posts id which will link the gossip network
(GS) entry and the blockchain entry. A user can collect a maximum number
of utility tokens after which point they can no longer collect any more,
e.g. 10 tokens. Users can also use tokens in order to activate accounts.
E.g. 5 tokens. Users can also report posts which they believe break the
established rules
