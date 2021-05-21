import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import time
import bestdllever
import os

try:
    TOKEN = os.getenv("BOT_TOKEN")
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='!',intents=intents)
    names = []
    main_target_member = ""
    active_channel_id = ""
    main_guild = ""

    @bot.event
    async def on_ready(): # Ивент срабатывает при запуске бота
        with open("names.txt","r",encoding="utf-8") as f:
            for line in f:
                if "\n" in line:
                    names.append(bestdllever.deleten(line))
                else:
                    names.append(line)

        if "Kolbaska" not in names:
            names.append("Kolbaska")

        print(names)
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

    @bot.command()
    async def join(ctx): # Функция по входу на канал
        global vc
        try: # Если не получается просто присоединиться бот пытается выйти и зайти 
            channel = ctx.author.voice.channel # Выбирается обьект канала, на котором в данный момент находится запросивший
            active_channel_id = channel.id
            print(time.strftime("%c",time.gmtime(time.time()))+" Connected to "+str(active_channel_id)) 
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe",source="soundOnJoin.mp3"))
        except:
            await ctx.voice_client.disconnect()
            channel = ctx.author.voice.channel
            active_channel_id = channel.id
            print(time.strftime("%c",time.gmtime(time.time()))+" Connected to "+str(active_channel_id)) 
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe",source="soundOnJoin.mp3"))

    @bot.command()
    async def leave(ctx):
        if ctx.voice_client != None: # Условие наличие канала у контекста 
            print("Disconnected from channel")
            await ctx.voice_client.disconnect()
            vc = None
        else:
            await ctx.send("Бот не находится в канале")

    @bot.command()
    async def admilist(ctx):
        mes = "Список админов: \n"
        for elem in names:
            mes += elem+", "
        mes = mes[:len(mes)-2]
        await ctx.send(mes)

    @bot.command()
    async def give_admin(ctx,name):
        admin_name = ctx.guild.get_member(int(name[3:name.find(">")])).name
        if admin_name != "Kolbaska": 
            if admin_name not in names:
                names.append(admin_name)
                await ctx.send(admin_name+" был добавлен в список админов")
            else:
                await ctx.send(admin_name+" уже в списке админов")
            updateFile("names.txt")
        else:
            await ctx.send("Божество не нуждается в ваших подачках")

    @bot.command()
    async def remove_admin(ctx,name):
        admin_name = ctx.guild.get_member(int(name[3:name.find(">")])).name
        if admin_name != "Kolbaska":
            if admin_name in names:
                names.remove(admin_name)
                await ctx.send(admin_name+" был убран из списка админов")
            else:
                await ctx.send(admin_name+" нету в списке админов")
        else:
            await ctx.send("Как вы посмели отобрать силу у бога?")

    @bot.command()
    async def get_target(ctx, name):  
        global main_target_member
        if ctx.author.name in names: # Проверка админки
            main_target_member = ctx.guild.get_member(int(name[3:name.find(">")]))
            print(name)
            if main_target_member != None:
                print(main_target_member.id)
                await ctx.send(main_target_member.name+" закреплен")
            else:
                await ctx.send(name+" не найден")
        else:
            await ctx.send(ctx.author.name+" не является администратором")

    @bot.command()  
    async def clear_target(ctx):  
        global main_target_member
        if ctx.author.name in names: # Проверка админки
            if main_target_member != "":
                await ctx.send(main_target_member.name+" откреплен")
            else:
                await ctx.send("Никто не закреплен")
            main_target_member = ""
        else:
            await ctx.send(ctx.author.name+" не является администратором")

    @bot.command() # Отдельная команда для мута
    async def mute(ctx,id_name):
        name = ctx.guild.get_member(int(id_name[3:id_name.find(">")])).name
        if ctx.author.name in names:
            print(time.strftime("%c",time.gmtime(time.time()))+" Member name: "+str(name))
            print("Member id: "+str(ctx.guild))
            print("Server id: "+str(ctx.message.guild.id))
            member = ctx.guild.get_member_named(name)
            if not member:
                await ctx.send('Нету такого')
                return
            else:
                await member.edit(mute = True)
        else:
            ctx.send(str(ctx.author.name)+" не администратор")

    @bot.command() # Отдельная команда анмута
    async def unmute(ctx,id_name):
        name = ctx.guild.get_member(int(id_name[3:id_name.find(">")])).name
        if ctx.author.name in names:
            print(time.strftime("%c",time.gmtime(time.time()))+" Member name: "+str(name))
            print("Member id: "+str(ctx.guild))
            print("Server id: "+str(ctx.message.guild.id))
            member = ctx.guild.get_member_named(name)
            if not member:
                await ctx.send('Нету такого')
                return
            else:
                await member.edit(mute = False)
        else:
            ctx.send(str(ctx.author.name)+" не администратор")

    def updateFile(fileName): # Создание файла с именами админов
        global names
        with open(fileName,"w",encoding='utf-8') as f:
            for name in names:
                f.write(name+"\n")

    @bot.event # Ивент, проверяющий состояние микрофонов на канале
    async def on_voice_state_update(upd_target_member,last_member,new_member):
        global main_target_member,vc
        print(time.strftime("%c",time.gmtime(time.time()))+' У '+str(upd_target_member.name)+" изменился микрофон")

        # print(list)
        if main_target_member == upd_target_member and upd_target_member.voice.self_mute == False:
            print(time.strftime("%c",time.gmtime(time.time()))+" ВЫБРАННАЯ ЦЕЛЬ ВКЛЮЧИЛА МИКРОФОН")
            target_channel = new_member.channel # Выбирается обьект канала
            list = target_channel.members # Список пользователей на канале

            if main_target_member:
                list.remove(main_target_member)
                if upd_target_member.guild.get_member(bot.user.id) in list: # Проверяет наличие самого бота на канале
                    list.remove(upd_target_member.guild.get_member(bot.user.id))

            for memb in list:
                print(time.strftime("%c",time.gmtime(time.time()))+" Антимут "+str(memb.name))
                await memb.edit(mute = False)

            if upd_target_member.guild.get_member(bot.user.id) in target_channel.members:
                if vc and not vc.is_playing():
                    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe",source="soundOnMicroState.mp3"))


        elif main_target_member == upd_target_member and upd_target_member.voice.self_mute == True:
            print(time.strftime("%c",time.gmtime(time.time()))+" ВЫБРАННАЯ ЦЕЛЬ ВЫКЛЮЧИЛА МИКРОФОН")
            target_channel = new_member.channel
            list = target_channel.members

            if main_target_member:
                list.remove(main_target_member)
                if upd_target_member.guild.get_member(bot.user.id) in list:
                    list.remove(upd_target_member.guild.get_member(bot.user.id))

            for memb in list:
                print(time.strftime("%c",time.gmtime(time.time()))+" Мут "+str(memb.name))
                await memb.edit(mute = True)

            if upd_target_member.guild.get_member(bot.user.id) in target_channel.members:
                if vc and not vc.is_playing():
                    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe",source="soundOnMicroState.mp3"))

    @bot.event
    async def on_command_error(ctx, error):
        await ctx.send('В команду насрали и получилось: '+str(error))

    bot.run(TOKEN)

except Exception as e:
    input(e)
