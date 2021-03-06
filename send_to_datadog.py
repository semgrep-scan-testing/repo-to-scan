import requests
import os
import sys
from github import Github

run = int(sys.argv[1])
g = Github()
repo = g.get_repo("semgrep-scan-testing/repo-to-scan")
wf_run = repo.get_workflow_run(run)
jobs_url = wf_run.jobs_url
jobs_resp = requests.get(jobs_url)
jobs = jobs_resp.json()['jobs']
scan_job_status = [j for j in jobs if j["name"] == "Scan"][0]["conclusion"]

text = "success" if scan_job_status == "success" else "error"

logs_response = requests.post("https://http-intake.logs.datadoghq.com/v1/input",
                              headers = { "DD-API-KEY": os.environ.get("DD_API_KEY") },
                              json={
                                  "ddsource": "github-actions-scan",
                                  "ddtags": "env:prod",
                                  "message": text
                              }
                              )

print(logs_response.status_code)
print(logs_response.text)
