---
name: intent-capture
description: Capture an idea, ticket, or incident as an intent.md proto-spec
  in the organization's template. Use whenever someone describes a problem,
  a feature idea, or an improvement they want, or asks to "write this up",
  "capture this", or "create an intent".
---
# Intent capture

You are helping an originator — often not an engineer — turn an idea into a
committed `intent.md`, the artifact that starts the SDLC loop.

1. Let them describe the problem in their own words. No formal language is
   required. Brainstorm until the idea is concrete; ask the questions an
   analyst would ask:
   - What can't you do today, and who is affected?
   - What does better look like? How would we know it worked?
   - What is out of scope?
   - What constraints apply (data, auth, regulation, systems)?
2. Write the result using `templates/intent.md`: Problem, Proposed outcome,
   Affected users and systems, Constraints, Open questions. Keep the
   originator's own terms — do not translate into engineering language.
3. Show the draft and let the originator correct anything you misunderstood.
4. Save it as `intent/<short-change-name>/intent.md` with the originator as
   Author and Status: draft, then commit it. Author and timestamp join the
   git record; the product owner picks the idea up from there.

Never invent requirements the originator didn't state — unknowns go under
Open questions, not into the Proposed outcome.
