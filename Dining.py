from gettext import dgettext
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import random
import json

class Dining(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open("./data/lunch.json", 'r', encoding='utf-8') as f:
            self.lunchDict = json.load(f)   
    @commands.Cog.listener()
    async def on_ready(self):
        print("Dining Cog is Ready")

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.command(name ="밥추천", description = "간단하게 식사에 대한 추천을 해드립니다.")
    async def recommand_lunch(self, ctx, arg1 = None, arg2 = None):
        if arg1 == None and arg2 == None :
            categories = list(self.lunchDict.keys()) # categories : ['한식', '일식', .. ]
            category = random.choice(categories)     # category : ex) '한식
            lunch = random.choice(self.lunchDict[category]) # lunch : ex) 떡볶이
            embed = discord.Embed(title = f'오늘의 식사 추천! <<{lunch}>> ', description = f"오늘 식사는 {category}, 그 중에서 {lunch} 어떠세요?", color = discord.Color.green())
            await ctx.send(embed=embed)

        elif arg1 != None and arg2 == None:
            category = arg1
            lunch = random.choice(self.lunchDict[category])
            embed = discord.Embed(title = f'오늘의 식사 추천! <<{lunch}>> ', description = f"오늘 식사는 {lunch} 어떠세요?", color = discord.Color.green())
            await ctx.send(embed=embed)


        elif arg1 != None and arg2 != None:
            category1, category2 = arg1, arg2
            random_list = self.lunchDict[category1]
            random_list += self.lunchDict[category2]
            lunch = random.choice(random_list)
            embed = discord.Embed(title = f'오늘의 식사 추천! <<{lunch}>> ', description = f"{category1}이랑 {category2}을 선택하셨어요. 그렇다면 오늘 식사는 {lunch} 어떠세요?", color = discord.Color.green())
            await ctx.send(embed=embed)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command(name ="맛집", description = "==맛집 동네 음식 순으로 입력해주세요")
    async def _맛집(self,ctx,*food):
        if food==():
            embed=discord.Embed(title='오류 발생',description='검색어를 입력해주세요',color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            food='%s'%(' '.join(food))

        url="https://www.mangoplate.com/search/%s"%food
            
        headers={'User-Agent': 'Mozilla/5.0'}
        response=requests.get(url, headers=headers)
        soup=BeautifulSoup(response.text,"html.parser")
        data=soup.select("li.server_render_search_result_item > div.list-restaurant-item")

        if len(data)==0:
            embed=discord.Embed(title='오류 발생',description='검색 결과가 없습니다',color=discord.Color.red())
            await ctx.send(embed=embed)
            raise commands.CommandError('No search results')
    
        if len(data)>3:
            limit=3
        else:
            limit=len(data)
            
        embed=discord.Embed(title='맛집 추천',description='%s 맛집입니다'%food,color=0xffd770)
        await ctx.send(embed=embed)
        
        for i in data[:limit]:
            image=i.select_one('img').get('data-original')
            link=i.select_one('a').get('href')
            title=i.select_one('h2.title').text.replace('\n', '')
            rating=i.select_one('strong.search_point').text
            category=i.select_one('p.etc').text
            view=i.select_one('span.view_count').text
            review=i.select_one('span.review_count').text

            embed=discord.Embed(title=title,description=category,color=0xff8c0)
            if len(rating)==0:
                embed.add_field(name='평점',value='None')
            else:
                embed.add_field(name='평점',value=rating)

            embed.add_field(name='조회수',value=view)
            embed.add_field(name='리뷰 수',value=review,inline=True)
            embed.add_field(name='링크',value='https://www.mangoplate.com%s'%link)

            if 'https' in image:
                embed.set_thumbnail(url=image)
            
            await ctx.send(embed=embed)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.command(name ="쿠팡")
    async def Coupang(self, ctx, keyword):

        url = f'https://coupang.com/np/search?component=&q={keyword}&channel=user'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select('li.search-product')

        if len(data) > 7:
            limit = 7
        else :
            limit = len(data)

        for item in data[:limit]:
            link = 'https://coupang.com' + item.select_one('a').get('href')
            if item.select_one('img').get('data-img-src') == None:
                image = 'https:'+item.select_one('img').get('src')
            else:
                image = 'https:'+item.select_one('img').get('data-img-src')
            title = item.select_one('div.name').text
            price = item.select_one('strong.price-value').text + '원'
            if item.select_one('div.used-product-info') !=None:
                product_info = item.select_one('div.used-product-info').text
            else : 
                product_info = '새 상품'
            rating = item.select_one('em.rating').text
            rating_count = item.select_one('span.rating-total-count').text

            embed = discord.Embed(title = title, description =  price, color = discord.Color.dark_gold())
            embed.set_thumbnail(url= image)
            embed.add_field(name = '제품 설명', value= product_info, inline=False)
            embed.add_field(name = '평점', value=rating)
            embed.add_field(name = '리뷰수', value = rating_count)
            embed.add_field(name='주소', value = link, inline=False)
            
            await ctx.send(embed=embed)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.command(name = '영화')
    async def current_movie(self, ctx):
        url = f"https://movie.naver.com/movie/running/current.naver"
        headers={'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select("#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li")

        if len(data) > 5 :
            limit = 5

        else:
            limit = len(data)
        
        for item in data[:limit]:
            image = item.select_one('img').get('src')
            link = item.select_one('a').get('href').split('=')[1]
            title = item.select_one('img').get('alt')
            film_rate = item.select_one('span').text
            ticket_sales = item.select_one('span.num:nth-child(1)').text + "%"
            rating = item.select_one('span.num').text
            genre = ' '.join(item.select_one('span.link_txt').text.split())
            
            c = -1
            for d in item.select_one('dd:nth-child(3)').text.split():
                if '분' in d:
                    showtimes = d
                    c=2
                if c == 0 :
                    release = d
                    break
            
            director = item.select_one('dd:nth-child(4)').text.strip()
            if item.select_one('dd:nth-child(6)') != None:
                cast = ' '.join(item.select_one('dd:nth-child(6)'.text.split()))

            embed = discord.Embed(tilte=title, description=genre,
                url="https://movie.naver.com/movie/bi/mi/basic.naver?code=" + link, color = discord.Color.blue())

            embed.set_thumbnail(url= image)
            embed.add_field(name='개봉날짜', value = release, inline=False)
            embed.add_field(name='등급', value = film_rate, inline=False)
            embed.add_field(name='상영 시간', value = showtimes, inline=False)
            embed.add_field(name='감독', value = director, inline=False)
            embed.add_field(name='평점', value = rating, inline=False)
            embed.add_field(name='예매율', value = ticket_sales, inline=False)
            embed.add_field(name='출연', value = cast, inline=False)
            
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Dining(client))