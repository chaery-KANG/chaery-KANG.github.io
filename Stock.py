#stock.py
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

class stock(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("stock Cog is Ready")
    
    @commands.command(name ="주가")
    async def restaurant(self, ctx, *args):
        keyword = ' '.join(args)
        url = "https://finance.naver.com/sise/sise_market_sum.nhn?page=1"

        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        stock_list = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")

        if len(stock_list) > 5:
            limit = 6
        else:
            limit = len(stock_list)
        for item in stock_list[:limit]:
            if len(item) <= 1 :
                continue
            stock_info = item.get_text().split()
            link = "https://finance.naver.com/"+item.select_one('a').get('href')
            title = stock_info[1]
            price = stock_info[2]
            diff = stock_info[4]
            diff_prc = stock_info[3]
            total = stock_info[6]
            per = stock_info[10]
            block = stock_info[5]
            
            if diff[0] == '-':
                diff_prc = ''.join(['-', diff_prc])
                COLOR = discord.Color.blue()
            else:
                diff_prc = ''.join(['+', diff_prc])
                COLOR = discord.Color.red()

            embed = discord.Embed(title = title, description = link, color = COLOR)
            # embed.set_thumbnail(url = thumbnail)
            embed.add_field(name = '종가' , value = price)
            embed.add_field(name = '전일비' , value = diff_prc)
            embed.add_field(name = '등락율' , value = diff)
            embed.add_field(name = '시가총액' , value = total)
            embed.add_field(name = 'PER' , value = per)
            embed.add_field(name = '액면가' , value = block)
            
            await ctx.send(embed = embed)

            
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.command(name="인기종목")
    async def restaurant(self, ctx):
        url = "https://finance.naver.com/sise/"
        headers = {'User-Agent':'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        data = soup.select("ul.lst_pop li")

        for item in data:
            ranking=item.select_one('em').text.replace('\"', '')
            title=item.select_one('a').text
            price = item.select_one('span').text
            embed = discord.Embed(title=title, description="", color=discord.Color.blue())
            embed.add_field(name="순위", value= ranking)
            embed.add_field(name="가격", value=price)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(stock(client))
