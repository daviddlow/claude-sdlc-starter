---
name: brand-voice
description: Apply the product's voice and UX writing standards. Use when
  writing or reviewing any customer-facing copy — UI text, next_step
  messages, error messages, or portal content.
---
# Brand voice and UX writing

Customer-facing text (including the `next_step` and error strings in the
claims API) follows these rules:

1. Speak to the customer directly ("Your handler is reviewing…"), never
   about them in the third person.
2. Plain words: "sent", not "remitted"; "reviewing", not "adjudicating".
3. Every status message says what happens next or states that nothing is
   needed. Never leave the customer without a next step.
4. Error messages state what went wrong and what to do, and never expose
   internals (stack traces, table names, upstream system names).
5. No exclamation marks; no blame ("you failed to…" → "we couldn't find…").

When a policy owner updates these rules, update this skill in the same PR
and have them sign it off — engineers pick up the new version automatically
in their next session.
