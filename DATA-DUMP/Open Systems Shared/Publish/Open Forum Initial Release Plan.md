# **Technology Choices for the Open Forum**

The specifications of the Open Forum are predominantly
technology-agnostic. This flexibility presents an opportunity for a
thoughtful discussion regarding the most suitable technology stack for
the current implementation of the Open Forum. Over the last half-decade,
I have implemented the forum using diverse technology stacks. The latest
proposal incorporates a mix of a gossip network, specifically GunJS, and
a Solana blockchain.

## **Leveraging Gossip Network and Blockchain**

The use of GunJS coupled with Solana blockchain would facilitate
cost-free posts for users, adding significant value to the platform. The
existing and preliminary release solely utilizes GunJS, thereby
embodying the principle of a \"first admin\" --- the first account
created assumes the admin role. This feature allows basic moderation
actions like post removals, which users can verify by checking the
signature of the super user.

However, it\'s important to note that these \"removed\" posts aren\'t
permanently deleted. Instead, they are relocated to a \'removed\' node,
making them invisible by default in the main post list while preserving
their existence. Simplicity was key in this initial release, leading to
the decision of not incorporating blockchain features.

A consideration for the next phase could be a blend of a gossip network
and blockchain, or even exclusively blockchain. These decisions should
be the subject of an informed and detailed discussion with a definitive
conclusion.

## **Task List: Finalizing the Open Forum Initial Release**

The finalization of the Open Forum Initial Release will comprise the
following key features:

### **1. Single Admin Moderation**

This will provide the admin with the ability to moderate the platform by
removing accounts and posts as necessary.

### **2. Single Admin Invitation**

The invitation to create new accounts will be solely under the control
of the admin.

### **3. Account Activation for New Users**

New users will be restricted from making posts until their accounts are
activated, ensuring a level of control and moderation in the initial
stages of their involvement.

### **4. Admin Oversight of Pending Accounts**

The admin will be able to see a list of pending accounts and activate
them at their discretion. This feature allows an additional level of
control and oversight for the admin, ensuring quality and adherence to
platform guidelines.

In conclusion, these planned improvements aim to enhance the forum\'s
functionality and user experience while maintaining the integrity and
quality of content shared.
