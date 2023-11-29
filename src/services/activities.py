import os
import json
import logging
import importlib.util


def _import_functions_from_file(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _process_config_file(root: str, entry: str, file: str):
    file_path = os.path.join(root, entry, file)
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading JSON from {file_path}: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")


def _process_py_file(root: str, entry: str, file: str):
    file_path = os.path.join(root, entry, file)
    try:
        return _import_functions_from_file(file_path)
    except FileNotFoundError as e:
        print(f"File not found: {e}")


class Activities:

    ROOT_DIR = "activities/"

    def __init__(self):
        self.activities = {}
        for entry in os.listdir(self.ROOT_DIR):
            config = _process_config_file(self.ROOT_DIR, entry, 'config.json')
            for py_file in [
                'leaderboard.py',
                'wallet_checker.py',
                'stats.py',
            ]:
                module = _process_py_file(self.ROOT_DIR, entry, py_file)
                try:
                    config[py_file.replace('.py', '')] = module
                except Exception as e:
                    logging.error(py_file, e)

            try:
                self.activities[config['ACTIVITY_NAME']] = config
            except Exception as e:
                logging.error(e)

    def get_all_activities(self):

        all_activities = []

        for activity_name in self.activities:
            activity = self.activities[activity_name]
            all_activities.append({
                "ACTIVITY_NAME": activity.get("ACTIVITY_NAME"),
                "DISPLAY_NAME": activity.get("DISPLAY_NAME"),
                "DATE_START": activity.get("DATE_START"),
                "DATE_END": activity.get("DATE_END"),
                "TAGS": activity.get("TAGS"),
            })

        return all_activities

    def get_activity_stats(self, activity):
        stats = self.activities[activity]["stats"].get_stats()
        common_stats = self.activities[activity]
        return {
            "DISPLAY_NAME": common_stats.get("DISPLAY_NAME"),
            "DATE_START": common_stats.get("DATE_START"),
            "DATE_END": common_stats.get("DATE_END"),
            "TAGS": common_stats.get("TAGS"),
            **stats
        }

    def get_activity_leaderboard(self, activity):
        return self.activities[activity]["leaderboard"].get_lb()

    def get_activity_wallet_score(self, activity, address):
        return self.activities[activity]["wallet_checker"].get_wallet_score(address)
