import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

class Movie(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Movie Cog is Ready")

    @commands.command(name = "영화추천", description = "구글무비에서 상위권영화를 제공합니다")
    async def Movie(self, ctx):
        url = "https://play.google.com/store/movies/top"
        headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Accept-Language":"ko-KR,ko"
        }

        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")

        movies = soup.find_all("div", attrs={"class":"ImZGtf mpg5gc"})


        with open("movie.html", "w", encoding="utf8") as f:
            f.write(res.text)
            f.write(soup.prettify()) # html 문서를 예쁘게 출력
        
        
         # 1부터 10까지 i 에 담는다
        a = 0
        
        for movie in movies:
            a += 1
            embed = discord.Embed(title = f'영화순위 TOP{a}', description = '', color = discord.Color.blue())
            
        # img = soup.select_one('img').get('srcset')

            title = movie.find("div", attrs={"class":"WsMG1c nnK0zc"}).get_text()
            # embed.set_image(url=img)
            embed.add_field(name=f"{a}위",value=f"{title}",inline=False)    
        # for item in soup:
        # image = soup.find('img', attrs = {'data-srcset' : True}.find('data-src'))
        # print(soup.find(attrs={"class":"yNWQ8e K3IMke"}))
            image = movie.find("img", attrs={"class":"T75of QNCnCf"})['data-src']
            link = movie.find("a", attrs={"class":"JC71ub"})['href']
            link = "https://play.google.com" + link
            print(link)
        # print(image)
            embed.set_thumbnail(url=image)
            embed.add_field(name='​​​​',value=f'[자세히보기]({link})')
            await ctx.send(embed = embed)

 #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
   

    @commands.command(name="넷플릭스순위")
    async def quiz(self, ctx, *keywords):
        keyword = ' '.join(keywords)
        url = f"https://flixpatrol.com/title/{keyword}/"
        headers = {'User-Agent':'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        print('응답 : ', response)

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.select_one("h2.mb-3").text
        data = soup.select("tbody.tabular-nums tr")

        embed=discord.Embed(title="넷플릭스 월드 순위", description="넷플릭스 월드 인기 순위를 안내합니다.", Color=discord.Color.blue())
        await ctx.send(embed=embed)


        embed = discord.Embed(title=title, description="", Color=discord.Color.blue())
        thumbnail = soup.select_one('body > div.content.mt-4 > div > div.w-40.md\:w-1\/5.mb-4.mx-auto.md\:mt-1.flex-shrink-0 > div > picture > img').get('src').replace('.jpg', '.webp')
        print(thumbnail)
        embed.set_thumbnail(url=f"https://flixpatrol.com/{thumbnail}")
        for item in data:
            contry=item.select_one('a').text
            ranking=item.select_one('#netflix > div:nth-child(2) > div > table > tbody > tr > td:nth-child(8)').text.replace("\t", "").replace("\n", "").replace(".", "")
            embed.add_field(name=f"나라:{contry}", value=f"순위:{ranking}", inline=False)
        await ctx.send(embed=embed)    

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def setup(client):
    client.add_cog(Movie(client))