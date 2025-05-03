import os
import pytest
import re
import requests
from dotenv import load_dotenv
from typing import Dict, Optional, Any

import os
os.environ["TESTING"] = "1"

# Load environment variables
load_dotenv()


class TestEmailHelper:
    """Helper class for interacting with Testmail API directly via HTTP requests"""

    def __init__(self):
        """Initialize Testmail API connection"""
        self.api_key = os.getenv("TESTMAIL_API_KEY")
        self.namespace = os.getenv("TESTMAIL_NAMESPACE")
        self.api_url = "https://api.testmail.app/api/json"
        self.message_url = "https://api.testmail.app/api/json/message"

    async def get_message(self, livequery=False):
        """Fetch all messages from Testmail inbox"""
        params = {
            'apikey': self.api_key,
            'namespace': self.namespace,
            'livequery': "true"
        }
        r = requests.get(url=self.api_url, params=params)
        data = r.json()
        return data

    @staticmethod
    def extract_verification_token_from_email(email_data, email_adress):
        print(type(email_data))
        emails = email_data.get("emails")
        email = emails[0]
        adress = email.get("to")
        print(adress)
        print(email_adress)
        if adress != email_adress:
            return None
        text_data = email.get("text")
        token = text_data.split("verification/")[2][:-1]
        print(token)
        return token



@pytest.fixture
def testemail():
    """Pytest fixture for Testemail helper"""
    helper = TestEmailHelper()
    print("Testemail test fixture initialized")
    yield helper
