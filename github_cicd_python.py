import sys
from datetime import timedelta, datetime
import json
import re
import requests
import getopt
import urllib3
import os
import time
import html
from jira import JIRA
from bs4 import BeautifulSoup
import markdown

pr_number = os.getenv("PR_NUMBER")
repo_name = os.getenv("GITHUB_REPOSITORY")
# access_token = os.getenv("GITHUB_TOKEN")
access_token = os.getenv("GITHUB_TOKEN")
pr_url = os.getenv("PR_URL")

def extract_sql_queries(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        # Use a simple regular expression to match SQL statement
        sql_pattern = re.compile(r'\b(SELECT|UPDATE|INSERT|DELETE|CREATE|ALTER|DROP)\b', re.IGNORECASE)
        sql_queries = sql_pattern.findall(content)

        return sql_queries
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error extracting SQL queries: {e}")
        return []

def perform_code_review(get_file_name_flag=False):
    # Get the changed file paths from the pull request event payload
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files'
    response = requests.get(url, headers=headers)
    print(response)
    files = response.json()
    print(files)
    changed_files = [file['filename'] for file in files]
    if get_file_name_flag == True:
        return changed_files
    print(changed_files)

    file_contents = {}
    for file in files:
        file_url = file['raw_url']
        print(file_url)
        file_response = requests.get(file_url)
        print(file_response)
        file_content = file_response.text
        print(file_content)
        file_contents[file['filename']] = file_content

    print(file_contents)

def send_to_api(sql_queries, api_endpoint):
    try:
        data = {"sql_queries": sql_queries}
        response = requests.post(api_endpoint, json=data)

        return {"status": response.status_code, "content": response.text}
    except Exception as e:
        return {"status": 500, "error": f"Error sending to API: {e}"}

def post_comment_on_pr(comment, pr_number, github_token, repo_owner, repo_name):
    try:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"
        headers = {"Authorization": f"Bearer {github_token}"}
        payload = {"body": comment}
        response = requests.post(url, headers=headers, json=payload)

        return {"status": response.status_code, "content": response.text}
    except Exception as e:
        return {"status": 500, "error": f"Error posting comment: {e}"}

if __name__ == "__main__":
    # Get the path of the changed file from GitHub Actions context
    pr_file_path = os.getenv("GITHUB_WORKSPACE") + os.getenv("GITHUB_EVENT_PATH")
    print(pr_file_path)
    perform_code_review()
    # Get other details from GitHub Secrets
    api_endpoint = os.getenv("API_ENDPOINT_SECRET")
    repo_owner = os.getenv("REPO_OWNER_SECRET")
    repo_name = os.getenv("REPO_NAME_SECRET")
    github_token = os.getenv("GITHUB_TOKEN_SECRET")

    # Get PR number dynamically from GitHub Actions context
    with open(os.getenv("GITHUB_EVENT_PATH"), 'r') as event_file:
        event_data = json.load(event_file)
        pr_number = event_data["number"]

    # Extract SQL queries
    sql_queries = extract_sql_queries(pr_file_path)
    print(sql_queries)

    # Send SQL queries to API
    api_response = send_to_api(sql_queries, api_endpoint)

    # Post comment on PR
    if api_response.get("status") == 200:
        comment = f"SQL Queries extraction successful. API Response: {api_response}"
    else:
        comment = f"SQL Queries extraction failed. API Response: {api_response}"

    post_response = post_comment_on_pr(comment, pr_number, github_token, repo_owner, repo_name)
    print(post_response)
