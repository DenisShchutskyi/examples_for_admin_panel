from pushjack import GCMClient
from config import key_android,\
    key_ios
import traceback


def push(GCMC, message, token_hex):
    resp = GCMC.send(token_hex,
                     message['title'],
                     # message['title'],
                     notification=message,
                     # collapse_key='collapse_key',
                     delay_while_idle=True,
                     time_to_live=604800)


def send_push(data_for_push, message):
    GCMC_android = GCMClient(api_key=key_android)
    GCMC_ios = GCMClient(api_key=key_ios)
    for l in data_for_push:
        if l[0]:
            try:
                push(GCMC_android, message, l[1])
            except:
                GCMC_android = GCMClient(api_key=key_android)
                try:
                    push(GCMC_android, message, l[1])
                except:
                    GCMC_android = GCMClient(api_key=key_android)
        else:
            try:
                push(GCMC_ios, message, l[1])
            except:
                traceback.print_exc()
                GCMC_ios = GCMClient(api_key=key_ios)

                try:
                    push(GCMC_ios, message, l[1])
                except:
                    GCMC_ios = GCMClient(api_key=key_ios)


