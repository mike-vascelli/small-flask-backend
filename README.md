# small-flask-backend
A small Flask backend that provides access to APIs to interact with an `Algorithm` resource

### Prompt for the exercise
Create a REST service that allows system to manage algorithms progress.
It should provide basic operation
1. Add/register a new algorithm by string ID (with 0 progress).
2. Update progress of specific algorithm by ID.
3. Retrieve a list of all registered algorithms with its progress.

To ensure reliability, algorithm progress should be stored in a database.
However, considering that the system experiences high read demand and low write
activity, the service should implement caching for reading progress data.
Please focus on proper project structure, proper REST API, proper error handling.


### APIs
1. POST /api/v1/algorithms

    {
      "pk": "6db22aea-00c4-488e-bc52-510d24bd1c05"
    }

    -> 201

2. PATCH /api/v1/algorithms/6db22aea-00c4-488e-bc52-510d24bd1c05

    {
      "progress": 0.1
    }

    -> 204

3. GET /api/v1/algorithms
    
    -> 200

     Sample response: [
        {
          "pk": "6db22aea-00c4-488e-bc52-510d24bd1c05",
          "progress": 0.1
        }
      ]

"""