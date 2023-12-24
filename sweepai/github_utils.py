from sweepai.gitlab_utils import (create_gitlab_merge_request,
                                  get_gitlab_issue, update_gitlab_pipeline)


def get_issue(project_id, issue_id):
    return get_gitlab_issue(project_id, issue_id)

def create_merge_request(project_id, source_branch, target_branch, title):
    return create_gitlab_merge_request(project_id, source_branch, target_branch, title)

def update_pipeline(project_id, pipeline_id, data):
    return update_gitlab_pipeline(project_id, pipeline_id, data)
