This document will attempt to describe the philosophy, systems and
applications of Open Systems. The first section covers the principals
the systems are built on, the second covers the features of open
systems, and the third covers the core applications of open systems.

# Open Principals

## No Authority

There is no authority to enforce open principles in companies or
services that wish to use open systems. The users can select which
principles to use. Some users can start with just a few open principles,
and as they gain trust in the system, can introduce more. A service or
system that follows all open principles can be referred to as open. A
company or service using only some open principles can be said to be
using open systems, but not an open service/system. In fact there is not
such a thing as an open company as we will see later.

There is no central authority to enforce anything in an open system. All
interactions with an open system are through community voted contracts.

In theory, a perfect system has no need for enforcement, just well
designed rules. Chasing perfection is insanity but chasing well designed
rules is a necessity.

## No Ownership

No one can own a system that is open. There can be founders, creators,
maintainers, contributors, but no individual, group or company can have
any legal right to ownership of the system. This does not mean they can
not earn income from their creation or contributions (more on that
later)

Though a system or service can be conceived, funded and built through
open systems, it does not have to be open itself and so individuals or
companies can create a system/service and still own it, but it will not
be designated open and thus can not be fully integrated with other open
systems.

## No Hierarchy : Democratized

No individual, group or company can have any power over any other
individual in an open system. Any action must be performed by community
vote; a consensus. No one can be designated with any type of power;
everyone has equal power. This results in no hierarchy of power or
decision making.

## Decentralized

An open system can not be shut down or modified without consensus. It
can not be controlled by any individual, group or company. An open
system also can not have any dependency on a centralized system. Since
being dependent on a centralized system means that an individual, group
or company can choose to shut down the system that is being dependent
on, and thus the depending system will be non functional; The depending
system is indirectly centralized by the centralized system.

## Transparent

All data is transparent. Any data going into an open system, any data
modified or deleted from an open system is logged and viewable by all,
publically.

A critical point to understand is transparency does not mean lack of
privacy. All individual data is anonymous. Therefore private data can
never be leaked unless someone gains a hold of a specific private key
(\~password), which could be a doctor you give permission to for
example, or if someone gains access to where you store your private key.
It is easy to secure a private key, just like securing your keys to your
home.

A consequence of all data from everything being open to all but yet
anonymous, is that the data can be studied by anyone in order to drive
science, make discoveries, predicting events, etc. The data however can
never be used for covert or exploitive purposes, since it is available
to all and owned by none.

Encrypted data is also permitted as long as it follows all other
principles. If data is encrypted, it must be encrypted for all, with no
one having the ability to decrypt the data. Data can only be
encrypted/decrypted by consensus or by a consensus contract. Data is
only mutable through consensus.

# Open Service

An open service allows applications to communicate with it using
protocols that follow open principals.

# Decentralized Democracy

The main feature needed for an open system is Decentralized Democracy.

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

This section will begin to describe Decentralized Democracy through
examples that face technical challenges, but it is not exclusive to
technical challenges and can be used for any type of assessment and
decision making as will be covered later in the document.

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
both #app and #idea. **Experience is earned in subjects.**

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

[If a user just created an account, they can not upvote #app, since they
do not have any experience in #app. **You must have experience in order
to vote.**]{.mark}

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
    describing it, and the CAD file so that users can print it and users
    can make open source improvements.

4.  They also post with the following tags: #3d printing #cad #floss
    #floss stick

5.  After 24 hours, several users upvote on many of the tags, user x
    receives 100 experience points in #3d printing, 100 points in #cad,
    and 2 points in #floss.

6.  User x then browses the forum and upvotes 10 points in a brand new
    post about another good idea for #3D printing that had 0 votes.

7.  Another user upvotes that same post and it is now 11, User x earns
    back 1 experience point for a total of 91 experience points.

8.  The post reaches 15 votes after a week, and the user recovers 5 of
    the points they spent voting, they now have 95.

9.  User x continues to make more post contributing value, and spends
    that earned experience on voting other posts they have experience
    in.

In summary, a user must first gain experience, by contributing original
value to the community, in order to build voting power, which can then
be used to affect decisions in that community which in turn might affect
them. This is the user-system cycle of an open system.

## Actionable Voting

Until this point we have covered upvoting and downvoting in order to
assess the value of something (a post, an accomplishment, some work,
etc). With value assessment voting, users can upvote indefinitely with
no end; with no vote count threshold that triggers an event. The higher
the vote count gets, the more value it represents.

Some community collaborations require decisions to be made and actions
to be taken. An example of that is something called a bounty. A bounty
is a goal that anyone can attempt to achieve. A bounty is posted like
any other type of content, but users are able to fund the bounty with
crypto (crypto currency). As the bounty fund grows larger and larger,
users might be more motivated to attempt to achieve it. A user can
respond to the bounty with a submission. By default (but can be
modified), If a day passes and the submission has double or more of the
upvotes than the downvotes, the submission is accepted and the funds are
delivered to the user who made the submission and won the bounty.

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

## Criteria of Actionable Votes

Actionable votes allow a smart contract to execute. The process of a
vote passing requires voting criteria to be selected before the final
vote. For example, If a bounty is created in order to create a new app
feature, as the bounty's funding is growing, users can also start voting
which tags they think will be required; any subject that the decision
will need to be judged on. By the time the first submission of the
bounty is made, and/or more than 24 hours since the bounty was made, the
voting criteria must be selected.

I propose the following equation in order to determine the criteria vote
count lower limit (the point at which subjects will not count as
criteria): The average of the positive lower median.

### Use Case

1.  Bounty made to develop a floss stick

2.  Users suggest the following tags: #cad, #3dprinting, #dentail,
    #floss printing, #funny (suggested by accident in this example).

3.  Several days later the first designer submits their design and a
    video of the prototype for review as a submission. By this time #cad
    had 100 votes, #3dprinting had 200 votes, #dental had 2 votes,
    #floss printing had 1 votes, and #funny had -2 votes.

4.  The vote criteria is determined by getting the average of the upper
    median:

> (2+1)/2 = 3/2= 1.5

5.  Since #funny was a negative vote, it never made it as a criteria
    subject. Since #floss printing was only 1 vote, and the cut off was
    1.5, it never made it as a subject criteria. #dental made it since
    it had 2 votes which was greater than the 1.5 vote cutoff.

6.  Once the criteria deadline ends, and the voting criteria is
    selected, users begin to vote on each criteria which they have
    experience in.

7.  24 hours later, all the votes are in the positive, the submission
    passes and the bounty fund is awarded to the programmer.

These criteria selection votes are what drive all actionable votes, no
matter if it is a bounty, milestone, or any other type of smart
contract.

# Core Applications

This section covers the applications that use open systems. Since there
is no central authority, there is no concept of an official application;
any user or group may develop their own application that can use the
open systems. E.g. The initial forum application that is used to
interact with the open forum system can have several alternatives as
long as they are developed with open principles. There is no official
development team, anyone can contribute and collaborate to create
alternatives or completely new types of apps and systems.

There are 3 initial core applications

1)  Forum

2)  Funding

3)  Claims

These applications all work together interdependently; They each require
the others, in order to function. E.g. You can not have funding with the
accountability of a claims process, you can not have a claims process
without the ability to discuss issues within the forum.

## Forum

The forum (Based on traditional forum concepts) is where content is
posted and discussions are had. All content; ideas, images, videos,
articles, etc, are posted in the forum. Discussions can then occur by
replying to the content posted. The initial features are similar to
Reddit.

In describing the features of open forum, we will need to revisit some
of the concepts of decentralized democracy since it is one of the core
features of open forum.

### Voting

Traditional digital forums might allow users to like, or upvote a post;
with Open Forum, this is where the differences begin.

In Open Forum you can upvote or downvote only subject tags/hashtags of a
post, not the post itself. E.g. If someone posts a grand canyon photo
they took a user might upvote a #grand canyon tag, another user could
upvote #photography, and yet another might upvote #landscape
photography.

### Experience

The original poster gains experience equal to the amount of votes they
receive in each tag. E.g. the user will get 10 experience in
#photography because there were 10 votes in photography from other
users. We will see how experience turns into merritt which affects
voting power later on.

### Accounts

A new user can start using the forum right away without any setup: A
user without an account can still post content to the forum, this
content will be posted as anonymous.

In order to vote and gain experience, a user must have an account. This
is a simple process of storing credentials that protect the key to your
account. This key must be kept secure at all times, just like your house
keys or any key to a store of value such as a safety deposit box at a
bank.

### Down Votes

If someone posted something inaccurate or untrue in a subject, users may
downvote it. E.g. a user posts about a flat earth theory, you might
downvote #science on their post. This will cause their account to to
have a -1 in #science. Though flat earthers might upvote #flatearth and
they will gain experience in that subject.

If someone posts an unappealing photo to #photography, a user will
probably not downvote #photography because 1) it is far more subjective
to assess general art appeal and 2) because the odds of doubling your
experience are far less likely since many people will not vote due to
point 1. An unappealing photo might have few #photography votes or none,
but they are likely not to have negative votes.

Therefore negative votes are more likely to be used when assessing more
objective truths; things that can be proven through reason or are
quantifiable.

### Open Posts

Thus far we have talked about posts where the content that was posted is
owned by the original poster. The data in these posts can not be
modified by the community, only by the original poster.

E.g. You post an idea for a new app, only you can remove the post or
modify it, no one else can: You own the content.

If we wanted to make a post that everyone could contribute to, such as
the concept of a "wiki", we could create an open post.

E.g. You post about the history of Egypt. Anyone can make edit
suggestions which the community can vote in. No user including the
original poster can delete or modify the post.

Users can make suggestions that can get voted in.

# Funding

Thus far we have mainly talked about posting content in exchange for
experience. This is analogous to working for sweat equity, as the
experience gained can lead to improving your odds of affecting the
system as well as potentially earning a profit (though experience can
never directly be exchanged for monetary value as it would violate open
principles).

## Accounts

By default each account is also able to store crypto currency (crypto).
This does not require any setup or any deposits. This is in place in
order to receive donations and payments.

## Donations

A user can donate to a post, and the original poster will receive the
donations in their account. Donating to a post will also show the
donation publicly on the post itself, and the total amount that has been
donated to the post. E.g. A remarkable photo of the grand canyon has
received 10 donations totalling \$200 dollars equivalent in crypto.

### Funds

Users can create a funding post. This creates a smart contract with
crypto storage in the post with certain rules. There are different type
funds with different smart contract rules, the most common are bounties
and goals.

If a user donates to a post that has a fund, such as a bounty, the
donation will go to the fund instead of the original poster directly.

## Bounties

A bounty is a fund with the reward being open to anyone that proves they
were first to meet the bounty criteria.

E.g. There is a bug with a new feature in an open system, a bounty is
created to fix it, and users begin to donate to the bounty over time.
The bounty reaches an amount that becomes very attractive to developers,
they now race to develop and submit the fix as a reply to the bounty
post. When users vote that it has in fact fixed the bug, the bounty is
awarded or held for some time before it is awarded.

## Goals

A goal is a fund with the reward being reserved for the original poster
or a predetermined account. This is different from a bounty, where any
user can receive the bounty fund.

E.g. A user promises to create something if a specific funding goal is
reached.

Goals are similar to today\'s crowdfunding funding goals.

## Funding

In order to donate to someone, you simply deposit crypto from an
existing crypto location to the address of the user account you wish to
donate to. A crypto exchange is a service that allows you to exchange
one currency for another, and so you can take dollars, and purchase
crypto coins, then use that to donate or invest in Open Funds. The
important note here is that open systems can utilize existing
decentralized infrastructure in order to make funding work and does not
require its own.

You can also transfer crypto into your own forum account, that way you
can donate directly from within the forum application (this is
optional).

## Projects

A project is a set of goals. Goals can have predetermined criteria that
the owner specifies, beyond just the funding criteria, such as in the
standard goal mentioned earlier.

E.g. In a project to design an electric scooter the first goal is to
create concept art for the scooter design. It has a funding requirement
of \$5,000 crypto equivalent. The user then posts proof of goal
completion; the scooter concept art. The community votes on whether they
accept or reject the submitted proof of completion. If the vote passes,
the \$5,000 crypto fund is released to the user. This allows the user to
now begin work on the next goal, unlocking the funding of each goal as
they progress through the project.

By having a crowdfunded project broken down into several goals that
unlock funding through a democractic process solves some of the most
common issues with current crowd funding by democratizing the entire
crowd funding process through the open principles, and factoring in
trust into funding progression

## Trust

Projects can be set up in many ways with many options. Some options will
create more trust, some will create less trust. One of these options is
to allow the project to become Open if it meets failure criteria. E.g.
If a project that was funded fully, but the owner loses interest half
way through and disappears, the community can vote the project as a
failure, this will make the project open; a crowd sourced project. The
original owner will automatically relinquish all legal rights by
contract, to anything that was created through the project funding thus
far.

In this example, users are more likely to fund this project because they
trust that if the original owner fails, the project will continue.

One last example is that owners can gradually increment the funding
requirement for each goal, so that trust grows proportionally with the
funding being unlocked, as opposed to all or a large amount of funding
being unlocked initially.

There are many more examples of how project trust can be increased (more
on this later).

## Tokens

In traditional crowdfunding, the user has the option of pre-purchasing a
product or service at a discount. The earlier the pre purchase, the more
of a discount received. Projects in Open Systems also have the option
for this with tokens. A token can be purchased at an established value
by the owner, and once the product or service is ready, they can
exchange the token for the product or service.

Another benefit to using tokens is that if local laws permit, the owner
can allow the token to be transferable and thus tradable on exchanges.
This is essentially like purchasing stock in a company early on such as
in an IPO, in order to make a profit off your speculation of increase in
value. In the crypto space this is known as an ICO, an initial coin
offering.

This will open the door to projects receiving much more diverse funding
from investors that are not only interested in the product or service
but want to fund the project to make a profit.

The project owner will be liable for any legal consequences and
responsibilities if tokens are not allowed to be transferable in their
local laws. This type of project should be reserved for more experienced
or expert project owners. Investors might not have trust in an
inexperienced owner trying to launch this type of project.

# Summary

## No Individual Voting Power

In order for a system to be open, it must be decentralized. Thus voting
must also be decentralized. Thus the voting system can not be dependent
on any centralized system, such as a centralized system that issues and
manages government Identification. Therefore voting power can not be
tied to identity issued by a central authority. The question becomes,
can identity be issued and validated through a decentralized system,
more so, by an open system?

Traditionally you create an identity with a government with a birth
certificate or with other nations identification if you are migrating.
Legitimacy of the documents is often a challenge. Fake identification
and multiple identities continues to be a problem.

The solution is to remove the need for identification, and the concept
of an individual as an identity. If there is no identification then how
will voting enforce 1 vote per individual. Without the need for the
concept of the individual, or identification, then there is no longer a
need to enforce voting power per identity. Instead voting power must be
developed by the individual through one or more accounts by providing
value to the community. E.g. an account that contributes value towards a
topic gains consumable voting points. These voting points are consumed
when voting.

## Equal Opportunity

The idea is that everyone has equal opportunity to profit. Therefore a
system can never be designed to make it possible for one individual to
have more opportunity than another. This is because no individual can
control an open system, and thus can not create any hidden opportunity
or margin for themselves.

An open system can not profit off any users, but users may profit off an
open system. A user can gain profit off an open system many ways. Mainly
through posting content.

## Contractual

Because there can be no owner, central control or authority, there can
be no human decision making on the outcome of any interaction with the
system. The outcome of all interactions with an open system is handled
through smart contracts. All contracts are community voted. This
guarantees equal opportunity amongst all accounts.

## Experts

An expert is a loose designation given to an account with a significant
amount of experience and thus meret. Experts can impact votes greatly in
the subjects they are an expert in compared to a non expert account. An
expert must contribute a great deal of value in order to to gain the
experience needed to become an expert. Value can be contributed through
content, or through intelligent interactions within the system, e.g.
investing experience intelligently in order to profit more experience.
Both contributing content and intelligently interacting with the system
provide value to everyone else in the system, in that specific subject.

The amount of experience needed to be considered an expert should not be
defined, since it has no bearing on any system interaction and is only
used figuratively as a social concept.

## No Institution

Since experts and experience is voted in through the community, there is
no longer a need for an institution to designate status or achievements
of knowledge.

## All data collection is transparent

Currently AI assistants such as google, alexa and serie collect as much
data as possible with no clear way to disable or select what data you
would like to share. This data is then monetized directly or indirectly
by targeting ads or content based on trends in the data that was
collected.

As a consequence of all data being transparent. Data being collected or
requested from the client or user will also be transparent. Data
requests will be clearly identified in the client so that the user can
disable all of them or pick and choose which they allow.

## Competency and Trustworthiness

Companies and Services that designate themselves as Open or using Open
systems are under constant user review. Users can post a claim against a
company or service.

A successful competency or trust claim against a company or service will
result in the user who discovered and made the claim to gain experience
in the subject(s) that best describe the claim. E.g. a company was
collecting data covertly but designated themselves as open will provide
#computer networking and #data service experience to the original poster
as voted by other users once the claim passes. The company or service
will also get labeled with a trust charge or a competency charge. This
will stay on the company or service account and they must gain back user
trust by providing good service going forward.

# Conclusion

Open systems is a concept; that, if all services and applications are
developed and operated using open principals, then they should naturally
work together without any conflict, this concept then extends beyonds
just the digital realm but into the social realm: Creating a system for
global collaboration of all things, where all individuals have equal
opportunity regardless of identity.

A system such as this is needed now more than ever; with global warming
affecting every individual in the globe, but with only a few companies
and nations deciding environmental policies that do not come close to
reversing the damage that our future generations will face.

With interplanetary establishments being a few years away from being
established, such as the moon, mars and larger space stations.

With AI already having greater capabilities than many humans in several
regards and with that capability growing exponentially. The few entities
and companies that will control AI will create an even larger disparity
of wealth, as jobs are displaced without any compensation. A system that
supports creating value without identity naturally supports AI.
