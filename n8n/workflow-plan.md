# Optional n8n Reference — Not Required for the Core Project

You can skip n8n and still complete the supply-chain analyst portfolio project. The core path is to validate the generated data, load PostgreSQL using the documented import steps, write and verify SQL analyses, and create a reconciled dashboard and project brief.

The file [`csv-to-postgresql.json`](csv-to-postgresql.json) and these notes are retained only as reference material for a possible later automation extension. The workflow has **not** been imported or executed against your n8n instance or PostgreSQL database. Do not claim it as a completed project component.

## Important version note

Your n8n version is 2.4.6. The repository workflow JSON uses PostgreSQL node version 2.8. The official n8n 2.4.6 source defines PostgreSQL node versions only through 2.6, so this export should not be treated as compatible with your installation. The version map is visible in the [official n8n 2.4.6 PostgreSQL node source](https://github.com/n8n-io/n8n/blob/n8n%402.4.6/packages/nodes-base/nodes/Postgres/Postgres.node.ts).

Do not spend time importing or debugging this optional export while completing the core analyst project. If you later decide that workflow automation is valuable for your portfolio, create or adapt an export for the installed n8n version, then verify import, credentials, local file permissions, table mapping, and end-to-end behavior before documenting it as built.

## Optional future test scope

If you implement the extension later, use only the synthetic clean files for successful loads and keep `data/fixtures/` out of analytical tables. Verify the accepted/rejected counts, database row counts, constraint behavior, and duplicate-load handling. Store credentials in n8n’s credential manager, never in the exported JSON or Git.
