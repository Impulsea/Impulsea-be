from datetime import datetime, timezone
from sqlalchemy import text

from services.db.base import BaseDbService
from config import CACHING_TIME


class DBActivityService(BaseDbService):

    def get_activity_id_by_name(self, activity_name: str) -> int:
        rows = self.session.execute(
            text(
                """
                SELECT activity_id
                FROM activities
                WHERE activity_name = :activity_name;
                """
            ), params={"activity_name": activity_name}
        )
        return rows.fetchall()[0][0]


class DBAddressService(DBActivityService):

    def save_scored_address(
        self,
        address: str,
        activity_name: str,
        protocol_activity: float,
        competitors_activity: float,
        program_engagement: float,
        sybil_likelihood: float
    ) -> None:

        activity_id = self.get_activity_id_by_name(activity_name=activity_name)

        self.session.execute(
            text(
                """
                INSERT INTO wallet_scorings (
                    activity_id,
                    wallet,
                    protocol_activity,
                    competitors_activity,
                    program_engagement,
                    sybil_likelihood,
                    dt
                ) VALUES (
                    :activity_id,
                    :wallet,
                    :protocol_activity,
                    :competitors_activity,
                    :program_engagement,
                    :sybil_likelihood,
                    :dt
                )
                """
            ), {
                "activity_id": activity_id,
                "wallet": address,
                "protocol_activity": protocol_activity,
                "competitors_activity": competitors_activity,
                "program_engagement": program_engagement,
                "sybil_likelihood": sybil_likelihood,
                "dt": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
               })

        self.session.commit()

    def load_cached_address(
            self,
            address: str,
            activity_name: str,
    ):
        # get activity id
        activity_id = self.get_activity_id_by_name(activity_name=activity_name)

        # cached data
        rows = self.session.execute(
            text(
                """
                SELECT
                    program_engagement, protocol_activity,
                    competitors_activity, sybil_likelihood,
                    program_engagement + protocol_activity +
                        competitors_activity + sybil_likelihood AS total_xp
                FROM wallet_scorings
                WHERE
                    activity_id = :activity_id
                    AND lower(wallet) = lower(:wallet)
                    AND dt > CURRENT_TIMESTAMP - INTERVAL ':caching_time MINUTE'
                ORDER BY dt
                LIMIT 1
                """
            ), params={"activity_id": activity_id, "wallet": address, "caching_time": CACHING_TIME}
        )
        data = rows.fetchall()

        if len(data) == 0:
            return False

        return {
            "Address": address,
            "Program Engegement": data[0][0],
            "Protocol Activity": data[0][1],
            "Competitors Activity": data[0][2],
            "Sybil Likelihood": data[0][3],
            "Total XP": data[0][4]
        }
