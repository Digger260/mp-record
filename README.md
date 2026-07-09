# MP Public Record Directory

A read-only signposting site for UK Members of Parliament. For every current MP, it collects direct links to their **official public records** in one place:

- Parliament profile and voting record (members.parliament.uk)
- Register of Members' Financial Interests
- TheyWorkForYou profile
- Electoral Commission donations search
- IPSA expenses
- Companies House officer search

## What this site is

A directory. It publishes **no commentary, no claims, and no user-submitted content** — only links to records published by Parliament, regulators, and government bodies themselves.

## Contributions

This repository does not accept pull requests or issues for content. All pages are generated automatically from the official [UK Parliament Members API](https://members-api.parliament.uk/). If a link is broken or an MP's details are out of date, re-running the generator fixes it.

## Setup

1. Create a repository on GitHub and push these files.
2. Generate the MP pages:
   ```bash
   pip install requests
   python scripts/fetch_mps.py --refresh
   ```
3. Commit the generated files in `mps/`.
4. Enable GitHub Pages: **Settings → Pages → Deploy from a branch → main**.
5. Your site is live at `https://yourusername.github.io/<repo-name>`, with a search box over all MPs by name, party, and constituency.

Re-run the script any time (after a by-election, reshuffle, or general election) — `--refresh` regenerates every page from the live API.

## Licence

Code: MIT. All linked records remain the property of their respective publishers.
