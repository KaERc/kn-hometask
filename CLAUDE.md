# kn-hometask

Home assignment: a REST API to maintain a list of shipments (Django REST framework) with a small Vue 3 frontend.

## Working rules

- Write the smallest thing that works. Use the standard library and installed packages before new code or new dependencies; add nothing speculative. A deliberate shortcut with a known ceiling gets a `ponytail:` comment naming the ceiling and the upgrade path.
- Test first: failing tests are committed before the implementation they cover. The frontend has no automated tests and is checked by hand.
- Branches are named subproject/epic/task, for example `api/shipments/crud`, and merged with `--no-ff`. Commits are few, each one a finished step, with English messages. Push only when asked.
- `DESIGN.md` is the source of design tokens. CSS takes its values from it, and anything in it that the app does not use gets removed.

## Commands

Backend:

```bash
uv venv --python 3.12 && uv pip install -r requirements-dev.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
.venv/bin/python manage.py test
.venv/bin/coverage run --source=shipments --omit='*/migrations/*,*/tests.py' manage.py test && .venv/bin/coverage report -m
.venv/bin/ruff check . && .venv/bin/ruff format --check .
```

`.github/workflows/ci.yml` runs the same checks plus `makemigrations --check`, `npm ci`, `npm run build` and the DESIGN.md lint.

Frontend (Node 20.19+ or 22.12+):

```bash
cd frontend && npm install
npm run dev    # Vite on :5173, proxies /api to Django on :8000
npm run build
```

Design tokens:

```bash
npx @google/design.md lint DESIGN.md
```
