import logging
import os

import aiohttp

from sirbot import SirBot
from sirbot.message import Attachment, Button, Field

token = os.environ['SIRBOT_TOKEN']

bot = SirBot(token=token)

logging.basicConfig()
logging.getLogger('sirbot').setLevel(logging.DEBUG)


# Example quote of the day plugin
async def get_quote_of_the_day():
    url = 'http://api.theysaidso.com/qod.json'
    quote_r = ''
    async with aiohttp.get(url) as response:
        if response.status != 200:
            raise Exception('Error talking to quote api')
        quote_r = await response.json()

    quote = quote_r['contents']['quotes'][0]['quote']
    author = quote_r['contents']['quotes'][0]['author']
    image = quote_r['contents']['quotes'][0]['background']

    return quote, author, image


@bot.listen('(([Cc]an|[Mm]ay) I have the )?quote of the day\?$')
async def quote_of_the_day(message, *args, **kwargs):
    quote, author, image = await get_quote_of_the_day()
    google_url = 'http://www.google.com/search?q={}'
    attachment = Attachment(fallback='The quote of the day',
                            text='_{}_'.format(quote),
                            author_name=author,
                            author_link=google_url.format(author),
                            footer='theysaidso.com',
                            color='good',
                            thumb_url=image)
    message.attachments.append(attachment)
    await bot.send(message)


@bot.listen('test message')
async def test_message(message, *args, **kwargs):
    message.text = 'A beautiful message'
    message.username = 'BOT'
    message.icon = ':tada:'
    att = Attachment(title='Carter',
                     fallback='A test attachment',
                     image_url='http://imgs.xkcd.com/comics/regex_golf.png',
                     )

    f1 = Field(title='Field1', value='A short field', short=True)
    f2 = Field(title='Field2', value='A short field', short=True)
    f3_str = 'A long *long* ~long~ `long` _long_ long field\n'
    f3 = Field(title='Field3', value=f3_str * 3)
    att.fields += f1, f2, f3

    b1 = Button(name='b1', text='Bonjour', style='primary')
    b2 = Button(name='b2', text='Hello')
    confirm = {'title': 'Are you sure?',
               'text': 'DANGER DANGER DANGER !!!',
               'ok_text': 'Yes',
               'dismiss_text': 'No'}
    b3 = Button(name='b3', text='Danger', style='danger', confirm=confirm)

    att.actions += b1, b2, b3

    message.attachments.append(att)
    await bot.send(message)


if __name__ == '__main__':
    bot.run()
