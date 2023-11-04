import requests
import sys

platform = 'leetcode'
base_url = 'https://leetcode.com'

query_url = 'https://leetcode.com/graphql'


def initialize():
    payload = {
        "query": """
        {
            allQuestionsCount {
                difficulty
                count
            }
        }
        """
    }

    response = requests.post(
        url = query_url,
        json = payload,
        headers = {
            'referer': base_url
        }
    )

    assert( response.status_code == 200 )
    return response.json()




def questions_solved_count(username: str):
    payload = {
            "variables": {
                "username": username
            },
            "query": """ 
            query getUserProfile($username: String!) {
                matchedUser(username: $username) {
                    submitStats {
                        acSubmissionNum {
                            difficulty
                            count
                            submissions
                        }
                    }
                }
            }
            """
        }

    response = requests.post(
        url = query_url, 
        json = payload,
        headers = {
            'referer': base_url + '/' + username
        }
    )

    assert( response.status_code == 200 )

    response_data = response.json()
    if 'errors' in response_data:
        print(response_data['errors'], file=sys.stderr)
        return dict()

    submission_stats = response_data['data']['matchedUser']['submitStats']['acSubmissionNum']
    return submission_stats


def contributions(username: str):
    payload = {
            "variables": {
                "username": username
            },
            "query": """ 
            query getUserProfile($username: String!) {
                matchedUser(username: $username) {
                    contributions {
                        points
                        questionCount
                        testcaseCount
                    }
                }
            }
            """
        }

    response = requests.post(
        url = query_url,
        json = payload,
        headers = {
            'referer': base_url + '/' + username
        }
    )

    assert( response.status_code == 200 )

    response_data = response.json()
    if 'errors' in response_data:
        print(response_data['errors'], file=sys.stderr)
        return dict()

    submission_stats = response_data['data']['matchedUser']['contributions']
    return submission_stats

def profile(username: str):
    payload = {
            "variables": {
                "username": username
            },
            "query": """ 
            query getUserProfile($username: String!) {
                matchedUser(username: $username) {
                    profile {
                        reputation
                        ranking
                    }
                }
            }
            """
        }

    response = requests.post(
        url = query_url,
        json = payload,
        headers = {
            'referer': base_url + '/' + username
        }
    )

    assert( response.status_code == 200 )

    response_data = response.json()
    if 'errors' in response_data:
        print(response_data['errors'], file=sys.stderr)
        return dict()

    submission_stats = response_data['data']['matchedUser']['profile']
    return submission_stats


def total_submissions(username: str):
    payload = {
            "variables": {
                "username": username
            },
            "query": """ 
            query getUserProfile($username: String!) {
                matchedUser(username: $username) {
                    submitStats {
                        totalSubmissionNum {
                            difficulty
                            count
                            submissions
                        }
                    }
                }
            }
            """
        }

    response = requests.post(
        url = query_url,
        json = payload,
        headers = {
            'referer': base_url + '/' + username
        }
    )

    assert( response.status_code == 200 )

    response_data = response.json()
    if 'errors' in response_data:
        print(response_data['errors'], file=sys.stderr)
        return dict()

    submission_stats = response_data['data']['matchedUser']['submitStats']['totalSubmissionNum']
    return submission_stats




def search_question_by_name(question_name: str, skip : int = 0, limit : int = 50):
    payload = {
            "variables": {
                "categorySlug": "",
                "limit": limit,
                "skip": skip,
                "filters": {
                    "searchKeywords": question_name,
                }
            },
            "query": """ 
                query problemsetQuestionList(
                    $categorySlug: String
                    $limit: Int
                    $skip: Int
                    $filters: QuestionListFilterInput
                ) {
                    problemsetQuestionList: questionList(
                    categorySlug: $categorySlug
                    limit: $limit
                    skip: $skip
                    filters: $filters
                    ) {
                        total: totalNum
                        questions: data {
                        difficulty
                        title
                    }
                }
            }
            """
        }

    response = requests.post(
        url = query_url,
        json = payload,
        headers = {
            'referer': base_url + '/problemset/all'
        }
    )

    assert( response.status_code == 200 )

    response_data = response.json()
    if 'errors' in response_data:
        print(response_data['errors'], file=sys.stderr)
        return dict()

    submission_stats = response_data['data']['problemsetQuestionList']
    return submission_stats

