## OWASP Top Ten Vulnberabilites
(Incorrect example is in comment, corrected version is outside)
### Broken Access Control
#### [1.](BrokenAccessControl/example1.js)

Four critical issues are fixed. First, any unauthenticated user can request `/profile/ANY_ID` and retrieve user's data as there is no check that a requester is logged in, or authorized for a specific profile. A attacker could simply iterate over userID values and harvest all user records. This is fixed by adding the auth middleware to verify the requester's session token, then comparing `req.user.id` against `req.params.userId` to make sure that only the user has access to their profile (Addresses OWASP A01). Second, there is a exposure because res.json(user) returns the entire database, usually including sensitive materials. This is fixed by chaining `.select('-password -resetToken -__v')` onto the query so the fields are stripped at the database layer before the response is built (Addresses OWASP A02). Third there is aother leak from `res.status(500).send(err)` which forwards raw node.js error to the client, which can reveal database type, collection names, an even internal IP addresses. This is fixed by replacing this line with `res.status(500).json({ error: 'Server error' })` and routing the error only to a server-side logger (`console.error`)(Addresses OWASP A05). Fourth and lastly, `req.params.userID` is passed directly to `findById()`, with no format validation, which can lead to Injection attacks. This is fixed by adding a `Types.ObjectId.isVaild()` guard, which rejects any value that is not a formed ObjectID before it reaches the database(Addresses OWASP A03).

#### [2.](BrokenAccessControl/example2.py)

Four vulnerabilites are fixed. First, any caller, they don't have to be authenticateed, can pass any `user_id` in the url and retrieve that account's data. This is fixed by adding a `@login-required` with Flask, so unauthenticated callers get a 401 automatically (Addresses OWASP A07). Second, this still leaves the problem of any logged-in user being ably to simply retreive someone else's data. This is fixed by after authentication, comparing the requested ID against the sessions `current_user.id`. Any mismatch is rejected with 403 before any DB query (Addresses OWAPS A01). Third, in `user = db.query(User).filter_by(id=user_id).first()` when no records match, `.first()` returns `None`. After, calling `.to_dict()` in `return jsonify(user.to_dict())` raises a AttributeError, which can dump imporant details in debug mode. This is fixed by checking for `None` explicitly, and calling a `abort(404)`, which returns a safe error (Addresses OWAP A05). Fourth and lastly, the `user_id` path segment is a plain string wiht no type enforcement. This is fixed by adding the `<int:user_id>` converter, which rejects any non-integer path before the function is called, returning a 400 on a bad match (Addresses OWASP A03).

### Cryptographic Failures

#### [3.](CryptographicFailures/example1)

