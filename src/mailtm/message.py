import json
import time
from threading import Thread

class Listen:
    listen = False
    message_ids = []

    def message_list(self, proxies):
        url = "https://api.mail.tm/messages"
        headers = { 'Authorization': 'Bearer ' + self.token }
        response = self.session.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()
        
        data = response.json()
        return  [
                    msg for i, msg in enumerate(data['hydra:member']) 
                        if data['hydra:member'][i]['id'] not in self.message_ids
                ]

    def message(self, idx, proxies):
        url = "https://api.mail.tm/messages/" + idx
        headers = { 'Authorization': 'Bearer ' + self.token }
        response = self.session.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()
        return response.json()

    def run(self, proxies):
        while self.listen:
            for message in self.message_list(proxies):
                self.message_ids.append(message['id'])
                message = self.message(message['id'], proxies)
                self.listener(message)

            time.sleep(self.interval)

    def start(self, listener, proxies):
        if self.listen:
            self.stop()

        self.listener = listener
        self.interval = 3
        self.listen = True

        # Start listening thread
        self.thread = Thread(target=self.run, args=[proxies])
        self.thread.start()
    
    def stop(self):
        self.listen = False
        self.thread.join()
