[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/UxpU_KWG)

# Group 08 Serverless

<br>

## Quick Start

1. Clone the repository
2. Create `.env` file with specified environment variables. Refer to [Environment Variables](#environment-variables) for the configuration
3. Configure serverless.yml according to your needs. If you need help, you can refer to this [documentation](https://www.serverless.com/framework/docs/getting-started/).
4. Run `pip3 install -r requirements.txt` to install the dependencies.

<br>

## Environment Variables

- [GRAPHQL_ENDPOINT](#graphql-endpoint)
- [GRAPHQL_QUERY](#graphql-query)
- [QUESTION_LIST_ENDPOINT](#question-list-endpoint)
- [QUESTION_SERVICE_URI](#question-service-uri)
- [TOKEN](#token)


### GraphQL Endpoint

`https://leetcode.com/graphql` <br>
This endpoint is used to retrieve individual question data.

### GraphQL Query

The following query returns data for one question given the title slug.

```graphql
query questionData($titleSlug: String!)
{
    question(titleSlug: $titleSlug)
    {
        title
        titleSlug
        content
        isPaidOnly
        difficulty
        topicTags
        {
            name
        }
        codeSnippets
        {
            lang
            langSlug
            code
        }
        hints
    }
}
```

#### Caveats

- GraphQL is not an official API of LeetCode and may be changed without any notice.
- If function is maliciously invoked (i.e., too many invocations within a small time frame), you may be temporarily blocked from using the API. Either use a VPN to change your IP address or wait.

### Question List Endpoint

`https://leetcode.com/api/problems/algorithms/` <br>
This endpoint is used to retrieve the list of questions in LeetCode.

### Question Service URI

HTTP Requests are posted here to add questions to the Question Service.

### Token

Authorization token required to add the questions.

<br>

## Serverless Function

The serverless function is used to populate the database with questions received from LeetCode.

### AWS Lambda (Cloud)

The function is hosted on AWS Lambda. Before deploying the function, please set up an account on your cloud provider using this [guide](https://www.serverless.com/framework/docs/providers/aws/guide/credentials/).

To deploy the serverless function, run:

```bash
serverless deploy
```

To invoke the serverless function, run:

```bash
serverless invoke --function updateQuestionDatabase
```

The serverless function is scheduled to run every 90 days.

### Local Deployment

To invoke the serverless function locally, run:

```bash
serverless invoke local --function updateQuestionDatabase
```

<br>

## Demonstration

The serverless function will be invoked locally to remove the hassle of cloud deployment.


