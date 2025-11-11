Much about the design has changed in the past two years, and so the
architecture must have changed. I will revisit it.

# Positing

When a post is made, it will be associated with the account of the
poster.

After 24 hours if the poster does not have experience in the subject(s)
they initially tagged the post with, and the tag does not get downvoted,
they will receive 1 experience in each of those tags. When a post is
made with non exp tags, add post to a timer list, then certain events
will trigger a timer check, such as login, refreshing that post or
viewing account page. When the timer is checked and if a timer is ready
(1 day later after post) then check if there were any downvotes, if not,
provide the user 1 extra experience. This

Steps:

1.  Make post

2.  Add post to timer list.

What if experience needs to be claimed. So that only the user can
trigger a timer check. If the user does not check the post where they
are able claim the experience, they will not claim it.

Advantages: not everyone on the network has to check with each view,
only the poster; this is elegant since it only affects the poster. This
could also work for the voter. Ill refer to this concept as, reward
claiming, since it can maybe be used for every type of reward.

# Voting

When a post is upvoted it will update an array of tags with
corresponding vote count. This will create a record of the vote with
\['tag'\]\['user'\] = vote count. It will also create a display value of
the total tag counts: \['tag'\] = vote count. The display value will be
what is displayed to the client. The record will be used to verify or
calculate in the service.

### Question

If i have a list of message objects, and each message object can have a
tag, am I able to filter that message list by a specific tag(s)

# Experience

After 24 hours of posting the original poster gets experience. The tag
counts set the users experience with \['tag'\] = experience count. Any
vote after the 24 hours on the post, will immediately get added to the
user, as well as the display count of the post, and the record on the
post.

# Thoughts

Some part of the dapp exists on the blockchain or p2p, this is the
service. Another part exists on a host, this is the client or the app.
Ideally both need to exist in a manner which meets all the open systems
principles.

If the traditional host of the app shuts down, then the system can no
longer be used. The app must then be hosted on distributed cloud
hosting.

Then how is it updated? Multiple clients can exist at the same time, but
only one service can exist at the same time. Because the changes of a
client only affect the client, but changes in the service affect
everyone.

## Client update

Individual users can select which type of client they will use, from
various hosts. They can even build and run their own local version. Same
goes for mobile apps, there can be multiple versions. The app is updated
by whatever means the developer chooses to update the app by.

## Clients connecting to service

Wether its a domain, smart contract address or ip address, the clients
need to have some connection point. As long as that connection point
follows open principals there is no risk of the service being shut down
or the address being changed to point elsewhere.

In the case of gunjs, a signaling server is required for now.
