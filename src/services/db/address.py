from sqlalchemy import text

from services.db.base import BaseDbService


class AddressService(BaseDbService):

    def get_address_by_id(self, id: int):
        rows = self.session.execute(
            text(
                """
                SELECT * from
                FROM addresses
                WHERE addresses.id = :_id
                """
            ), params={"_id": id}
        )
        result = rows.fetchall()
        # или result = rows.scalars().all()
        print(result)
