# Solution - Workshop 1 Reference

This is the instructor reference solution for Workshop 1.

Use it after participants have worked through the exercises.

Root workshop files:

- [`../SETUP.md`](../docs/SETUP.md): setup, providers, `.env`, SQLite, and prompt files
- [`../EXERCISES.md`](../docs/EXERCISES.md): ordered exercises with timings
- [`../ATTACK_PROMPTS.md`](../docs/ATTACK_PROMPTS.md): prompt-injection prompts adapted from AWS common attack categories
- [`../NOTES_TEMPLATE.md`](../docs/NOTES_TEMPLATE.md): reusable notes tables

## What This Solution Adds

- separates trusted policy from untrusted user text
- checks obvious attacks before model calls
- blocks hidden-instruction and synthetic-record requests
- blocks persona override, ignored-instruction, fake-completion, encoded, and obfuscated workshop attacks
- redacts the protected demo record from model output
- keeps normal in-scope prompts working
- stores chat messages one row at a time in plaintext for this workshop
- includes tests for prompt rendering, guardrail behavior, redaction, provider routing, and chat storage

## Run

From this folder after setup:

```bash
python manage.py runserver 127.0.0.1:8001
```

Open `http://127.0.0.1:8001`.

## Verify

```bash
python manage.py test
python -m scanner.scan_app
```



