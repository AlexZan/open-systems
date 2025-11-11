> ![](media/image1.png){width="4.929571303587052in"
> height="4.234375546806649in"}

Leading thought: This is really a sentient interaction protocol (SIP)

What is needed to convert the Open World Alpha into Open Fund?

Key Differences

1.  Instead of posts, there are just projects being shown. A project has
    a title, description, goals and owner.

2.  An owner can only be one account for now, so if the owner is a
    group, there will need to be one representative or manager managing
    the project on OFer.

3.  Goals do not have their own funding, they are just community
    checkpoints for progress.

4.  Goal Payments

    a.  A user can either request payment for a goal upfront. E.g. I
        need 10k to make this watch prototype.

    b.  Or a user can request payment once goal is completed. E.g. When
        I finish this watch prototype, I will get 10k

    c.  Users will need a much higher rep in order for their project to
        be funded with upfront payment goals. If you are new, then a
        project with completion payment goals is suggested

5.  Goals will indicate when there is enough funds in the project to
    fund them, in the order they are listed.

## Adding a Goal

An id is generated with an amount of 0. When an amount is contributed to
a goal

# Dilemmas

1.  Should it be a contract per goal, or per project?

    a.  If a goal is cancelled, that means the entire project is
        cancelled. Therefore it would be much easier to cancel all
        goals, project wide, if the contract was for the project.

2.  Should there be one big fund for the full project and the goals just
    indicate how much they need, or should each goal should act as its
    own fund?

    a.  If a goal is its own fund, then people would have to micromanage
        contributions, might be too much work for most. A solution is to
        allow contribution to the project as a whole, which will auto
        distribute funds to each goal.

    b.  If a goal is not its own fund, then users can only contribute to
        the project as a whole.

    c.  Is there any benefit to contributing to specific goals? In the
        case of OFer, there is no value added by this since the end goal
        is to finish the full project, there is no case of value
        delivered from half a project finished.

    d.  Really then the point of a goal is not a point of funding, but a
        control point, where the community must validate the progress of
        the project.

    e.  Therefore, there will only be one project fund

## What will be BlockChain and what will be standard DB?

The campaign fund will be the only initial thing that must be a smart
contract for the following reasons:

1.  Guarantee to return funds based on smart contract rules

2.  It is impossible for anyone to handle or touch the campaign funds
    until the campaign is approved and the funds delivered after holding
    period, after community vote.

3.  Only the community can control the smart contract through votes.

4.  Tamper proof

5.  Full transparency

Later more elements of the platform can be migrated over to blockchain
where it makes sense, such as accounts.

How does the platform get the campaign list data from the blockchain or
from a synched db?

## What is the sequence of starting a campaign?

1.  Meet requirements: karma

2.  Auth with ethereum wallet you will be depositing from

3.  Fill out campaign form

    a.  Fill out one or more goals with funding needs

4.  Submit form

5.  Creates smart contract for campaign

6.  Creates database entry linking to smart contract for campaign

What should be locked in after a campaign is created?

Number of goals? Goal details?

The requirements should be locked in, since thats what people are
funding. If they need to be changed, this would need a community vote.
Anything after publishing should be a community vote, since from the
moment it recieves its first funding, the community is locked into a
"contract" with the owner against the parameters of the campaign and its
goals. Changing any parameters, will theoretically void the existing
"contract" and should void the smart contract as well. The only way
around this is to request edits or changes to the parameters and
properties, that the community can vote in.

## Failed Goals

If an owner fails to pass a goal by the expiry date, all funds will be
returned immediately.

Reasoning:

\[1:09 PM, 8/23/2019\] Alexander: i guess the question is

\[1:09 PM, 8/23/2019\] Alexander: return the funds, or wait for
community to vote to return funds

\[1:10 PM, 8/23/2019\] Alexander: i think by waiting for community to
vote, the owner could think they have some time to slack, so they wont
apply for an extension

\[1:10 PM, 8/23/2019\] Alexander: where as by returning them
immediately, they will apply for an extension as soon as they are
worried

# Token Distribution

How to determine how many tokens get created? What their value is, and
what the exchange is per goal?

Lets start with a traditional example.

A company starts a Kickstarter campaign, and offers to sell printer for
100 for early buy ins, 200 dollars, for second phase, and 400 for
regular retail.

This could correspond to 100 dollars for 1 token in goal 1, 200 dollars
for 1 token in goal 2, and regular 400 for 1 goal once funding for all
goals has been reached.

In this example, the owner is solely responsible for picking the price.

What about a service example? Lets say an uber equivillent. 1 token gets
you 1km of travel. Goal 1 could sell 1 token at 10 cents. If goal one
needed 20,000 dollars. Then it would sell, 200,000 tokens.

But after a year or two after the service goes public, the token price
may fluctuate. So the price the owner picked is just an estimate. If the
community thinks 10 cents is too much, maybe they wont want to fund it.
The owner would then modify it or take a consensus.

# Smart Contracts

Creating a campaign will start a smart contract with a wallet, with the
following rules:

1.  If project does not start before expiry

    a.  funds are returned

    b.  karma is reduced

    c.  Project marked as expired

2.  If a goal is marked as submitted

    a.  Users can submit votes

3.  If a goal vote is submitted

    a.  Check if votes is greater than participants, then goal is
        approved

4.  If goal gets voted as approved

    a.  Funds are then immediately transferred (for use on campaign)

5.  If all goals get voted as approved then project is marked as
    complete and

    a.  Extra funds are marked for a holding period

6.  If a votes pass to cancel extra funds

    a.  Funds will be returned

    b.  Owner will have this marked on their history, with the reason as
        to why the funds were cancelled, with possible karma
        repercussions (TBFD)

7.  If the holding period ends

    a.  Funds are delivered to the user

    b.  A successful campaign gets marked in history

8.  If funds are contributed after a project is complete, the donation
    goes straight to the owner without holding

9.  If funds are contributed during holding period, they are also put in
    the wallet that is in holding

### Therefore the following must be purely determined from smart contract

1.  Campaign and Goal status

2.  Goal Votes

3.  Goal fund amounts

## Goal Votes Smart Contract

Each goal will need to have a smart contract created. Contract will keep
track of

1.  Users can fund the goal

2.  If the fund is greater than the fund requirement of the goal is
    transferred

    a.  goal funds marked as transferred

3.  If goal is votable (open by owner when submitted deliveries) userse
    can

    a.  Vote yes

    b.  Vote no

4.  If vote yes is greater than campaign participants

    a.  The goal will pass

    b.  and will not be votable

5.  If user voted, cant vote again

6.  If time expires before a vote is completed

    a.  Funds will be refundable

7.  If a user submits an extension request

    a.  Users can vote on it

8.  If a retry request is submitted, users can vote on it.

    a.  User specifies retry time required, and funds needed.

9.  If a retry vote passes

    a.  Current goal is marked as closed/retried

    b.  New goal is created after this goal (even if other goals exist
        after already, it pushes them)

## Campaign Smart Contract

1.  Owners can create goals

2.  If the owner submits deliverables to goal

    a.  The goal is votable

3.  if a goal passes the next goals funds are unlocked

4.  If all goals pass, the contract is marked as complete

5.  If the fund time expires then funds will be returned. This will
    reset each time a goal is funded.

## CampaignFactory SmartContract

1.  Creating a campaign adds it to the campaigns list

2.  Getting the campaign list

3.  Can get new campaign by providing owner address

4.  Can only build one campaign at a time

5.  Campaign will stay in new campaign list until campaign is published

## Front End App

1.  Can not add new goal until active goal is saved succesfully.

2.  On load of new campaign view

    a.  Get goals

    b.  Add goals to completed goals list

# Problems

1.  How to refund all backers money, how to itterate through backer
    mapping?

## How much to return if part of the backing is used to fund a goal

1.  Jim funds 50 dollars.

2.  Tim funds 100 dollars

3.  Funding goal of 100 reached

4.  A remainder of 50 dollars is left

5.  Goal expires, project canceled.

6.  Who gets the 50 dollars?

#### Problem

The first goal always has higher risk in funding because the funds will
be transferred without any deliverables.

#### Possible Solutions

1.  Biggest discount for tokens until first goal is delivered.

2.  Another option is to create a fund and wallet per goal.

## Benefits of Per Goal Wallet

1.  More secure, only one goal might get compromised, not the entire
    campaign

2.  If goals has to restart, it is easy to create another goal with
    fund, keeping the original funds in place for refunds.

## Should goal contracts know the owner?

1.  If they do, when an owner changes, it will have to change owners on
    all goal contracts

2.  If they only know campaign contract, then the owner only needs to
    change on the campaign

3.  Less to to track if only keeping track of campaign contract

# Future Features

### Changing ownership

If a campaign has more than 1/3 retries to completed goals, the
community can vote in a new project owner.

If the owner is deemed fraudulent, the community can vote in a new
project owner.

1.  If all goals pass, the contract is marked as complete and

    a.  Extra funds go into a holding period

2.  If holding period ends, extra funds are transferred to owner

3.  If a user contributes to the campaign after the holding period, they
    are transferred directly to the owner as a donation.

4.  If the fund time expires then funds will be returned. This will
    reset each time a goal is funded.

In the current version, goals are static once the campaign is created.
Cannot add or create new goals. But later, goals can be added, retried
if failed, etc.

## Using node/nosql to serve campaigns list vs blockchain contract

### node, nosql

1.  \+ Much faster, more efficient to sort and page campaigns list

2.  \+ Much easier to code and maintain, cleaner

3.  \- Have to synchronize with blockchain data

4.  \- Have to sign against ethereum account (auth with metamask)

### blockchain

1.  \+ Auth handled by blockchain

2.  \+ Data already in blockchain

3.  \- Much slower, less efficient to sort and page campaigns list

4.  \- title, description, etc, do not need to be on ledger, since they
    do not affect the smart contract behaviour in any way.

## Use Case for node,nosql method

### Create Campaign

1.  Front end submits new campaign with 2 goals

2.  Deploy contract with ethersjs or with factory call

3.  Get new contract address

4.  Send node confirmation (or node gets it from event from factory
    event)

5.  Update node with title, description and any extra meta as well as
    all blockchain data: fundrequirment, time requirment, etc.

### Update Campaign: New Goal

1.  Front end submits update: adds new goal

2.  Add goal to blockchain through campaign contract

3.  Send node confirmation (or node gets it from event from factory
    event)

### Update Campaign: Description

1.  Front end submits update: changes campaign description

2.  Send update to node (auth with metamask)

### User Participantes

1.  Front end calls participate on campaign contract

2.  Send node confirmation, or gets it from event

### Display Contract List

1.  Get list of top x campaigns, sorted and filtered

## Use Case for blockchain

### Create Campaign

1.  Front end submits new campaign with 2 goals

2.  Deploy contract with ethersjs or with factory call

### Update Campaign: New Goal

1.  Front end submits update: adds new goal

2.  Add goal to blockchain through campaign contract

### Update Campaign: Description

1.  Front end submits update: changes campaign description

### User Participantes

1.  Front end calls participate on campaign contract

2.  Campaign contract lets factory know about participation update

3.  Factory checks if the campaign moves up in order above

Problem with this is that its rigid. What if we want to sort by funding
amount. What if we want to sort by funding amount and filter by keywords
found all text. We would need a pre sorted list for each sorting type.
Then to filter with each get campaign call.

### Display Contract List

1.  Get page of x sorted contracts addresses from factory

2.  Get details from each campaign contract, and from each goal

    a.  Load details in as they come in

    b.  Check hash to see if changed from current

## Different States or Status for a Campaign

1.  Fundraising - when funding for any unfinished goal is not achieved

2.  Started - when funding for the first goal is achieved

3.  Voting - when goal is delivered, and the a goal is being voted

# Node Blockchain Hybrid Concept

1.  Get list of sorted and filtered campaigns from node minus blockchain
    data

2.  Get all smart contract dependent data from blochain.

What is the advantage of this?

1.  No duplicate data on node, that alraedy exists on BC

2.  less synchronization needed

What are the disadvantages compared to full node solution

1.  Wait for two requests

2.  Individual contract query for each campaign (because it has sub
    arrays, goals)

# Campaign Steps vs One Big Package

1.  If there is a problem, progress is naturally saved with steps

2.  Less data in a transfer with steps

3.  Cant send list of goals because goals contain strings

4.  Limit of how much arguments u supply a function in solidity

# Delivery

How will owners deliver goals? It will be picture, video and any other
files. It could almost be like a little mini website or presentation.
Where users scroll down to see the delivery and presentation. At the
bottom they can vote?

### Security

Since the content being submitted will not live on the blockchain. How
will it be secure against tampering? E.g. owner submits an impressive
but fake image, then at the end changes it to the real image after it
was voted as passed.

One solution is to store a hash of any content item on the blockchain.
The hash on node can be checked against the hash on the blockchain to
make sure it matches.

### Initially

While security features can be eventually rolled out. Initially maybe
just a text area, where owners can provide links to github, dropbox,
youtube, and link images to might be the best solution. If an owner
exploits one goal, users will vote the owner as fraudulent stop any
further damage as well as recover some losses.

# Thoughts

It is not for the SME to decide how much to give to the contributor, but
for them to decide how much the contributor gets.

A programmer upgrades a core service. Most people will not understand
the value, and will not know how much to donate for their contribution,
but a SME will vote that the contribution is worth x amount, sitting
between previous contribution C and D. Now when a donation is made by
anyone, they will get a proportional amount of the donation. The other
contributors will get the remainder. Users know they are contributing
fairly, even though they don\'t understand the value and distribution.

## No Identification, No vote limit

Users do not need to identify. They can create as many accounts as they
like.

Users can not vote when they create an account. Most features are
locked. Users must gain a karma rating in order to unlock voting. But
also:

In order to vote any type of vote, wether its upvote, or goal vote, etc,
a user must spend vote points. Users earn vote points by contributing
valuable comments. The vote points are specific to a topic.

In order to vote in a specific topic. E.g. #electronics. Users must
comment on something in the campaign that is tagged with the
#electronics tag (or maybe tag their comment with a desired tag). If the
comment gets upvote, and if the campaign is successful. The user with
the comment will get #electronics points The amount depends on how many
upvotes they received.

Users can also earn vote points if they upvote a comment that is
valuable, once the campaign completes. The earlier they upvote the
comment, the more vote points they can earn. If you are the first
upvoter you then earn half the vote points the original poster earns, if
you the 2nd you earn 1/3 of the points, and so on.

In order to gain your first vote points, you can exchange karma for vote
points of your chosing topic.

### Emergent Rules

A user should not be able to do more with more accounts than they can
with one. Therefore there should be no incentive to create multiple
accounts, other than to separate identities. Or to seperate accounts
that focus on different areas.

## Thought vs Resource

There is thought and action? Thought work requires intelligence,
processing and creativity. While actions require resources; food,
material, funding.

Resources can be transferred from person to person without change in the
person, while thought changes the person when it is transferred to them.
Thought work creates understanding, experience and wisdom in the person.

Therefore

Votes should be earned with thought work. Resource gain should be gained
from action work. A person will gain wisdom about a subject through
thought work, and thus should have a greater impact on the outcome in
regards to that subject. A person with vast resources should have no
additional impact on a subject based on their resources.

You can gain voting points by demonstrating knowledge, wisdom,
experience. You can gain resources by contributing resources, e.g. you
can buy tokens by funding a campaign, but you can never buy votes.

## First Goal and Work upfront or funds upfront?

The first goal is a bit different. There is no previous goal to unlock
it. So what are the conditions that deliver the funds?

What if the first goal has an option of asking for the funds upfront, so
that once the fund requirements are reached, goals are delivered and
work is started. Or work upfront, and once the delivery is approved,
funds are delivered?

So really the option is, what is the funding condition. Delivery success
or funding reached? Work upfront or funding upfront? And if so, couldn't
that be an option for all goals?

If funding upfront, then, goal only starts when funding goal is reached.
And if work upfront then goal starts right away.

What if funding goal is never reached for work upfront before the goal
expires? Does it expire? That makes sense since it was a commitment made
with no guarantee for reaching those funds, but a guarantee to finish
the work by that time. Maybe the time should start when funding is
reached?

What if goal is delivered before funds are reached? Then if the delivery
is voted approved, the goal is complete, and the user can withdraw what
was funded.

What if the owner has the delivery ready, but refuses to continue until
the fund requirement is met

### Cases Work upfront

1.  First goal is work upfront.

2.  User starts working or doesnt.

3.  Some time later the fund requirement is reached

4.  The goal time starts, and they have the requested time to finish it.

#### They deliver in time

1.  They deliver the goal on time, and vote passes and goal is marked as
    complete

2.  They withdraw their funds

#### They don't deliver in time

1.  They dont make the goal on time.

2.  The goal fund remains unlocked and gets marked as refundable

3.  Funders can now request refunds for their original funds

#### The fund requirement is not reached and they deliver

1.  Owner delivers, voted as pass.

2.  Owner can wait for fund requirement to be met

    a.  The owner can now wait for the fund requirement to be reached
        before starting the next goal if the next goal is work upfront
        again.

    b.  If the next goal is fund upfront, they dont have a choice, the
        first goal must get funded in order for the next goal to get
        funded

    c.  ?? this is currently not the case, users can choose to fund
        whatever goal they like, but should this be changed so that the
        campaign auto manages funding??

    d.  ?? Should the campaign hang indefinitely ?? or should there be a
        limit ??

3.  Or can choose to accept to accept the current fund.

4.  At this point they begin to start working on the next goal if work
    upfront, or they wait some more for the second goal to get funding
    if funding upfront.

### Cases Fund Upfront

User can wait for funds before delivering or deliver and wait for funds
before continuing

#### Fund requirement met

1.  First goal is fund upfront

2.  Goal fund requirement is met, and owner delivers

#### Fund requirement not met

1.  Fund requirement not met

2.  ?? should campaign be able to wait indefinitely for funds??

    a.  No because campaign might not be relevant in the future, and
        people should not be able to fund it. This can be a vote to
        close campaigns or automatically close them.

3.  Campaign closes if fund never achieved.

#### Fund never met but owner delivers anyways

1.  Owner delivers, voted as pass.

2.  Owner can wait for fund requirement to be met

3.  Or can choose to accept to accept the current fund.

4.  At this point they begin to start working on the next goal if work
    upfront, or they wait some more for the second goal to get funding
    if funding upfront.

## Work fund vs Completion fund Concept

each goal has two funds: work fund and completion fund. The work fund is
how much they require to do the work, the completion fund they get once
the work has been voted as completed.

1.  Maybe there is value in this method only when there is only one goal

    a.  even though this same behaviour can be replicated with two
        goals; the second acting as the completion for the first

    b.  no because then the second goal would have a redundant delivery

2.  Or when a campaign is funded slowly, so that by the time the first
    goal finishes, the second goal is not funded. In this case they will
    not get funding soon as the current goal finishes, and must wait for
    the next goal to achieve funding. What is the issue with that?

    a.  By having a completion fund, this can raise trust with the
        community, because they are not asking for everything upfront.

3.  This is getting very complicated.

    a.  Its much simpler to have the previous goal unlock the next goals
        funding upfront. But then the first goal will never have any
        funding upfront. So the firstgoal will always have to be
        fundless. Maybe they will take out a loan, or do it with sweat
        work.

#### Potential Uses for First goal

1.  Get community approval on your campaign plan. Make the first goal
    your plan approval.

2.  Create community confidence in your ability, by delivering some
    valued without asking for upfront funding. Either through a loan or
    sweat work. Get rewarded for the completion, then unlock your next
    goals funding upfront.

3.  Create a 0 fund requirement goal. Where you sweat work, and users
    can decide to donate for that sweat work. Will provide even more
    confidence in your dedication to the campaign.

Are there any downsides to always having upfront next goal unlock?

1.  If a goal has very large funding requirements, for example to
    manufacture something, people might not have the confidence to fund
    it.

    a.  In this case the owner can break it up into smaller goals.

2.  What if an owner wants to have all their goals work upfront?

<!-- -->

1.  Goal 1 gets funded

2.  Goal 1 deliver

3.  Get goal 1 funding

4.  Goal 2 gets funded

5.  Goal 2 deliver

6.  Get goal 2 funding.

<!-- -->

1.  Goal 1 gets funded

2.  Get goal 1 funding

3.  Goal 1 deliver

4.  Goal 2 gets funded

5.  Get goal 2 funding

6.  Goal 2 deliver

Maybe goal 1 should always be work first by default, and the other goals
will be fund first by default.

Initially the first goal will always be work first (unlock on delivery)
and the others will always be unlock by previous goal completion. Later
more options can be introduced.

Now the question is. If the funding for goal 2+ is not achieved, should
the owner be able to withdraw the best they can get to start work?

An issue could be that while most the community realises the campaign is
a fraud, some will not and fund it, the owner realising it will never
reach full funding, could just take the current funds and run.

# Voting & Participants

Should a vote pass if there are more yes votes than participants?

Or should there be a voting window, and yes votes must outweigh no votes
within that window?

What if, goal has remaining expiry time, in order to get a total vote
count greater or equal than participant count. There is also a minimal
voting time, where participants get a chance to submit their vote and
earn karma and experience (voting points). Maybe this value is 24 hours
by default.

# What Currency

Why not allow the user to choose the currency of their choice. But in
the backend, it can just be based off Eth.

Maybe by default can just have eth to begin with. And role out
conversion features later.

# A case against General Karma

As seen on Reddit, someone can post a nude on a nude sub and get lots of
karma. Someone can make an valid ethical reply on a meme sub and lose
lots of karma. As a result, karma is not so much a rating about how good
of a user you are, but about how good you can work the system. Working a
system is the very thing I would like to try to de-incentivize. As a
result, it might be best to do away with general purpose karma.

# Should comments be on the blockchain

The content of the comment is not relevant to the contract, but the
users interpretation of the content expressed through votes is. So votes
on the comment should be on the blockchain, and maybe a hash of the
comment, or the comment itself.

It would be good to have the comment itself on the blockchain, incase
the service or service database goes down, there will always be a
redundancy for all data that has a fault point (even if its
decentralized). That way the system as a whole can never be compromised
through any fault point.

Although comments would ideally be backed up in a palce that cannot be
compromised, the question then becomes, do they need a ledger? Since a
comment cannot be deleted or the original modified, there is no real
reason to keep a ledger of what was changed since there will not be any
change. The next point is that any contract will not depend on the
comments themselves, and so once gain they do not need to have a ledger,
or be in the blockchain. The ideal solution is to have the comments in a
decentralized location with no single point of fault.

A cloud host for mongodb will still have a single point of fault as the
company that operates the cloud service could choose to shut it down.
The ideal solution for this a decentralized storage solution like an
IPFS.

After some research, it seems all decentralize storage solution keep a
ledger, they are geared towards storing large files and media, which
would be great for pictures and video for the proof of delivery, but for
comments it does not fit.

I will try a linked list approach to saving comments in the contract
itself.

## Comments in Contract workflow

1.  Post on campaign, msg index 0

2.  Reply to post, msg index 1

3.  Parent id set to 0

Or

1.  Post on campaign, msg index 0

2.  Reply to post, msg index 0 on reply mapping of parent

The purpose of this structure is to compose a hierarchy of campaign
comments to post to the client request. It should look something like
this:

1.  Message

    a.  Reply

        i.  Reply

        ii. Reply

2.  Message

3.  Message

So a list of comment objects, each with a child array that has more
comment objects with their own replies recursively. This structure
matches the structure of option two better.

As it turns out, and as I already forgot, nested arrays can not be sent
with soldity yet. So a child array of replies is not an option. A flat
array is the only option., thus parent index.

# Replacing General Karma with Experience and Maturity

Maturity is the concept that the more you used the platform, the more
mature you are in it. This is general like karma, but factors in time.
So that you cant gain too much maturity in a little amount of time, it
is throttled.

Maturity ads weight to to experience generation.

With low maturity, which you might have in the first few days, a comment
you up will generate very little experience for the poster from your up.

Maturity = Time \* Action

Experience = Experience Generation \* visibility

Experience Generation = SUM ( voter maturity \* \...

Further thoughts. Since maturity is really just another general karma
that is throttled over time. Why not try to get rid of it also? And the
only thing that is needed is experience.

So then how do you gain experience when accounts start with 0
experience. You can vote things, wether its upvoting comments or goals,
but since you have 0 experience, your vote will not count for anything,
it will not affect it in any way. But if a comment gets upvotes after
your upvote, or vice versa, you will gain some experience.

The problem with this is that someone can still farm experience with
multiple accounts. Need a solution to that does not allow this.

What about a simple rule. You must positively influence others in order
to have more positive influence. You must contribute to others, in order
to be able to influence direction. You vote through original content
contributions.

Since contributing funds can also be a positive contribution, yet funds
should never result in voting power, this dilemma needs to be debated.

What is the problem with buying influence or voting power. I believe
since funds are transferable. Someone that does not deserve any
influence or voting power, can have funds transferred to them, and as a
result have the influence and voting power transferred to them. This
corrupts the system.

If that is the only issue, then someone that should have influence and
voting power, because of original contributions should be able to earn
more influence and voting power through funding contributions? But then
an argument could be that its the same issue, that the extra voting
power was just trasnfered. So then maybe only original content
contributions should ever result in influence and voting power.

Whatever you earned outside, wether it was transfered to you, or you
earned it by some outside contribution should still not affect the
influence and voting power over the system.

Therefore funding should never result in voting power. It might result
in influence since funding can make a goal possible.

Only original content within the platform/system should ever result in
voting power.

So now back to the origins question. When the system first starts, how
do new accounts gain experience. Since experience is voting power then
you gain it through original content.

Use Case:

1.  New account makes a good suggestion on a campaign

2.  It gets 100 upvotes

3.  The new account now has 100 experience in the subjects of the
    campaign

<!-- -->

1.  A user suggests a new subject on a comment that thinks is suitable.
    (it wasnt tagged with #electronics even though they were talking a
    bit about electronics)

2.  5 other users agree with that suggestion

3.  The user who made the suggestion gets 5 experience in electronics.

<!-- -->

1.  New account make an auto generated comment to try and farm
    experience

2.  Same user creates 1000 bot accounts

3.  1000 bot accounts all like the auto generated comment

4.  The user for now has 1000 exp in the subjects

5.  As time passes on, real users will see that this is an exploit
    attempt and it will begin to get down votes

6.  If 2000 users downvote it, the user will go into negative
    experience.

7.  In conclusion, the original post, plus all the upvotes of the bot
    accounts would have cost the user real ether. They will have lost
    that, as well be placed into negative experience.

8.  Reporting a user for common exploits can also be a feature that gets
    added.

<!-- -->

1.  User posts a purposely bad comment, then gets their other account to
    downvote it knowing that they will earn exp for every downvote
    after.

The only solution I can think of is not to provide experience for
downvoting. The only incentive to downvote is then to socially moderate
the system. Which does follow the rule, that any voting power/experience
is only gained through original content contributions. Moderation is not
an original content contribution. (But maybe any value to the system
should be rewarded, not just original content)

1.  User posts good original content, but then gets their 1000 bot
    accounts to upvote it, giving. The 1000 bot accounts dont get
    anything out of it. The upvotes for the bot accounts will barely
    affect visibility of the original content post since they themselves
    will have 0 experience (since they are new bot accounts). This will
    cost the user to do 1000 upvotes, and provide them with nearly
    nothing.

In this case, we can see why upvoting should not provide any experience
either, since that could also be exploited by multiple accounts. Again
the only thing that should provide experience is good original content.

## Day 0 Genesis Case

1.  First campaign is made

2.  First comment is made on the campaign

If no accounts have any experience at this point then upvoting and
downvoting the first comment will do absolutely nothing, visibility will
not change, and experience will not be earned.

Therefore accounts do need be able to have a bit of influence even with
0 experience. This could either be so little that it is negligible or it
tapers off the more global experience there is. Maybe some parallels to
a mining reward that tapers off.

If a user can affect visibility by 1 even with 0 experience. If a user
has 1 experience in the subject then they can wage an extra 1
experience, if the comment gets more upvotes after the users, they get
back 2 exp. If the comment gets no further upvotes (including getting
downvotes), the user loses their exp and they are back to 0 exp. The
original comment poster will have their experience directly affected by
the visibility of their post.

Since the user can only gain more experience by waging existing
experience, does this break the rule that experience can only be gained
through good original content? Maybe this should be expanded to include
moderation, or as in this case, in supporting another original poster
through investing your exp in their content? Investing with experience
does not violate the ownership transfer rule for experience as mentioned
in the funding dilemma earlier.

This also does not cause the farming problem. Since multiple accounts
would have to have existing experience in order to wage. In which case
all accounts would have had to provide good original content
individually, which the single account could have done multiple times
and earned the same experience to wage from a single account.

# Specific Experience

So how will specific experience work? A post or campaign can touch on
multiple subjects, on some subjects more than others. This has to be
socially identified and moderated.

Each subject will need to have a weight. For example example, a post on
smartphones, can have #smartphone and #electronics as the subject. They
do not need to compete. If they are both voted 100 times, so they each
have a weight of 100, what happens to experience that gets awarded from
that post?

If some was owed 1 experience, do they now earn 1 in #smartphone and 1
in #electronics?

Should there even be weight? Or should it be awarded equally across all
voted subjects?

Maybe for now there is no need for weight, and can be a feature for
later.

1.  User suggests a subject tag

2.  Another user votes on it and it is now added as a tag.

3.  It would now take 3 downvotes in order to remove it (passing 50%
    vote)

4.  And another 4 upvotes to add it again, and so on.

5.  Whenever someone gets awarded experience, whatever tags are added at
    the time are awarded.

# When should the experience be awarded?

Should it be real time? So as comments get voted, or should it be when
the campaign concludes?

If its real time, then we need to keep track of which user was alraedy
awarded what, so that if a comment changes direction, we know to remove
twice the amount already awarded.

If it is when the campaign concludes, then we just go throughall the
comments, and look through the upvotes, and award the accounts.

It gets more complicated when tags get added after comments are already
made. Then we have to go back and award the already awarded accounts
with a new exp tag.

Which shouldnt be to bad, because on the even when the tag is added, we
just go through the list of account in the commment votes, and award
them this new tag exp.

If the vote swings in the other direction, then all the opposing votes
get deducted what we know what would have already been awarded, without
needing to store it.

Should accounts be awarded when its obvious that a comment has already
been approved? There is no real value to the campaign at that point
since we alraedy know its been far approved. So the voter would realy
just be geting a free exp even though they didnt really contribute, they
just bandwagoned.

Maybe a vote will no longer provide exp if it is already passed a 75%
approval.

Question: will people really care to farm experience? It can't be
monetized.

### Question: should accounts gain experience from voting? Problem is farming. A user can vote on endless posts to gain experience from voting.

What if only the first x votes get experience? Then users will just be
looking for new posts to vote on. Regardless of a truthful vote. A
truthful vote, one where experience provides value should be encouraged.

Ideally only original content will provide exp.

The problem is then someone could create endless accounts to farm exp by
liking their own post.

A solution is to not be able to upvote on anything until acquiring exp
in the subject. But then there is the genisis paradox; the first
accounts have no experience to vote and so the system will not progress.

What if you only gain experience if you are early to upvote, and there
are many upvotes after yours. That way farming exp will involving
predicting quality posts and upvoting them early. Which has value to the
campaign and community by moderating the visibility of quality content.

Experience gained = number of same votes after your vote / 1000

### Encourage moderation though rewarding for voting

Can allow users to wage their experience for a change to double up. But
does this actually reflect their experience? Yes because they are
assessing the value of content, which is value to the community.

### What about sponsorship as a paradox solution?

When a user sponsors a new account they gain some general experience,
which they can use to make some initial votes.

# Sponsorship use case

1.  New account sponsors another new account in #electronics

2.  2nd new account now has 10exp in #electronics

3.  2nd account upvotes 10 comments, or upvotes one comment with 10
    votes.

If experience is consumed when upvoting, and experience is gained when
having a comment upvoted, isnt this just transfer of experience, and
thus voting power? No because its not upvoting that transfers
experience, it is visibility; the net value of upvotes:downvotes that
determines the experience gained, this is a community action, and not
just an individual transferring experience from their account to
another.

A user can sponsor a new account with an old account. The problem is
that every new user will just create a second account to get exp, and
they will make accounts each time they want more exp in a new subject.

What if new accounts cant sponsor accounts. The only account that can
sponsor is the first account. And what if thats expanded to the first 10
or 100 accounts. But then what type of experience do they get? They
would have to determine what they are experienced in.

By limiting extra power to the first accounts, a user could claim all
the initial accounts and collapse the system.

### Emergent Rule: An account should not be able to influence the system without experience

All an account can do without experience is post original content, to
try and gain experience.

Genesis Paradox: How do the first accounts gain experience in order to
propagate experience and the system?

There needs to be some initial seed of experience.

### Question: Can experience propagate with a seed of 1 experience.

1.  Two accounts, one makes post, the other has an exp

2.  Exp account votes on post and consumes that 1 exp

3.  Since there were no contending votes when the block gets mined, the
    comment remains in the positive votes, even if its just one.

4.  The exp acounnt now gains 2 exp, and has a total of 2 exp

5.  The posting account now has an exp of 1.

Both the poster and the voter each gained 1 new exp. So from 1 exp,
there were 2 more exp introduced into the system.

### Question: should users be able to vote multiple times on a comment?

Yes because they can do it with multiple accounts, so they should be
able to do it with one account. Why would they want to? To give it
exposure.

## Should accounts lose experience for voting against the masses?

Problem is that the quality of a post is subject, and someone should not
lose exp for having a different opinion, expressing all opinions should
be encouraged. This is debatable.

Use Cases:

1.  Posts a technical review with an error with #electronics tag

2.  At first masses vote in favour, due to group think

3.  Then someone rebuts with correction in #electronics

4.  The rebut post gets upvotes

5.  And the parent post begins to swing in downvotes

6.  The post drops into negative visibility

7.  The users that voted down now gain experience, while those who voted
    up lose exp.

This seems fine since this is more of on objective technical post. A
question that arises is, should the post lose visibility because it is
wrong? Maybe there is value in people seeing the story and discussion?

1.  Posts a general opinion, saying "this sucks" to a car campaign, and
    tags the post #car

2.  A few people upvote, but most downvote and it goes into negative

3.  The upvote users never get back their exp

This seems fine as the user provided no info to backup their opinion.
Even though the campaign might actually suck, its not very usefull, nor
does it prove any experience in #car(s) for the poster. People that
voted up should not be rewarded for supporting that.

1.  User posts a valid point about #electronics but makes a invlaid
    point about #legal

2.  Users upvote in #electronics, but downvote in #legal

This works fine with losing exp for going against masses?

So what is an example where exp should not be lost for going against
masses?

1.  User replies with their idea for a solution

2.  Its nearly a 60:40 split

3.  It is trending towards 70:30

Voting against the trend means greater chance of losing your exp, but if
you are passionate about your opinion, you will risk it. You inherently
wage your experience against your opinion.

Also, you are not really losing exp for voting against the masses, you
are trading an exp for a vote, that is gone no matter what. You are just
not getting exp back as if you voted with the masses.

So it seems that not gaining exp for going against the masses is fine,
especially if votes become free once past a threshold.

### Question: What is the point of upvoting something beyond establishing its ratio between upvotes and downvotes; visibility? 

Global ranking comes to mind, how it ranks in visibility compared to
other content. Is there value in global ranking? Yes when its specific
to a subject. In this case ranking is per subject, and so there is value
in it.

# How is experience seeded?

A seeding mechanism is required for the first experience to propagate.

Requirements:

1.  People can\'t request it indefinitely

2.  Falls off or disables when no longer needed

What if the initial upvotes are the seed. So just for a limited time,
users are able to upvote for free. Then it would be once again easy for
someone to create 1000 accounts to just upvote their post for 1000 exp.

Hypothetically even if only the first 10 accounts get free upvoting, a
user could just create the first 10 accounts.

Even in a mature system, there will still be the issue of seeding. For
example, lets say someone experienced in many topics, wants to vote on a
topic they are knowledgeable in, but have no experience in, how can
they? No this is not correct because in a mature system. A user will
make a post in that new subject, and if there is value, established
users will vote for them.

Maybe the first few upvotes should be free.

If a post is between -10 or 10 visibility, the upvotes are free. This is
no good because then it could create a battle condition of creating
accounts to vote against the masses.

The first 10 votes are free. Now a user can gain up to 10 free
experience. But this does not create a battle condition. Nor can u farm
more than 10 exp with creating accounts, you also risk losing exp for
creating bad content and having the masses greater than 10 votes
downvote you.

What if users like or dislike new comments at random just to farm exp?
How can we encourage quality control. If a user votes a specific tag
they want exp in. it will cost them 1 exp, so they will be -1 in that
topic, and if the vote is not supported (gets x more votes) then they
will never see a return.

So then maybe there should always be a cost to voting, and u just go
into the negative, but only the first few votes of a comment are allowed
to be debt votes, where you can vote into the negative. After that you
must give exp to vote. So if you spam vote a specific topic that no one
supports, or vote a comment that no one will support, you can not farm
it that way.

### Version 2.0

1.  You can vote an existing tag, or vote a new one

2.  Voting costs 1exp

3.  The first x votes of a comment can allow exp debt ( u can go into
    negative exp)

4.  If the comment passes a threshold then all previous votes double up
    and all future votes gain no exp, but voting becomes free.

### Version 3.0

1.  You can vote an existing tag, or vote a new one

2.  Voting costs 1exp

3.  The first x votes of a comment can allow exp debt ( u can go into
    negative exp)

4.  If the comment passes a threshold then all previous **majority**
    votes double up and all future votes gain no exp, but voting becomes
    free.

Another problem arises, that someone can make x accounts in order to get
the vote in one direction early on, so then a single account should be
able to vote x times on the same comment early on. since a single user
can push a comment vote past its threshold, this could be a problem
early on, when other non exp users cant correct the vote if voted
incorrectly. Later on this will not be an issue since users with exp can
wage their exp against a wrong vote, and the user will lose exp in their
single account or multiple accounts.

A solution to this, instead of allowing debt votes within a threshold,
users can select to audit certain topics. They will be given an item
(comment, campaign, etc) within that subject that has not been
established yet, and they are allowed to wage their exp, including -10
into debt towards or against an item.

Users can use this audit system initially to gain exp. The audit system
can be rolled out later since the threshold option in Version 3.0 should
suffice for now.

### Version 4.0

1.  You can vote an existing tag, or vote a new one

2.  Voting costs 1exp

3.  If the comment passes a threshold then all previous **majority**
    votes double up and all future votes gain no exp, but voting becomes
    free.

4.  You can borrow exp in a subject when you try to audit content in the
    subject, if you are successful, you can double up.

# Should experience (voting power) be consumable?

Yes. When you wage with it, it is consumed and when you vote a goal with
it is consumed. That way your interaction with the system is limited by
the experience you have gained thus far. You cannot use the same
experience on multiple voting items or upvotes.

But, you can earn experience back or more than the original investment
by investing in a successful original post or campaign.

# Timed voting vs passive voting

24 hours to vote vs reaching a participant mark. Each type of voting
system will suite a different purpose. A participant vote will be open,
people can see it grow in real time, and what people are voting for. A
timed vote is closed, people can not see the voting results until the
vote is done. The idea is to use a timed vote when group think might
influence the outcome in a way that compromises the campaign.

# Should Posting comment auto vote your comment in the tag? 

If it does, it will auto cost you one exp? It will also require you to
put in a tag when u post a comment. Maybe if you leave it blank you
don\'t put in any tag? And thus don\'t commit any exp.

Or should u get one free vote when posting your own comment?

Jan 14th 2020

# Gun.js

I am assessing wether gunjs would be a good alternative to my node
backend solution. It looks very impressive and promising so far.

I now need to determine a workflow for propagating data to and from
smart contract and frontend.

There are two apparent options. A Parallel; send data from frontend to
gun and to blockchain in parallel. B Serial; send data to blockchain
which then passes it to gun with an event.

A user goes to the OF web app, they need to authenticate. Using
metamask, they login. As usual metamask has the blockchain credentials,
but somehow the gun credentials should be created also.

Having to login in twice should not be an option.

With option b, the front end would listen for the event, and then would
relay any data to gun. This might be favourable incase there is a
revert, option A would not know of the revert and continue to post the
data to gun.

If option A could handle reverts it would be ideal, since it would be a
faster parallel process vs a serial process.

This could be done by listening for specific revert events, and
modifying the according data in gun.

The question is then, what is the point of seeing your data posted on
the frontend, if seconds or minutes later, it might get reverted? Maybe
it is best to go with a serial process, that guarantees data.

The other downside to a serial process is that most of the data, the
blockchain never needs to know, e.g. comment string. There is no reason
to pass it to the blockchain.

What about cases where this metadata needs to be hashed? For example,
since experience should be immutable, and is based on comment strings,
then comment strings should be hashed since it can verify the mutable
string data on gun.

The question then is where should the data be hashed? Should it be on
the frontend or in the blockchain? If the frontend creates the hash,
then a user could create a hash not matching the data, could this be
exploited?

## Exclusively Gunjs

Some users on the gunjs gitter chatroom are suggesting to use gunjs
entirely for a dapp + btc lighting where its needed, for a dapp that
needs exchange of value. Although this seems promising as a concept in
the future, it has no field testing, and the infrastructure for such a
system is not in place. Although this does feel like the right option.

Lets consider how this would work?

A user creates an account with gun, alias + secret.

To create a campaign, they would make the js campaign object, add it to
the user list of campaign drafts.

To publish a campaign, it would then get moved to the list of global
campaigns.

To contribute to a campaign is where it gets tricky. Maybe here is where
smart contracts only come in.

The first time a contribution is made, a smart contract is created. The
problem with this is that the first person contributing will have to
front the cost of gas for creating the contract, which is not ideal, and
should be the owners or initiators responsibility as an investment.

So maybe instead when the campaign is published, it can also be created
on the blockchain, thus being the owners investment.

Contibutions would then be made as normal to the blockchain, and an
event on the users frontend would sync gun with the blockchain. What if
the browser is closed when the event is recieved? Then the option could
be to have some users periodically poll the blockchain. Or it could que
up a check for a specific request, knowing that specific request was
sent to the blockchain. Then the user that sent it or another user that
picks up the que will check with throttle, until it is posted.

What does transfer of value really need to know? For the funds to go
from contract to owner, what needs to be verified? I think just votes
passing.

1.  User authenticates on gunjs and metamask (somehow?)

2.  Creates a draft campaign, this will be only on gunjs

3.  Publishes draft campaign, this will be created on the blockchain

    a.  Request sent as regular from front end

    b.  Request is added to a que

        i.  Item in que is picked up by the client that made the request
            or another that sees the que and marked as checking,

        ii. if there is no update, then item is marked as checked

        iii. After some delay, it is picked up by the first client again

What if somehow the gun network is needs to be reset, can it update from
the blockchain? If that happens it will be nearly as devastating as the
blockchain resetting. As all the meaningful data will have been lost. In
the case of the blockchain resetting, potential funds be lost.

What about during development, when gun needs to catch up to the
blockchain, would it ever need to? Yes, if a script inits the
blockchain, then a gun init script can exist also to synch it, in which
case it shouldn\'t need to. Therefore there should not need to be a mass
sync or mass check for gun against blockchain, those will be granular
and organic in function.

Authentication

Initially, have the user auth from both gun and metamask, then
eventually find a way to streamline the auth process.

Todo 1/16/2020

I now have to take the existing react app, and replace the node api
calls, with gun api calls. The first time is to make the draft campaign
process fully on p2p web with gun. Later we can support multiple draft
campaigns, but for now, just one will do, as is currently in the
existing prototype.

1.  Create login/register page

2.  Store gun user globally somewhere

3.  

## Gunjs and Redux

Should an app using gunjs need to use Redux? Or should it just use local
component state since gunjs will sync everything. If multiple components
can have access to the same state through gunjs, then there is no need
for redux for anything come from gunjs. The only beneift to Redux might
be what it does beyond just global state management. Such as any global
modifications to the data coming in that are needed locally only. What
are some cases of this? Unknown at this time.

To begin with i will start by not using redux.

Jan 31 2020

## Goal Voting Updated

In order to vote for a delivered goal, a user must also wage their
experience.

A user delivers a goal for a smart phone 3d render draft. There are no
default vote yes, or no to accepting the goal delivery. A user must now
decide what do they think this delivery passes for them. So they might
choose to upvote a #smartphone render tag. In order for that tag to be a
valid voting tag, so that it affects the progression of the campaign and
smart contract, the tag needs to pass its threshold. During this time
other users need to wage their #smartphone render experience.

The goal will have time window of when all the votes must be made.
Within that time window, other users could also vote for #smartphone
design and #smartphone. These are more broad but still applicable. So
there will be a much broader assessment for the smart phone goal. Other
users could vote even more specialized such as #OLED screen and
#ergonomics, and these might get less votes, but from very specialized
experience, which is also valuable.

As long as these tags pass a threshold, the votes must be in the
positive for the goal to pass.

A confused or bad actor user could also vote for #anime on the goal.
Since this tag has no relevance to the goal or the campaign, it will get
no further votes. The bad tag will not pass the threshold and it will be
disregarded. The tag will not even be displayed on the goal if it does
not pass the threshold.

Therefore all tags must be manually entered by voting users before they
pass the tags threshold and before they are displayed as required votes
for the goal.

## Content vote not shown until it passes threshold

The idea is not to show votes until the threshold is passed. This will
not allow users then to ride the wave and catch the last few votes in on
a tag before it passes the thresholdw , but instead it will allow for
genuine experience voting, and incentivize catching content early before
it passes a threshold.

## Negative Votes

Since users vote on experience tag, the only objective is to gain
experience, not social standing. But what about someone that says
something incorrect, should they not lose experience rating. Yes they
should. The key is experience rating, not experience, this will always
be fluctuating and the community needs a way to lower it.

# Non BlockChain Rethink

Feb 06 2020

Since I have now successfully integrated gunjs, a distributed compute
and data service into the AWopen world client, there is no longer a need
to place anything but funding related data onto the blockchain. I will
have to rethink every component of the service.

Goals will continue to have to be on the blockchain since they hold the
funds for each goal, but the title and description can just be hashed on
the blockchain and live only in the p2p network.

Campaign will be similar, since the logic for handling funds needs to be
on the blockchain, but title and description can be on p2p.

It will be quite easy to create discussion forums now using the
experience system that will be purely p2p. It might be good to first
launch that as the prototype. Experience and voting on comments can live
fully on p2p.

Draft campaigns and goals could also be p2p. And the idea that they
could be published on p2p, and only when funding comes into play then it
could get delivered on the blockchain. Maybe a project must gain a
certain amount of subscribers, at that point, the user can then publish
it on the block chain. The value in this is that they get to test out
their design, easily make changes from community feedback, before they
spend any funds on the blockchain.

It will be a good exercise to get familiar with p2p dev by focusing on
the discussion forum which will be a lighter weight application.

## Initial Tagging

Posts need initial tagging by the OP in order to be filtered, sorted,
categorized. This also means that there is no threshold for any initial
tags; a bad actor could abuse this by posting mismatching content to
tags.

Maybe new posts could be in a new post section, where users looking to
gain experience can browse. Here users can borrow 1 exp per vote.

## Proofing

New users can proof their experience, by proof voting active votes. A
proof vote does not count as a vote towards the content. If the proof
voter matches majority threshold vote, than they gain one experience, if
it they do not match majority vote at threshold, than they lose an
experience.

This still faces the 0day issue; on day 0, there will be no one with
experience in order to actually vote something passed a threshold.

## 0 Day issue revisited

## On day 0, there will be no one with experience in order to actually vote something passed a threshold. Auditing somewhat solves this, but the idea of having to wait and not be able to audit on demand does not sit right with me.

Though if users can audit on demand (essentially proofing with valid
votes) then a user can create indefinite new accounts to get as many
votes and experience as they like. The idea is to only allow random
people the ability to debt vote, which is essentially auditing, minus
notifications.

The other option is to delay or require some work from the new user
before they can vote. By adding a delay, a bad actor cant create
unlimited accounts to counter a communities vote, and it would pass a
threshold before they do.

What work could they do to gain experience, that would value the
community; posting valuable content, but then on 0 day there is no one
to vote. A time delay is the only real measure.

### 0 user and sponsorship

0 user on 0 day gets x amount of exp any tag. With this they can vote,
but more importantly they can sponsor new users. Sponsoring a new user
gives them x amount of exp from the sponsoring user. The new user must
have 0 exp in the tag they are being sponsored in. If the new user
double the sponsored exp, than the sponsoring user gains back double
what they sponsored with. This way you can invest in the value of new
users. On the other hand, if the new user goes into negative experience,
all the sponsored users will also lose experience of the same amount.

If a user gets banned the sponsoring user will get a sponsored user
banned tag on their account.

This essentially allows intelligence to seed the initial experience in
the world. After which it should be able to pass a threshold.

Problems with this include, the world now relies on the 0 user for all
experience seed. A tag that has never been used before a year after 0
day, might finally make sense, but no one has the expereince to vote it,
and the 0day user might not be around any longer. **This problem is a
deal breaker for the 0 user solution.** Although sponsorship could still
be a valid later feature.

## Exploiting the Audit

A bad actor could create n accounts and sign up for proof of experience
on #subject. Over the next week many of those accounts will get
different invites. The bad actor will still have to go there and assess
each post, and vote in the right direction in order to get a return on
the borrowed exp for the vote. These votes still require intelligence
and add value to the community. Even if the bad actor installs AI to do
the assessments, it's still intelligence that is valuable to the
community.

Could this exploit counter not then be used beyond auditing to not
require auditing? No because by being able to vote with experience debt
at any time, you can stack all bit account votes to make it pass the
threshold, therefore hijacking the vote. By auditing, it is at a random
time to a random account and that is not possible. The main point
though, I just realised, is that they are given a random post to proof,
and so stacking becomes nearly impossible at that point. The exploit
counter is that they are being given a proof post, they do not get to
select one. And this is why Auditing as far as i see it now, is
required.

Another main point I realised, is that by not picking which post to
proof, the bad actor cant pick their own post. Although they might get
some of their bots that get to proof their post, majority will not.

A complicated exploit attempt though can be performed. Where a bad actor
keeps making posts, in hopes that their bot account swill get some
proofs on it. But the community at that point well have negated their
experience in the fake post. So this is not possible.

## When can a user audit/proof?

At any time, as long as they have less than 1 experience in the tag they
are selecting to audit, they are able to wave 1 exp in debt.

## Should it be called auditing?

Auditing makes it sound like someone with experience is looking into
someone else. This is not the case and is not a good match for what is
actually occuring. The user is proving their experience, proof of
experience. So then what are our options?

1.  Proovers

2.  Proof auditors

## Downvoting for wrong tag

If the OP or other user vote a tag that does not make sense, should or
will other users down vote it? If the op posts the wrong tag, its a
mistake but does not necessarily mean they are lacking experience in
that subject. This could easily be a way for bad actors to exploit users
by purposely voting a wrong tag on their account.

If the consensus is not to down vote for mismatched tags, then users
will not use experience points downvoting knowing that their exp will be
lost by the vote most likely not passing the threshold.

So what is the correct action when you see a post that has nothing to do
with electronics showing up in an electronics tag search. Maybe there
can be a tag miss-match vote. When this mismatch vote passes a
threshold, then the tag will get removed.

## Should unvoted tag not be sortable/searchable?

If it is not, then all posts by default will just be in a general area.
That simply wont work. There for as soon as a post gets a tag vote, it
will be sortable by that tag, but the post should indicate its still in
voting progress.

## Appeals with reason (maybe?)

When a vote passes, anyone can appeal it, including the OP. For example
if they lose a good deal of experience over a mistake. They can appeal
it and apologize, explain what they learned from the mistake, in hopes
they can revert the action. Though an appeal can be done naturally by
just replying to the downvoted post, with what you learned, why you were
wrong, etc, in hopes people will upvote so that you may recover some of
the lost experience.Therefore the only real reason for an appeal would
be for account affecting votes, such as bans.

## Rule of No Multiple Account Bonus

Anything a user can do over to influence the system over multiple
accounts they should be able to do with one account, since that would be
an exploitation . Though in the case of having multiple accounts for
separate identities, it is fine, since it does not give any extra
influence capability.

Therefore, any time throttling, or limit counts, that can be bypassed
with other accounts by the same user, will be useless.

## Everything should be an investment, everything should cost something

If it does not, interaction with the system can be thoughtless. Someone
could spam a tag indefinitely, and even though it would not make it into
a positive threshold to be listed, it would still create a bottleneck in
the proof auditors. Worse yet, it would give proof auditors free exp
since it will be a consistent form of downvoting. The idea is that a
post costs experience in the tags it is being posted with. Posting can
always borrow experience, but you can only borrow one experience point.
Therefore a user can only make one post as a new user of a tag, if that
post fails, they will have -1 experience and will not be able to post
again until they raise it to greater than -1 through proof auditing.

Allowing only 1 borrowed experience points incentivises well thought out
posts, going for your first best, versus being able to post many posts,
and hoping one of those pays off.

## Values Should always be a function/derivitives

Values for rules should always be of a function, or until a function is
discovered, it will be community voted. The function of course is
community voted function. Though i feel a function could also be an
emergent one, or a derivative as possibilities.

Example. Why should a user be able to borrow more than 1 experience
point? Since the value 2 or 3 can not be derived from any existing
function, it should remain one.

## Default Original Poster Tags and Suggested Tags

When a post is first made, a user must have provided at least one tag.
These do not need to pass a threshold since they are not suggestions. If
a user does not agree with the tag they can ignore it, or if they really
disagree with it they may down vote it.

A suggested tag by a user will need to pass a threshold until it is
displayed in a main area.

## Miss Match Tag Vote

Maybe a 3rd option should be provide, up down and mismatch as previously
suggested.

If an post attempts value in a tag, then it\'s suggested to up or down
vote. But if there is clear mismatch between the post topics and the
tag, a user has the option to upovte the mismatch

#### February 16 2020

I need to determine what tag will be valid for voting on a goal. I will
spend the next few days brainstorming this and designing it.

## Voting Goals and Tag Proposals

When a goal is delivered, users can begin up voting whatever Tags that
they think need improvement or it passes in. If one tag has many votes,
but another has many down votes, then the goal probably shouldn\'t pass.
A goal should have all passed tags as positive. Is that it? As long as
it passes the tag threshold and it is positive, the goal will pass? No
matter what the tag is?

Let\'s run some use cases:

Phone Render Delivered. OP had previously suggested #phone design #3d
rendering.

What if tags voted in before a goal is delivered will be merely used to
judge the goal on. Then once the goal is delivered, the tags that were
voted in must stay in the positive. Essentially creating two phases to
voting. Pre Delivery tag votes to lock in vote criteria, and post
delivery vote to have the goal pass or not.

A goal must have all accepted tags in the positive to pass.

## Goal Vote Deadline

When a goal is delivered, it should have a window of time in which votes
can be made. This is to provide equal opportunity for the global
community to make a vote, considering time zones. Therefore 1 full day
should allow this, and by default all vote deadlines after delivery will
be 24 hours.

## Post Voting After Threshold

Maybe votes after the threshold can still cost experience, but the voter
does not earn anything. It is similar to donating experience to show
appreciation for really great content.

## Donating to OP for Content

Any content tag can accept donations. These donations go to the OP after
a holding period. Donating to a tag reinforces the specific value
provided, to show why it was donated.

## Voting where not tag fits

How do we handle situations where no tags apparently fit?

Use Case:

1.  User posts a theory, but fails to explain 1 of his concepts that he
    refers to as "blurb" that is needed to understand the entire theory.

    a.  A user replies "What is blurb?"

    b.  This reply is valuable because it points out a missing required
        piece of information

    c.  But what tag can this value be categorized as

    d.  Maybe \#

Feb 18 2020

## Bounties, the Precursor to Campaigns and Goals

Since I have decided to launch with simply forums, since all the
features of forums will be in campaigns/goals but not all the features
of campaigns/goals are in forums. The same logic applies to the concept
of bounty.

A bounty is like a goal that is without a campaign. It can be attached
to any post. By default the bounty will go to the delivery that has the
most votes in the accepted tags.

Custom behaviour can be attached to bounties by the OP providing a
custom contract, or having it voted in. This will set the stage for
campaigns and goals, or they will naturally emerge.

Feb 18 2020

### Personal Thoughts

I lately feel as if i am dancing on the edge of insanity, consciously
careless, but subconsciously terrified, having this fear oozing out in
my day to day reality. The more I design, the more I believe, but the
less I can communicate. The further I go down this rabbit hole, the more
of a challenge loneliness feels. I remind myself that I need to observe
these emotions and thoughts and not identify, not identify with my
belief, the persuit or the imagined better tomorrow.

## Should Experience be on the Blockchain?

Experience will be how value to the community is measured, and also how
much influence over the community one has. The value of experience is
not measurable or interchangeable with monetary value, which is the
resource to make items actionable.

Concepts are created and voted through experience, concepts are actioned
into items through tokens (monetary value). Both have value. The
question is then why do only tokens have the security of the blockchain?

A p2p network/graph does not require a 51% consensus, it could be just a
few confirmations to pass, which could be less than 1%, this has its
advantages and disadvantages. Because these confirmations will be sent
out at random, it is impossible to hijack the system. Since it is just a
few it is fast, since it does not require proof of work it is much more
efficient. What is then the advantage of using blockchain?

It is the difficulty of mining gold that gives gold its token value
ability, versus the material actually having historical utility.

The value is in the rarity of being rewarded through proof of work,
therefore it is not just a store of value, but the actual value. For
this reason alone, monetary value tokens must be stored in the
blockchain. In a sense, experience is roughly the same concept of token,
but without monetary value, therefore it does not need the blockchain,
and thus it can benefit from the many advantages of being in a p2p
network vs a blockchain network.

## P2P Voting

Since there is no backend, authority must be on the client. So when a
vote is cast. The other clients receive the vote, and check if the user
casting the vote has the experience needed.

If am trying to do upvotes/likes on my posts in my forum gun app. What
would be the best way to go about this? have other clients listen for
the upvote event, then check if the client who submitted the upvote has
the requirements to actually upvote, then have the listening/checking
client mark the post as upvoted on their side, hoping that all other
clients do the same? But what about bad actors who alter the result to
throw off the network? since each client is also checking every other
client, how is a consensus achieved?

The idea is to have a database that no one can write to, which is only
written two when a vote comes in. So the only effect anyone can have on
this database, is to vote, up or down.

#### Replies from gunjs from mark

\@AlexZan bullet-catcher is for people who want to learn how to write
lowest level wire adapters, they work for any gun peer. They can only
really be used for \"universal\" logic, not app-specific logic or
data-specific logic.

\@AlexZan consensus is thru determinism (see
<https://gun.eco/distributed/matters.html> ), but what you\'re asking
about (validation) should be handled through schema - all users loading
your app are gonna load that schema, so even if 1 alters it, it doesn\'t
matter, all others enforce it. This is also how SEA works, but at a wire
level, rather than app level or read level.

Yeah upvotes/likes I\'d say check out \@go1dfish \'s work, he\'s got
lots of fancy tricks/cheats that are very advanced.

### Use Case

1.  User votes on post

2.  Vote call is a custom CRDT that checks for required experience

    a.  If required experience, increase vote

    b.  If not required experience, return

For now I should just implement the check on the voter client only,
since that will also be required as a primary measure before receiving
client checks.

## Posting non Original Content

If a user posts a very informative electronics video or video link, but
it is not their creation. Should they get experience for #electronics?
No, but should the post be categorized as #electronics? Yes. And such is
the dilemma.

I think a user should be explicit if they are posting original content
or not, and if they are not, they must reference the original poster if
possible. In this case, any votes made on the post will be used just to
categorize the content. And to incentivize fair promotion of content,
the poster, who is the promoter in this case, will get double the votes
they invested into the post when posting it.

If it is proven that the poster lied about it being original content.
Then a user can report them for this action. If the vote passes then all
of the positive experience they earned will automatically turn into
negative experience. As usual they can post an appeal, and attempt to
recover some experience.

## Backup Hierarchical authority

In the case of a failure of vote or emergency (maybe) an individual can
be empowered to be a representative for the selected category. They will
be automatically selected based on the voted in criteria of experience
types needed, such as; leadership, empathy, etc, whatever qualities are
voted in as important.

When voting can resume, they will no longer have authority.

## Voting Threshold and Experience Assignment

How will the voting threshold function, and how will experience get
handed out? What determines the threshold?

If its just a static number, like 10. Then until a user base that is
able to acquire a combined experience of 10, and is interested in voting
on the vote, no votes in that subject will be able to pass.

If its dynamic, then it might be 2 votes, which also is a problem
because then it could easily pass without a true consensus. The other
argument is that if there are only two users, then that is the
consensus.

Some use cases to explore this:

#### With just two users and no minimal:

User posts artwork. Second user likes it and votes it, vote passes.

User asks a question "

#### With just two users and a 10 minimal

User posts artwork. Second user likes it, but still needs 8 more users
to pass. So they wait, or they try to promote it.

What if the threshold is purely time based. So each new post has a 24
hour treshold, to give the globe equal time to vote.

But what if a post gets no votes in a day or no exposure, yet has value.
since it is passed the threshold it will not incentivise voting. day
threshold voting does not work well alone in this case.

WHAT IF\... threshold is unlocked through op providing more exp. no
because this would break the rule of power equilebrium and give one
person potentially more power over the outcome of a vote.

are there different thresholds for different tags? each tag could have
its own threshold, or a post could have a post level threshold. Need to
explore both possibilities, though the feeling is with each tag having a
threshold.

what if threshold is based off imppresions or views, but not votes. This
seems ideal because it gives equal opportunity to all posts for exposure

what if threshold is based off the difference in votes, and the
difference must pass the threshold. so if a vote has 100 negative, and
100 positive, its still deadlocked

what about the concept of taking lift. a vote must take lift within a
full day. if itdoes not not, it stays grounded.

What if votes can be redone at any time, by anyone? so if an old post is
relevant again, or something changes about its circumstance, it can get
reassessed.

though the reasssement should be expressed in a reply, and then maybe it
should be the reply that gets voted?

for example what if someone posts a lie that everyone believes, votes
pass. the lie is discovered, and so a reassement should be done.

This could be automatic, just the the difference between the current up
and down votes changing, when it goes below the treshold again, it
behaves the same as if it never passed the threshold the first time,
until the difference clears.

so then the treshold should be minimal 24 hours for equal exposure
opportunity and outside the threshold vote difference.

so then the question is, what is the difference required between votes
to pass threshold?

If there are 100 people voting in one day, then a 49/51 vote is not very
decisive. In Fact this type of vote should never pass, as there would be
a great deal of unhappy people. The ideal vote is 100 to 0. This maybe
the goal is to have the threshold approach that.

Though there are different votes. The above paragraph might be true for
anything requiring some sort of approval, such as a goal delivery, or
maybe an assessment.

Therefore we need to create different use cases for every type of vote.

Vote Types:

1.  Goal deliver

    a.  3d render of phone design

    b.  Features of phone

    c.  Electronic blueprint

    d.  Prototype of phone

2.  Local issues

    a.  Idea as to why a road is always backed up

    b.  Solution to solve road backups

3.  Providing evidence

    a.  Irrefutable photo evidence proving guilt

    b.  Logical proof proving guilt

4.  Posting artwork

I will begin with just forum posts since the algorithm only needs to
support those for now.

A user posts about a local constant traffic problem with the tag
#traffic problem and #traffic. Both tags start getting upvotes. This
post is valuable because this user is identifying a traffic problem.
Several users reply with ideas for causes of the traffic problem with
tags #traffic #traffic problem and #traffic causes.

An aside, since no one had any #traffic causes experience, it will not
get much votes. Two posts start getting more votes, but they are
competing theories.

Then another reply to one of the traffic causes providing actual
evidence with a diagram that proves this is the cause. It gets many
#traffic votes and many #logical votes, some #diagram votes.

Someone also votes #cars and #policy on some of the posts. Even though
they are somewhat related to the subject of the post, they are not
directly related or anything to judge any of the posts by. Another way
to think of it, none of those posts are providing value to the community
in either #cars or #policy. But the tags are not that far off that
anyone might report it as miscatagorized, such as #clown. And so if the
vote can pass only by 1, then the only vote in received from the
original voter will be enough to pass after 24 hours if no one
downvotes. But no one will downvote since they are not trying to
indicate that the poster compromised any value within #policy or #cars.
So it will pass, but the user did not provide any value in those
categories.

What if all votes first have a tag approval time, so the first vote is
if the tag should even be votable? For some things this feels almost
redundant.

If instead there is a minimum count threshold as well as a difference,
then lets say a vote must get 10 votes minimal for the threshold to
pass, and so #cars and #policy would not pass, and if it did then it
would be worth it. This seems to work but what is this 10 value? And
would it be dynamic based on some factor?

If its one, its too small and anyone can make it pass, if its two votes,
then one person could still make it pass, even if it was 10, one person
could make it pass if they had 10 experience and were willing to use it.
We cant limit the amount of votes one account can use because then u
create power with having experience across multiple accounts.

The question is now what factors the min count? Or the other option is
to have an approval vote first, but that delays all votes by 24 hours,
and might be very redundant for some tags. I feel as if the min count is
the right solution.

What if the last vote does not get experience. So if you are voting, you
need to have confidence that there will be other votes. If you are
trying to farm votes by voting like votes, then you might not see your
investment back. If you vote 10 though, you will still be able to double
up on 9, making 18, but only lose 1. So that is not a good solution.

### Two Day Solution

What if the min count is double the acquired votes in 24 hours? If a
user votes 10 votes, now they must wait for a total of 24. The vote will
stay open indefinitely until it passes that threshold and stays passed
for 24 hours.

Lets test this out:

Continuing with the above example, the user votes #cars and #policy with
1 vote each. 24 pass and no one else has voted, now another 24 hours
pass, and since no one has voted it does not pass. In this case since
there is a risk to voting any tag, more risk the further it is away from
the core topic, then users can no longer farm with this means, and if it
passes because a few people voted it in, then that is also fine, because
if it is a complete tangent of a topic, then users will report it as a
mismatch and any voted exp is lost.

Lets continue with the traffic example. As a result of the votes, the
cause is voted in. Users area already posting solutions with #traffic
solution #traffic, #problem solving and #solution. Several solutions get
voted in. Two possibilities A) there is a clear winner, or B) 2 or 3
solutions have similar vote counts but with one slightly more.

In B's case, people might want to debate the solutions further until
there is a clear winner since there is no vote deadline. At which point
B will have the same resulting path as A.

In A's case, a bounty will be created as a reply to the solution post.
Users can start donating to the bounty.

#### lightweight car battery use case

A user creates a post about creating a lightweight car battery, they
propose lithium ion battery tech. Users upvote with #car battery
#battery #car #electronics #lithium ion battery. Another user replies
with a suggestion to use super capacitors for extra benefits, they also
get upvoted for the above tags plus #supercapacitor. Users then start
posting designs with diagrams and schematics. An open source design
conversation chain begins. After several weeks of back and forth, there
are no more proposed improvements, and the final design has the most
upvotes in various tags. During this process users also donated to
various users that contributed with posts, these amounts being displayed
next to the post.

##### Painting use case

A user posts their new oil painting with tag #painting #art #oil
painting #abstract. A user gets triggered for some reason by the
painting and upvotes #hate, #ugly. If no one else agrees with that vote,
it never passes threshold and the user looses the experience they waged
in #hate and #ugly. The other votes pass their threshold and the exp is
awarded for all. #painting gets 1000 upvotes, 4 downvotes. #art gets
3000 upvotes and 10 downvotes, etc.

#### Joke use case

A user posts a controversial joke that might be in bad taste for a
select few with the tags #joke #funny. The joke gets many upvotes and
many downvotes in both tags. #joke gets 4000 votes, 1000 downvotes, and
#funny gets 1000 upvotes, and 980 downvotes, in the first 24 hours. Then
in the next 24 hours #joke gets 9000 votes and 1020 downvotes and passes
threshold. It stays passed for 24 hours and exp is awarded. #funny gets
2000 upvotes and 1998 upvotes and also passes threshold, then 5 minutes
later gets 2002 downvotes, its back and forth like this between positive
and negative for more than 24 hours, then a week. Finally it settles and
is deemed funny just by 10 votes out of 10,0000 to 9,990. This hardley
seems fair that the upvoters should get full experience, and downvoters
should lose their experience. Maybe the ratio between up and down should
dictate the awards. Also in this case the user will only get 10 points
in #funny, which is fair since it was a controversial joke. Another user
votes #tooSoonJoke and it gets equal votes from people that didnt think
it was funny and from people that thought it was funny, they found a
middle ground.

Now there needs to be an algorithm that determines exp reward based on
up:down ratio, but first we need to see if it is valid in all cases.

## Exp factors up down ratio

If a vote does not pass by much, then not much exp should be awarded. If
a vote passes with 2 ups and 1 down, how much exp should be awarded?
What about 9001 to 9000? In both cases the difference is 1. Maybe the
difference is what should be awarded, plainly. So the poster gets 1
experience, and the votes get 1 exp distributed amongst them. So in the
first example the up voters gets 1/2 or 0.5, the downvoters should also
not lose the entire experience they waged. So maybe they only lose 0.5
also instead of 1, therefore they are actually getting back 0.5?.

Lets try the 9000 case. Thats 0.0001 exp to each up voter, and \~0.0001
lost by each voter. Thats not much. What are the implications?

Lets try 100up to 50 down. The difference is 50 in this case. So the
poster gets 50 exp. The 100 up voters get 50 exp divided amongst them,
so 0.5 exp each. While the 50 downvoters lose 50 downvotes devided
against them, so 1 vote each.

500 up to 100 down, the difference is 400. Poster gets 400, the 500 up
voters get 400/500 = .8 each. The downvoters get 400 exp devided against
100, so 400/100 or 4. So they lose 4 exp? Is this fair? They only waged
1, but lose 4? No you should only lose what you wage, MAX.

What about 10 up, 8 down. The difference is 2. The 10 upvoters get 2 exp
divided among 10, or .2. The 5 down voters lose 2 exp between them, so
0.4 each.

Seems to work pretty good.

### What if most of the people vote in the first 24 hours and there is no one left to vote after to pass the threshold?

Then the vote will not pass in 48 hours, and must wait for new
experience to be generated by the community in order to pass it. Is this
the desirable effect? This will incentivise holding off your vote if you
care about the tag passing the threshold more than getting the exp of
the vote passing. Which is not really exploitable, this should work for
now. I dont fully understand all the consequences of this behaviour yet.

### What happens when a vote goes back into threshold? 

The exp awarded should be subtracted. And if it passes the threshold
again for 24 hours, positive or negative experience will be awarded.

Maybe then the idea is that the treshold can pass even by 1 vote, as
long as it stays passed for 24 hours.

## What about hateful tags?

If someone posts something that is distasteful to the masses.what would
be the consequences of being voted in #distasteful, #stupid, etc. Would
there ever be any value to having experience in negative things? No goal
would ever pass through a negative tag?

### Are there any tags that can be used for categorization that are not positive community contributions?

As an extreme example, a user could make a post analysing the holocoust.
With tags #holocoust and #analysis. Even though holocoust can be a
negative subject, the analysis of it can be positive. If someone tags a
post with #stupid, there is by no means any positive community
contribution indicated through stupid, and the analysis or philosophy of
stupid is still derogetory. But how will someone even get #stupid
expereince, that is an oxymoron in itself. One could request to audit
#stupid tags, and maybe someone will make a stupid post, so it should be
allowed. I just realised someone might want to post about comedy that is
#stupid, a very dumb down comedy, like dumb and dumber, in this case it
might make sense. As can be seen, there is no hard and fast rule with
categorizing contributions.

## General Trust Algorithm

Can there be a way for users to somehow gain trust so that they can
borrow experience on demand without the audit process? For example if a
user has been active for a total of 1000 hours, and has a combined
experience greater than 100, then they can borrow 1 exp on demand

## Could limiting debt upvotes be a way to replace auditing?

What if a post can only have 50% debt upvotes. Meaning a brand new user
can go straight to a post, and upvote it, getting -1 exp in that tag
without having to audit? But then on 0 day, where do the other non debt
votes come from, therefore auditing is required. And debt limiting could
be used to augment auditing before community experience is developed.
This could be a great way for a new user to begin voting in communities
that area already developed.

## Investment in individuals

In order to complete a bounty an individual might need capital to do so.
Investors can front these individuals capital for a return if they
achieve the bounty. The terms of the agreement can be standard or custom
and agreed up front.

## Funding vs Voting Dilemma

What if there is a street that some users think is too slow, but most
users think is too fast, but the users who think its too slow create a
bounty to change it to their desire, and they all fund it. In this case
it will still go to a townhall vote I assume and only the individuals
who it impacts get to vote on it. But what about in parts of the world
where it does not work with local votes. Then in those parts, they
lobbyists could just change it without even requiring the open platform.
