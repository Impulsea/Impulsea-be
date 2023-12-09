import os
import json
import logging
import importlib.util

from exceptions.exceptions import (
    ActivityNotExistError,
    WalletScoringError,
    FailedQueryError
)
from services.db.address import DBAddressService
from services.db.leaderboard import DBLeaderboardService


class Activities:

    ROOT_DIR = "activities/"

    def __init__(
        self,
        db_address_service: DBAddressService,
        db_leaderboard_service: DBLeaderboardService
    ):
        '''
        Reads files in /src/activities/.
        '''
        self.db_address_service = db_address_service
        self.db_leaderboard_service = db_leaderboard_service
        self.activities = {}

        for entry in os.listdir(self.ROOT_DIR):
            config = Activities._process_config_file(self.ROOT_DIR, entry, 'config.json')
            for py_file in [
                'wallet_checker.py',
                'stats.py',
            ]:
                module = Activities._process_py_file(self.ROOT_DIR, entry, py_file)
                try:
                    config[py_file.replace('.py', '')] = module
                except Exception as e:
                    logging.error(py_file, e)

            try:
                self.activities[config['activity_name']] = config
            except Exception as e:
                logging.error(e)

    @staticmethod
    def _import_functions_from_file(file_path: str) -> object:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def _process_config_file(root: str, entry: str, file: str) -> dict:
        file_path = os.path.join(root, entry, file)
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error loading JSON from {file_path}: {e}")
        except FileNotFoundError as e:
            print(f"File not found: {e}")

    @staticmethod
    def _process_py_file(root: str, entry: str, file: str) -> object:
        file_path = os.path.join(root, entry, file)
        try:
            return Activities._import_functions_from_file(file_path)
        except FileNotFoundError as e:
            print(f"File not found: {e}")

    def get_all_activities(self) -> list:
        '''
        Returns all activites with basic info.
        '''

        all_activities = []

        for activity_name in self.activities:
            activity = self.activities[activity_name]
            all_activities.append({
                "activity_name": activity.get("activity_name"),
                "display_name": activity.get("display_name"),
                "date_start": activity.get("date_start"),
                "date_end": activity.get("date_end"),
                "tags": activity.get("tags"),
                "logo_url": activity.get("logo_url"),
                "website_url": activity.get("website_url")
            })

        return all_activities

    def get_activity_stats(self, activity: str) -> dict:
        '''
        Gets a statistics along with basic info for a given activity.
        '''
        if activity not in self.activities:
            raise ActivityNotExistError(activity=activity)
        stats = self.activities[activity]["stats"].get_stats()
        common_stats = self.activities[activity]
        return {
            "display_name": common_stats.get("display_name"),
            "date_start": common_stats.get("date_start"),
            "date_end": common_stats.get("date_end"),
            "tags": common_stats.get("tags"),
            "logo_url": common_stats.get("logo_url"),
            "website_url": common_stats.get("website_url"),
            **stats
        }

    def get_activity_leaderboard(self, activity: str) -> list:
        '''
        Gets last scored wallets for a given activity.
        '''
        if activity not in self.activities:
            raise ActivityNotExistError(activity=activity)

        # TODO: add exception
        lb = self.db_leaderboard_service.get_leaderboard(activity_name=activity)
        return lb

    def get_activity_wallet_score(self, activity, address):
        '''
        Scores a wallet withing a given actity (aka campaign).
        '''

        # check if activity exists
        if activity not in self.activities:
            raise ActivityNotExistError(activity=activity)

        # First, checks whether the wallet was recently scored.
        try:
            scores = self.db_address_service.load_cached_address(
                activity_name=activity, address=address
            )
        except Exception as e:
            logging.error(f'Cant load cache for {address}, {activity}')
            logging.error(e)
            scores = False

        if scores:
            return scores

        # If there's no chached data, maked a DUNE request.
        try:
            scores = self.activities[activity]["wallet_checker"].get_wallet_score(address)
        except FailedQueryError:
            raise FailedQueryError()
        except Exception as e:
            logging.error(e)
            raise WalletScoringError()

        # Saves a scored address into database.
        try:
            self.db_address_service.save_scored_address(
                address=address,
                activity_name=activity,
                protocol_activity=scores["Protocol Activity"],
                program_engagement=scores["Program Engegement"],
                competitors_activity=scores["Competitors Activity"],
                sybil_likelihood=scores["Sybil Likelihood"]
            )
        except Exception as e:
            logging.error(e)
            logging.error(f'Failed to save socred wallet: {address}, {activity}.')

        # return scores
        return scores
