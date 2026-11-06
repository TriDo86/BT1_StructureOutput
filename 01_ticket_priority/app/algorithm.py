from datetime import datetime, timedelta

def cal_deadline(received_at: datetime, severity: str):
    TIME_LOOKUP = {"low": 24*60, 
                   "medium": 8*60, 
                   "high": 2*60, 
                   "critical": 30}
    return received_at + timedelta(minutes=TIME_LOOKUP[severity])

def cal_priority(ticket_id: str, received_at: datetime, severity: str) -> tuple:
    severity_rank = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    return (cal_deadline(received_at, severity), -severity_rank[severity], received_at, ticket_id)
