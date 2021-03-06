# slack_tools

A set of tools I've been using to send information from Python to Slack using the [Slack API](https://github.com/slackapi/python-slack-sdk).

## Setting up a slack bot

To make any of this work, you have to have a slack bot/app in your slack workspace (and in the channel you wish to post to), some guides for making the bot/app can be found here:

- [Fullstackpython](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html)
- [Python slack sdk tutorial](https://github.com/slackapi/python-slack-sdk/blob/main/tutorial/01-creating-the-slack-app.md)

## Tools

- **Progress bar**: The `SlackProgress` class in `slack-progressbar.py` allows one to wrap an iterable and automatically send and update a progress bar in a specified slack channel.

## Usage

```Python
from slack_tools.slack_progressbar import SlackProgress

prbr = SlackProgress(token='YOUR_APP_TOKEN', channel='DESTINATION_CHANNEL')
for i in prbr.iter(range(100)):
    time.sleep(0.1)
```
