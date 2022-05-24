import requests
from subprocess import check_output, CalledProcessError

import json, filecmp

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
    result = [' ']
    if issues.json():
        for issue in issues.json():
            result.append(f"Line {issue['line']}:")
            result.append(f"SC{issue['code']} ({issue['level']}): {issue['message']}")
        return result
    else:
        return issues.json()



script_path = "./transfer_work.sh"

def run_shell_test(script, *args):

    out = check_output([script] + list(args), universal_newlines=True)
    return out

def get_file(url):
    response = requests.get(url)
    return response.text

def upload_file(url, path):

    files = {'upload_file': open(path,'rb')}
    response = requests.post(url, files=files)
    
    return response.content.decode('utf-8')

def test_upload():
    result = run_shell_test(script_path, "tests/test.txt", "tests/test.txt")

    for line in result.splitlines():
        if line.startswith('Transfer File URL:'):
            url = line.replace('Transfer File URL: ', '')
            downloaded_file = get_file(url)
            with open("tests/test.txt", encoding = 'utf-8') as f:
                assert downloaded_file == f.read()

def test_download():

    upload_file_url = upload_file("https://transfer.sh/", "tests/test.txt")
    url = upload_file_url.split("https://transfer.sh/")[1].strip().split("/")
    result = run_shell_test(script_path, "-d", "./test", url[0], url[1])
    
    if "Success!" in result:
        assert filecmp.cmp("tests/test.txt", "./test/test.txt") == True

def test_help():
    check = False
    result = run_shell_test(script_path, "-h")

    if "Usage:" in result:
        check = True
    assert check == True

def test_version():
    check = False
    result = run_shell_test(script_path, "-v")

    if "1.23.0" in result:
        check = True
    assert check == True

def test_shellcheck():
    result = check_shellcheck(script_path)
    assert result == []