from fastapi import APIRouter, HTTPException, Depends
from typing import Union
from app.services import utils
from uuid import UUID
from app.models.votes import VoteById, VoteByLabel, Vote, Voter
from app.models.polls import Poll
from app.services import utils


router = APIRouter()

def common_validations(poll_id: UUID, vote: Union[VoteById, VoteByLabel]):
    # Dependency injection
    vote_email = vote.voter.email
    poll = utils.get_poll(poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="The poll was not found")
    if not poll.is_active():
        raise HTTPException(status_code = 400, detail="The poll has expired")
    # Check for double votes
    if utils.get_vote(poll_id, vote_email):
        raise HTTPException(
            status_code= 400,
            detail = "already voted"
        )
    return poll
@router.post("/{poll_id}/id")
def vote_by_id(poll_id: UUID, vote: VoteById, poll: Poll = Depends(common_validations)):
    # Check for poll expiration before voting
    # poll = utils.get_poll(poll_id)
    # if not poll:
    #     raise HTTPException(status_code=404, detail="The poll was not found")
    # if not poll.is_active():
    #     raise HTTPException(status_code = 400, detail="The poll has expired")
    # # Check for double votes
    # if utils.get_vote(poll_id, vote.voter.email):
    #     raise HTTPException(
    #         status_code= 400,
    #         detail = "already voted"
    #     )

    if vote.choice_id not in [choice.id for choice in poll.options]:
        raise HTTPException(status_code = 400, detail="Invalid choice id specified")
    #Create the vote instance and return it to the user
    vote = Vote(poll_id=poll_id,choice_id=vote.choice_id, voter=Voter(**vote.voter.model_dump()))
    utils.save_vote(poll_id, vote)
    return {
        "message": "Vote recorded",
        "vote": vote
    }
@router.post("/{poll_id}/label")
def vote_by_label(poll_id: UUID, vote: VoteByLabel, poll: Poll = Depends(common_validations)):
    # poll = utils.get_poll(poll_id)
    # if not poll:
    #     raise HTTPException(status_code=404, detail="The poll was not found")
    # if not poll.is_active():
    #     raise HTTPException(status_code = 400, detail="The poll has expired")
    
    # if utils.get_vote(poll_id, vote.voter.email):
    #     raise HTTPException(
    #         status_code= 400,
    #         detail = "already voted"
    #     )
    # #choice_id = utils.get_choice_id_by_label(poll_id, vote.choice_label)
    choice_id = utils.get_choice_id_by_label_given(poll, vote.choice_label)
    if not choice_id:
        raise HTTPException(
            status_code = 400,
            details="invalid choice label provided"
        )
    vote = Vote(poll_id=poll_id,choice_id=choice_id, voter=Voter(**vote.voter.model_dump()))
    utils.save_vote(poll_id, vote)
    return {
        "message": "Vote recorded",
        "vote": vote
    }
