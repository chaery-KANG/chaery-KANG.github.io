from logging import fatal
import discord
from discord.ext import commands
from gtts import gTTS

class Help(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help Cog is ready!")

    @commands.command(name="명령어", decription="명령어 목록을 보여줍니다.")
    async def pint(self,ctx):
        embed = discord.Embed(title='명령어 도움말', description = "명령어 목록을 보여줍니다.", color=0xff9999)
        cogs = self.client.cogs

        for name,cog in cogs.items():
            commandList = ""
            for command in cog.walk_commands():
                commandList += f"```=={command.name} {command.signature}```{command.description}\n"
            commandList += "\n"
            embed.add_field(name=name,value=commandList,inline=False)

        await ctx.send(embed=embed)


    @commands.command(name='음성')
    async def play_tts(self,ctx,*args):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connnet()
                embed=discord.Embed(title='TTS 연결',description='TTS 사용을 시작합니다.', color=0x99ffff)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='오류 발생', description='음성 채널에 들어간 후 명령어를 사용해주세요!', color=0x993300)
                await ctx.send(embed=embed)
                raise commands.CommandError("Author not connected to a voice channel.")

            text=' '.join(args)
            tts=gTTS(text=text, lang='ko', slow=False)
            tts.save('voice.mp3')

            player=discord.FFmpegPCMAudio(source="c:",options='-vn', executable="c:/ffmpeg/bin/ffmpeg.exe")

            embed=discord.Embed(title=f"{ctx.author.name}'s Say", description=text, color=0xff9999)
            await ctx.send(embed=embed)

    @commands.command(name='음성종료', description='TTS 사용을 종료합니다.')
    async def play_tts(self,ctx):
        voice=ctx.voice_client
        if voice.is_connected():
            await voice.disconnnet()
            embed=discord.Embed(title='TTS 연결 종료',description='TTS 사용을 종료합니다.', color=0xcc99ff)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))