## Downvoting experience

Experience should never be earned on downvoting since anyone can create
posts that reduce value. No part of the down voting process should allow
earning of experience since people can purposely post which takes away
value, to provide experience to others. The most is being able to
recover a downvote.

## Should downvotes always be free?

And recoverable after 24 hours through claiming?

### 

### Tag Network & Inheritance

After some thought tag inheritance makes no sense. Because each post and
bounty must be assessed naturally. Each post, no matter if it\'s a
child, or bounty or a child bounty, must get individually assessed and
thus voted by tag.

Can a bounty get few tag votes, but a high bounty reward? And what does
that mean? If people see a high and growing bounty reward, are they more
likely to start voting for the bounty? What if they don\'t agree with
the bounty but want to farm the experience?

Use Case : A bad feature

A user posts a bounty for a feature that would ruin the current user
interface. (? would down voting #interface make sense? Its an open post
since its a bounty, and so the experience would not net to the poster).
A user would then reply expressing their concern. The reply would then
get many upvotes in #open forum and #interface. The original poster
would then reply saying they understand why it wont work, and maybe they
too would get some #open forum and #interface experience.

What if before that reply, some users with a bit of experience in those
tags upvote it, and donate.

### What does voting an open post do?

Since the experience does not go to the poster, what is the point? Users
can still invest the voted experience if they believe in the value of
the open post. (think of an open post like a wiki). Then votes could
help categorize it and express its value. Maybe there is no point to
voting on an open post.

If a user posts a wiki about ww2, but it has incorrect information, then

Use Case

A user creates an open post about interface improvements and features
for an open forum. Another user crates a bounty for a suggestion they
have. The bounty inherits the tags and tag votes from the parent post.

#1

After a solution is posted to the bounty, the users who voted the tags
on the parent post, must vote on the bounty of the matching tag in order
to have it pass as completed.

#2

Users can vote specifically on the bounty tags. ( If they vote on the
bounty tags, they do not have to vote on other child bounties of the
parent post, as if they had voted for the parent post tags). After a
solution is posted to the bounty, the users who voted the tags on the
parent post and the bounty post, must vote on the bounty of the matching
tag in order to have it pass as completed.

#3

A child bounty is posted to the current bounty. The child bounty
inherits the tags and tag votes from the parent post. Everyone who voted
on tags of the parents must vote for the child bounty to pass.

By voting a post tag, you commit to voting on all child bounties.

### Voting Deadline

No deadline see below.

### Vote Rewarding

Should voting be rewarded beyond the initial ROI of experience? E.g. you
vote on a post tag 10 votes, and if the votes double from when you
voted, you get 20 exp back. Should you keep getting experience for
voting on child bounties? Or should that also be an investment? Hint:
Everything should try to be an investment. If it is an investment then
if a new bounty gets posted you should have to invest exp in order to
get a return, it should not be a return from the original investment
that already had a return. Hint: each bounty should be assessed in
detail by willing experts. Forcing an expert who voted on a parent to
now vote for all child bounties might cause a hassle. Therefore no
deadline. So then maybe vote count should not pass to children, just
tags. Because it could cause a problem, where the initial voters on the
parent, are not available to vote on the child bounties, and a vote
might not pass when it should.

Issue with current voting mechanic. A user could vote several months ago
to accept a solution, the solution might have changed drastically. A
solution could be to reset votes everytime a solution changes, or maybe
everytime there is a response, or maybe once someone votes to accept
there is a 24 hour period where users can vote to accept or reject.
Either vote must be and investment.

Maybe in order for a vote to pass, there must be more or equal accept
votes within a 24 hour period than half the tag upvotes. This way anyone
can vote at any time to accept, but if it does not pass, they will lose
that experience. Maybe a reject vote can not be made if no accept vote
has been made in the last 24 hours, and if there arnt more rejected
votes than half of the accepted votes. E.g. if there are 10 accept votes
in the past 24 hours, than there can only be -15 rejection votes.

?What happens to experience gained from a vote return, after cancelling
the vote? Should it be kept, or subtracted from the account? If its
kept, then it will incentivize cancelling all votes after they double.
Maybe cancelling a vote will not return the experience invested. That
way if you cancel after doubling, you will receive nothing, but the vote
is removed. If you cancel before doubling, you also get nothing back and
lose your experience. This encourages longer positions in investment and
more informed decision making. This will also not incentivize cancelling
votes after doubling since it creates no gain.

### Max votes

When a vote is more than double of the (opposing votes + base), no more
votes of that direction can be made.

Exploring what the base is?

Use case:

If a new post is made, double of 0 negative votes is 0, and max votes is
0, therefore base can not be 0. If it is 1 then max votes is 2. This
would also mean that the max experience gained from any post is 2, this
also does not make sense. This also incentivizes controversy since if
they get more negative votes, they are able to get more positive votes.
Instead a clear winner with the least amount of controversy should be
encouraged.

In the case of negative votes, it should be limited, since its much
easier to mass determine that a post is not of value, then that it is of
value.

Maybe positive max votes could be used when there is a passing
threshold, such as in a suggestion or a goal. In which case the base can
be the positive vote count of the leading competing post(suggestion or
goal).

E.g. if suggestion A has 100 votes, suggestion B will be double 100
votes as its max voting limit. After this limit it can not be voted any
longer.

### Passing Votes

When they type of vote is a passing vote, such as in a bounty
completion, goal acceptance, or suggestion acceptance. Votes will double
again for all voters. So early voters will get the double return, and
the pass return, getting 4x their original vote.

### Passing Vote Tag Qualification

a tag vote must get more than vote tag count / 100 \* greatest tag
count. So if #open forum api has 1000 votes, and there are 10 other
tags, then 10 / 100 = .1 \* 1000 = 100. Since #forum does not have more
than 100 votes, it does not need to get voted completed in order to be
voted completed. In this case only 3 tags must be voted complete #open
forum api, #programming #react.

## 

The voting criteria threshold (the lowest point at which a subject is
accepted as voting criteria) is

Use case

  -------------------------------------------------------------------------------------------
  #code      #finance        #creative   #interface   cutoff       method
  ---------- --------------- ----------- ------------ ------------ --------------------------
  100        100             100         1            50           Half of half, half is
                                                                   #c:100, 50

  100        50              25          20           12.5         Half of half

  100        100             10          10           25.25        Half of average

  1000       100             10          10           140          Half of average

  1000       100             10          10           140          High divided by lowest

  1000       100             10          10           550/10=55    Avg low div avg high

  100        100             100         1            100/55=\~2   Avg low div avg high

  100        100             10          10           100/10=10    Avg low div avg high

  100        100             10          10,1,2,3,4   73/3.2=24    Avg low div avg high

  100,100,   1,1,1,5,6,8,5                            27/7 = 4     Avg of lower median
  10,8                                                             
  -------------------------------------------------------------------------------------------

## Potential exploit

A user could transfer experience to another user by creating a post that
has no real value, and having the other user upvote it. People would
have no incentive to downvote it, since they would lose experience by
downvoting it. But what would this exploit result in? Since the original
account would have equal opportunity to use the experience as much as
the new account. There is no reason to perform this exploit. It might be
a way from a user to give another user experience, maybe for outside
funds? This would then need to be reported with a claim with evidence.

## Votes and Experience Sync

Votes need to directly reflect user experience. This is done through a
sync at most actions.

## Should users by default get experience from non original content?

Non original content:

1.  Administratie post like creating a goal, project, bounty, etc. where
    an administrative task is being performed but no content is being
    created. It\'s not that only creativity is rewarded, but,
    administrative work is not rewarded by default when voting, but can
    optionally be rewarded

2.  Reposting someone\'s original work

## Optional Experience donations on non original content post

Since non original content posts like administrative posts still create
some value, they should not be excluded from receiving experience. But
if users are allowed to donate experience, this makes experience
transferable and not dependent on value, breaking a rule. This can be
exploited. E.g. A user who has lots of experience but received a ruling
against them which shows up on their account might want to transfer
their experience to a new account, and now they can.

## Transferring experience exploits

A user could also create an original content post, such as a technical
drawing that provides no real value and is nonsense, so that they can
get voted by their other tarnished experienced account. If a user sees
this and thinks it is an exploit, then they can report the post and user

### Audit experience that gets locked up.

If a user locks in 1 experience globally in #technical drawing, othen
when a post with #technical drawing gets reported, the user might get
selected at random to audit the post. The user consumes #technical
drawing, for reporting, but if it passes they receive the experience
back, and the auditing user earns the amount of experience they have
auditing experience they have locked up.

Subscription voting should not allow users to earn new experience since
this incentivises valueless voting, instead subscription based voting
should allow users to vote for free with the experience they have
locked, always allowing them to return it.
