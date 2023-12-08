from sqlalchemy import text

from services.db.address import DBActivityService


class DBLeaderboardService(DBActivityService):

    def get_leaderboard(
        self,
        activity_name: str,
        n_rows: int = 10
    ):

        activity_id = self.get_activity_id_by_name(activity_name=activity_name)

        rows = self.session.execute(
            text(
                """
                SELECT
                    wallet,
                    program_engagement,
                    protocol_activity,
                    competitors_activity,
                    sybil_likelihood
                FROM (
                    SELECT DISTINCT ON (wallet)
                        wallet,
                        protocol_activity, competitors_activity,
                        program_engagement, sybil_likelihood, dt
                    FROM wallet_scorings
                    WHERE activity_id = :activity_id
                    ORDER BY wallet
                    LIMIT :n_rows
                ) tmp
                ORDER BY dt DESC;
                """
            ), params={"activity_id": activity_id, "n_rows": n_rows}
        )
        res = rows.fetchall()

        lb = []
        for item in res:
            lb.append({
                "Address": item[0],
                "Program Engegement": item[1],
                "Protocol Activity": item[2],
                "Competitors Activity": item[3],
                "Sybil Likelihood": item[4],
                "Total XP": item[1] + item[2] + item[3] + item[4]
            })
        return lb
