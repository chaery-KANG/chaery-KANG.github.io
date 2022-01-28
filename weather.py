#weather.py

from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup

class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.Cog.listener()
    async def on_ready(self):
        print("Weather Cog is Ready")


    @commands. command (name ="오늘날씨")
    async def restaurant(self, ctx, *args):
        keyword =' '.join(args)
        url=f"https://search.naver.com/search.naver?where=nexearch&sm=top_fbm=1&ie=utf8&query={keyword}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html. parser')
        data = soup. select(".status _wrap")
        
        embed = discord.Embed(title = "오늘의 날씨", description = "날씨", color = discord.Color.blue())
        embed.add_field (name = "제목", value = f"{data[0].select_one('h3').text}")
        embed. add_field (name = f"{keyword}", value = f"{data[0].select_one('.temperature_text').text.strip()}")
        
        await ctx.send(embed = embed)


    @commands.command(name='날씨')
    async def _날씨(self,ctx,*area):
        if len(area)==0:
            embed=discord.Embed(title='날씨',description="'==날씨'와 함께 시, 군/구, 동을 입력하세요\nex) ==날씨 서울, ==날씨 서울 여의도동, ==날씨 서울 여등포구 여의도동",color=0x87cefa)
            await ctx.send(embed=embed)
            
        else:
            area='%s'%(' '.join(area))
            url='https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%s날씨'%area

            raw=requests.get(url)
            soup=BeautifulSoup(raw.text,"html.parser")
            box=soup.find('div', {'class' : 'today_area _mainTabContent'})
            temp=box.find_all('span',{'class':'todaytemp'})
            temps=box.find_all('span',{'class':'num'})
            dust=box.find_all('dd')
            feel=box.find_all('p',{'class':'cast_txt'})
            sense=box.find('span',{'class':'sensible'})
            sensetemp=sense.find_all('em')

            embed=discord.Embed(title='날씨',description='오늘 %s의 날씨에 대한 정보입니다.'%area,color=0x87cefa)
            embed.add_field(name='현재온도',value='현재온도는 %s°로 %s'%(temp[0].text,feel[0].text),inline=False)
            embed.add_field(name='기온',value='체감온도 : %s°\n최저기온 : %s°, 최고기온 :  %s°'%(sensetemp[0].text,temps[0].text,temps[1].text),inline=False)
            embed.add_field(name='미세먼지',value="미세먼지는 %s, 초미세먼지는 %s입니다"%(dust[0].text,dust[1].text),inline=False)
            await ctx.send(embed=embed)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    @commands.command(name ="번역")
    async def transs(self, ctx, arg = None):
        def checkMessage(message):
            return message.author == ctx.author and message.channel == ctx.channel

        while True:
            embed = discord.Embed(title = '번역기', description = f'번역하고 싶은 말을 입력해 주세요!', color = discord.Color.blue())
            await ctx.send(embed = embed)

            message = await self.client.wait_for("message", check = checkMessage)
            wd = message.content

            x = wd.replace(" ", "%20")
            
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(f'https://papago.naver.com/?sk=auto&tk=ko&hn=0&st={x}', headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
    
            trans = soup.find_all(".div/", {"id" : "txtTarget"})
            

            
            embed = discord.Embed(title = "번역 결과입니다", description = '', color = discord.Color.blue())
            embed.add_field(name = '₍ᐢɞ̴̶̷ ̫ ɞ̴̶̷ ᐢ₎', value = trans, inline = True)
            await ctx.send(embed = embed)

            embed = discord.Embed(title = "번역을 계속하시겠습니까?", description = 'y/n', color = discord.Color.purple())
            await ctx.send(embed = embed)
        

            message = await self.client.wait_for("message", check = checkMessage)
            answer = message.content

            if(answer == 'n'):
                embed = discord.Embed(title = "번역을 종료합니다", description = '', color = discord.Color.purple())
                await ctx.send(embed = embed)
                break
            
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def setup(client):
    client.add_cog(Weather(client))