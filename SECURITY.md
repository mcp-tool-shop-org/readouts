# Security Policy

## Supported versions

readouts is a rolling corpus. The `main` branch is the only supported version: every publication is a commit on `main`, and [CHANGELOG.md](CHANGELOG.md) lists what each one changed. Older commits are not patched.

## What counts as a security problem here

readouts is data, so its risks are mostly about what the data contains:

- **Exposed personal data or credentials:** an email address, a home-directory path, a token or a key inside a database, a wave file, a log or a script.
- **A script that does more than it says:** anything on the read path (queries, `verify.py`, the generators) that opens a network connection, reads credentials, or writes outside the checkout.
- **Content that could hurt someone who follows it:** a verified entry whose instructions are unsafe to run as written.

A wrong or outdated fact is not a security problem, but it is still worth reporting as an ordinary issue.

## Reporting

Report it by opening an issue at https://github.com/mcp-tool-shop-org/readouts/issues.

- For exposed data, name the file and the line or database row. **Do not paste the sensitive text itself into the issue.**
- For a script, name the script and the command you ran.
- Do not include your own credentials or keys in a report.

### Response timeline

| Action | Target |
|--------|--------|
| Acknowledge the report | 72 hours |
| Remove exposed data from `main` | 7 days |
| Fix a script | 30 days |

Removing data from `main` does not remove it from git history. When a report shows exposed data in an earlier commit, the reply says whether the history was rewritten.

## How the repository guards itself

- Every publication is exported from a private working repository by a script that refuses to finish unless four gates pass. They check for studio identity, home-directory paths in any spelling, private project names, and links to files that do not ship.
- `python verify.py` runs in CI on every push that changes the corpus.
- The read path has no network access, reads no credentials and sends no telemetry. The research tooling that built the waves can call model APIs, but only with keys you supply in your own environment; no key is stored in the repository. See the threat model in the [README](README.md#security-and-threat-model).
