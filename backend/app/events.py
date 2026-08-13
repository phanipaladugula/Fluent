import asyncio
import json


def enqueue_message(queue, text):
    try:
        queue.put_nowait(text)
    except Exception:
        return


class LeaderboardHub:
    def __init__(self):
        self.listeners = []
        self.loop = None

    def subscribe(self, queue):
        self.listeners.append(queue)
        self.loop = asyncio.get_running_loop()

    def unsubscribe(self, queue):
        remaining = []
        for item in self.listeners:
            if item is not queue:
                remaining.append(item)
        self.listeners = remaining

    def publish(self, payload):
        if self.loop is None:
            return
        text = json.dumps(payload)
        snapshot = []
        for item in self.listeners:
            snapshot.append(item)
        for queue in snapshot:
            self.loop.call_soon_threadsafe(enqueue_message, queue, text)


hub = LeaderboardHub()


def broadcast_leaderboard(db, current_user):
    from app.services.profile_service import LeaderboardService

    service = LeaderboardService(db)
    rows = service.get_board(current_user)
    payload = []
    for row in rows:
        payload.append(
            {
                "rank": row.rank,
                "user_id": row.user_id,
                "display_name": row.display_name,
                "username": row.username,
                "total_xp": row.total_xp,
                "streak_count": row.streak_count,
                "is_current_user": row.is_current_user,
            }
        )
    hub.publish({"entries": payload})


def safe_broadcast_leaderboard(db, current_user):
    try:
        broadcast_leaderboard(db, current_user)
    except Exception:
        return
