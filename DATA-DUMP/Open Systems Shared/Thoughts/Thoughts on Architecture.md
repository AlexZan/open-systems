Any content you submit is a content item (CI).

It will be able to hold media (text,image, video, audio) and a reference
to post children

Examples:

1.  A post will have a title and body and a list of post children

2.  A goal will hold a title, detail, bounty and a list of post children

3.  A suggestion will hold a body, an update, and a list of poste
    children

Each content item gets an action bar with:

1.  Upvote

2.  Downvote

3.  Reply (auto follow) : CI

4.  Report

5.  Commit

6.  Follow

7.  Edit : CI

CI:

0:parent

1:data

2:children

## Should any CI have all actions apply to them?

If a suggestion is a ci, then a suggestion should not be able to have a
suggestion.

What about in the rare case where an edit gets many votes, but then one
user realises there was a grammatical error everyone missed, or
something about the initial post changed, so that edit needs to be
edited so that it doesnt need to start the vote again. In this case the
vote should start again, because as long as any aspect about what you
are voting on changes, then the vote should be redone.

## Should there be CI action disables?

Since some ci's should not have some actions, should there be a list
with disabled actions? Edit seems to be the only action that creates a
CI which should not have all the actions, should then an Edit be a CI?
People will need to upvote or downvote it, and comment on it.

## Should some CI's have extra actions?

When voting if a goal is completed, in order to hand out the bounty,
starting the completed vote will require users to vote on the completed
vote. In other words, when a user thinks the vote is completed, they can
suggest the goal is completed, if the vote is passed, the goal will be
completed.

## Upvoting a goal or post is not the same as upvoting on it being completed. This needs to be made clear.

Upvoting and downvoting are really only used to increase or decrease
visibility of a CI. so then should it be called something else?

It does not mean you like or dislike it. If a post is made about
something tragic, you might want to increase its visibility, but it does
not mean you like it, agree with it, or approve of it.

What about up and down, without the use of the word vote. That way its
clear, by upping something, you are upping its visibility. Other
options:

1.  Increase/Decrease

2.  Up/Down

3.  Upping/Downing

4.  Upit/Downit

5.  +1/-1

## If a post can contain goals created by the OP, then what is the point of upping a goal made by the op, it does not change its visibility?

Based on the no authority principil, than a goal made by the op, should
not have any special privilage over any other goal made for that post.

Therefore goals non op, should function in the same place, and be held
in the same place.

Therefore, there should be no special section for OP goals, or any Op
content for that matter, except for Title and Body.

## Posts should have section views, that users can manipulate

A post will begin by showing the following section views in default
order:

1.  Title

2.  Body

3.  Goals

4.  Replies

Each of these section views, will have their own area below which can be
expanded to show CI replies, which are replies specific to that section.
E.g. replies made for a specific goal will be shown when the goal is
clicked. Not just replies but any information pertaining to goals will
show in the goal section.

## How does suggesting work?

Every post will have an edit button. This will open up that post into
its edit view. You then press the suggest button. Now when a user hovers
over the post, they will see a badge with the suggestion count. Clicking
this badge opens up the post in a separate post view. This will show all
the suggestions below. Each suggestion is its own post.

\*\*thought, maybe instead of post, the unit level item can be called
content or content item: CI, and this concept as recursive content.

Suggestions get their own action bars, since they are also content
items. And are sorted based on upvotes by default.

## How do votes pass for suggestions? How do editors get shares for their contributions?

A suggestion will get upvoted, what is the threshold where it gets
accepted?

What about anyone that has committed to the parent post has to vote on
it, when it passes half of the commited votes, it pass.

A history of all changes is kept. Any content can have its change
history accessed.

## How do editors get shares for contributions?

Maybe there will be a standard division of shares. E.g:

1.  5% for editing

2.  5% for posting

3.  90% other

If there is one suggestion accepted, then the editor gets the full 5%,
if there are two edits accepted from two different editors, then they
each get half of the 5% or 2.5%

## The general pattern behind who gets to vote?

Whoever commits to a content item is responsible for it. If you commit
to a large post with 10 goals, 30 edit suggestions.

## Actions and Voting

All actions must be voted. An action can be the following:

1.  Editing a content item

2.  Completing a goal

3.  Deleting a content item

4.  Moving a reply item into the main post

    a.  Such as a

## Client View

How a user chooses to view the data of OW is up to them, what client
they choose is up to them. There is no official view and no official
client.

## How does the original poster get share?

Just a default 5%, this can be modified maybe with the share + and -
button.

## Maybe there should be a list of votable items

This will show as a notification hover bubble or something on the
periphery of the app. When a user clicks this, they can see every
actionable item waiting on a vote.

## All content item posts will require different karma unlocks, and some might even cost karma?

In order to reply with text it will cost 10 karma, and you must have
over 10% of the posts karma to reply. You get 1 karma back for every
upvote, and lose further karma for downvotes.

Therefore every interaction is an investment. Is this desired? Yes a
good identity is something viable for the foreseeable future.

## Starting a vote should cost?

Maybe when a user suggests a vote for something, in order to begin the
vote, it will cost them karma. If the vote passes maybe it doubles? If
it does not pass, they do not get the karma back.

# Architecture

The core object will be the content item or CI. This will have a parent
reference, content, an op (original poster) and a list of children
references. Should call object; content.

1.  A post will be a CI that has an object with a title and body
    property.

2.  A reply will be a CI that has an object with a title and body
    property with its parent reference set to another CI. the only
    difference between a post and a reply is that it has a parent
    reference.

3.  A vote will be a CI that has its parent reference set to the CI that
    is being voted on, the object will contain a body and votetype

    a.  Vote types: GoalComplete, SuggestionAccept

4.  A suggestion will be a CI vote type, that has the parent reference
    set to the CI it is modifying, modification data as its object
    (which must match the structure of the parent object structure)
    along with the vote type as SuggestionAccept.

A collection of contentItems will hold all of the CI's.

To get the list of posts, a server will get the CI's that dont have a
parent, and create virtuals showing bounty, goal count, replies,
priority (ups vs downs)

To display a list of posts, the client will display

## Alternate

There could be a post type, with a mixed list of other types, such as
post, goal, etc. the parent could be a mixed type also. The idea is then
there is no need for a general CI post type to wrap the concrete CI
types.

### The child list could just have a type id, with the object id reference. 

The downside to this is that a standard populate would not be able to be
used, but would have to be done with an aggregate.

What is the benefit of it being true recursive?

### Is there a benefit to wrapping with a general type?

1.  It will include all of the CI functionality in one place

### What is the downside?

1.  Don\'t know what type of post it is, will have to manually track
    somehow.

Or there could be a post type with a list for each other type. The
downside to this is the post type will have to keep changing when a new
CI type gets introduced.

### The question is, will every every CI have a list of every CI?

As i thought earlier, an edit CI will not have an edit CI. But it is
easy to remove a property.

Could have javascript inheritance, with a base CI object, and specialty
objects that add content. Then there would be a collection for every ci
type.

If a collection is a subdocument, is it easy to retrieve on its own?
E.g. if a user just wants to link a single goal from a post. It would be
parent+goal id's. What about something that is very deep, which has 10
parents.There will be a good amount of recursive searching. If all CI
types were all on their own list, it would be a direct link to a single
id and so much faster.

So then should each CI object have a list for each CI type.

If each CI type will have its own child list for each CI type, then what
type is the parent?

## What is the benefit of having replies with posts in one post collection, vs having replies part of the parent post?

1.  Up: searching for a reply might be faster than recursive searching
    through all posts and any recursive replies

2.  Up: Might be easier to link a reply as a reply to another post (if
    it has a good general answer)

    a.  Is this better than linking the whole post? Linking the whole
        post might provide context. In the case of a duplicate question,
        it should probably get merged.

3.  Down: searching for a post might have to be include all replies
    also, potentially slowing it down.

## What is the benefit of having replies with posts in one post collection, vs having a separate replies collection?

1.  One search for all posts wether its a main post or a reply

2.  There really is no difference between a reply and post other than a
    reply has a parent, maybe a reply wont have a title? Or maybe its
    optional

3.  

The front end actions need to be generic, to be able to operate on any
CI. By having each CI in a separate list, there is no way to determine
what type of CI has the requested action. there is no way to determine
what collection the id for the required for. The backend can have a
different end point for each CI type. But the front end component now
needs to worry about which endpoint to call. It will require a seperate
action, component, path, collection for each CI. Therefore seperating
the CI's should be reassessed. By having a single ci collection, we can
add and remove any CI item with a single component, action, endpoint.

But by putting all ci's in one collection, population can still happen
from that one collection.

The front end should split up the CI's depending on their type into
seperate collections in each parent CI. that way the UI or individual
component is not responsible for that logic.

## Dynamic Recursive Populate with Aggregation

Now the challenge is how to recursively populate children with aggregate
functionality.

Maybe i dont use aggregate, i calculate the upvote when the upvote is
made, and store it, then i have the upvoteUsers as a record to just
double check against if needed. Why use gas calculating upvotecount each
query, instead of doing it just once when the upvote happens.

I then dont even need to keep the upvoting records in the post any
longer if thats needed for wahtever reason.

\[11:18 PM, 2/27/2019\] Alexz: instead of having the server figure out
if you up\'d or down\'d any of the posts you requested (which is a ton
of iterating) what do you think if I store what posts the user
up\'d/down\'d with the user instead. Then when they load the app, i send
over both those lists, and now the client checks if the post they are
viewing matches the local list id of up\'d/down\'d posts

\[11:19 PM, 2/27/2019\] Alexz: I can even keep it in localstorage, so
that i only need to send it once, and then i just update local and
remote seperatly

\[11:19 PM, 2/27/2019\] Alexz: infact thats how all local requests
shoudl be handled, they are stored locally, and the server never has to
send that data except initially and on errors

## Question:Which will take more storage/processing. Storing users in posts, or posts in users?

Which will be smaller? There are probably many more posts than users.

If there was one user, and 10 posts, then the user would be stored on 10
posts one way, or there would be 10 posts saved in 1 user. Possibly the
same size.

There are many more sub collections to manage if we save user in posts,
therefore more processing.

For now ideally its best to store the posts in the user.
