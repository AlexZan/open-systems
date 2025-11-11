When structuring your \"removed\" node, you have two primary options:

1.  Maintain the hierarchical structure: In this approach, you preserve
    the relationship between a message and its replies. When a message
    is removed, all of its replies are removed with it and retained in
    the hierarchical structure. This would allow a user to view the
    removed post and all of its replies in a nested fashion. However, it
    could become complicated if you want to restore a specific reply
    without restoring the entire message. If only a single reply is
    removed, it should still show up as part of its parent message, even
    if the parent message isn\'t removed.

2.  Flatten the structure: Here, you treat each removed item (message or
    reply) as an individual entity. This makes it easy to manage
    individual removals and restorations, but it could make it harder to
    view the context of a removed reply, especially if its parent
    message isn\'t removed. This approach might require additional
    metadata to link a reply back to its parent message.

The best approach really depends on your specific use case and how you
want your users to interact with the removed items.

If it\'s important for users to understand the context of a removed
reply, option 1 might be a better choice. But if you want more
flexibility in managing individual removals and restorations, option 2
could be a better fit.

Remember that deletion is a sensitive operation, especially in a social
context. When designing this feature, make sure you consider user
privacy, data permanence, and any potential for misuse or harassment.
