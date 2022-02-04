import time
from slack_sdk import WebClient

class SlackProgress():
    def __init__(self, token, channel):
        self.channel = channel
        self.token = token
        self.client = WebClient(token=self.token)
        self.channel_id()


    def iter(self, iterable):
        '''
        Function to wrap the iterable and pass information
        to the progress bar functions.
        
        Iterable: something to loop over, can be list/array/iterable/etc.
        '''
        
        self.nmax = len(iterable)
        self.nbar = 0
        self.stime = time.time()

        self.progressbar_init()

        for idx, item in enumerate(iterable):
            yield(item)
            self.slack_progress_bar(idx)
        
        self.slack_progress_bar(self.nmax)


    def progressbar_init(self):
        '''
        Function that sends initial slack message, which
        is subsequently updated with the progress bar.
        '''
        
        result = self.client.chat_postMessage(channel=self.channel,
                                         text=' 0%')
        self.ts = str(result['ts'])
        print(self.ts)
        self.nbar += 1


    def slack_progress_bar(self, idx):
        '''
        Function which updates the slack message with
        the current progress, speed and estimated time
        to completion.
        '''
        
        prog = round(100 * idx / self.nmax)
        if (prog//5) > self.nbar:

            self.progress_timing(idx)

            bar = chr(9608) * (prog//5)
            result = self.client.chat_update(channel=self.channel_id,
                                        ts = self.ts,
                                        text='{0} {1:.0f}% | {2} | {3:.1f} s'.format(bar, prog, self.speed, self.etime))
            self.nbar += 1


    def progress_timing(self, idx):
        '''
        Function to calculate timing related information.
        '''
        
        c_time = time.time()
        its_per_s = idx / (c_time - self.stime)
        s_per_it = (c_time - self.stime) / idx

        if idx < self.nmax - 1:
            self.etime = (self.nmax - idx) * s_per_it
        else:
            self.etime = c_time - self.stime
        
        if its_per_s < 1:
            self.speed = '{:.1f} s/it'.format(s_per_it)
        else:
            self.speed = '{:.1f} its/s'.format(its_per_s)


    def channel_id(self):
        '''
        Function to get the channel ID from the channel name.
        '''
        channel_id = None
        try:
            for response in self.client.conversations_list():
                if channel_id is not None:
                    break
                for channel in response["channels"]:
                    if channel["name"] == self.channel:
                        channel_id = channel["id"]
                        break
            self.channel_id = channel_id
        except SlackApiError as e:
            print(f"Error: {e}")
