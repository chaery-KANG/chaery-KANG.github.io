# .cogs/Music.py

import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from .module.youtube import getUrl

class Music(commands.Cog):
    def __init__(self, client):
        option={
            'format': 'bestaudio/best',
            'noplaylist': True,
        }
        self.client = client
        self.DL = YoutubeDL(option)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Cog is Ready")
    

    #음악재생 명령어 입력 (아래)
    @commands.command(name ="음악재생", aliases=['p'])
    
    async def play_music(self, ctx, *keywords):
        keyword = ' '.join(keywords)
        url = getUrl(keyword)
    
    ##음악정보 가져와 출력 
        #await ctx.send(url) ##음악 url 전송
        data=self.DL.extract_info(url, download=False) #extract_info()함수는 url에 해당하는 영상정보를 딕셔너리로 리턴해준다.
        title=data['title']
        uploader=data['uploader']
        uploader_url=data['uploader_url']
        thumbnail=data['thumbnail']
        view_count=data['view_count']
        like_count = data['like_count']
        average_rating = data['average_rating']
        average_rating=data['average_rating']
        tags=data['tags']
        
        embed=discord.Embed(title=title, url=url, color=0x9999ff)        
        embed.set_author(name = uploader, url = uploader_url )
        embed.add_field(name = '조회수', value = view_count, inline = True)
        embed.add_field(name = '평점', value = average_rating, inline = True)
        embed.add_field(name='좋아요', value=like_count)
        embed.add_field(name = '관련 태그', value = tags)
        embed.set_image(url = thumbnail)
        await ctx.send(embed=embed)

    ##음악 재생 메인 구축
        #봇의 음성 채널 연결이 없으면
        if ctx.voice_client is None: # 명령어(ctx) 작성자(author)의 음성 채널에 연결 상태(voice)
            if ctx.author.voice: # 봇을 명령어 작성자가 연결되어 있는 음성 채널에 연결
                await ctx.author.voice.channel.connect()
            else:
                embed = discord.Embed(title = '오류 발생', description = "음성 채널에 들어간 후 명령어를 사용 해 주세요!", color=0x990000)
                await ctx.send(embed=embed)
                raise commands.CommandError("Author not connected to a voice channel.")

        #봇이 음성채널에 연결되어 있고, 재생중이라면
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop() # 현재 재생중인 음원을 종료


      ##음악 재생 꾸미기
        embed = discord.Embed(title = '음악 재생', description = '음악 재생을 준비하고있어요. 잠시만 기다려 주세요!' , color=0xff9900)
        await ctx.send(embed=embed)

        data = self.DL.extract_info(url, download = False)
        link = data['url']
        title = data['title']

        ffmpeg_options = {
            'options': '-vn',
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        }
        player = discord.FFmpegPCMAudio(link, **ffmpeg_options, executable = "C:/ffmpeg/bin/ffmpeg")
        ctx.voice_client.play(player)
        
        embed = discord.Embed(title = '음악 재생', description = f'{title} 재생을 시작힐게요!' , color=0xff9900)
        await ctx.send(embed=embed)
        embed=discord.Embed(title='도움말',description= '"음악재생", "p" => 음악재생\n"음악종료", "q" => 음악종료\n"일시정지", "s" => 일시정지\n"다시시작", "r" => 음악종료', color=0xcc99ff) 
        await ctx.send(embed=embed)
    

    @commands.command(name ="음악종료", aliases=['q'])
    async def quit_music(self, ctx):
        voice = ctx.voice_client
        if voice.is_connected():
            await voice.disconnect()
            embed = discord.Embed(title = '', description = '음악 재생을 종료합니다.' , color=0xcc3300)
            await ctx.send(embed=embed)

    @commands.command(name='일시정지', aliases=['s'])
    async def pause_music(self,ctx):
        voice=ctx.voice_client
        if voice.is_playing():
            voice.pause()
            embed=discord.Embed(title='',description= '음악 재생을 일시정지합니다',color=0x99ffcc) 
            await ctx.send(embed=embed)

    @commands.command(name='다시시작', aliases=['r'])
    async def resum_music(self,ctx):
        voice=ctx.voice_client
        if voice.is_paused():
            voice.resume()
            embed=discord.Embed(title='',description= '음악 재생을 다시 시작합니다',color=0xff9900) 
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Music(client))