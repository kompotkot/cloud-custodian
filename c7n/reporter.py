import json
import os
from typing import Any, Dict, Optional
import uuid

from humbug.consent import HumbugConsent
from humbug.report import Reporter

HUMBUG_TOKEN = "7c8802bd-e5e1-4351-be07-43adeb48874a"
HUMBUG_KB_ID = "dddd1df7-d05e-45a0-97f6-83f3104c9cef"

c7n_REPORT_CONFIG_FILE_NAME = "reporting_config.json"


def save_reporting_config(consent: bool, client_id: Optional[str] = None) -> None:
    """
    Allow or disallow c7n reporting.
    """
    reporting_config = {}

    repo_dir = os.getcwd()

    config_report_path = os.path.join(repo_dir, c7n_REPORT_CONFIG_FILE_NAME)
    if os.path.isfile(config_report_path):
        try:
            with open(config_report_path, "r") as ifp:
                reporting_config = json.load(ifp)
        except Exception:
            pass

    if client_id is not None and reporting_config.get("client_id") is None:
        reporting_config["client_id"] = client_id

    if reporting_config.get("client_id") is None:
        reporting_config["client_id"] = str(uuid.uuid4())

    reporting_config["consent"] = consent

    try:
        with open(config_report_path, "w") as ofp:
            json.dump(reporting_config, ofp)
    except Exception:
        pass


def get_reporting_config() -> Dict[str, Any]:
    reporting_config = {}
    repo_dir = os.getcwd()
    if repo_dir is not None:
        config_report_path = os.path.join(repo_dir, c7n_REPORT_CONFIG_FILE_NAME)
        try:
            if not os.path.exists(config_report_path):
                client_id = str(uuid.uuid4())
                reporting_config["client_id"] = client_id
                save_reporting_config(True, client_id)
            else:
                with open(config_report_path, "r") as ifp:
                    reporting_config = json.load(ifp)
        except Exception:
            pass
    return reporting_config


def c7n_consent_from_reporting_config_file() -> bool:
    reporting_config = get_reporting_config()
    return reporting_config.get("consent", False)


session_id = str(uuid.uuid4())
client_id = get_reporting_config().get("client_id")

c7n_consent = HumbugConsent(c7n_consent_from_reporting_config_file)
c7n_reporter = Reporter(
    name="c7n",
    consent=c7n_consent,
    client_id=client_id,
    session_id=session_id,
    bugout_token=HUMBUG_TOKEN,
    bugout_journal_id=HUMBUG_KB_ID,
)
