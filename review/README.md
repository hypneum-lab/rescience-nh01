# Independent review before submission

Two automated review passes were run on this package on 2026-10-31,
before any human review, with OpenAI models driven through the Codex CLI
(v0.162+, `--search`, reasoning effort `xhigh`, sandbox `workspace-write`
on a scratch copy; nothing in the repositories was modified by the
reviewer). Every finding was then checked by the author's assistant
against the cells, the summaries, the runner code and the original
paper before any change was made; the verdict table records what was
confirmed, nuanced or rejected, and what was done. Open points were
decided by the PI.

| File | Content |
|---|---|
| `2026-10-31-brief-pass1-blind.md` | brief of pass 1: blind review (`gpt-6.1-sol`), repositories only, no access to the author's conclusions |
| `2026-10-31-report-pass1-blind.md` | report of pass 1 (10 596 words, 278 876 tokens, 10:41–11:03 CET) |
| `2026-10-31-verdicts.md` | verdict table, pass 1 then pass 2: finding, verification, verdict, action |
| `2026-10-31-brief-pass2-cross.md` | brief of pass 2: cross review (`gpt-6-astra`) of the corrected package and of the verdict table; the blind report was not given to it |
| `2026-10-31-report-pass2-cross.md` | report of pass 2 (6 791 words, 177 956 tokens, 11:13–11:23 CET) |
| `2026-10-31-article-before-review.md` | `article/article.md` as it stood before pass 1 (commit `2addde6`) |

Outcome in short. Pass 1 found one blocking statement (the conclusion
claimed that every stored pattern is a fixed point up to load 0.95; the
pilot data contradict it) and confirmed every number of the article by
an independent recalculation over the 66 840 cells. Pass 2 judged 20 of
the 30 corrections right, 8 insufficient and none wrong, found one new
error (the Hebbian network has 51/320 spurious final states at load
0.14, not "almost only"), and argued that the registered ratio at
m = 0.30, T = 0 (44.38) had to be reported next to its reservation
rather than withheld; the PI followed that argument. The two reports are
reproduced verbatim; their paths refer to the reviewer's scratch copy.
The reviewers' findings are not endorsements, and the human review of
ReScience C is the one that counts.
