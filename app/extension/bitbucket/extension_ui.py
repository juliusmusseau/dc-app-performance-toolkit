import random
import json

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing

from util.conf import BITBUCKET_SETTINGS

def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)

    randomInt = 10000 + random.randint(0, 25)
    project_key = "PRJ-" + str(randomInt)
    repo_slug = "prj-" + str(randomInt) + "-repo-1"

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_repo_page")
        def sub_measure():
            prNotifierMenu = (By.ID, 'prNotifierActualButton')
            prNotifierButton = (By.CLASS_NAME, 'prnfb-button')

            prUrl = f"{BITBUCKET_SETTINGS.server_url}/projects/{project_key}/repos/{repo_slug}/pull-requests/25/overview"
            page.go_to_url(prUrl)
            page.wait_until_visible(page.get_selector(prNotifierMenu)).click()
            page.wait_until_visible(page.get_selector(prNotifierButton)).click()

        sub_measure()
    measure()
