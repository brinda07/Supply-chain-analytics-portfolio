# n8n Workflow Plan

## Intended flow

Manual trigger (first reproducible version) → select input file → identify dataset → parse CSV → normalize fields and types → validate required columns/keys → route invalid records → insert accepted rows into PostgreSQL staging → write batch counts/status to an audit table.

An optional email-trigger variant may be added later using a dedicated test inbox. Do not use personal email content in a public demo. Keep credentials in n8n's credential store/environment, not in exported workflow JSON or Git.

## Required safeguards

- Record source filename, batch identifier, and load timestamp.
- Detect unsupported file names, missing columns, invalid types, duplicates, and orphan keys.
- Make reprocessing idempotent; repeated ingestion must not silently double row counts.
- Reconcile input rows = accepted rows + rejected rows.
- Fail the workflow visibly on load errors and preserve a diagnostic message.
- Export JSON only after removing credentials, private email addresses, hostnames, and other secrets.

## Build status

Not implemented. Add the redacted workflow export under this directory after testing it against the actual files. The design will change once the schemas are inspected.
