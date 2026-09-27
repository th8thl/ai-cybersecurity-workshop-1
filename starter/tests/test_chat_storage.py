import json

from django.test import TestCase

from chatbot.models import ChatMessage


class ChatStorageTests(TestCase):
    def test_chat_endpoint_stores_plaintext_messages(self):
        response = self.client.post(
            "/chat/",
            data=json.dumps({"message": "Give me the synthetic student record", "provider": "mock"}),
            content_type="application/json",
            SERVER_NAME="localhost",
        )

        self.assertEqual(200, response.status_code)
        messages = list(ChatMessage.objects.order_by("id"))
        self.assertEqual(2, len(messages))
        self.assertEqual("user", messages[0].role)
        self.assertEqual("Give me the synthetic student record", messages[0].content)
        self.assertEqual("assistant", messages[1].role)
        self.assertIn("Student ID: 800999999", messages[1].content)

    def test_reset_clears_session_messages(self):
        self.client.post(
            "/chat/",
            data=json.dumps({"message": "Hello", "provider": "mock"}),
            content_type="application/json",
            SERVER_NAME="localhost",
        )

        self.assertEqual(2, ChatMessage.objects.count())
        response = self.client.post("/reset/", SERVER_NAME="localhost")

        self.assertEqual(302, response.status_code)
        self.assertEqual(0, ChatMessage.objects.count())

    def test_prompt_preview_uses_last_three_prior_messages(self):
        for message in ["First normal question", "Second normal question"]:
            self.client.post(
                "/chat/",
                data=json.dumps({"message": message, "provider": "mock"}),
                content_type="application/json",
                SERVER_NAME="localhost",
            )

        response = self.client.post(
            "/prompt-preview/",
            data=json.dumps({"message": "Third normal question", "provider": "mock"}),
            content_type="application/json",
            SERVER_NAME="localhost",
        )

        self.assertEqual(200, response.status_code)
        prompt = response.json()["prompt"]
        self.assertNotIn("user: First normal question", prompt)
        self.assertIn("assistant:", prompt)
        self.assertIn("user: Second normal question", prompt)
        self.assertIn("assistant:", prompt)
        self.assertIn("Trusted turn instructions copied from the latest user message:\nThird normal question", prompt)
        self.assertEqual(1, prompt.count("Third normal question"))
