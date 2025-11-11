## Post Vote Meta Data

Maybe each post can have an object sent as a parameter that defines a
type of metadata. E.g. If someone is making a block post, the type can
be "block". This way the post types can be upgraded without having to
upgrade the contract. Although the smart contract post handler will have
to be added. Each post handler can be its own contract which links by a
type value in a mapping. A function for adding a new handler type can
accept new handler smart contracts. This of course can only be called by
the consensus contract.

## The Consensus Contract

Maybe the id of this contract is the only sender that is accepted in all
other global contracts? Maybe all actionable posts are linked to the
consensus contract. Maybe a mapping of post to actionable contract. The
consensus contract is what executes the proposed and passing smart
contracts. The consensus contract can then add the proposed contract to
a handler when the vote becomes actionable.

This should be similar to middleware like in node express.

## What about upgrading/replacing or competing behavior?

E.G

OnVote() would have several base middlewares

1.  RemoveVoterExp

2.  AddPostVotes

3.  AddOwnerVotes

Now what if we wanted to update AddOwnderVotes. Then we would specify
the title, and supply a new contract. Consensus would then replace the
reference from the old one to the new one.

What if we wanted to replace it? We would instruct consensus to remove
the old one by title, and add the new one. Making sure there is no
conflicting behavior is the developer's and voting communities
responsibility.

Maybe the process of time sensitive consensus could involve selecting
experts at random, and asking them to pass or deny the proposal.

## Then there are 3 potential stages of consensus

1.  Acknowledging and passing without block

    a.  While random experts are asked if it is time sensitive

2.  If time sensitive

    a.  Random experts are asked to pass or deny the proposal

3.  If not time sensitive

    a.  Pass if no blocks after more than half of global users with
        experience in the tags acknowledge

4.  Last case scenario, If more than half of users with experience vote
    to pass or fail (experience is consumed, not returned), (vote can
    pass and fail at any time).

### What if something breaks?

Worst case scenario, a brand new contract is uploaded, the database is
copied over from the old, and all clients must update to the new
contract. Unless the data is corrupt, then it would be basically
starting from zero.

## Components

Forum

- State: Posts

- SendPost

- GetPosts

Experience

- State: Experience

- GetExperience

Consensus

Voting

- State: Votes

- SendVote

Claimable Experience

- Claim

Make a post to execute update middleware, show what is being replaced by
what. Since only the consensus system can execute the update, users must
achieve consensus. Users start to acknowledge the proposed update.

How does the consensus know of the update? How does it know what to
update? How does this sit outside the forum?

Maybe there are only certain functions that Consensus has access to.
Such as modifying middleware.

Maybe consensus can have access to the entire states of all systems. And
so contracts that excuse can have access to all system states. The
systems just check if it is consensus requesting the state change. Maybe
a crud consensus interface must be used by each open system.

It seems that an interface for being an open system is a good idea. This
interface forces crud for each state. Maybe each contract has to be
limited to one state with the consensus crud interface. And a system can
be composed of multiple contracts that instantiate each other and
provide ownership to the parent contract, system and consensus.

Maybe there should be exceptions, such as to the voting system, even
consensus should never be able to change the voting state, nothing
should. Obviously the consensus system should not provide crud access
through consensus since it is redundant, so that is another exception.

Consensus should be able to change:

Experience: Incase someone was discovered to have exploited the system
in some way, the penalty could be the removal of experience.

Forum: Posts can be removed, modified through consensus only

Maybe each public crud function can have a consensus interface/protocol,
that must run middleware, from a middleware state, that is only
consensus accessible.

Example:

1.  SendPost()

2.  Loop through list of middleware calling OnPost on each

3.  A dataobject of a post is provided in OnPost as a parameter, this
    object has the post info of the incoming post request.

Since the default middleware of sendpost must modify the Experience
System state, and Claimable Experience state, how will it gain access to
those?
