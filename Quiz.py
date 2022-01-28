#Homework2
import discord
from discord.ext import commands
import random
import json
import asyncio
import csv

class Quiz(commands.Cog):
    def __init__(self, client):
        self.client = client   
        self.quizDict = {}
        with open("./data/quiz.csv", 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                self.quizDict[row[0]] = row[1]
    @commands.Cog.listener()
    async def on_ready(self):
        print("Quiz Cog is Ready")

    #6일차
    
    @commands.command(name ="퀴즈", description = "넌센스 퀴즈를 통해서 게임을 진행합니다. 퀴즈랭킹을 통해 자신의 순위를 알아보실 수 있으세요!")
    async def quiz(self, ctx):
        problemList = list(self.quizDict.keys())
        problem = random.choice(problemList)
        answer = self.quizDict[problem]
        embed = discord.Embed(title = '퀴즈', description = problem, color=0x9966ff)
        await ctx.send(embed=embed)

        def checkAnswer(message):
            if message.channel == ctx.channel and answer in message.content:
                name = message.author.name
                with open("data/score.json", 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if name in data.keys():
                    data[name] += 1
                else:
                    data[name] = 1
                with open("data/score.json", 'w', encoding='utf-8') as f:
                    json.dump(data,f, ensure_ascii = False)
                return True
            else:
                return False
        try:
            message = await self.client.wait_for("message", timeout = 10.0, check = checkAnswer)
            name = message.author.name
            embed = discord.Embed(title = '', description = f'{name} 님, 정답이에요 !', color=0x99ffff)
            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            embed = discord.Embed(title = '', description = f'땡! 시간초과입니다~ 정답은 {answer}이에요!', color=0x990000)
            await ctx.send(embed=embed)
  
    @commands.command(name = '퀴즈랭킹', description = "전체 순위 혹은 개인 순위를 나타냅니다.")
    async def _rank(self, ctx, arg1 = None):
        with open("./data/score.json", 'r', encoding= 'utf-8') as f:
            self.scoreDict = json.load(f)
        ranking = sorted(self.scoreDict.items(), key = lambda x:x[1], reverse=True)

        if arg1 == None:
            embed = discord.Embed(
                    title = "전체 퀴즈 랭킹", 
                    description = "전체 퀴즈 랭킹입니다.\n한 문제를 맞출 때 마다 1점이 증가해요!!", 
                    color = discord.Color.green())

            for i in range(len(ranking)):
                embed.add_field(name = str(i+1)+"등 " + str(ranking[i][0]),
                value=f'점수: {ranking[i][1]}',
                inline = False)

        elif arg1 in self.scoreDict.keys() :
            for i in range(len(ranking)) :
                if arg1 == ranking[i][0] :
                    name = i + 1
                    
            embed = discord.Embed(title='개인 퀴즈 랭킹', description='개인 퀴즈 랭킹입니다.', color=0x9966ff, inline=False)
            embed.add_field(name=f"{arg1}", value=f"{arg1}님은 {self.scoreDict[arg1]}점으로 {name}등입니다.", inline=False)
            
        else:
            embed = discord.Embed(title='', description=f'{arg1}님의 정보가 없습니다.', color=0x993300)

        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Quiz(client))