import os
import requests


class DiscordWorker:
    def __init__(self):
        self.API_ENDPOINT = "https://discordapp.com/api/"

        self.bot_token = os.getenv("BOT_TOKEN", "")
        if not self.bot_token:
            raise ValueError("Bot token is not set")

        self.headers = {
            "Authorization": f"Bot {self.bot_token}"
        }

    def __make_api_request(self, url, data, method="GET"):
        endpoint = self.API_ENDPOINT + url
        if method == "GET":
            r = requests.get(endpoint, params=data, headers=self.headers)
        elif method == "POST":
            r = requests.post(endpoint, json=data, headers=self.headers)
        elif method == "PATCH":
            r = requests.patch(endpoint, json=data, headers=self.headers)
        elif method == "DELETE":
            r = requests.delete(endpoint, json=data, headers=self.headers)
        else:
            raise NotImplementedError

        return r.json(), r.status_code

    def get_user_data(self, member, server="895445476969705473"):
        return self.__make_api_request(f"guilds/{server}/members/{member}", {})

    def send_message(self, channel_id, message):
        return self.__make_api_request(f"channels/{channel_id}/messages", message, method="POST")

    def update_message(self, message_id, channel_id, message):
        return self.__make_api_request(f"channels/{channel_id}/messages/{message_id}", message, method="PATCH")

    def delete_message(self, message_id, channel_id):
        return self.__make_api_request(f"channels/{channel_id}/messages/{message_id}", {}, method="DELETE")

    @staticmethod
    def build_message(content, embed):
        message = {
            "content": content,
            "embed": embed
        }
        return message


class EmbedBuilder:
    def build_embed(self, title, color, fields):
        return {
            "title": title,
            "color": color,
            "fields": fields
        }

    def build_field(self, name, value, inline=False):
        return {
            "name": name,
            "value": value,
            "inline": inline
        }


if __name__ == '__main__':
    dw = DiscordWorker()
    # data, _ = dw.get_user_data("1121526846618607720")
    data = dw.send_message("1157758899756224612", dw.build_message("Hello", ""))
    print(data)
