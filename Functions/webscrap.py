import random
from datetime import datetime
import discord
import requests
from bs4 import BeautifulSoup


def quote_choice():
    choice = quote_scraped(), quote_scraped_islamic()
    return choice


def quote_scraped_islamic():
    randomNum = random.randint(1, 60)
    randomNum2 = random.randint(1, 12)

    html_text = requests.get('https://www.goodreads.com/quotes/tag/islam?page=' + str(randomNum)).text
    soup = BeautifulSoup(html_text, 'lxml')
    quote = soup.find_all('div', class_='quoteText')
    randomQuote = quote[randomNum2].text
    randomQuoteSplitted0 = randomQuote.split("―")[0]
    randomQuoteSplitted1 = randomQuote.split("―")[1].replace("  ", "")
    quoteFormatted = "```Quote:- \n" + randomQuoteSplitted0 + "\nAuthor:- \n" + randomQuoteSplitted1 + "\n```"
    return quoteFormatted


def quote_scraped():
    randomNum2 = random.randint(1, 12)
    randomNum3 = random.randint(1, 100)

    html_text = requests.get("https://www.goodreads.com/quotes?page=" + str(randomNum3)).text
    soup = BeautifulSoup(html_text, 'lxml')
    quote = soup.find_all('div', class_='quoteText')
    randomQuote = quote[randomNum2].text
    randomQuoteSplitted0 = randomQuote.split("―")[0]
    randomQuoteSplitted1 = randomQuote.split("―")[1].replace("  ", "")
    quoteFormatted = "```Quote:- \n" + randomQuoteSplitted0 + "\nAuthor:- \n" + randomQuoteSplitted1 + "\n```"
    return quoteFormatted


def urdu_quote_scraped():
    randomNum2 = random.randint(1, 94)

    html_text = requests.get("https://www.urdughr.com/2020/03/best-quotes-in-urdu.html").text
    soup = BeautifulSoup(html_text, 'lxml')
    quote = soup.find_all('span', style='font-family: "jameel noori nastaleeq"; font-size: 22px;')
    randomQuote = quote[randomNum2].text
    quoteFormatted = f'```Quote:-{randomQuote}```'
    return quoteFormatted


def taymiyah_quote_scraped():
    randomNum2 = random.randint(1, 30)

    html_text = requests.get("https://www.inspiringquotes.us/author/2554-ibn-taymiyyah").text
    soup = BeautifulSoup(html_text, 'lxml')
    quote = soup.find_all('p', class_='quote')
    randomQuote = quote[randomNum2].text
    quote_splitted = randomQuote.split("--")
    quoteFormatted = f"```Quote:- \n\n{quote_splitted[0]} \n\n\nAuthor:-\n\n {quote_splitted[1]}```"
    return quoteFormatted


def ghazaali_quote_scraped():
    randomNum2 = random.randint(1, 30)

    html_text = requests.get("https://www.inspiringquotes.us/author/6463-al-ghazali").text
    soup = BeautifulSoup(html_text, 'lxml')
    quote = soup.find_all('p', class_='quote')
    randomQuote = quote[randomNum2].text
    quote_splitted = randomQuote.split("--")
    quoteFormatted = f"```Quote:- \n\n{quote_splitted[0]} \n\n\nAuthor:-\n\n {quote_splitted[1]}```"
    return quoteFormatted


def al_jawzi_quote_scraped():
    randomNum2 = random.randint(1, 30)

    html_text = requests.get("https://www.inspiringquotes.us/author/6464-ibn-qayyim-al-jawziyya").text
    soup = BeautifulSoup(html_text, 'lxml')
    quote = soup.find_all('p', class_='quote')
    randomQuote = quote[randomNum2].text
    quote_splitted = randomQuote.split("--")
    quoteFormatted = f"```Quote:- \n\n{quote_splitted[0]} \n\n\nAuthor:-\n\n {quote_splitted[1]}```"
    return quoteFormatted


def create_list(r1, r2):
    return [item for item in range(r1, r2 + 1)]


def history_today():
    text = ""
    html_text = requests.get("https://www.history.com/this-day-in-history").text
    soup = BeautifulSoup(html_text, "lxml")
    history_today_text = soup.find_all('h2', class_='m-ellipsis--text m-card--header-text')
    history_today_date = soup.find_all('div', class_="m-card--label mm-card--tdih-year")
    length = len(history_today_date)
    list_of_events = create_list(0, length - 1)
    count = 0
    for x in history_today_date:
        if (count % 2) == 0:
            list_of_events[count] = x.text
            count = count + 1
        else:
            count = count + 1
    count = 0
    for y in history_today_text:
        if (count % 2) != 0:
            list_of_events[count] = y.text
            count = count + 1
        else:
            count = count + 1
    count = 0
    for z in list_of_events:
        if count % 2 == 0:
            text = text + str(z) + ":-\n"
        else:
            text = text + str(z) + "\n"
        count = count + 1
    print(text)


history_today()


def history_today_second(ctx):
    html_text = requests.get("https://www.timeanddate.com/on-this-day/").text
    soup = BeautifulSoup(html_text, "lxml")
    history_today_text = soup.find("ul", class_="list--big")
    history_today_text = history_today_text.find_all("h3", class_="otd-title")
    text_of_history = create_list(0, len(history_today_text) - 1)
    dates = create_list(0, len(history_today_text) - 1)
    count = 0
    for x in history_today_text:
        date = x.text
        item = date.split(" ")
        date = item[0]
        text_of_history[count] = item[1:]
        dates[count] = date
        count = count + 1

    print(str(text_of_history))

    embed = discord.Embed(title="__***History of Today in the Past***__", color=0xe600ff, timestamp=datetime.utcnow())
    counter = 0
    text = ""
    for x in dates:
        for y in text_of_history[counter]:
            text = text + " " + y
        text = text + "."
        embed.add_field(name=f"📍{str(x)}", value=f"```{str(text)}```", inline=False)
        counter = counter + 1
        text = ""
    try:
        if ctx == "none":
            embed.set_footer(text=f"✔ Requested Autonomously")
        else:
            embed.set_footer(text=f"✔ Request by: {ctx.author.name}")
    except:
        embed.set_footer(text=f"✔ Requested Autonomously")

    return embed
