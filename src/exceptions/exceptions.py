class ActivityNotExistError(Exception):
    def __init__(self, activity):
        super().__init__(f"Activity {activity} doesn't exist")

    def error_code(self):
        return 404


class FailedQueryError(Exception):
    def __init__(self):
        super().__init__("Query failed")

    def error_code(self):
        return 400


class EmptyQueryResultError(Exception):
    def __init__(self):
        super().__init__("Query results not found")

    def error_code(self):
        return 404


class WalletScoringError(Exception):
    def __init__(self):
        super().__init__("Cant score a given address")

    def error_code(self):
        return 400
