import requests
from subprocess import check_output, CalledProcessError

import json

API_URL = "https://www.shellcheck.net/shellcheck.php"

def check_shellcheck(file):

    with open(f"./{file}", "r") as f:
        script = f.readlines()
        script_lines = ''.join(script)
        issues = requests.post(
            API_URL,
            data=f'script={script_lines}',
            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }
        )

    if issues.json():
        for issue in issues.json():
            print(f"Line {issue['line']}:")
            print(f" SC{issue['code']} ({issue['level']}): {issue['message']}")
        return False
    else:
        return True



script_path = "./transfer.sh"

def run_shell_test(script, *args):

    out = check_output([script] + list(args), universal_newlines=True)
    return out

def test_shellcheck():
    assert check_shellcheck(script_path) == True

