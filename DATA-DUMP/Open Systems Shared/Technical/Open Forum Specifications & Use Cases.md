# Message Posts

1.  If there are no posts yet, a message will say nothing posted yet

2.  A loading message will appear before messages are loaded in

3.  There will be a new post UI above the message posts, only when the
    user is logged in

4.  Last posts will be shown first

5.  Clicking on a post in the post list will show the individual post
    view

# Login

1.  A user will be notified if they have successfully logged in

2.  A user will be notified if there was a problem logging in

# Header

1.  A user should be able to logout by pressing the logout button in the
    header

# Register

1.  A user will be automatically logged in after successfully
    registering

2.  A user will be notified if the alias or email already is registered

# General

1.  A status at the top of the app, will indicate whether the user is
    online or offline.

# Profile

1.  A logout button in the profile page lets the user log off.

# Reasoning

It is simpler to not allow the user to change their name, they can only
set it once on the register. Later on we can add those anonymity
features.

# First Release Specification

1.  SUM features

2.  Non activated accounts can not post

3.  Super user unlimited activations.

# Utility Token Release Specification

The first user account on the system will be the super user. The super
user will have access to extra settings on their profile page. They will
be able to set the max user count. Users can not create an account
without an invite token.

## Utility Token System

1.  User Token Wallet: Each user would have a \"wallet\" associated with
    their account where tokens are stored. This could be a field in the
    user\'s data node that starts at 0 and increases as they earn
    tokens.

2.  Token Generation: Every 24 hours, users are able to claim a token.
    When a token is claimed, it would add the token to the user\'s
    wallet. A function will calculate if a day has passed since the last
    claim, and allow the user to claim the token. If the user tries to
    claim the token before a day has passed, they will be given a
    notification with the time remaining. When a user makes a new
    account they will get their first token immediately and must wait a
    day for the next one.

3.  Token Spending: Users spend tokens when they post or send an invite.
    When a user creates a post or sends an invite, the system would
    deduct a token from their wallet. If the user does not have enough
    tokens, they would be prevented from completing the action.

4.  Invite Tokens: When a user sends an invite, they would spend a
    certain amount of utility tokens (for example, 5 tokens). The
    invitee would receive an invite token, which they could use to
    create a new account.

5.  Token Limit and Accumulation: Users have a maximum limit of tokens
    they can hold (for example, 10 tokens). If a user hits their token
    limit, they stop accumulating new tokens until they spend some. This
    could be enforced by a condition in the token generation function
    that checks if a user has reached their limit before adding a token.

6.  Token Claim Bonus: Each time a user claims tokens they increase a
    claim count value. Each time this claim count value doubles, the
    user is able to generate an extra token every 24 hours. E.g. If a
    user has claimed tokens 2 times, they are now able to generate 2
    tokens every 24 hours. If a user has claimed tokens 4 times, they
    are now able to generate 3 tokens every 24 hours. If a user has
    claimed tokens 8 times, they are now able to generate 4 tokens every
    24 hours.

7.  Moderation Strikes and Penalty: If a user receives a moderation
    strike, they would lose their tokens and stop generating new ones.
    This could be implemented as a function that is called when a user
    receives a strike. The function would set the user\'s token count to
    0 and set a flag on their account that prevents them from generating
    new tokens.

8.  Super User Control: A \"super user\" can set a maximum user limit to
    control the growth of the community. The token generation process
    would also check this limit and stop generating new tokens for
    invites if the limit is reached. Account creation would also be
    disabled when this limit is reached.

9.  
