import random
import json

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
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
            bitBoosterTbl = (By.ID, 'bit-booster-tbl')

            cherryUrl = f"{BITBUCKET_SETTINGS.server_url}/plugins/servlet/bb_ag/projects/{project_key}/repos/{repo_slug}/commits"
            page.go_to_url(cherryUrl)
            page.wait_until_visible(page.get_selector(bitBoosterTbl))

        sub_measure()
    measure()
