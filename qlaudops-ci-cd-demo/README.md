# QlaudOps CloudOps Command Center — CI/CD Demo

A responsive CloudOps dashboard designed for a practical CI/CD presentation. It includes cloud spend, service health, backup status, recent activity, and a sample pipeline run. **All metrics, service states, and activity records are illustrative demo data, not live QlaudOps or AWS telemetry.**

## Stack
- Python standard-library HTTP server (no third-party runtime packages)
- Responsive HTML, CSS, and JavaScript dashboard
- Automated `unittest` tests
- Docker image with non-root runtime user and health check
- GitHub Actions: tests and syntax checks first; Docker build runs only if tests pass

## Run locally (Windows PowerShell)
Install Python 3.10+ if needed, then run:
```powershell
python app.py
```
Open `http://127.0.0.1:5000`.

## Run tests
```powershell
python -m unittest discover -s tests -v
```

## Run with Docker
```bash
docker build -t qlaudops-cloudops-demo .
docker run --rm -p 5000:5000 qlaudops-cloudops-demo
```
Open `http://127.0.0.1:5000`. The container health check calls `/health`.

## CI/CD demo: successful change
1. Create a GitHub repository and push this project to the `main` branch.
2. Change a visible label in `index.html` or update the test data in `app.py`.
3. Commit and push. GitHub Actions runs tests and syntax checks, then builds the Docker image if tests pass.
4. Open the **Actions** tab and inspect each green stage.

## CI/CD demo: intentional failure
1. In `tests/test_app.py`, temporarily change the expected health status from `healthy` to `broken`.
2. Commit and push to a feature branch and open a pull request, or push to `main` for a direct demo.
3. The test job fails and the `docker-build` job is skipped because it depends on `needs: test`.
4. Open the failed test logs, restore the expected value to `healthy`, commit, and push again.

**Important:** a failed pipeline does not undo a Git push. It blocks later workflow stages (here, the Docker build). This starter does not deploy to AWS or push images to a registry; that needs configured credentials, environment approvals, and a deployment target. Never commit AWS keys to the repository.

## Endpoints
- `/` — dashboard
- `/health` — JSON health check
- `/api/services` — demo service status JSON

## Project layout
```text
app.py
index.html
static/styles.css
static/app.js
tests/test_app.py
Dockerfile
.dockerignore
.gitignore
requirements.txt
README.md
.github/workflows/ci-cd.yml
```
