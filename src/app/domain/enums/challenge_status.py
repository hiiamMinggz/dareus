from enum import StrEnum


class ChallengeStatus(StrEnum):
    PENDING = "pending" # viewer requests new challenge
    ACCEPTED = "accepted" # streamer accepts challenge
    REJECTED = "rejected" # streamer rejects challenge
    STREAMER_COMPLETED = "streamer_completed" # streamer completes challenge
    VIEWER_CONFIRMED = "viewer_confirmed" # viewer confirms challenge
    VIEWER_REJECTED = "viewer_rejected" # viewer rejects challenge status
    REFUNDED = "refunded" # system refunds challenge
    DONE = "done" # system completes challenge

