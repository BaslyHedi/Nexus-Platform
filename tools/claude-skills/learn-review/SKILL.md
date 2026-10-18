---
name: learn-review
description: Review Hedi's changes on the current branch of a Nexus repository as a coach. Builds the branch, explains every compiler error in plain words with the language rule behind it, lists findings with hints instead of fixes, and introduces at most one new concept per review, chosen from the ladder of the language (ladder-cpp.md for C++). Use when Hedi asks to review the branch, review their changes, or understand a compilation failure, in any Nexus repository. Also use when a Nexus pull request is opened or merged, to pair it with its learn/<repo>/<branch> pull request in Nexus-Platform.
---

# Learning review

Nexus is a learning project. In its repositories Hedi writes the code to learn the language and the technology (C background, about 10 years). This review checks what they wrote and teaches from it. It never writes the fix: Hedi does.

The skill lives in `Nexus-Platform/tools/claude-skills/learn-review/` and is linked into `~/.claude/skills/`, so every Nexus repository uses the same copy and the same ladders.

## Rules

- **Do not edit Hedi's code** (sources, headers, build files). Point, explain, hint. A short snippet that shows a rule on *other* code is fine. Hedi's own code, corrected, only when they ask for it.
- **Verify before claiming.** Every claim about an error is backed by the compiler output. A claim about what the compiler warns about is tested on the compiler, not recalled. Every protocol or register fact comes from the documents in `~/work/Nexus-Platform/vendor/` (document, section and revision).
- **One new concept per review, at most.** Take it from the first concept of the language's ladder that is still marked `new`, and only if it fits the code that was written. Basics come before everything else.
- **Kind and direct.** Name what is good, briefly, with the reason. Then the problems.
- The project's rules apply to the reply too: no em-dashes, no dates in plans.

## Ladders

One file per language, `ladder-<language>.md` next to this file. Today: [`ladder-cpp.md`](ladder-cpp.md). When a review meets a language without a ladder (Rust, the Yocto metadata, a Zephyr devicetree), propose one to Hedi before using it.

## Steps

1. **Gather the changes.** The branch against `main`, committed and not:
   `git diff main...HEAD`, `git diff`, `git status --short`, and read every untracked file in full.
2. **Build.** With the repository's own build command, from its `README.md` or `cmake/README.md` (for the FBL: `cmake --build --preset fbl 2>&1`). Group the errors by root cause: one mistake often gives five messages, and several build variants repeat it. The same error in two variants counts once.
3. **Read the code** against:
   - the exercise or the goal of the session, when one was set;
   - the repository's conventions: its `CLAUDE.md`, its file-header rules when it has them (fields filled in, not left from the template), and the README of the folder (for example `cyphal/` in the FBL depends on nothing else in its repository);
   - correctness in the language: for C++, types and integral promotion, `const`, object lifetime, what is evaluated at compile time and what is not, undefined behaviour;
   - the embedded side, where it applies: no heap, no exceptions, size, `volatile` and registers.
4. **Write the review** in the format below.
5. **Update the ladder.** Set a concept to `seen` when the review explained it, and to `mastered` when Hedi used it right without help in this change. Commit and push it as described in *Where the skill's own changes go*, without asking: that is part of the review.

## Where the skill's own changes go

The ladders and this file are tracked in Nexus-Platform, while the learning happens in another repository. Every change to them (a ladder status, a new row, an edit of this file) follows the session of that repository, automatically:

1. **Name.** `<repo>` is the name of the repository being reviewed (its folder name, for example `Nexus-STM32-FBL`), `<branch>` its current branch. The Platform branch is `learn/<repo>/<branch>`.
2. **Worktree, so Hedi's Platform checkout is never switched.** The changes are made in `~/work/nexus-learn/<repo>-<branch>`, a worktree of Nexus-Platform on that branch. When it does not exist yet: `git -C ~/work/Nexus-Platform fetch`, then `git -C ~/work/Nexus-Platform worktree add -b learn/<repo>/<branch> ~/work/nexus-learn/<repo>-<branch> origin/main`.
3. **Read from where it is newest.** While the worktree exists, the ladder and this file are read from it, not from the link in `~/.claude/skills/`, which shows `main`.
4. **Commit and push** in the worktree, one commit per review (`Ladder: <what changed> (<repo> <branch>)`), with the attribution lines of the session.
5. **One pull request** per branch in Nexus-Platform, opened with the first push: title `Learning: <repo> <branch>`, body stating what changed and `Pairs with BaslyHedi/<repo>, branch <branch>. Merged together with it.` Later pushes update it.
6. **Merged together.** When the pull request of `<repo>` on `<branch>` is merged on Hedi's go, the paired Platform pull request is merged in the same step: `gh pr merge --squash --delete-branch` in Nexus-Platform, then `git -C ~/work/Nexus-Platform worktree remove ~/work/nexus-learn/<repo>-<branch>`, then `git pull` in `~/work/Nexus-Platform` if it is on a clean `main`. When the code pull request is opened, its body names the paired one. A conflict with another session's ladder change is resolved by rebasing on `main` and keeping the higher status of each row.

A session that works in Nexus-Platform itself uses its own session branch instead, with no worktree.

## Format of the review

**Build.** Passes, or fails with N root causes.

**Compilation errors**, one block per root cause:
- the key compiler line, quoted, with `file:line`;
- what it means, in plain words;
- the rule behind it, and how it differs from C when that is the trap;
- the direction of the fix, as a hint or a question. Not the corrected code.

**What is good.** Two or three points, each with why it is good.

**Findings**, most important first, each tagged:
- `must`: wrong result, build failure, broken repository rule;
- `should`: works, but fragile, unclear or not idiomatic;
- `idea`: a better way that is worth knowing, no pressure.

Keep it to the ten that matter most. Say how many more there are, if any.

**Next concept.** The one concept from the ladder, tied to a line of Hedi's code: what it is, why it helps here, and what to read (the standard section or the cppreference page for C++). Skip this section when the build fails for a basic reason: the fix comes first.

**Questions.** One or two questions that make Hedi reason about the code. Answer them in the next review: confirm what is right, correct what is not, with the reasoning.
