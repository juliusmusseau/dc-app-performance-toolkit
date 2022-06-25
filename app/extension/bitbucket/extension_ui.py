import random
import json

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing

from selenium_ui.bitbucket.pages.pages import LoginPage, GetStarted, Dashboard, Projects, Project, Repository, \
    RepoNavigationPanel, PopupManager, RepoPullRequests, PullRequest, RepositoryBranches, RepositoryCommits, LogoutPage

from selenium_ui.bitbucket.pages.selectors import LoginPageLocators, GetStartedLocators, \
    DashboardLocators, ProjectsLocators, ProjectLocators, RepoLocators, RepoNavigationPanelLocators, PopupLocators, \
    PullRequestLocator, BranchesLocator, RepositorySettingsLocator, UserSettingsLocator, RepoCommitsLocator, \
    LogoutPageLocators, UrlManager

from util.conf import BITBUCKET_SETTINGS

def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)

    # randomInt = 999
    randomInt = 10000 + random.randint(1, 999)
    project_key = "PRJ-" + str(randomInt)
    repo_slug = "prj-" + str(randomInt) + "-repo-1"
    pull_request_key = datasets['pull_request_id']

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_commit_graph")
        def sub_measure():
            cherryUrl = f"{BITBUCKET_SETTINGS.server_url}/plugins/servlet/bb_ag/projects/{project_key}/repos/{repo_slug}/commits"
            page.go_to_url(cherryUrl)
            page.wait_until_clickable((By.ID, 'bb-apply'))
        sub_measure()
    measure()
