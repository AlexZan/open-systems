This document will describe a system for voting that will work in
decentralized systems.

This document focuses on Decentralized Democracy and voting, but not on
the application of Open Systems. Instead this is covered in:
[[Application of Open
Systems]{.underline}](https://docs.google.com/document/u/0/d/1nGDT53WrHlsRiddWcqr2CiOlu7NFN01wXTfh1uKR-SU/edit).

This section will begin to describe Decentralized Democracy through
examples that face technical challenges, but it is not exclusive to
technical challenges and can be used for any type of assessment and
decision making as will be covered later in the document.

## The Need for Decentralized Democracy

The decentralized movement is taking many shapes, starting with peer to
peer file sharing like torrent, then bitcoin, ethereum smart contract
and now DeFi (Decentralized Finance). Even though the services
themselves are decentralized, the decisions which may take the systems
in a direction or another are made by key individuals (those who control
the code repository, and decide what feature they allow/implement or
not). E.g. what bug should be prioritized, should a feature be
implemented or not.

Imagine a decentralized financial system where the development team, or
just an individual on the team has a covert financial interest in
prioritizing a new feature or bug, they can do so without any resistance
and personally benefit. This is just one extreme example of how a
centralized development process suffers from the same exploits and
corruption centralized operations suffer from, e.g. an investing firm
group or individual deciding to put money into an investment that
covertly benefits them personally.

In summary, I propose that the same open principles that govern the
operation of decentralized systems, should be applicable to the open
source/decentralized development process also. To achieve this we will
need a democratic method of deciding such things as direction and
priority in development.

To achieve this, a decentralized voting system that does not suffer from
the same exploits as a centralized voting system, is first required.

## The Identity Problem with Voting

There is no way to guarantee that one person gets one vote currently.
This can be and has been historically exploited in online systems that
try to vote priority on a bug or feature, but this is also an issue in
non online systems such as in national voting systems.

We will look at all the common ways services have tried to handle
identity and authorization, and the problems they face with attempting
to guarantee that one individual only receives one vote.

Starting with online systems, any attempt to make a voting system for
prioritising features or direction of a system has had issues. Currently
you can make as many accounts as you make emails for and vote many more
times than just once. This makes voting power rely on tedious work that
can be done in seconds by bots (remote scripts which can automate
tedious tasks) to make accounts and cast a vote.

A solution some services have relied on is using government
identification as a way to prove identity. Using this, you could
theoretically achieve one vote per government id, but that does not
guarantee one vote per individual, since it is possible to exploit
government id.

As we can see from the above problems, depending on email can lead to
exploits, since email systems are easily exploitable themselves, and
depending on a government id can also be exploited in many ways. The
pattern that emerges here is a system can not be dependable, if the
system which it depends on is not dependable. More specifically, a
decentralized system can not be truly decentralized if the system which
it depends on is centralized and can suffer from the exploits of
centralized systems.

In summary, If identity can be exploited with current centralized
systems that authorize identity, then one vote per identity can be
exploited.

## Decentralized Identity Ideas

We will look at potential solutions to the centralized identity problem,
and see how they also fail, in order to prove that identity is
inherently the problem.

### Biometrics

Some services have begun using fingerprints and face recognition to
identify an individual. These systems can easily be made decentralized
in order to authorize an individual user with their various biometrics.
So an individual can take a picture/video of their face, scan their
fingerprint with their phone, etc and submit it to the decentralized
system which either authorizes them or not. The issues with this might
be obvious; anyone can share that picture/video or fingerprint scan and
present it to their device as their own identity. This makes identity
fraud even easier than having a human verifying your face in person over
the picture on your id, since there is no way to duplicate your physical
face. But in the digital space, everything can be duplicated.

### Identity Challenge

A solution some systems have come up with is to ask the user to perform
an action in a picture or video, e.g. "touch your nose with 3 fingers
while looking upwards with an angry face" and the system using AI or
humans will verify you have done those things accurately and authorize
you. This is a much harder system to exploit but it is increasingly
becoming easier with technologies such as deep-fake, where you can take
a picture or video of an individual you are trying to steal the identity
of, record yourself perform the challenge, and an AI will generate a
very lifelike result of the other individual performing the challenge
with your actions. This will easily trick most humans with today\'s
technologies. Imagine just a few more years from now. Essentially this
becomes an AI arms race game, where the "challenge" AI tries to
outperform the deep-fake AI. We are already seeing this arms race game
being performed by the now familiar Captcha challenges. Captcha has
increasingly become more difficult over the years in order to make it
difficult for bots, but I believe it has reached the point now where it
is more difficult in some cases for humans to pass the challenge than
the bots it was intended for.

### Peer to Peer Authorization

A system could be possible where users are asked to verify each other.
When you wish to identify yourself with a device on a system, the
decentralized system will have a group of random users in your location
that you must physically get verified by. E.g. When I wish to authorize
my new smartphone on the decentralized system, I am given 3 random users
in my area. They are also notified that they have been selected to
verify my physical identity. I am then required to arrange a time and
place to meet with them at which point they will take a picture or video
of me, submitting it to the decentralized system in order to compare
against the other 4 submissions of me. Once the system detects an
accurate match, I am now authorized on my device. In regards to voting,
if the system detects an accurate match between two or more identities
in voting, it will flag those votes and individuals.

The idea of peer to peer authorization works hypothetically, and it will
be proposed as part of the full solution in conjunction with the
identity-less solution, but it faces several challenges on its own.

First, it is a very time consuming process, having to meet with people
in order to get authorized might sound ridiculous to some.

Second, providing indefinite authorization is dangerous, as the device
itself could be compromised, and then someone could vote with your
identity. Therefore periodic re identification is required, where the
authorization expires after some time and must be reauthorized. This
inturn adds more weight to the first point.

Third, it is still possible to exploit, even if statistically not
likely. E.g. offer 1 million dollars to each user who is verifying you
to record a video of another individual on your phone instead of you. If
Peer to Peer Authorization is combined with Identity Challenge then it
becomes even less likely to exploit, but it still does not guarantee it
can not be exploited with the AI arms race game.

In summary, anything digital can be duplicated and thus exploited,
therefore we need some human element for verification, but humans can be
exploited also and trust compromised. There is no way to guarantee an
identity is ever genuine. The full solution for decentralized democracy
must not rely on identity.

## Identity-less Voting as a Solution

In order to solve the identification management and authorization issues
mentioned above the proposed solution is to remove the dependency to
identity all together.

Voting power will instead be dependent on things which can not be
exploited with multiple or false identities. Voting power will no longer
be provided by default as it is with identity in traditional democracy.

## Voting Power

All users start with 0 voting power when they first begin using an open
system; they are not able to vote until they acquire some voting power.
To acquire voting power, a user must first contribute some value to a
community. One example of contributing value is through an open
discussion forum, referred to as Open Forum.

The Open Forum application is described in greater detail in the
application section, but for now it will be used as an example to
describe a form of voting; upvotting.

Open Forum is similar to a standard discussion forum, but users upvote
and downvote subject tags on posts, instead of the post itself. By
contributing value to a #community (defined by a subject tag) that
community votes on the value you provided, and those votes are converted
into experience (voting power).

## Earning Experience

Users can generate experience several ways. The best way to start
earning experience points is by creating a post.

For example, You have an idea for an app. You post your app idea and tag
it with #app #idea. After one day, if no one believes it is a bad idea
and does not down vote the post, you are awarded 1 experience point in
both #app and #idea. **Experience is earned in subject tags.**

If users upvote your idea in #app and #idea after one day, on top of the
1 experience you earn by default, you also earn all the votes made
towards your post. E.g. there were 10 votes in #app, and 5 votes in
#idea. After a day you earn 11 votes in #app and 6 votes in
#development. **Votes received are turned into experience points.**

A user upvotes your app idea with a new tag, for example if it is a
rideshare app idea, but you didn\'t initially tag it with #rideshare, a
user might add #rideshare as a new tag and give you 1 experience in that
subject. **Any subject can be upvoted or downvoted**

Essentially you are contributing value to the community just by posting
an idea, but you could also be a programmer submitting your code for
review as a post, earning points in #programming and #app. You could be
an artist posting your #painting. You could be a #mechanic posting a
#DIY video. **Any content can be posted, text, code, links, video,
pictures, etc.**

If a user just created an account, they can not upvote #app, since they
do not have any experience in #app. **You must have experience in order
to vote.**

When a user votes on a post\'s tag, the experience they voted with is
consumed. E.g. you upvote #app, and you lose 1 experience from your
total experience point. This forces users to play smart with their
experience points and thus voting power. **Voting power is consumed.**

When a user votes on a tag, and the vote count doubles from the point at
which they voted, they will also earn experience. E.g. User x has 1
experience point in #app and upvotes #app when it had 0 votes, taking it
to 1 vote. Another user upvotes #app and it is now 2 votes, causing user
x to earn back 1 experience point in #app. **Experience points can be
recovered by voting early.**

If you find a post that you think has a great deal of potential, you may
upvote it for as many experience points as you have. E.g. You can upvote
100 points in #app, thinking that this is a great idea, and the post
will easily reach a high number of votes, allowing you to earn back 200
experience points as an investment. **You can upvote with multiple
points.**

If a user posts something ignorant, or something that would cause a
decrease in value in some subject, users can downvote the post in those
tags. E.g. A user makes a post about making money by inconveniencing
other people, this user could get downvotes in #ethics. **Users can lose
experience by being downvoted.**

A tag can only receive as many downvotes as the total amount of upvotes
in that tag -1. E.g. this post has 0 upvotes in #ethics, a user can
downvote it just one time down to -1, but if another user disagrees and
upvotes #ethics, it has one upvote, and one downvote, for a total of 0
points. At this point users could downvote the tag two more times taking
it down to -2. **Downvoting has a limit.**

### Use Case

1.  New user (user x) makes account on an open forum

2.  They created a 3d printed reusable floss stick and want to share it

3.  They make a post, with a picture of the floss stick, a paragraph
    describing it, and the CAD file so that users can print it, and make
    open source improvements.

4.  They also post with the following tags: #3d printing #cad #floss
    #floss stick

5.  After 24 hours, several users upvote on many of the tags, user x
    receives 100 experience points in #3d printing, 100 points in #cad,
    and 2 points in #floss.

6.  User x then browses the forum and upvotes 10 points in a brand new
    post about another good idea for #3d printing that had 0 votes.

7.  Another user upvotes that same post and it is now 11, User x earns
    back 1 experience point for a total of 91 experience points.

8.  The post reaches 15 votes after a week, and the user recovers 5 of
    the points they spent voting, they now have 95.

9.  User x continues to make more post contributing value, and spending
    that earned experience on voting other posts they have experience
    in.

## Actionable Voting

Until this point we have covered upvoting and downvoting in order to
assess the value of something (a post, an accomplishment, some work,
etc). Users can upvote indefinitely with no end; with no vote count
threshold that triggers an event. The higher the vote count gets, the
more value it represents.

Some community collaborations require decisions to be made and actions
to be taken. An example of that is something called a bounty. A bounty
is a goal that anyone can attempt to achieve. A bounty is posted like
any other type of content, but users are able to fund the bounty with
crypto (crypto currency). As the bounty fund grows larger and larger,
users might be more motivated to attempt to achieve it. A user can
respond to the bounty with a submission. If a day passes and the
submission has double or more of the upvotes than the downvotes, the
submission is accepted and the funds are delivered to the user who made
the submission and won the bounty.

More details on the entire funding process and funding application will
be covered later in this document.

Voting in a bounty has an end goal, to award a community voted winner
with the fund. As a result, it has a smart contract that is instantiated
when the bounty is created. This smart contract will activate when a
submission is made by a user. The smart contract will be responsible for
the action of delivering the funds when the vote passing condition is
met.

This is just one example of an actionable vote, but there are many more,
and anyone can develop their own for use in the system.

Actionable Voting on the other hand has a vote count threshold that
executes a smart contract (an automated set of actions). This is often
used when deciding between two or more options that will result in
different actions being executed. This type of voting will often be used
in open/democratized crowdfunding.

One example of a method of crowdfunding using open systems is with the
proposed Open Funder application.

The Open Funder application is described in greater detail in the
application section, but for now it will be used as an example to
describe crowdfunding examples.

Open crowdfunding will require voting between accept and reject when
crowd assessing work submitted to a crowdfund campaign or deciding
between several submissions for a work bounty.

In summary, a user must first gain experience, by contributing original
value to the community, in order to build voting power, which can then
be used to affect decisions in that community which in turn might affect
them. This is the user-system cycle of an open system.

## How is Merit Managed and What is an Open System?

Merit is managed by an Open System.

An Open System must satisfy all the following requirements (A summary of
Open Systems Principals):

1.  Open; No ownership. No one has any legal right to any part of the
    open system. Even if they created it; they may be the founders of
    the system or contributors of the system, but they do not own the
    system, no one does.

2.  Transparent; All actions, transactions and interactions with an OS
    must be kept on a permanent open ledger.

3.  Direct Democratic control; No individual control. An Open System can
    not have a single point of control, all actions that require input
    must be accomplished through vote. E.g. a system that can be shut
    down by a master user or admin violets this open principal. All
    things must be able to change through democracy, including this
    list.

4.  Decentralized; No central location. A decentralized system must have
    the ability to spread organically with incentives provided to
    individuals to join the network and can not exist in preset,
    predetermined physical locations.

5.  Open Source; Nothing proprietary. An OS must follow a standard open
    source which allows users to vote in improvements.

6.  Equal Opportunity; Non Profit. An open system can not profit for any
    users. Although users may profit easily off an open system. The idea
    is that everyone has equal opportunity to profit and all else.
    Therefore a system can never be designed to make it possible for one
    individual to have more opportunity than another.

7.  Private; No Identity. An OS can never require a user to identify
    themselves. Although they might choose to identify themselves.

## Decentralized Democracy requires Open Systems

As seen above. Since voting ability is tied to merit, then an open
system that manages merit is required. A true open system also requires
Decentralized Democracy to function; since a true Open System can't have
a single point of control and a national government that manages
identification has a single point of control; it can be modified without
vote. As a result an Open System can not base vote on government
identity and Decentralized Democracy is required. Therefore
Decentralized Democracy and Open Systems are co-dependent.

## Isn't This Going to Conflict With Local Government?

No, DDand OS work with the local government. Discussions had on OS can
be used by the local government to help with decision making. Funds
raised towards a cause or project through OS will not affect government
funding in any way, in fact it might help alleviate it in some cases.
Decentralized Democracy votes have no impact on the local democractic
process. The local law will always come first, and any votes, actions
and causes through OS and DeDem are not above the law and will have to
follow local laws in order for those actions or causes to be legal.
These are no different than a group of people getting together in person
and deciding to work on a project for example, it must be within the law
to be legal.

## Will There be Representatives?

Yes and No. Not in the current sense of representative. We currently
elect representatives. Once elected they hold that title for a term and
there is only one position or a few, that are managed from the top down.
In an OS by upvoting a user in a specific category, you are now voting
merit for them, by doing this, they now have more voting power, and you
have in turn given them a slight boost to being a representative in that
field. They can lose that at any time by getting downvoted, or can gain
more by contributing more and gaining more merit, getting even greater
voting power in that field.

Essentially because of merit you voted towards someone, you are trusting
them to represent you in the field you voted them into.

The entire process of elected representatives and the privilege that
goes with the position is streamlined. There is no longer the concept of
a term since it is now fluid based on merrit. Privilege that anyone has
equal opportunity to earn is always in a constant state of flux, and all
the actions that affect this flux are fully transparent.

## Experience

Experience is the unit that represents merit; the value that a user
contributed in a subject. E.g. A user posted an idea in the #electronics
field, they earned 10 experience from other users who appreciated their
idea.

## Investing Experience

A user can only vote if they themselves have experience in that subject.
When they vote on a subject, they are consuming the experience points
they currently have in order to cast the vote. If a vote is successful
(more on that later) the user who voted will double their experience in
that subject. As you can see, voting can be an investment (most
interactions with the system are investments; monetary or experiential).

## Different Types of Voting

### Voting on Value

This is the voting that has been described thus far. Votes are used to
assess the value of a user contribution; a proposed solution, work of
art, proof of work as some examples.

### Decision Voting

Deciding between or more options will require decision voting. E.g.
Voting between accept and reject when crowd assessing work submitted to
a crowdfund campaign or deciding between several submissions for a work
bounty.

There are two votes that need to occur. Up to and in the first 24 hour
period of the vote starting users must vote on the criteria of the main
vote. E.g. users vote that criteria for a goal to create a camera render
#cameras #design #ergonomics. Next after the first 24 hour period the
actual vote takes place. All the criteria tags must pass their votes for
the entire vote to pass.

A full example:

1.  A user(project owner) creates a crowdfunding campaign to produce a
    watch

2.  The project owner creates several goals: sketch concepts, 3d
    concept, Cad design, Prototype, and so on.

3.  The owner submits the work for the first goal. By that time, several
    users including the owner have suggested the criteria to vote the
    goal submission by, including; #watch design, #watch, #concept
    design, #draft. Users have up to another day to finalize the
    criteria by upvoting or downvoting existing subject tag proposals,
    or adding new ones.

4.  The criteria voting period is over, and the voting period begins.
    Users begin to upvote or downvote each criteria tag to decide if the
    submission has passed.

5.  After a day, if all the criteria tags are in the positive, the vote
    passes and the owner receives the funding of the goal to start work
    on the next goals.

This example uses the funding application from Open Systems
Applications.

### Closed Voting

Closed voting is traditional voting; 1 vote per identity. Closed votes
can be as simple as inviting your friends accounts to a vote on the team
most likely to win this year, or a community voting between several
choices of what to build in a park in their community. With closed
voting the group is solely responsible for maintaining the integrity of
the votes and vetting the identities. There are several strategies to
help with this.

1.  Referral

2.  Consumable Token Verification

3.  Image/Video/Bio verification

## 

# Scrap - To be deleted

Summary of Discussion with Imad

1.  Confused direct democracy with Decentralized Democracy

2.  Did not initially understand voting with merit

3.  Decision voting became clear once a in depth use case was run.

## XL Pipeline Discussion use case

1.  A user supporting the building of oil pipeline posts his case as why
    it\'s needed

    a.  Argues that it benefits the entire Canadian economy, since it is
        an oil based economy

    b.  Argues the job losses by cancelling the project

    c.  Argues the loss of already invested Canadian dollar

2.  Users that see value in his points begin to upvote in #economy
    #financial #canadian economy #oil

3.  Users then respond with points about the cost of remediation of
    tailing ponds and the large environmental impacts of more carbon
    production as well as the impacts of the tailing ponds leaking into
    the ground.

4.  Users that see value in the responses, upvote them with
    #environment, #remediation, #global warming.

5.  Since the original poster does not make any mention of the
    environmental impacts and does not address them or respond to the
    concerns, users begin to downvote the original post in #environment
    #global warming.

## Demolish a Park and Build a Parking lot use case

Draft

## Overview of DeDem

DeDem through identity-less voting provides a global direct democracy;
the ability to vote on all matters, local, global, anywhere, anything,
using only open decentralized systems that do not depend on a central
authority of identity.

## Global Issues and DeDem

In many parts of the world, the current version of democracy does not
work well. It is exploited or is not implemented fairly. Everyone should
be able to vote for matters that affect them directly or indirectly.
Everyone should be able to contribute positively to any matter. We do
not currently have a global system that allows this. DeDem enables this.

We currently vote on representatives who we hope have our best interest
in mind. Those representatives then vote on other representatives who
currently attempt to manage global matters such as the UN and WHO.
Decentralized Democracy could allow a global vote on such global
matters.

Coupled with internet-as-a-right, DeDem will provide a voice for anyone,
anywhere.

## Why hasn't Decentralized Democracy been possible previously?

Until now, the paradigm of one vote per user, person or identity has
been the go-to solution for creating equality in voting.

Local democracy is dependent on a nation, since current democracy is one
vote per citizen of that nation. Therefore the government of that nation
must manage and authorize the identification for voting.

Having a system that depends on multinational management and
authorization of identification becomes challenging as each nation has
different motivations, ideals, relations and as a result, one government
trusting another government with fairly managing and authorizing
identification for a global vote is nearly impossible.

In conclusion, a decentralized system that depends on a centralized
system of identity, can not truly be decentralized, this has been the
biggest hurdle in decentralized democratic systems until now.

Solving the challenge of going beyond 1 vote per individual/identity
goes far beyond enabling global democracy, it also enables a system of
global collaboration.

Afterall the matter of a national citizen is only for that specific
nation, the system is global, universal.

It no longer matters what nation you are in, a citizen of, what religion
you may be, race; none of these things matter. What you identify with
has no impact on your universal voting ability. Every individual should
have equal opportunity at a voting ability.
