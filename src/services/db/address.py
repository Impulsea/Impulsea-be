from datetime import datetime
from sqlalchemy import text

from services.db.base import BaseDbService


class DBActivityService(BaseDbService):

    def get_activity_id_by_name(self, activity_name):
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
    ):

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
                "dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
               })

        self.session.commit()
