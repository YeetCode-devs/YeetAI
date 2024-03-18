from g4f.client import Client
from g4f.Provider import FreeChatgpt
from g4f.models import default


def generate_response() -> str:
    client = Client(provider=FreeChatgpt)

    try:
        response = client.chat.completions.create(
            model=default,
            messages=[
                {"role": "user", "content": "Say hi, with your response starting with START and ending with END"}
            ],
        )
    except:
        print("ERROR: Could not create a prompt!")

    return response.choices[0].message.content


class TestOutput:
    def test_output(self):
        response = generate_response()

        if len(response) > 0:
            print("✅ FreeChatgpt is up!")
        else:
            print("❌ FreeChatgpt is down...")

        assert response.startswith("START") and response.endswith("END")
