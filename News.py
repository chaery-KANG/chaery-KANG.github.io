#News.py
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests

class News(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.base_url = "https://media.naver.com/press/056"
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("News Cog is Ready")


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------        

    @commands.command(name ="주요뉴스", description="오늘의 주요뉴스를 보여줍니다.")
    async def news(self, ctx):
        url = "https://media.naver.com/press/056"

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select("li.press_news_item")

        for item in data:
            title = item.select_one('span.press_news_text').text.replace('\n', '')
            link = item.select_one('a').get('href')

            embed = discord.Embed(title = 'News', color =discord.Color.blue())

            embed.add_field(name = '기사제목', value = title)
            embed.add_field(name = 'url', value = 'https://media.naver.com/press/0560' + link)
            await ctx.send(embed=embed)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.command(name ="코로나")
    async def restaurant(self, ctx, *args):
        keyword = ' '.join(args)
        url = "http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun="


        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)


        soup = BeautifulSoup(response.text, 'html.parser')
        items1 = soup.select("div.caseTable > div > ul.ca_body")


        print("확진환자")
        today =items1[-1].select_one('dd.ca_value').text
        print("  오늘 확진자 :", today)
        
        items2 = soup.select("div.mini > table.num > tbody") #div.data_table mgt16 tbl_scrl_m mini
        
        yesterday =items2[3].select('td')
        yester = yesterday[5].text
        print("  전일 확진자 :", yester)


        a=today.replace(',', '')
        b=yester.replace(',', '')


        sub = int(a) - int(b)
        if sub>0:
            ch = '+'
        else:
            ch = ''
        sub_char = ch+str(sub)
        
        embed = discord.Embed(title = '국내 코로나 확진자 수 발생 현황', description = '코로나바이러스감영증-19 국내 발생 현황입니다.', color = discord.Color.dark_green())
        embed.add_field(name = '오늘 확진자' , value = today)
        embed.add_field(name = '전일 확진자' , value = yester)
        embed.add_field(name = '전일 대비' , value = sub_char)
            
        await ctx.send(embed = embed)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.command(name ="많이본뉴스", description="오늘 많이 본 뉴스순위를 보여줍니다.")
    async def news(self, ctx):
        url = "https://news.kbs.co.kr/common/main.html"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select("div.col-rank")
  
        for item in data:
            title = item.select_one('h3.header').text
            news_title = item.select_one('em.tit').text.replace('\n', '')
            link = item.select_one('a').get('href')

            embed = discord.Embed(title = title, color = discord.Color.purple())

            embed.add_field(name = '기사제목', value = news_title)
            embed.add_field(name = 'url', value = 'https://news.kbs.co.kr/common/main.html' + link)
            
            await ctx.send(embed=embed)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.command(name ="기사검색")
    async def gisagumsaek(self, ctx, *args):
        keyword = ' '.join(args)
        url = f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={keyword}"

        # 요청 전송
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        # html 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        news_titles = soup.select('ul.list_news > li.bx')
        

        await ctx.send(f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={keyword}")
        if len(news_titles) > 5:
            limit = 5
        else:
            limit = len(news_titles)

        for item in news_titles[:limit]:
            gisa = item.select_one('a.news_tit').text
            where = item.select_one('a.info.press').text
            thumbnail = item.select_one('a.dsc_thumb > img').get("src")
            link = item.select_one('a').get('href')

            embed = discord.Embed(title = gisa, description = where, color=0xccffff)
            embed.set_thumbnail(url = thumbnail)
            

            await ctx.send(embed = embed)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.command(name = "환율")
    async def exchange_rate(self, ctx):
        keyword = "환율"
        url = f"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bk01&qvt=0&query={keyword}"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select("table.rate_table_info > tbody > tr")

        for item in data :
            link = item.select_one('a').get('href')
            title = item.select_one('a span').text.replace('\n', '')
            rate =item.select_one('td span').text
            dtd = item.select_one('td.flu_nm span.ico').text +" "+ item.select_one('table.rate_table_info td.flu_nm em').text 
            fluctuation_rate = item.select_one('td.flu_pct span').text
            
            if item.select_one('td.flu_nm span.ico').text == "상승" :
                embed = discord.Embed(title = title, color = discord.Color.red())
            else : 
                embed = discord.Embed(title = title, color = discord.Color.blue())
            
            embed.add_field(name = '매매기준율' , value = rate,)
            embed.add_field(name = '전일대비' , value = dtd)
            embed.add_field(name = '등락률' , value = fluctuation_rate)
            embed.add_field(name = '링크' , value = "https://search.naver.com/search.naver"+link, inline=False)
            
            await ctx.send(embed = embed)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
def setup(client):
    client.add_cog(News(client))