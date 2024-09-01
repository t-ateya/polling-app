Below is the application main layout: A package contains the __init__.py method 
main.py
.env for environment variables (for reddis api token and server)
app 
    - api 
    - models 
    - routes 
    - services 
    config.py 


uvicorn main:app --reload
http://127.0.0.1:8000/docs


### explore and discard
"""
    Objective:
      - Connect to reddis instance
      - save a record
      - retrieve
"""

"""
@app.post("/redis/save", tags = ["throw away"])
def save_to_redis(id:str, name: str):
    redis_client.set(id, name)
    return {"status": "success"}

@app.get("/redis/get/{id}", tags = ["throw away"])
def retrieve_from_redis(id:str):
    name = redis_client.get(id)
    return {
        "id": id,
        "name" : name
    }

"""

"""
    Objective:
    - Create a utils.py module in the service package
    - define a new save_poll method that takes a poll instance and saves it to Redis
    - hint: use "poll:{poll_id}" as the key, and the entire poll object as the value.
"""

## Objective:
  - Define a new method in utils.py called get_poll(poll_id: UUID) that retrieves and returns poll objects from Redis
  - The method should also ensure that the retrieved poll object is actually consistent with the poll data model
  - Finally, define a GET /polls/{poll_id} route and handler and write it up to get_poll() method
  - If a poll by a given id cannot be found, and HTTP exception with status 404 is raised.

## Objective:
 - Define a new module called polls.py  within the api package
 - Within it, create a new FastAPI APIRouter that will encapsulate all the /polls/endpoints
 - cleanup main.py so that it includes only the app instance and functionally 
 - integrates the poll router 

## Objective:
 - Define the vote and voter pydantic data models 
 - a voter is represented by just an "email" address; the read model of voter
  - should also automatically capture the 'voted_at' timestamp
  - voters could vote by choice UUID or choice label, so vote should have two disparate write models
  - the Vote read model is represented by a combination of "poll_id", "choice_id" as well as a voter.

## Objective:
    - Define a new APIRouter for votes
    - define two placeholder routers:
        POST /vote/{poll_id}/id
            > expects vote as VoteById
        POST /vote/{poll_id}/label
            > expects vote as VoteByLabel
    - both methods should return a placeholder "Vote recorded" for now
    - integrate the new router with the application under a "/vote" prefix

## Objective:
- Define a new method in utils.py that returns the UUID of a choice given the UUID of a poll and the choice's label
- e.g get_choice_id_by_label(poll_id : UUID, label: int)-> Optional[UUID]

## Objective:
- Update both of the voting routes to return a full Vote() instance rather than just the place holder.

## Objective:
   Define two new methods in utils.py for saving and retrieving votes.
   - Save the vote object as full JSON in hashset alongside voter email under a "votes: {poll_id}" key
   - Hint: Use the .hset/hget methods in the Redis client instead of the .set/get method to work with hashes
   - hashset ->(key, value1, value2)

## Objective:
- integrate the save_vote() method from utils.py with the voting routes 

## Objective:
- Prevent a voter (Technically, their email) from casting more than one vote in a give poll

## objective:
  - Prevent a voter from casting a vote on an expired poll 

## Objective:
 - Implement some further validations:
   - in both routes, ensure that a poll by a given poll_id exists
   - in the vote by id route, ensure that choice_id is actually a valid choice
     for the specified poll.

## Objective: 
- Optimize the choice label -> choice id transition so that it doesn't unnecessarily hit Redis twice.

## Objective:
    - In the vote APIRouter, refactor the common validations into a standalone dependency that both route paths depend on

### Objective:
- Add GET / polls routes that return all the polls wherether expired or not from the database 

### Objective:
- Optimize the get_all_polls to utiiize a batch request rather than many individual requests to Redis.
- Hint: explore the .mget() command.

## Objective:
- Update GET / polls routes so that it has  the ability to filter for active and expired polls rather than always returning everything.
- Also add a count of polls field in the response 
- Hint: You could implement this as a 3-member enumeration (ACTIVE, EXPIRED, ALL) and then integrate with the poll route as an optional query parameter, the default for which should be "ACTIVE".

## Objective:
# - save vote counts by poll_id and choice_id in Redis
# hint: use .hincrby() under a "vote_count:{poll_id} key 

## Objective:
 - Implement a new method to retrieve the vote_counts by poll id
 - add a new GET /polls/{poll_id}/results that returns a JSON of choice_id's and vote counts for a given poll e.g {
    "choice_id_1" : 2,
    "choice_id_2": 1,
 }

## Objective:
- Define new pydantic data models:

- Result which will represent a human readable choice tally consisting of a string description and an integer vote_count.
- e.g {"abstaint": 3}

- PollResults which will represent a human-readable summary of the voting results at the poll level, including title, total_votes cast, and a list of Result objects 
{
    "title": "Should the UK leave the EU?",
    "total_votes":32,
    "results": [
        Result(...), Result(...),Result(...)
    ]
}

## Objective:
    - Define a new helper function in utils.py that returns PollResults 
    - hint: use the existing get_poll() and get_vote_count() helpers
    - finally, update the GET /polls/{poll_id}/results endpoint so that it reflects PollResults

## Objective:
- Implement a delete_poll(poll_id: UUID) helper in utils.py which should delete all the poll, votes, vote_count data associated with a given poll_id
- connect this helper to the DELETE /polls/{poll_id} route
- define this functionality as a separate APIRouter and inclue it under a "danger" tag 

## Objective:
- Reshape the pydantic error messages into custom messages that only include the "msg" property of the error


## ########   Deployment Checklist #################
1. freeze our requirements.txt : pip freeze > requirements.txt
2. Define a vercel.json to configure the build
3. Define a .gitignore
4. create a local git repo and add all the code files 
5. create a git repo and push the local one to remote
6. On the Vercel dashboard start a new deployment from the github remote repo

