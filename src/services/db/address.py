from datetime import datetime
from sqlalchemy import text

from services.db.base import BaseDbService


class DBSAddressService(BaseDbService):

    def save_scored_address(
        self,
        address: str,
        activity_name: str,
        protocol_activity: float,
        competitors_activity: float,
        program_engagement: float,
        sybil_likelihood: float
    ):

        rows = self.session.execute(
            text(
                """
                SELECT activity_id
                FROM activities
                WHERE activity_name = :activity_name;
                """
            ), params={"activity_name": activity_name}
        )
        activity_id = rows.fetchall()[0][0]

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
