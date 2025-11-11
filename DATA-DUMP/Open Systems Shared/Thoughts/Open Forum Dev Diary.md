This is a continuation from Open Funder Technical. Which eventually
became a dev diary. Then the development focus changed to Open Forum
since I determined that all the features of Open Forum will be required
in Open Funder, but not vice versa, therefore I can have a product out
sooner by focusing on Open Forum. I then decided that Bounties can be
precursors to Campaigns and Goals with the same logic as above.

## Experience Farming

If someone posts artwork with tag #art. In a few hours it might get many
likes, making it obvious that the threshold will pass. If the threshold
is guaranteed to be 24 hours, than it incentivises waiting until the end
of the period in order to have an optimal chance of earning experience.
This is creating an unhealthy positive feedback loop of farmers.
Something that provides no net value to the community.

Thus time alone can not be the only threshold.

We can consider the following: taking half the vote count value of the
largest vote count previously. Lets say a previous post in #art had 1000
votes. We get a value of 500 in #art. Now any new post must either
achieve 500 #art or wait 24 hours since posting to pass a threshold.

This way one can not predict easily when a post might pass the
threshold, and is incentivised to vote in it only if they see #art value
in the post.

Some cases to consider:

### First post

What about the first art post, will the first vote pass its threshold
since max is 0 and 1 is greater than that? A solution to this could be
to wait for just 24 hours since the other threshold factor is null.
Another solution would be take the total community experience in #art,
and half it. But if its really the first post, then the community
experience would also be 0 since there were no audits done previously to
gain exp. In this case the only option that i see at this point is the
first, waiting the 24 hours.

### What if the max voted was negative.

So only one previous post was made, and it had a max votes of -10, half
of that is -5, does that mean that even a vote of 1 will cause the vote
to pass threshold? What if its always half the max absolute, so it does
not matter if its positive or negative. In this case it would be 5.

### What about negative thresholds?

What would a posts negative threshold be? Would it just be the negative
form of the half max as the positive? I see no reason why it cant be.

### Issue of slow growth

Lets say that the half max is 1000. A post gets made, and every hour it
gets several dozen votes, and they are 99% positive votes. Its clear
this is going to positively pass the threshold, and so experience can
still be safely farmed at this point.

New solution, half of average vote counts, not max, without 24 hours. If
there are 1000 posts, and the average vote count of all lets say is 50.
Then the half of that, 25 will be the only threshold needed to pass.

### Double threshold

Another option I would like to explore is the one defined in the Open
Funder document. The first 24 hours defines what the next 24 hours must
surpass. This does not feel like the right method but i\'d like to
consider it.

### Double threshold vs half of average vote count

User posts painting with #art. In a few hours it gets more than 25 votes
and passes the threshold. Or it never passes 25 votes and never passes
the threshold.

Or

In 24 hours it gets 50 votes, then a few days later it gets another 50
votes and passes the threshold.

What about the combination of the two. If in 24 hours, the vote count is
less than half the half the avg vote counts, so 1/4 the avg vote counts,
then the new threshold is double the current votes.

This is nice because it might provide a more realistic thresholds for
non "hot" posts. But since this is extra behaviour ontop of half avg
vote count, then it can be saved for later.

### What is the point of a threshold

To incentivise discovering new content. By assessing new content first,
you are able to earn experience. To de-incentivise exp farming. If this
is the case then, these are both concerns with just the voter, not the
poster. Therefore could the poster continue to earn experience even
after the threshold? Maybe a feature for later, since it is extra
behaviour on top of an already established behaviour.

## Half Average Vote Count Use Cases

After much deliberation on thresholds, it seems the half average vote
count is the best candidate. To reinforce that I will run more use
cases.

## Posting Credit

I had the idea that users can get 1 credit for whatever tags they post
with. So on 0 day, this could be the means of getting experience. If a
user posts spam in order to get a credit, then they will quickly lose
experience from down votes. This might be a viable replacement for
auditing.

But since posting will cost 1 expereince, that means when u first post
with a tag you do not have experience with, you must pay 1 exp for the
post, but you get to borrow 2 exp, to pay for the post, and to have one
to vote with.

So a user that has 0 exp in a tag, is able to borrow 2 (will go down to
-1 for the post, and -1 for a vote).

What about a user that has -1 exp and they post? If they already made a
post in the past, then the credit is not available to them. But then if
posting costs exp, and there is no auditing, there is no way for the to
be able to post again unless there is auditing, or the credit is
available indefinitely, or the credit is available indefinitely.

Another issue is that by limiting the credit to just the first post,
this incentivises creating multiple accounts. Unless there is auditing,
then its the same effort for a new account or existing account. Or if
the credit is available indefinitely if they have less than 1 exp.

So even someone with -100 in #art can make an art post, they would just
have -101 and they get one one credit. It could look something like this
to the user #art: -101(+1 voting credit) to indicate they have +1 credit
they can use for voting.

### What is the point of negative exp if you can keep posting?

You can't vote with less than 1 exp, unless you make a post, which gives
you a posting credit. So the point of negative exp means, you can only
ever vote once, for every post.

### Wouldn't someone abandon their account if they get a lot of negative exp?

You can always abandon your account, and create as many accounts as you
like. If someone gets a lot of negative experience then yes they will
want to start fresh, and thats fine, as long as they and/or the
community got some value out of it (maybe they learned something through
the specific failure).

A user might not want to start fresh if they have positive experience in
another tag, it is a tradeoff which a user must manage.

Doesn\'t it then make sense that if a brand new account with no
experience of any kind, gets negative experience from a failed post, to
just start a new account immediately? Yes, so maybe some rethinking
needs to go there. Maybe posts should not cost experience then. So that
a post that does not pass a threshold, does not result in -1 exp to the
poster.

Since they can keep posting anyways, posts costing exp really does
nothing.

## Should posting be free then?

Since u can post as many times as you want regardless of how much exp u
have or have in the negative it serves no purpose for posts to cost exp.

## Is user experience public and easily visible to all users?

The idea is that there is no private data stored remotely, there aren\'t
even passwords. Experience should be no different.

#### Benefits to public experience

If someone appears to be trolling or exploiting, looking at experience
might confirm that.

Someone might spend more time and effort considering content from a user
that has experience in a subject they have interest in. This could be
valuable since it gives users more accurate tools to prioritize and
generalize off a healthy measure. They have the choice to ignore
experience and treat all posts equally.

#### Down sides to public experience

If users look at a posters experience before they vote on a post or
reply, then they are basing their action on the person, and thus
identity, and not the persons actions. But why is this a bad thing?
Could it result in group think? So if several people with lots of
experience in specific tags are supporting something, then many other
users will mindlessly support it also?

I dont think so, since group think occurs due to psychological factors
that often revolve around ego and identity. People are very likely to
speak their mind in this environment, no matter what experience another
user might have.

What if in a debate, another person uses a person\'s experience as an
argument. This can be easily pointed out as a counter against the person
making that point.

## Karma & Categorization

Example: Someone posts an provocative picture with a link with a popular
tag like #covid19. It is an easy assumption that this is exploitation. A
solution to this could be to allow general karma, where anyone can
upvote downvote regardless of any experience requirement.

If people wanted to look at the account to see if it has a history of
these types of posts they might not be able to since most people
probably won't have experience in #nudity to be able to categorize it.
The solution to this is that you can upvote in any tag, but unless you
wage your experience in that tag, you do not gain any new experience and
neither does the user of the post.

## Actionable Voting

Whenever a contract requires a vote, there must be an initial vote to
select the vote tags that the vote will pass on. The amount of votes a
vote tag gets for selection will determine its weight towards the final
vote. E.g. A vote in order to select a phone design is required, and so
the initial 24 hour vote to select tags begins. 100 people vote for
#phone design tag, and 50 people vote for #3d design. Once 24 hours are
up, then the final vote begins. In the 4 day period of the goal
deadline, there is a net 1000 people yes vote for #phone design, and a
net 1000 people no vote for #3d design. Even though its a net 50/50
vote, since #3d design had double the weight from double the initial
votes, the vote passed 2 to 1 at the deadline.

Anyone can vote on a tag selection vote as long as they have karma.

# Phases

1.  Open Forum

    a.  No subs, just tags to categorize posts

    b.  General karma

2.  Tag voting for OF

3.  Bounties

4.  

## Experience creates democratized SMEs (Subject Matter Experts)

By allowing users to gain experience in specific subjects, voted in by
other users who already have experience in those specific subjects, it
is creating a democratized SME system. Moreso it is creating a ranking
system of experience where the rank is not utilized for a social
standing figure, but instead used to invest in more experience through
well placed voting on social or project decisions.

## Bounty vs Goal

A goal is something the poster tries to achieve, a bounty is something
anyone can attempt to achieve. They both must get voted to pass. The
difference between goal and bounty is somewhat ambiguous in this sense;
maybe instead goal should be called promise, since the poster promises
to make something actionable. Or Deliverable

Can they just be unified? In a closed source project that wants
community funding through open funder then the community should not be
able to achieve the goal. Then what about goal vs open goal. An open
goal is open to anyone, a regular goal is only available for the poster
or one of their group members. There is more to this as can be seen in
the Bounties section below.

## Bounties

A goal that is open to the public to raise funds for achieving it. It is
open to anyone to achieve and must be voted in by the public in order to
be accepted and for the funds to be transfered.

Examples:

1.  Produce evidence proving something. E.g. when a public claim or
    accusation is made, providing irrefutable evidence to prove or or
    disprove the claim.

2.  A new feature. E.g through a forum discussion, many people liked a
    suggestion for a new feature and so a bounty was created by a user
    in order to create it.

3.  A new product. E.g. The ideal smartphone was established through a
    forum discussion and now a bounty is created to make an open source
    design for it that manufacturers can use to create.

4.  

## Goals

A bounty can not be used to raise funds for a specific cause e.g to pay
for a hospital bill; since bounties deliver the funds to the poster that
was voted in, it can not be used to pay for a hospital bill. Those types
of goals need to have a designated account when the goal is established
that the funds will go to, such as the hospital, or the poster who will
pay the hospital (with proof).

A goal is like a bounty but the funds go to a designated location when
it is awarded.

Can the fund designation be changed by the poster or changed after
posting? No because this can be exploited. There might be exceptions to
this that require future feature development.

## Contest

This could be yet another funding feature added later. It is like a
bounty, but with a deadline, and anyone can submit proof of their
effort, and the winner gets voted.

## Open Goal

Like a goal, but open to anyone, but unlike a bounty, this can be
collaborative between multiple accounts. Several accounts/individuals
can submit pieces of the effort, and users will vote on the value each
provided. The payout will get distributed to all accounts with an amount
relative to the value submitted by that account.

## Explaining Openisim

Not really sure what to call it, so I will go with this for now. It has
been very difficult to explain the concept to people. Up until today I
could not figure out the main reason why, and it finally clicked. I did
not differentiate the technology concepts from the social implications.
I assumed that they were the same, in a sense, and so explaining the
tech would magically allow people to envision the implications. Where it
gets even more weird is that the tech used to allow the implications to
take shape is just common tech, and so people would see me getting
visibly excited about its implications while explaining this new
combination of common tech. This did not make sense. Most people\'s
reaction to that was to disconnect from the concept and in some cases
from me, with concern or just awkwardness.

Furthermore I would often jump to the end result of a social implication
because explaining the derivation steps is where I would lose most
people, since it is a very in depth process involving subjects most
people do not find interesting or are able to grasp in the 5-20 minute
explanation. No one really signed up for listening to this, they wanted
some brilliant tech concept to justify my excitement, but there was
none.

There was no tech concept, or at least not an apparent one on the
surface. The tech solution takes several old ideas and combines them in
new ways that aren't very exciting.

Let's imagine the founders of the internet got together before the
internet proliferated, and pitched it to the public that was already
used to radio and telephones, and telling them, this allows you to
communicate with other computers. Their response would be, so you mean
like a radio or phone, or is it a new device? Well no it\'s not a
device, it\'s just a way of doing things, a protocol for communication,
it lets computers talk together. At that point people would have
thought, okay cool, but what\'s the point.. It\'s not new tech or a
device, and we already have things like phones and radio for
communication. No one but a very select few could envision the enormous
social implications it would have had just 10 years later.

One last quick example. Bitcoin 2008, I can imagine a conversion; "well
it's a datastore, to keep data safe, and can be used to store currency
values". "Well we already have banking that can be done online, with
digital value tracking, what's the point? Is it new tech?" "Kind of,
sort of, its a database of sorts." "well that already exists." "yes but
this one makes it impossible to change previous records when a new
record goes in, because of math and physics\..." "oh well yes.. that's
different, cool?" Again no one but a select few would have imagined the
social implications. Implications which I think have just begun to
become realised.

Imagine there was a time traveller. Who travelled back in time, from
today, 2020 May, to 6 August 1991. And confidently and coherently
painted a picture of what it will become, but more so, told the story of
how it grows and evolves, because without a narrative that makes sense,
we are just left with disbelief, concern and we disconnect.

But anyone can create a story, how do you guarantee that it will happen?
You can't. Though, if the tech is understood, it will create confidence
in that being the most likely outcome. Why? Another analogy.

There is a meteor in the sky, heading towards earth, those that know,
panic. But then a select few that understand gravitation, explain that
the gravity well from another planet will cause it to sling shot
completely missing earth. Upon hearing this people are skeptical because
panic is strong, but those that actually decide to follow along and
understand the concepts of gravity now understand how it will behave,
and how it will miss earth, they now have the confidence in this new
behaviour from this new understanding. Rudimentary stuff, but advanced
concepts can be easily or better understood through a series of simple,
rudimentary examples.

As a result, I will now be creating a narrative of how the different
phases of "Openisim" will affect society, with each phase impacting and
changing society in different ways. I will not go all the way to the
end, but just a few phases in.
