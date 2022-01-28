import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


class Melon(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.base_url = "https://www.melon.com/chart/index.htm"
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Melon Cog is Ready")
        
    @commands.command(name ="음악순위")
    async def restaurant(self, ctx, *args):
        keyword = ' '.join(args)
        url = "https://www.melon.com/chart/index.htm"


        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)


        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select("tbody > tr.lst50")


        if len(data) > 5: 
            limit = 5
        else:
            limit = len(data) 
        # 출력될 데이터의 개수를 5개로 제한해줌
        i=0

        for item in data[:limit]:
            i=i+1
            image= item.select_one('img').get('src')
            title = item.select_one('div.rank01').text.replace('\n', '')
            singer =item.select_one('span.checkEllipsis').text.replace('\n', '')
            album = item.select_one('div.rank03').text.replace('\n', '')
            
            embed = discord.Embed(title = title, description = f'{i}위', color = discord.Color.blue())
            embed.set_thumbnail(url = image)
            embed.add_field(name = '제목' , value = title, inline=False)
            embed.add_field(name = '가수' , value = singer, inline=False)
            embed.add_field(name = '앨범 제목' , value = album)
            
            await ctx.send(embed = embed)
 


def setup(client):
    client.add_cog(Melon(client))