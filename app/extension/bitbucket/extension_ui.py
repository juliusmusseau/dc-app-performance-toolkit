import random
import json

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.bitbucket.pages.pages import LoginPage, GetStarted, PopupManager
from selenium_ui.bitbucket.pages.selectors import RepoLocators, PullRequestLocator
from util.conf import BITBUCKET_SETTINGS

def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)

    randomInt = 10000 + random.randint(1, 999)
    project_key = "PRJ-" + str(randomInt)
    repo_slug = "prj-" + str(randomInt) + "-repo-1"

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_repo_page")
        def sub_measure():
            cherryUrl = f"{BITBUCKET_SETTINGS.server_url}/plugins/servlet/bb_rb/projects/{project_key}/repos/{repo_slug}/commits/perf-branch-99"
            page.go_to_url(cherryUrl)
            raw_json = webdriver.find_element(By.TAG_NAME, 'pre').text
            json_data = json.loads(raw_json)

            # print(json_data)
            if json_data['defaultCherryBranch'] is None or json_data['defaultCherryBranch'] == '':
                raise Exception("No Default Cherry Branch")

            javascriptRequest1 = ('var xhr = new XMLHttpRequest();'
            'xhr.open("POST", "' + cherryUrl + '", false);'
            'xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");'
            'xhr.send(JSON.stringify({"mode": "bbRevert", "msg": "revert", "author": "Fake Generator <fake.user@atlassian.com>", "targetBranch": "perf-branch-99", "newBranch": "", "pushAsNew": "false", "parentNumber": 1, "strategyOption": "default"}));'
            # 'while(xhr.readyState !== 4){ await new Promise(r => setTimeout(r, 11)); }'
            'return xhr.responseText;')

            javascriptRequest2 = ('var xhr = new XMLHttpRequest();'
            'xhr.open("POST", "' + cherryUrl + '", false);'
            'xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");'
            'xhr.send(JSON.stringify({"mode": "bbRevert", "msg": "revert-revert", "author": "Fake Generator <fake.user@atlassian.com>", "targetBranch": "perf-branch-99", "newBranch": "", "pushAsNew": "false", "parentNumber": 1, "strategyOption": "default"}));'
            # 'while(xhr.readyState !== 4){ await new Promise(r => setTimeout(r, 11)); }'
            'return xhr.responseText;')

            # first bbRevert
            result = webdriver.execute_script(javascriptRequest1)
            # print(result)
            json_data = json.loads(result)
            #print("revert1 DONE")

            if json_data['rbSuccess'] is None or not bool(json_data['rbSuccess']):
                raise Exception("Bit-Booster Revert Failed")

            # and revert the revert !
            result = webdriver.execute_script(javascriptRequest2)
            # print(result)
            json_data = json.loads(result)
            #print("revert2 DONE")

            if json_data['rbSuccess'] is None or not bool(json_data['rbSuccess']):
                raise Exception("Bit-Booster Revert-Revert Failed")


            prUrl = f"{BITBUCKET_SETTINGS.server_url}/projects/{project_key}/repos/{repo_slug}/pull-requests?create&sourceBranch=perf-branch-99&targetBranch=master"
            page.go_to_url(prUrl)
            PopupManager(webdriver).dismiss_default_popup()
            page.wait_until_visible(page.get_selector(RepoLocators.pr_continue_button)).click()
            page.wait_until_visible(page.get_selector(RepoLocators.pr_submit_button)).click()
            page.wait_until_clickable(PullRequestLocator.pull_request_page_merge_button)


            url = webdriver.current_url
            url = url.replace("http://a13c0501f99b8495e8199a729f650b1a-618884428.us-east-2.elb.amazonaws.com/", "")
            url = url.replace("/overview", "")
            print("CLEANED-URL: " + url)

            squashUrl = f"{BITBUCKET_SETTINGS.server_url}/plugins/servlet/bb_rb/" + url
            page.go_to_url(squashUrl)
            raw_json = webdriver.find_element(By.TAG_NAME, 'pre').text
            json_data = json.loads(raw_json)
            # print("CAN-SQUASH? " + squashUrl)
            #print(json_data)
            if json_data['userHasWrite'] is None or json_data['squashMsg'] is None or not bool(json_data['userHasWrite']):
                raise Exception("Bit-Booster Can-Squash Failed")

            javascriptRequest1 = ('var xhr = new XMLHttpRequest();'
            'xhr.open("POST", "' + squashUrl + '", false);'
            'xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");'
            'xhr.send(JSON.stringify({"mode": "bbSquash", "msg": "squash", "author": "Fake Generator <fake.user@atlassian.com>", "targetBranch": "", "newBranch": "", "pushAsNew": "", "parentNumber": "", "strategyOption": ""}));'
            # 'while(xhr.readyState !== 4){ await new Promise(r => setTimeout(r, 11)); }'
            'return xhr.responseText;')

            result = webdriver.execute_script(javascriptRequest1)
            # print(result)
            json_data = json.loads(result)
            #print("squash DONE")

            if json_data['rbSuccess'] is None or not bool(json_data['rbSuccess']):
                raise Exception("Bit-Booster Squash Failed")

            deleteUrl = f"{BITBUCKET_SETTINGS.server_url}/rest/api/1.0/" + url
            javascriptRequest2 = ('var xhr = new XMLHttpRequest();'
            'xhr.open("DELETE", "' + deleteUrl + '", false);'
            'xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");'
            'xhr.send(JSON.stringify({"version":1}));'
            # 'while(xhr.readyState !== 4){ await new Promise(r => setTimeout(r, 11)); }'
            'return xhr.responseText;')
            result = webdriver.execute_script(javascriptRequest2)
            # print("delete PR attempt 1 DONE - [" + result + "]")

            if (result != ""):
                deleteUrl = f"{BITBUCKET_SETTINGS.server_url}/rest/api/1.0/" + url
                javascriptRequest2 = ('var xhr = new XMLHttpRequest();'
                'xhr.open("DELETE", "' + deleteUrl + '", false);'
                'xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");'
                'xhr.send(JSON.stringify({"version":0}));'
                # 'while(xhr.readyState !== 4){ await new Promise(r => setTimeout(r, 11)); }'
                'return xhr.responseText;')
                result = webdriver.execute_script(javascriptRequest2)
                # print("delete PR attempt 2 DONE - [" + result + "]")

                if (result != ""):
                    deleteUrl = f"{BITBUCKET_SETTINGS.server_url}/rest/api/1.0/" + url
                    javascriptRequest2 = ('var xhr = new XMLHttpRequest();'
                    'xhr.open("DELETE", "' + deleteUrl + '", false);'
                    'xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");'
                    'xhr.send(JSON.stringify({"version":1}));'
                    # 'while(xhr.readyState !== 4){ await new Promise(r => setTimeout(r, 11)); }'
                    'return xhr.responseText;')
                    result = webdriver.execute_script(javascriptRequest2)
                    # print("delete PR attempt 3 DONE - [" + result + "]")


        sub_measure()
    measure()
