## OWASP Top Ten Vulnberabilites
(Incorrect example is in comment, corrected version is outside)
### Broken Access Control
#### [1.](BrokenAccessControl/example1.js)

Four critical issues are fixed. First, any unauthenticated user can request `/profile/ANY_ID` and retrieve user's data as there is no check that a requester is logged in, or authorized for a specific profile. A attacker could simply iterate over userID values and harvest all user records. This is fixed by adding the auth middleware to verify the requester's session token, then comparing `req.user.id` against `req.params.userId` to make sure that only the user has access to their profile (Addresses OWASP A01). Second, there is a exposure because res.json(user) returns the entire database, usually including sensitive materials. This is fixed by chaining `.select('-password -resetToken -__v')` onto the query so the fields are stripped at the database layer before the response is built (Addresses OWASP A02). Third there is aother leak from `res.status(500).send(err)` which forwards raw node.js error to the client, which can reveal database type, collection names, an even internal IP addresses. This is fixed by replacing this line with `res.status(500).json({ error: 'Server error' })` and routing the error only to a server-side logger (`console.error`)(Addresses OWASP A05). Fourth and lastly, `req.params.userID` is passed directly to `findById()`, with no format validation, which can lead to Injection attacks. This is fixed by adding a `Types.ObjectId.isVaild()` guard
2.

## Cryptographic Failures