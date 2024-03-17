# SPDX-License-Identifier: GPL-3.0-only
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Copyright (c) 2024, YeetCode Developers <YeetCode-devs@protonmail.com>

from g4f.client import Client
from g4f.Provider import Bing


def generate_response() -> str:
    client = Client(provider=Bing)

    try:
        response = client.chat.completions.create(
            model="gpt-4.0-turbo",
            messages=[{"role": "user", "content": "Say hi, with your response starting with START and ending with END"}],
        )
    except:
        print("ERROR: Could not create a prompt!")

    return response.choices[0].message.content


class TestOutput:
    def test_output(self):
        response = generate_response()

        if (len(response) > 0):
            print("✅ Bing is up!")
        else:
            print("❌ Bing is down...")

        assert response.startswith("START") and response.endswith("END")
