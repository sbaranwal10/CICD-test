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

def extract_sql_statements(content):
    # Split content into lines and filter lines containing SQL keywords
    sql_lines = [line.strip() for line in content.split('\n') if any(keyword in line.upper() for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER'])]

    return sql_lines

def get_raw_file_content(get_file_name_flag=False):
    # Get the changed file paths from the pull request event payload
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files'
    response = requests.get(url, headers=headers)
    files = response.json()
    changed_files = [file['filename'] for file in files]
    if get_file_name_flag == True:
        return changed_files

    file_contents = {}
    for file in files:
        file_url = file['raw_url']
        file_response = requests.get(file_url, headers=headers)
        file_content = file_response.text
        file_contents[file['filename']] = file_content

    print(file_contents)
    return file_contents

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
    content=get_raw_file_content()
    # Get other details from GitHub Secrets
    api_endpoint = os.getenv("API_ENDPOINT")
    repo_owner = os.getenv("REPO_OWNER")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    github_token = os.getenv("GITHUB_TOKEN")

    # Extract SQL queries
    for filename, content in content.items():
        sql_statements = extract_sql_statements(content)
    print(sql_statements)

    # Send SQL queries to API
    api_response = send_to_api(sql_statements, api_endpoint)

    # Post comment on PR
    if api_response.get("status") == 200:
        comment = f"SQL Queries extraction successful. API Response: {api_response}"
    else:
        comment = f"SQL Queries extraction failed. API Response: {api_response}"

    post_response = post_comment_on_pr(comment, pr_number, github_token, repo_owner, repo_name)
    print(post_response)
