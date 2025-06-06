from api.services.exceptions import ExternalServiceError


class GithubServiceException(ExternalServiceError):
    pass

class GraphQLGithubServiceException(GithubServiceException):
    pass
