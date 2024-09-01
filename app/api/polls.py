from fastapi import APIRouter, HTTPException
from app.models.polls import PollCreate
from app.services import utils
from uuid import UUID
from enum import Enum


class PollStatus(Enum):
    ACTIVE="active"
    EXPIRED="expired"
    ALL="all"


router = APIRouter()
#@app.post("/polls/create")
@router.post("/create")
def create_polls(poll: PollCreate):
    
    new_poll = poll.create_poll()
    # persist created poll to redis database
    utils.save_poll(new_poll)
    return {
        "detail": "Poll created successfully",
        "poll_id" : new_poll.id,
        "poll" : new_poll 
    }
    

#@app.get("/polls/{poll_id}")
@router.get("/{poll_id}")
def get_poll(poll_id: UUID):
    poll = utils.get_poll(poll_id)
    if poll is None:
        raise HTTPException(
            status_code=404,
            detail="No poll found with id {}".format(poll_id)
        )
    return poll 

@router.get("/")
def get_polls(status: PollStatus=PollStatus.ACTIVE):
    polls = utils.get_all_polls()
    if polls is None:
        raise HTTPException(
            status_code=404,
            details="No polls were found"
        )
    
    if status == PollStatus.ACTIVE:
        required_polls = [poll for poll in polls if poll.is_active()]
    elif status == PollStatus.EXPIRED:
        required_polls = [poll for poll in polls if not poll.is_active()]
    elif status == PollStatus.ALL:
        required_polls = polls
    return {
        "count": len(required_polls),
        "polls": required_polls
    }

@router.get("/{poll_id}/results")
def get_results(poll_id: UUID):
    # results = utils.get_vote_count(poll_id)
    # return {"results": results}
    return utils.get_poll_results(poll_id)



