# Normal

1.  A user creates a bounty "why is my 3d printer not working", they
    post some images and a description. They also fund the bounty a
    little, and give it the tags #3d printing #problem solving.

2.  A user replies the next day with a solution.

3.  The user replies saying that the solution worked and they vote the
    solution in both #3d printing and #problem solving

4.  A day later after a few other users voted the solution, the solution
    is accepted and the user gets the bounty as well as all the
    experience from the initial post upvotes, and from the acceptance
    vote itself.

The upvotes to the bounty post act as the accepting vote criteria for
the submissions.

# Fail

Continuing from above .2

1.  The solution does not work and the user replies to the solution with
    proof that it does not work.

2.  The original poster downvotes the solution

3.  A few other users downvote the solution

4.  A day later the solution does not pass. The vote experience is
    returned to all the users.

5.  The solution poster does not lose any experience other than their
    own they might have upvoted their own solution with.

6.  Any users that upvoted the solution lose their experience.

# Possible Fail & Correction

A users initial seems to have failed, but the solution poster clarifies
that it was done incorrectly. it is then determened the solution did
pass, and the votes are corrected before the deadline.

1.  Continuing from point 3

2.  The original solution poster noticed the original bounty poster did
    not implement their solution correctly and replies to their response
    that they missed a step.

3.  The original bouny poster edits their intilal response to the
    solution and indicates they were wrong and it did actually work.

4.  They vote two upvotes to counteract the downvote they cant retract

5.  The vote passes a day later and the two experience is returned, but
    1 is lost to the initial downvote.

# Possible Fail & Correction without vote passing

A use case of not being corrected before the deadline is also covered.

1.  Continuing from point 4

2.  Even though users reaslise the solution did work all along, there
    were too many intial downvotes on the solution and not enough time
    in the deadline to correct them.

3.  The deadline passes and the solution fails even though it worked

4.  Everyone looses their upvote experience but any downvotes are
    returned.

5.  The solution is reposted and revoted

6.  It now passes

Mistakes can cause deserved experience to be lost. This incentivises
scrutent analysis of solutions.

# Possible Pass & Correction

A solution is posted but another user determines it has a harmful
conseqeunce

1.  Continuing from point 3 of "Normal" use case.

2.  A user replicates the problem and solution on their end before
    voting to make sure that it truely does work. Even though it does
    work they notice a harmful consequence that could actually damage
    the printer in some cases.

3.  This user posts their finding as a response to the solution with a
    video or picture as evidence.

4.  Several users upvote the response

5.  The votes on the solution begin to trend towards the negative.

6.  The solution does not pass by the deadline

7.  The user who found the flaw gets all the experience of the upvotes
    on their response.

# Double Solutions

1.  A solution is posted that does not work

2.  another solution is posted a few minutes later that does work

3.  A day after the initial solution, it does not pass

4.  A few minutes later the second solution passes

# Double Solution with shared content

1.  A solution is posted that works except for one small flaw.

2.  The flaw is pointed out by a user who also posts their own solution
    that used 90% of the original solution with their own fix.

90% of the value was created by the original solution poster, even
though as a whole it did not work. Do they desever 90% of the value? Who
decides that value? What mechanisim is there for ariving at this value?

The user can specifiy in their solution that x% of the rewaard will go
to the original solution poster. But what if they propose only 10%,
should the solution not be accepted even though it works even though the
split is unfair? The two sould be seperate. Since the value is to have a
record of a problem to solution post, and fund split is not part of the
community value but just of individidual value, but regardless it still
must get addressed at some point.

the community can then somehow specifiy the split through voting. Or a
response to the original solution can be made. The original solution
poster can then propose a split that the response will recieve.

In either case the split is decided by an individual with breaks open
principals of no individual control.

Maybe then in either case each user can propose a number as an initial
value. Then user can upvote or downvote that number. An upvote will move
the value up by one unit and consume 1 experience from any of the
criteria tags that had been initially voted in.

# Bounty Reward Split

These will be several use cases that cover splitting of proposed bounty
splits. All bounty smart contracts will have to have fund split
capabilities for multiple users.

## New Solution with split

1.  A solution is proposed that used material from another user. The
    solution poster references the material or post from the other user,
    and proposes a 50/50%.

2.  Some users upvote the split, some downvote it, but it settles
    roughly around 50/50.

3.  The deadline is passed and the fund is awarded with a split

4.  All the experience is returned for the passing votes and for the
    bounty split votes.

There can maybe be a experience return range for bounty split voting. So
that if you voted against the final split by more that x%, your
experience is not returned.

##  Tripple Split

1.  A solution is proposed that has two other authors specified in the
    bounty split for a even split across all 3.

2.  If a user upvotes a split for an individual user specified in the
    fund split, it will remove a % point from another user selected at
    random.

## Can votes be changed before the deadline and are there any problems with doing so?

Maybe they should not be allowed to, so that in order to fix the
outcome, they must vote twice, so that the net vote is +1, and when the
vote pases the two positive votes are returned, and they only lose one.

## Lost experince when voting against the masses?

If a user votes to pass a vote that does not pass and vice versa, should
they not have their experince returned? It should not be returned
because this will put risk on voting without validation.

## Required experience for posting?

Should posting a solution require experience? If yes then this would
reduce the amount of poor quality posts, but also reduce the chance of a
solution being provided by someone who is capable but new to the system.
I think initially posting a solution should not require experience. This
can be left as a consideration for the beta.

## Double, Single or No experience for decision voting?

Question: Should votes be doubled when there is a threshold? So anyone
that voted can get double their experience back, or should it just be
returned? Or just consumed? An analysis of what they each incentivise
should be done.

#### No experience, it is consumed

The user would then be voting purely to influence the system, there is
only the natural incentive to have the vote go in their favour.

Also this would require users to constantly produce value in order to
continue voting

#### Experience returned when vote goes in their favour

The user now has extra incentive in order to have the vote swing in
their favor, but there is already the natural incentive. What is the
purpose of overlapping incentives? None that I see.

Double experience

The user can now farm experience by voting likely passing votes.

In conclusion it seems that votes should be consumed.

## Returned experience for voting criteria?

When voting criteria for a decision vote, should the experience be
returned?

Yes, because there is no natural incentive to select criteria, since
anyone can do it, it is a prisoner\'s dilemma of who will do it(since
maybe just one vote is enough to have it become criteria), and users
will save their votes for actually voting the decision, which does
influence the system. Therefore when a vote passes based off the
specific criteria, all the experience is returned for that subject.

## What about negative votes? If someone downvotes a criteria vote

This means they don\'t think it should be a subject the decision should
be judged by. If they are wrong and majority votes that it should be,
should their vote be consumed? Or returned regardless if the vote
passes?
