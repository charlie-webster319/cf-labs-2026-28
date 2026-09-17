# Instructor setup — 2026–27

[Classroom and assignments](https://classroom50.org/ustandrews-ec3318-mn3101/cf-2026-27/assignments) · [Roster](https://classroom50.org/ustandrews-ec3318-mn3101/cf-2026-27/roster) · [Assignment settings](https://classroom50.org/ustandrews-ec3318-mn3101/cf-2026-27/assignments/python-labs/settings)

## Configured

- Classroom: **EC3318/MN3101 Corporate Finance 2026–27**, term 2026–27, slug `cf-2026-27`.
- Assignment: **Corporate Finance Python Labs**, slug `python-labs`, individual, containing both labs.
- Starter: private template `ustandrews-ec3318-mn3101/cf-labs-2026-27`, default branch only.
- Private student repositories, Write access, feedback pull requests enabled; student Pages disabled.
- Not graded; built-in autograder disabled; no deadline. Submission mode is tagged commits so routine notebook autosaves do not count as formal submissions. Students do not need to submit tags for these formative labs.
- No release date: distribute the acceptance link directly when ready. Accepted students retain access to the assignment. Classroom assignment metadata uses an unlisted URL; this is not access control for that metadata. Repositories remain private.
- The instructor validation workflow runs only in the exact starter repository. Student copies have a separate manual **Check my notebooks (optional)** action.

## Before students start

1. Add this year's students using university email addresses or GitHub usernames. A CSV with an `email` column is sufficient; names and section are optional. Email invitees must add and verify the invited address on their GitHub account before accepting. Classroom 50 links their account when they accept. Do not import a previous cohort automatically. See the [roster guide](https://github.com/foundation50/classroom50/wiki/Web-Teacher-Guide#invitations-by-email) and [GitHub invitation requirements](https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization).
2. Pilot acceptance with one rostered student. Check that their new repository is private, permits writing to their own work, opens in Codespaces, executes the first notebook cell, syncs a saved change and has a feedback pull request. Check their own Codespaces allowance; the instructor pilot does not establish student billing or eligibility.
3. On the assignment's **Submissions → Share** dialog, copy the full accept link, including its query string, to the appropriate Moodle activity. The link alone does not enrol students. Moodle was not changed during this setup.
4. Students accept once and use the same repository and Codespace for both labs. Refer them to its README.

The service token was generated and saved directly by Christian. Its selected expiry was **15 January 2027**; renew it before further use after that date. No token value is stored in this template or its verification records.

## Verification

The [classroom publication run](https://github.com/ustandrews-ec3318-mn3101/classroom50/actions/runs/35213264721) completed successfully on 17 September 2026. The roster contains Christian as teacher and one enrolled test student, `christian-engels-25`. The test student accepted the assignment and opened a Codespace. Their generated repository is private, grants them Write access and has an open feedback pull request. Student-account notebook execution and sync after the startup fix still need checking. See [implementation verification](verification.md) for the completed installation, notebook, financial, plot and Codespaces checks.

## Education seat follow-up

A test email invitation later failed with `No seats are available to invite this user`. The organisation had one Team seat, already occupied. The free academic organisation upgrade was requested through Christian's verified teacher benefits; the licensing page then showed $0.00. Christian retried the invitation successfully and the test student joined the organisation. No cohort invitations were sent by the agent.

## Updating an existing Codespace after the startup fix

New assignment copies inherit the corrected template. Existing repositories do not automatically receive template updates. The two configuration files were also updated in the test student repository. In that existing Codespace, run `git pull --ff-only`, then use **Codespaces: Rebuild Container** from the Command Palette. This keeps notebook work; if Git reports a conflict or divergence, inspect it rather than resetting or force-pushing.
