import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import datetime
from selenium import webdriver
import time

class Webnovel(commands.Cog):
    def __init__(self,client):
        self.client = client

    def get_detail_data(self,name):
        # 띄워쓰기 연결하기
        novel_data = ' '.join(name)

        # chrome webdriver 연결하기
        driver_path = "D:\...\selenium\chromedriver.exe"
        url = f"https://novel.naver.com/search?keyword={novel_data}&section=webnovel&target=novel"

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(driver_path,options=options)
        driver.get(url)
        time.sleep(1)
        
        href = ""
        data = driver.find_element_by_css_selector("#content > div > div.cont_sub > ul > li.on > a > span.cnt")
        detail_data = []
        
        if data.text == "1":
            data = driver.find_element_by_css_selector("#content > div > div.cont_sub > div.srch_cont.NE\=a\:nov > ul > li > a")
            href = data.get_attribute("href")
            driver.get(href)
            time.sleep(1)
            
            href = driver.find_elements_by_css_selector("div.section_area_info a")[0].get_attribute("href")
            href = href.split("=")[1]
            detail_data.append(driver.find_elements_by_css_selector("div.section_area_info a img")[0].get_attribute("src"))
            detail_data.append(href)
            detail_data.append(driver.find_elements_by_css_selector("div.section_area_info p.dsc")[0].text)
            detail_data.append(driver.find_elements_by_css_selector("div.section_area_info span.download")[0].text)
            detail_data.append(driver.find_elements_by_css_selector("div.section_area_info span.publish")[0].text)
            detail_data.append(driver.find_elements_by_css_selector("div.section_area_info span.genre")[0].text)
            detail_data.append(driver.find_elements_by_css_selector("div.section_area_info a img")[0].get_attribute("alt"))
        driver.close()
        return detail_data

    def get_data(self,args):
        order_dict = {"조회순":"Read","별점순":"Star","제목순":"Title","관심등록순":"Like"}
        genre_dict = {"전체":"all","로맨스":"101","로판":"109","판타지":"102","현판":"110","무협":"103","미스테리":"104"}
        week_list = ["월","화","수","목","금","토","일"]
        week_keyword = ["MON","TUE","WED","THU","FRI","SAT","SUN"]

        week_day = week_keyword[datetime.datetime.today().weekday()]
        order = "조회순"    
        genre = "전체"
        if len(args) > 0:
            for key in args:
                if key in order_dict.keys():
                    order = order_dict[key]
                if key in genre_dict.keys():
                    genre = genre_dict[key]
                if key in week_list:
                    week_day = week_keyword[int(week_list.index(key))]

        url = f"https://novel.naver.com/webnovel/weekdayList?week={week_day}&genre={genre}&order={order}"
        headers = {"User-Agent":"Mozilla/5.0"}
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text,"html.parser")
        return soup.select("ul.list_type1 li")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Webnovel Cog is ready!")

    @commands.command(name="소설상세",description="정확한 소설명을 적어주세요.")
    async def webnovel_detail(self,ctx,*novel):
        if novel is None:
            embed = discord.Embed(
                title="웹소설 이름",
                description="보고싶은 웹소설명을 정확히 적어주세요.",
                color=discord.Color.red()
            )         
        else:
            data = self.get_detail_data(novel)
            if len(data) == 0:
                embed = discord.Embed(
                    title="존재하지 않는 소설",
                    description="해당 소설이 검색되지 않습니다.",
                    color=discord.Color.red()
                )            
            else:
                embed = discord.Embed(
                    title=data[6],
                    description=data[2],
                    color=discord.Color.dark_purple()
                )
                embed.set_thumbnail(url=data[0])
                embed.add_field(name="download",value=data[3])
                embed.add_field(name="연재일",value=data[4])
                embed.add_field(name="장르",value=data[5])
                embed.add_field(name="소설보기",value=f"[전체보기](https://novel.naver.com/webnovel/list?novelId={data[1]})",inline=False)
        await ctx.send(embed=embed)

    # 네이버 웹소설 검색
    @commands.command(name="웹소설")
    async def today_update(self,ctx,*args):
        data = self.get_data(args)
        for item in data[:5]:
            img = item.select_one("img").get("src")
            title = item.select_one("li > a").get("title")
            artist = item.select_one("span.ellipsis").text
            rating = item.select_one("p.rating em").text
            updt = item.select_one("span.bullet_up")
            total = item.select_one("span.num_total").text
            tot_list = item.select_one("li > a").get("href")
            update = " up!up!" if updt is not None else ""
            # print(tot_list,updt,total,rating)
            embed = discord.Embed(
                title=title + update,
                description = "",
                color = discord.Color.blue()
            )
            embed.set_thumbnail(url=img)
            embed.add_field(name="작가",value=artist)
            embed.add_field(name="총회차",value=total)
            embed.add_field(name="평점",value=rating)
            embed.add_field(name="전체보기",value=f"['{title}' 전체보기](https://novel.naver.com{tot_list})",inline=False)
            await ctx.send(embed=embed)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.command(name ="베스트셀러")
    async def bestbook(self, ctx):
        def checkMessage(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
    
        genres = list(self.bookDict.keys())
        embed = discord.Embed(title = '베스트셀러 목록', description = f'{genres} 중에서 하나를 골라주세요.', color = discord.Color.dark_green())
        await ctx.send(embed=embed)

        message = await self.client.wait_for("message", check=checkMessage)
        genre = message.content

        url = self.bookDict[f'{genre}']
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select("ul.list_type01 li")

        rank = 1
        for item in data[:5]:
            bimg = item.select_one("img").get("src")
            title = item.select_one("div.title strong").text
            detail = item.select_one("div.author").text
            dt = detail.split('|')
            author = dt[0].split()[0]
            publisher = dt[1].split()[0]
            date = dt[2]
            price = item.select_one("div.price strong").text
            deliver = item.select_one("div.info strong").text
            link = item.select_one("div.title a").get("href")

            embed = discord.Embed(title = f"{rank}. {title}", description = '', color = discord.Color.dark_green())
            embed.set_thumbnail(url = bimg)
            embed.add_field(name = '작가  |  출판사  |  출간일' , value = f"{author}  |  {publisher}  |  {date}", inline=False)
            embed.add_field(name = '가격' , value = price, inline=False)
            embed.add_field(name = '배송일' , value = f'지금 주문하면 {deliver} 도착 예정입니다.', inline=False)
            embed.add_field(name = '구매 링크' , value = link, inline=False)

            rank +=1
            
            await ctx.send(embed = embed)


            
def setup(client):
    client.add_cog(Webnovel(client))