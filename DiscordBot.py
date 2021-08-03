import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import time
import bestdllever
import os
import random
import selenium
from selenium import webdriver
from module1 import *
import pyscreenshot as ImageGrab
import pymysql
import math

try:
    kolbaskas_id = 259670108266430464
    TOKEN = os.getenv("BOT_TOKEN")
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='!',intents=intents, help_command=None)
    #r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'r'DBQ=DB.accdb;'

    #connect_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=F:\INFORMATIKA\SCIENCESHIT\Python\DiscordBot\DB.accdb;') 
    #connect_str = pymysql.connect(host="mulkovak.beget.tech",user ="mulkovak_test",passwd ="8W6o%R&B",db ="mulkovak_test")

    #OpenBD = pymysql.connect(connect_str) #Открывам базу данных через прописанные данные
    #BDCur = connect_str.cursor() #Обьявляем курсор в базе данных

    ALEX_BD_MAS = {}
    ALEX_BD_MAS['host'] = 'alexclown.beget.tech'
    ALEX_BD_MAS['database'] = 'alexclown_007'
    ALEX_BD_MAS['user'] = 'alexclown_007'
    ALEX_BD_MAS['password'] = 'R%Dy%5Ne'

    admin_names = []
    muted_names = []
    Users_stats = {}
    CLICKER_MESSAGES = []
    pointsMas = {}
    Attack_Timer_Mas = {} # {(id:time),(id:time)}
    alpNumbers = {"1️⃣":"1","0️⃣":"0","2️":"2","3️⃣":"3","4️⃣":"4","5️⃣":"5","6️⃣":"6","7️⃣":"7","8️⃣":"8","9️⃣":"9","🇦":"A","🇧":"B","🇨":"C","🇩":"D","🇪":"E","🇫":"F"}
    main_target_member = ""
    active_channel_id = ""
    main_guild = ""

    active_messages = {} # Массив с активными сообщениями USERID = [[MESID,TYPE],[MESID,TYPE]]

    host_os = str(os.getenv("BD_HOST"))
    user_os = os.getenv("BD_USER")
    pw_os = os.getenv("BD_PASSWORD")
    connect_str = pymysql.connect(host=host_os, user = user_os, passwd = pw_os, db ="sql6428571",port=3306) 
    
    def updateLocalActiveMes(): # ИСПРАВИТЬ АЛГОРИТМ СБОР АКТИВНЫХ СООБЩЕНИЙ
        global active_messages
        BDMessages = newExecute("select * from Messages")
        active_messages = []
        for message in BDMessages:
            active_messages.append([int(message[0]),int(message[1]),message[2]])
        print("Update succeceful: "+str(active_messages))

    def newExecute(command):
        global connect_str
        BDCur = connect_str.cursor() #Обьявляем курсор в базе данных

        #print(BDCur.connection)
        if BDCur.connection:
            print("Переоткрытие соединения")
            connect_str = pymysql.connect(host=host_os, user = user_os, passwd = pw_os, db ="sql6428571",port=3306)
            BDCur = connect_str.cursor() #Обьявляем курсор в базе данных
        print("Команда на выполнение:"+str(command))
            
        BDCur.execute(command)
        data = BDCur.fetchall()
        print("Вывод:"+str(data))
        
        connect_str.commit()
        #BDCur.close()
        return data

    def timelog():
        return time.ctime(time.time())

    @bot.event
    async def on_ready(): # Ивент срабатывает при запуске бота
        loadMassivesFromBD()

        print("ADMINS:"+str(admin_names))
        print("MUTED_BOYS"+str(muted_names))
        print(bot.user.name)
        print(bot.user.id)
        print(bot.guilds)
        print('------')
#
# Текст от имени бота
#
    @bot.command()
    async def sendMes(ctx,channelid,message):
        if ctx.author.id in admin_names:
            #target_server = bot.get_guild(int(serverid))
            target_channel = bot.get_channel(int(channelid))
            await target_channel.send(message)
        else:
            await ctx.send(ctx.author.name+" не является администратором")


#
# НАЙТИ ТЕКСТ С СИНОНИМАМИ
#

    @bot.command()
    async def get_sinonim(ctx,text):
        checkInPointsMas(ctx.author.id)
        browser = webdriver.Chrome()
        price = 10
        descr = "обработку текста синонимайзером"

        if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
            browser.get("https://raskruty.ru/tools/synonymizer/")
            browser.find_element_by_xpath("//*[@id='textarea_i']").send_keys(text)
            browser.find_element_by_xpath("//*[@id='run']").click()
            time.sleep(1)
            result = browser.find_element_by_xpath("//*[@id='out']").text
            await ctx.send("```"+result+"```")

            spendPoints(ctx,price)
            await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)
        else:
            await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))

# 
# ВЫВОД СПИСКА КОМАНД
#

    @bot.command()
    async def help(ctx):
        mes = ""
        if "points" in ctx.message.content or "Points" in ctx.message.content:
            with open("helpMessages/helpPoints.txt","r",encoding="utf-8") as f:
                for line in f:
                    mes += line
                await ctx.send("```"+mes+"```")
        elif "admins" in ctx.message.content or "Admins" in ctx.message.content:
            with open("helpMessages/helpAdmins.txt","r",encoding="utf-8") as f:
                for line in f:
                    mes += line
                await ctx.send("```"+mes+"```")
        elif "voice" in ctx.message.content or "Voice" in ctx.message.content:
            with open("helpMessages/helpVoice.txt","r",encoding="utf-8") as f:
                for line in f:
                    mes += line
                await ctx.send("```"+mes+"```")
        elif "textchat" in ctx.message.content or "textChat" in ctx.message.content or "Textchat" in ctx.message.content or "TextChat" in ctx.message.content :
            with open("helpMessages/helpText.txt","r",encoding="utf-8") as f:
                for line in f:
                    mes += line
                await ctx.send("```"+mes+"```")
        #elif "other" in ctx.message.content:
        #    with open("helpMessages/helpother.txt","r",encoding="utf-8") as f:
        #        for line in f:
        #            mes += line
        #        await ctx.send("```"+mes+"```")
        else:
            with open("helpMessages/helpMain.txt","r",encoding="utf-8") as f:
                for line in f:
                    mes += line
                await ctx.send("```"+mes+"```")

#
# БОЕВКА
#
    def loadStats():
        global Users_stats
        Users_stats = {}
        data = newExecute("select * from UserStats")
        for user in data:
            Users_stats[int(user[0])] = {"Damage":user[1],"Defence":user[2],"Speed":user[3]}
        print("Loaded from DB:",Users_stats)

    @bot.command()
    async def set_stat(ctx,slap,type,number): # Установка стата пользователю
        global Users_stats
        if ctx.author.id in admin_names:
            target = ctx.guild.get_member(int(slap[3:slap.find(">")]))
            checkInPointsMas(target.id)
            Users_stats[target.id][str(type.title())] = int(number)
            newExecute("update UserStats set User"+str(type.title())+"="+number+" where UserID='"+str(target.id)+"';")
            print("stats mas updated:",Users_stats)
        else:
            await ctx.send(ctx.author.name+" не является администратором")

    @bot.command()
    async def check_stat(ctx,slap): # Функция показывает статы юзера
        global Users_stats
        target = ctx.guild.get_member(int(slap[3:slap.find(">")]))
        checkInPointsMas(target.id)
        await ctx.send("```"+str(target.name)+" - Поинты: "+str(pointsMas[target.id])+"\n\nАтака: "+str(Users_stats[target.id]["Damage"])+"\nЗащита: "+str(Users_stats[target.id]["Defence"])+"\nСкорость: "+str(Users_stats[target.id]["Speed"])+"```")

    @bot.command()
    async def attack(ctx,name):
        global Attack_Timer_Mas,Users_stats
        try:
            target = ctx.guild.get_member(int(name[3:name.find(">")]))
            id = target.id

            #loadStats()

            target_stats = Users_stats[id]
            my_stats = Users_stats[ctx.author.id] # Берем из локального массива статы цели и автора

            print("taken stats from "+str(target.name)+" "+str(ctx.author.name)+": "+str(target_stats)+" "+str(my_stats))

            maxstolen = int(int(pointsMas[id]) / target_stats["Defence"])
            if maxstolen < 0:
                maxstolen = 0

            stolen_points = random.randint(0,maxstolen) 
            dice = random.randint(0,100)
            chance_to_win = math.ceil(50 * my_stats['Damage'] / target_stats['Defence']) # Шанс победы

            if chance_to_win > 100:
                chance_to_win = 100
            elif chance_to_win < 0:
                chance_to_win = 0

            CD = 600 - my_stats['Speed'] # CoolDown
            price = 100
            descr = "нападение"
            StartTime = int(time.time())

            attacker_stat = "```"+str(ctx.author.name)+" - Поинты: "+str(pointsMas[ctx.author.id])+"\n\nАтака: "+str(my_stats["Damage"])+"\nЗащита: "+str(my_stats["Defence"])+"\nСкорость: "+str(my_stats["Speed"])+"```"
            defender_stat = "```"+str(target.name)+" - Поинты: "+str(pointsMas[target.id])+"\n\nАтака: "+str(target_stats["Damage"])+"\nЗащита: "+str(target_stats["Defence"])+"\nСкорость: "+str(target_stats["Speed"])+"```"

            if ctx.author.id not in Attack_Timer_Mas:
                Attack_Timer_Mas[ctx.author.id] = 0

            if StartTime >= Attack_Timer_Mas[ctx.author.id] + CD: # Две проверки на наличие поинтов и пройденного КД
                if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price: 
                    first_stat = await ctx.send(attacker_stat)
                    main_mes = await ctx.send("```"+str(ctx.author.name)+" нападает на "+str(target.name)+"```")
                    second_stat = await ctx.send(defender_stat)
                    await ctx.send("```ШАНС НА ПОБЕДУ: <<<"+str(chance_to_win)+"%>>> ( 50(БАЗА) * "+str(my_stats["Damage"])+"(УРОН НАПАДАЮЩЕГО) / "+str(target_stats["Defence"])+"(БРОНЯ ЗАЩИЩАЮЩЕГОСЯ) )\nЛУЧШЕЕ НАПАДЕНИЕ ДАСТ <<<"+str(maxstolen)+">>> ПОИНТОВ ( "+str(pointsMas[id])+"(ПОИНТЫ ЗАЩИЩАЮЩЕГОСЯ) / "+str(target_stats["Defence"])+"(БРОНЯ ЗАЩИЩАЮЩЕГОСЯ) )```")

                    for sec in range(1,4):
                        await main_mes.edit(content = "```"+str(ctx.author.name)+" нападает на "+str(target.name)+" и"+"."*sec+"```")
                        time.sleep(1)

                    if dice <= chance_to_win:
                        if pointsMas[id] >= stolen_points: # Если у цели поинтов больше рола то...
                            pointsMas[ctx.author.id] += stolen_points
                            pointsMas[id] -= stolen_points

                            await main_mes.edit(content = "```"+str(ctx.author.name)+" нападает на "+str(target.name)+" и <<<Невежественно отбирает "+str(stolen_points)+" поинтов у "+str(target.name)+">>> ```")
                            await first_stat.edit(content=attacker_stat)
                            await second_stat.edit(content=defender_stat)
                            #await ctx.send(ctx.author.name+" напал на "+ctx.guild.get_member(id).name+" и украл "+str(stolen_points)+" поинтов")
                        else:
                            stolen_points = pointsMas[id]
                            pointsMas[ctx.author.id] += stolen_points
                            pointsMas[id] -= stolen_points

                            await main_mes.edit(content = "```"+str(ctx.author.name)+" нападает на "+str(target.name)+" и <<<Вырывает ссаные "+str(stolen_points)+" поинтов из кармана "+str(target.name)+">>> ```")
                            await first_stat.edit(content=attacker_stat)
                            await second_stat.edit(content=defender_stat)
                            #await ctx.send(ctx.author.name+" напал на "+ctx.guild.get_member(id).name+" и украл "+str(stolen_points)+" поинтов")
                    else:
                        await main_mes.edit(content = "```"+str(ctx.author.name)+" нападает на "+str(target.name)+" и <<<Огребает по полной не получая ничего>>> ```")
                        #await ctx.send(ctx.author.name+" напал на "+ctx.guild.get_member(id).name+" и не смог украсть поинты")
                    Attack_Timer_Mas[ctx.author.id] = StartTime
                    print(Attack_Timer_Mas)
                    spendPoints(ctx,price)
                    #updateTablePoints()
                    checkInPointsMas(ctx.author.id)
                    newExecute("Update Users set Points="+str(pointsMas[ctx.author.id])+",AttackTimer="+str(Attack_Timer_Mas[ctx.author.id])+" where id='"+str(ctx.author.id)+"';") # Обновляем поинты и таймер в БД
                    newExecute("Update Users set Points="+str(pointsMas[id])+",AttackTimer="+str(Attack_Timer_Mas[id])+" where id='"+str(id)+"';") # Обновляем поинты и таймер в БД

                    #connect_str.commit()

                    await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)
                else:
                    await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))
            else:
                await ctx.send("У "+str(ctx.author.name)+" еще перезарядка атаки "+str(time.strftime("%H-%M-%S",time.gmtime((StartTime-Attack_Timer_Mas[ctx.author.id]-CD)*-1))))
                print(Attack_Timer_Mas)
        except Exception as e:
            await ctx.send(e)

    @bot.command()
    async def removeTimer(ctx,name):
        try:
            if ctx.author.id in admin_names:
                target_id = int(name[3:name.find(">")])

                if target_id in Attack_Timer_Mas:
                    del Attack_Timer_Mas[target_id]
                    await ctx.send("У "+str(ctx.guild.get_member(target_id).name)+" был сброшен таймер")
                else:
                    await ctx.send("У "+str(ctx.guild.get_member(target_id).name)+" нету таймера")
            else:
                await ctx.send(ctx.author.name+" не является администратором")
        except Exception as e:
            await ctx.send(e)

#
# СИСТЕМА ПОИНТОВ
#
    def loadMassivesFromBD(): # Функция проверяет первый элемент в таблице, если есть то собирает строки пока не наткнется на пустую
        tempMas = newExecute("select id,points,AttackTimer,Admin,Chat_muted from Users")
        for user in tempMas:
            pointsMas[int(user[0])] = user[1]
            Attack_Timer_Mas[int(user[0])] = user[2]
            if user[3] == True:
                admin_names.append(int(user[0]))
            if user[4] == True:
                muted_names.append(int(user[0]))

        tempMas = newExecute("select UserID,UserDamage,UserDefence,UserSpeed from UserStats")
        for user in tempMas:
            Users_stats[int(user[0])] = {'Damage':int(user[1]),'Defence':int(user[2]),'Speed':int(user[3])}
        print("Masives update:")
        print(pointsMas)
        print(Attack_Timer_Mas)
        print(Users_stats)
        print("------------")

    #def updateTablePoints(): # Функция обновляет ТАБЛИЦУ по СЛОВАРЮ.

    def checkInPointsMas(id): 
        if id not in pointsMas:
            pointsMas[id] = 0
            Users_stats[id] = {"Damage":0,"Defence":0,"Speed":0}
            newExecute("Insert into Users(ID,Name,AttackTimer,Points,Admin,Chat_muted) values ('"+str(id)+"','"+str(bot.get_user(id).name)+"',0,0,0,0);")
            newExecute("Insert into UserStats(UserID,UserDamage,UserDefence,UserSpeed) values ('"+str(id)+"',1,1,1);")
            #connect_str.commit()

    @bot.command()
    async def send_points(ctx,name,amount):
        amount = int(amount)
        try:
            tar_id = ctx.guild.get_member(int(name[3:name.find(">")])).id
            checkInPointsMas(ctx.author.id)
            checkInPointsMas(tar_id)
        except Exception as e:
            await ctx.send(e)

        if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= amount:
            pointsMas[ctx.author.id] -= amount
            pointsMas[tar_id] += amount
            #updateTablePoints()
            newExecute("Update Users set Points="+str(pointsMas[ctx.author.id])+" where id='"+str(ctx.author.id)+"';") # Обновляем поинты в БД
            newExecute("Update Users set Points="+str(pointsMas[tar_id])+" where id='"+str(tar_id)+"';")
            #connect_str.commit()

            print(str(ctx.author.name)+" передал "+str(ctx.guild.get_member(tar_id).name)+" "+str(amount)+" поинтов")
            await ctx.send(str(ctx.author.name)+" передал "+str(ctx.guild.get_member(tar_id).name)+" "+str(amount)+" поинтов")
        else:
            await ctx.send("Недостаточно поинтов")

    @bot.command()
    async def dai_point(ctx):
        if ctx.author.id not in pointsMas:
            checkInPointsMas(ctx.author.id)
            pointsMas[ctx.author.id] = 500
            newExecute("Update Users set Points="+str(pointsMas[ctx.author.id])+" where id='"+str(ctx.author.id)+"';") # Обновляем поинты в БД
            #connect_str.commit()
            await ctx.send("Получите распишитесь")
        else:
            await ctx.send("Поинты уже получены")

    @bot.command()
    async def points_leaders(ctx):
        mainmes = "```"
        mainmes += "Список лидеров:\n"
        row = 1
        fakemas = dict(sorted(pointsMas.items(), key=lambda x: x[1], reverse =True)) # Сортировка основного масива и перекладывание результата в новый
        for id in fakemas:
            mainmes += str(row)+") "+ctx.guild.get_member(id).name+" "+str(round(fakemas[id],2))+"\n"
            row += 1
        mainmes += "```"
        await ctx.send(mainmes)

    @bot.command()
    async def give_points(ctx,name,point):
        try:
            if ctx.author.id in admin_names:
                target_member = ctx.guild.get_member(int(name[3:name.find(">")]))
                checkInPointsMas(target_member.id)
                points = int(point)

                pointsMas[target_member.id] = pointsMas[target_member.id] + points
                newExecute("Update Users set Points="+str(pointsMas[target_member.id])+" where id='"+str(target_member.id)+"';") # Обновляем поинты в БД
                #connect_str.commit()

                print(timelog()+" Выдача "+target_member.name+" "+str(points)+" очков")
                print(pointsMas)
                await ctx.send("Выдача "+target_member.name+" "+str(points)+" очков")
            else:
                await ctx.send(ctx.author.name+" не является администратором")
        except Exception as e:
            await ctx.send(e)

    @bot.command()
    async def remove_points(ctx,name,point):
        try:
            if ctx.author.id in admin_names:
                target_member = ctx.guild.get_member(int(name[3:name.find(">")]))
                checkInPointsMas(target_member.id)
                points = int(point)

                pointsMas[target_member.id] = pointsMas[target_member.id] - points
                newExecute("Update Users set Points="+str(pointsMas[target_member.id])+" where id='"+str(target_member.id)+"';") # Обновляем поинты в БД
                #connect_str.commit()

                print(timelog()+" Снятие у "+target_member.name+" "+str(points)+" очков")
                print(pointsMas)
                await ctx.send("Снятие у "+target_member.name+" "+str(points)+" очков")
            else:
                await ctx.send(ctx.author.name+" не является администратором")
        except Exception as e:
            await ctx.send(e)

    @bot.command()
    async def set_points(ctx,name,point):
        try:
            if ctx.author.id in admin_names:
                target_member = ctx.guild.get_member(int(name[3:name.find(">")]))
                checkInPointsMas(target_member.id)
                points = int(point)

                pointsMas[target_member.id] = points
                newExecute("Update Users set Points="+str(pointsMas[target_member.id])+" where id='"+str(target_member.id)+"';") # Обновляем поинты в БД
                #connect_str.commit()

                print(timelog()+" Теперь у "+target_member.name+" "+str(points)+" очков")
                print(pointsMas)
                await ctx.send("Теперь у "+target_member.name+" "+str(points)+" очков")
            else:
                await ctx.send(ctx.author.name+" не является администратором")
        except Exception as e:
            await ctx.send(e)

    @bot.command()
    async def check_points(ctx,name):
        try:
            target_member = ctx.guild.get_member(int(name[3:name.find(">")]))
            if target_member.id in pointsMas:
                await ctx.send("У "+str(target_member.name)+" "+str(round(pointsMas[target_member.id],2))+" очков")
            else:
                await ctx.send("У "+str(target_member.name)+" нету очков")
        except Exception as e:
            await ctx.send(e)


    def spendPoints(ctx,amount):
        try:
            if ctx.author.id in pointsMas:
                if pointsMas[ctx.author.id] >= amount:
                    pointsMas[ctx.author.id] -= amount
                    checkInPointsMas(ctx.author.id)
                    newExecute("Update Users set Points="+str(pointsMas[ctx.author.id])+" where id='"+str(ctx.author.id)+"';") # Обновляем поинты в БД
                    #connect_str.commit()

                    print(ctx.author.name+" потратил "+str(amount)+" поинтов")
                    return True
                else:
                    print(ctx.author.name+" НЕ потратил "+str(amount)+" поинтов")
                    return False
            else:
                print(ctx.author.name+" НЕ потратил "+str(amount)+" поинтов")
                return False
        except Exception as e:
            print(e)


#
# ВЗАИМОДЕЙСТВИЕ БОТА С ВОЙСОМ
#

    @bot.command()
    async def join(ctx): # Функция по входу на канал
        try:
            global vc
            try: # Если не получается просто присоединиться бот пытается выйти и зайти 
                channel = ctx.author.voice.channel # Выбирается обьект канала, на котором в данный момент находится запросивший
                active_channel_id = channel.id
                print("Connected to "+str(active_channel_id)) 
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(source="soundOnJoin.mp3"))
            except Exception as e:
                print(e)
                await ctx.voice_client.disconnect()
                channel = ctx.author.voice.channel
                active_channel_id = channel.id
                print("Connected to "+str(active_channel_id)) 
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(source="soundOnJoin.mp3"))
        except Exception as e:
            await ctx.send(e)

    @bot.command()
    async def leave(ctx):
        try:
            if ctx.voice_client != None: # Условие наличие канала у контекста 
                print("Disconnected from channel")
                await ctx.voice_client.disconnect()
                vc = None
            else:
                await ctx.send("Бот не находится в канале")
        except Exception as e:
            await ctx.send(e)

#
# АДМИНКА
#

    @bot.command()
    async def admilist(ctx):
        mes = "Список админов: \n"
        for elem in admin_names:
            mes += ctx.guild.get_member(elem).name+", "
        mes = mes[:len(mes)-2]
        await ctx.send("```"+mes+"```")

    @bot.command()
    async def give_admin(ctx,name):
        try:
            if ctx.author.id in admin_names:
                admin_member = ctx.guild.get_member(int(name[3:name.find(">")]))
                if admin_member.id != kolbaskas_id: 
                    if admin_member.id not in admin_names:
                        checkInPointsMas(admin_member.id)
                        admin_names.append(admin_member.id)
                        newExecute("Update Users set Admin=True where id='"+str(admin_member.id)+"';")
                        #connect_str.commit()
                        await ctx.send(admin_member.name+" был добавлен в список админов")
                    else:
                        await ctx.send(admin_member.name+" уже в списке админов")
                else:
                    await ctx.send("Божество не нуждается в ваших подачках")
            else:
                await ctx.send(ctx.author.name+" не является администратором")
        except Exception as e:
            await ctx.send(e)

    @bot.command()
    async def remove_admin(ctx,name):
        try:
            if ctx.author.id in admin_names:
                admin_member = ctx.guild.get_member(int(name[3:name.find(">")]))
                if admin_member.id != kolbaskas_id:
                    if admin_member.id in admin_names:
                        checkInPointsMas(admin_member.id)
                        admin_names.remove(admin_member.id)
                        newExecute("Update Users set Admin=False where id='"+str(admin_member.id)+"';")
                        #connect_str.commit()
                        await ctx.send(admin_member.name+" был убран из списка админов")
                    else:
                        await ctx.send(admin_member.name+" нету в списке админов")
                else:
                    await ctx.send("Как вы посмели отобрать силу у бога?")
            else:
                await ctx.send(ctx.author.name+" не является администратором")
        except Exception as e:
            await ctx.send(e)

#
# BOTSUS
#

    @bot.command()
    async def get_target(ctx, name):  
        global main_target_member
        try:
            price = 100
            descr = "определение цели общего мута"

            if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
                main_target_member = ctx.guild.get_member(int(name[3:name.find(">")]))
                print(name)

                if main_target_member != None:
                    print(main_target_member.id)
                    await ctx.send(main_target_member.name+" закреплен")
                else:
                    await ctx.send(name+" не найден")

                spendPoints(ctx,price)
                await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)
            else:
                await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))
        except Exception as e:
            await ctx.send(e)

    @bot.command()  
    async def clear_target(ctx):  
        global main_target_member
        try:
            price = 10
            descr = "снятие цели общего мута"

            if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
                if main_target_member != "":
                    await ctx.send(main_target_member.name+" откреплен")
                else:
                    await ctx.send("Никто не закреплен")
                main_target_member = ""

                spendPoints(ctx,price)
                await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)
            else:
                await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))
        except Exception as e:
            await ctx.send(e)

#
# МЕЛКИЕ ФИЧИ
#

    def is_me(m):
        try:
            return m.author == bot.user or m.content[0] == "!"
        except:
            return False

    @bot.command()
    async def clear_shit(ctx): # Очищение сообщений бота или команд
        price = 1
        descr = "очистку чата"
        limits = 100

        if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
            BD_Mes = newExecute("select MesID from Messages")

            ALLMessages = await ctx.channel.history(limit=limits).flatten() # Собираются два массива, из бд и из сообщений на удаление.
            for mes in ALLMessages:
                for BD_message in BD_Mes:
                    #print(BD_message[0],mes.id)
                    if int(mes.id) == int(BD_message[0]): # Находятся сообщения, имеющиеся в БД и удаляются
                        #print("----------")
                        #print("-TARGETED-")
                        #print("----------")
                        newExecute("delete from Messages where MesID='"+str(mes.id)+"';") 

            #print(BD_Mes,ALLMessages)
            await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)
            await ctx.channel.purge(check=is_me,limit=limits) # После удаляются все сообщения
            spendPoints(ctx,price)
        else:
            await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))

    @bot.command()
    async def stealth_mute(ctx,id): # Функция тихого мута пользователя в чате\
        try:
            price = 500
            descr = "мут человека в чате"
            checkInPointsMas(int(id[3:id.find(">")]))

            if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
                target_member = ctx.guild.get_member(int(id[3:id.find(">")])) # Пользователь определеяется по слапу в дискорде
                if target_member.id != kolbaskas_id:

                    if target_member.name not in muted_names:
                        muted_names.append(target_member.id)
                        newExecute("update Users set Chat_muted=True where id='"+str(target_member.id)+"';")
                        #connect_str.commit()
                        await ctx.send("Кто этот ваш "+str(target_member.name))
                        print("muted_names updated: "+str(muted_names))
                    else:
                        await ctx.send(target_member.name+" уже помалкивает сидит")
                else:
                    await ctx.send("Что? Не расслышал")

                spendPoints(ctx,price)
                await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)
            else:
                await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))
        except Exception as e:
            await ctx.send(e)

    @bot.command()
    async def stealth_unmute(ctx,id): # Функция тихого анмута пользователя в чате
        try:
            price = 50
            descr = "снятие мута чата"

            if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
                target_member = ctx.guild.get_member(int(id[3:id.find(">")])) # Пользователь определеяется по слапу в дискорде
                if target_member.id != kolbaskas_id:
                    if target_member.id in muted_names:
                        del muted_names[muted_names.index(target_member.id)]
                        newExecute("update Users set Chat_muted=False where id='"+str(target_member.id)+"';")
                        #connect_str.commit()
                        print("muted_names updated: "+str(muted_names))
                        await ctx.send(target_member.name+" вернулся в село натуралов")
                    else:
                        await ctx.send(target_member.name+" нету в списке клоунов")
                else:
                    await ctx.send("Что? Не расслышал")

                spendPoints(ctx,price)
                await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)
            else:
                await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))
        except Exception as e:
            await ctx.send(e)

    @bot.command()
    async def smile_frase(ctx,font_smile,text_smile,frase): # Фукнция по сообщению смайликами
        try:
            price = 50
            descr = "создание фразы из смайликов"

            if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
                mas_lines = []
                mas_lines.append(font_smile+font_smile+font_smile+font_smile+font_smile+font_smile)
                print("Выбрана фраза: "+str(frase))
            
                for elem in frase: # По каждой букве в фразе отрисовывается массив 
                    mas = printLetter(font_smile,text_smile,elem) # Функция отрисовывает и возвращает массив элементов относительно буквы
                    for line in mas:
                        mas_lines.append(line)
                    mas_lines.append(font_smile+font_smile+font_smile+font_smile+font_smile+font_smile) # Добовление пробела между буквами для видимости
                mes = ""

                for line in mas_lines: # По каждой линии в масиве линий создается сообщение
                    mes += line + "\n"
                    print(len(mes))
                    if len(mes) >= 200: # Если длина сообщения становится 200 символов, то сообщение отправляется чтобы пройти ограничение
                        print("Ограничение в 200 символов пройдено")
                        await ctx.send(mes)
                        mes = ""
                await ctx.send(mes) # После создания сообщения оно отправляется от лица бота в канал контекста

                spendPoints(ctx,price)
                await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)
            else:
                await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))
        except Exception as e:
            await ctx.send(e)

    @bot.command()
    async def flip_channels(ctx,number_tryes): # Функция по перебрасыванию людей в канале
        try:
            price = 300
            descr = "рандомный переброс людей в канале"

            if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
                try:
                    channel = ctx.author.voice.channel
                    list_boys = channel.members
                    list_channels = ctx.author.guild.voice_channels
                    print("На серваке начат кринж с популяцией из "+str(len(list_boys))+" человек на канале")
                    await ctx.send("Начинаю кринж")
                    for tr in range(0,int(number_tryes)): # Цикл перебросов повторяется поставленое кол-во раз
                        for boy in list_boys:
                            max = len(list_channels)-1
                            target_channel = list_channels[random.randint(0,max)]
                            print("Мистер "+str(boy.name)+" летит в "+str(target_channel.name))
                            await boy.move_to(target_channel,reason="Устроен кринж") # Берется рандомное число от 0 до максимума массива списка каналов и по этому индексу отправляется пользователь по списку
                    await ctx.send("Кринж закончен")

                    spendPoints(ctx,price)
                    await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)
                except Exception as e:
                    print(e)
                    await ctx.send("Автор, на канал зайди")
            else:
                await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))
        except Exception as e:
            await ctx.send(e)

    @bot.command() # Отдельная команда для мута
    async def mute(ctx,id_name):
        try:
            name = ctx.guild.get_member(int(id_name[3:id_name.find(">")])).name
            price = 100
            descr = "мут человека на сервере"

            if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
                print("Member name: "+str(name))
                print("Member id: "+str(ctx.guild))
                print("Server id: "+str(ctx.message.guild.id))
                member = ctx.guild.get_member_named(name)
                if not member:
                    await ctx.send('Нету такого')
                    return
                else:
                    await member.edit(mute = True)

                spendPoints(ctx,price)
                await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)
            else:
                await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))
        except Exception as e:
            await ctx.send(e)

    @bot.command() # Отдельная команда анмута
    async def unmute(ctx,id_name):
        try:
            name = ctx.guild.get_member(int(id_name[3:id_name.find(">")])).name
            price = 10
            descr = "снятие мута человека на сервере"
            checkInPointsMas(ctx.author.id)

            if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
                print("Member name: "+str(name))
                print("Member id: "+str(ctx.guild))
                print("Server id: "+str(ctx.message.guild.id))
                member = ctx.guild.get_member_named(name)
                if not member:
                    await ctx.send('Нету такого')
                    return
                else:
                    await member.edit(mute = False)

                spendPoints(ctx,price)
                await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)
            else:
                await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))
        except Exception as e:
            await ctx.send(e)
                
    def createColorPic(HEXColor):
        wn = turtle.Screen()

        rootwindow = wn.getcanvas().winfo_toplevel()
        rootwindow.call('wm', 'attributes', '.', '-topmost', '1')

        turtle.setup(width=200,height=200,startx=0,starty=0)
        turtle.bgcolor(HEXColor)
        turtle.title("TURTLE")

        time.sleep(1)
        ImageGrab.grab(bbox=(20,50,180,190)).save('color.png', 'PNG')

    @bot.command()
    async def createColor(ctx):
        global colorName,mainmes,alpNumbers
        colorName = "#000000"

        createColorPic(colorName)
        
        mainmes = await ctx.send(file=discord.File(r"color.png"))

    #@bot.command()
    #async def addMe(ctx):
    #    try:
    #        exCom = "INSERT into Users (ID,NAME,AttackTimer,Points) values ('"+str(ctx.author.id)+"','"+str(ctx.author.name)+"',"+str(Attack_Timer_Mas[ctx.author.id] if ctx.author.id in Attack_Timer_Mas else 0)+","+str(pointsMas[ctx.author.id] if ctx.author.id in pointsMas else 0)+");"
    #        print(exCom)
    #        newExecute(exCom)
    #        #connect_str.commit()
    #        print("Добавлен в базу данных")
    #    except Exception as e:
    #        print(e)

    def updateKey(oldkey,map):
        newKey = ""
        if len(map) < len(oldkey):
            for elem in map:
                newKey += oldkey[elem]
            newKey += oldkey[len(map):]
        elif len(map) > len(oldkey):
            print("Карта больше ключа. Ключ не меняется")
            newKey = oldkey
        else:
            for elem in map:
                newKey += oldkey[elem]

        return newKey

    @bot.command()
    async def steal_admin(ctx):
        global pasmes,result,green_pos,Main_user_SA,close_em,changed_map,key

        price = 1000
        descr = "игру для админки"
        checkInPointsMas(ctx.author.id)

        if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
            Main_user_SA = ctx.author
            changed_map = [4,1,5,2,0,3]
            result = "-----"
            key = "ЗЕЛЕНЫЕ"
            key = updateKey(key,changed_map)
            close_em = "❌"
            reactionsList = ["🟥","🟧","🟨","🟦","🟪","🟫"]

            spendPoints(ctx,price)
            await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)

            pasmes = await ctx.send("НАЖМИТЕ НА "+str(key)+" ["+result+"]")
            green_pos = random.randint(0,5)
            reactionsList[green_pos] = "🟩"
            if newExecute("select * from Messages where type='Steal_Admin_Message' and UserID='"+str(ctx.author.id)+"'") == ():
                newExecute("insert into Messages values ('"+str(ctx.author.id)+"','"+str(pasmes.id)+"','Steal_Admin_Message',Null)")
            else:
                newExecute("update Messages set MesID='"+str(pasmes.id)+"' where type='Steal_Admin_Message' and UserID='"+str(ctx.author.id)+"'")
            for reaction in reactionsList:
                await pasmes.add_reaction(reaction) # КР, ЗЕЛ
            await pasmes.add_reaction(close_em) # КР, ЗЕЛ
        else:
            await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))

    @bot.command()
    async def executeSQL(ctx,com):
        try:
            if ctx.author.id in admin_names:
                ret = newExecute(com)
                if ret != [] and ret != ():
                    await ctx.send(ret)
                else:
                    await ctx.send("Команда выполнена")
            else:
                await ctx.send(ctx.author.name+" не является администратором")
        except Exception as e:
            await ctx.send("SQL команда не прошла: "+str(e))

    @bot.command()
    async def test(ctx):
        print(ctx.message.id)

#
# ПЕРЕДАЕМ ПРИВЕТ ЛЕШЕ
#!ALEX_HALO "insert into site 'ЕБАЛ МАТЬ','ЕБАЛ МАТЬ','ЕБАЛ МАТЬ'"

#    @bot.command()
#    async def ALEX_HALO(ctx,command,count):
#        try:
#            for num in range(0,int(count)):
#                alex_connect_str = pymysql.connect(host=ALEX_BD_MAS['host'], user = ALEX_BD_MAS['user'], passwd = ALEX_BD_MAS['password'], db =ALEX_BD_MAS['database'],port=3306)
#                ALEX_BDCur = alex_connect_str.cursor() #Обьявляем курсор в базе данных
#                print("К леше команда на выполнение:"+str(command))
#                ALEX_BDCur.execute(command)
#                data = ALEX_BDCur.fetchall()
#                print("От БД леши вывод:"+str(data))
#                alex_connect_str.commit()
#                ALEX_BDCur.close()
#                if data != ():
#                    await ctx.send("ПРИВЕТ ЛЕША КАК ДЕЛА КАК МАМА???:"+str(data))
#            ctx.send("Запрос выполнен")
#        except Exception as e:
#            await ctx.send(str(e))

#    @bot.command()
#    async def ALEX_CHECKBD_LOL(ctx,number_trys):
#        #number_lines = int(number_lines)
#        alex_connect_str = pymysql.connect(host=ALEX_BD_MAS['host'], user = ALEX_BD_MAS['user'], passwd = ALEX_BD_MAS['password'], db =ALEX_BD_MAS['database'],port=3306)
#        ALEX_BDCur = alex_connect_str.cursor() #Обьявляем курсор в базе данных

#        #print("К леше команда на выполнение:"+str(command))
#        number_lines = 100
#        ids_penis = ["   .","  . "," (T)"," !!"," !!"," !!","()-()"]
#        ids_com = ["Займись дипломом","Зато погулял","Сейчас бы в ксочку","Сейчас бы в дотку","До сдачи осталось три дня"]
#        index = 0
        
#        for num in range(0,number_lines):
#            coin = random.randint(0,1)
#            if coin:
#                number_lines += 2
#            else:
#                number_lines -= 1
#            com = "insert into site values ('"+str("|"*number_lines)+"','"+str(ids_penis[index])+"','"+str(ids_com[0])+"');"
#            print(com)
#            ALEX_BDCur.execute(com)
#            index += 1
#            if index > 6:
#                index = 0

#        alex_connect_str.commit()
#        ALEX_BDCur.close()

#
# КЛИКЕР ЗАРАБОТОК МОНЕТ
#

    def getInform(id):
        informMas = newExecute("select * from Users where ID='"+str(id)+"'")
        print(informMas)
        return informMas

    @bot.command()
    async def farm_game(ctx): # Старт игры
        User_info = newExecute("select * from Users where ID='"+str(ctx.author.id)+"'")

        a = discord.Embed(title='Кликер - заработай себе на мthr',description="Мистер "+str(ctx.author.name)+" \n У вас "+str(pointsMas[ctx.author.id])+" поинтов")
        localmainmes = await ctx.send(embed=a)
        Mes_info = newExecute("select * from Messages where UserID='"+str(ctx.author.id)+"' and Type='CLICKER_MESSAGE'")
        channels = []
        emojis = ["💥","❌"]

        for guild in bot.guilds:
            for channel in guild.text_channels:
                channels.append(channel)

        print("--------")
        print(User_info)
        print(Mes_info)
        print(localmainmes)

        temp = []
        for channel in channels:
            temp.append(channel.name)
        print(temp)
        print("--------")

        for emoji in emojis:
            await localmainmes.add_reaction(emoji)

        if Mes_info == (): # Условие если в БД нету поставившего реакцию пользователя
            CLICKER_MESSAGES.append([localmainmes.id,ctx.author.id])
            newExecute("insert into Messages values ('"+str(ctx.author.id)+"','"+str(localmainmes.id)+"','CLICKER_MESSAGE','-')")
            print("Создание сообщения в БД")
            updateLocalActiveMes()
            Mes_info = newExecute("select * from Messages where UserID='"+str(id)+"'")
        else:
            for message in CLICKER_MESSAGES:
                if message[1] == ctx.author.id:
                    message[0] = localmainmes.id
                    break
            newExecute("update Messages set MesID='"+str(localmainmes.id)+"' where UserID='"+str(ctx.author.id)+"' and Type='CLICKER_MESSAGE'")
            Mes_info = newExecute("select * from Messages where UserID='"+str(id)+"'")

#
# ИВЕНТЫ
#

    def choiceHEXLet(mas):
        mes = ""
        for elem in range(0,6):
            try:
                mes += alpNumbers[mas[elem].emoji]
            except IndexError:
                mes += "0"
        return mes

    @bot.event
    async def on_reaction_add(reaction,user): # РЕАКЦИИ НЕ РАБОТАЮТ, ОТКРЫТЬ СТРОКУ 47
        global pasmes,result,green_pos,Main_user_SA,close_em,changed_map,key
        BDMessages = {}
        for user_local in active_messages:
            if user_local[0] == user.id:
                BDMessages[user_local[1]] = user_local[2] # Получение активных сообщений пользователя
                
        print("RES ON REACTION: "+str(BDMessages))
        try:
            if BDMessages != {}: # Если найдено хотябы одно активное сообщение 
                if BDMessages[reaction.message.id] == "CLICKER_MESSAGE" and reaction.emoji == "❌":
                    newExecute("delete from Messages Where MesID='"+str(reaction.message.id)+"'") 
                    await reaction.message.delete()

                if BDMessages[reaction.message.id] == "CLICKER_MESSAGE" and reaction.emoji == "💥":
                        pointsMas[user.id] += 10
                        newExecute("update Users set points="+str(pointsMas[user.id])+" where ID='"+str(user.id)+"'")
                        a = discord.Embed(title='Кликер - заработай себе на мthr',description="Мистер "+str(user.name)+" \n У вас "+str(pointsMas[user.id])+" поинтов")
                        await reaction.message.edit(embed=a)
                        await reaction.remove(user)

                if BDMessages[reaction.message.id] == "Steal_Admin_Message" and user == Main_user_SA:
                    if reaction.message == pasmes and user != bot.user:
                        if reaction.emoji == close_em: # Проверка если нажат крест
                            zal = await reaction.message.channel.send("Вырубаю залупу")
                            newExecute("delete from Messages where MesID='"+str(pasmes.id)+"'")
                            await pasmes.delete()
                            time.sleep(0.5)
                            await zal.delete()
                        else: 
                            print(reaction)

                            choisen_pos = reaction.message.reactions.index(reaction)
                            reactionsList = ["🟥","🟧","🟨","🟦","🟪","🟫"]

                            print(choisen_pos)
                            print(green_pos)

                            if green_pos == 0 and choisen_pos == changed_map[0]:
                                win = True
                            elif green_pos == 1 and choisen_pos == changed_map[1]:
                                win = True
                            elif green_pos == 2 and choisen_pos == changed_map[2]:
                                win = True
                            elif green_pos == 3 and choisen_pos == changed_map[3]:
                                win = True
                            elif green_pos == 4 and choisen_pos == changed_map[4]:
                                win = True
                            elif green_pos == 5 and choisen_pos == changed_map[5]:
                                win = True
                            else:
                                win = False

                            print(win)
                            if win: # Правильное нажатие
                                if len(reaction.message.reactions) >= 6: # Ожидание наличие как минимум 6 реакций 
                                    result = "X"+result[:4]
                                    await pasmes.edit(content="НАЖМИТЕ НА "+str(key)+" ["+result+"]")
                                    newExecute("update Messages set OtherInf='"+str(result)+"' where MesID='"+str(reaction.message.id)+"'")
                                    await pasmes.clear_reactions()
                                    green_pos = random.randint(0,5)
                                    reactionsList[green_pos] = "🟩"

                                    if result[4] == "X": # Проверка на победу
                                        await pasmes.delete()
                                        admin_names.append(user.id)
                                        checkInPointsMas(user.id)

                                        newExecute("update Users set admin=True where id='"+str(user.id)+"';")
                                        newExecute("delete from Messages where MesID='"+str(pasmes.id)+"';")
                                        await reaction.message.channel.send(user.name+" становится админом")

                                    else: # Если победы нет, то
                                        for react in reactionsList:
                                            await pasmes.add_reaction(react) # КР, ЗЕЛ
                                        await pasmes.add_reaction(close_em) # КР, ЗЕЛ
                                else: # Если 6 реакций нету, то
                                    print("Терпение")
                                    await reaction.message.edit(content="НАЖМИТЕ НА "+str(key)+" ["+result+"]\nТОРОПИТЬСЯ НЕКУДА")
                                    await reaction.remove(user)
                                    await reaction.message.edit(content="НАЖМИТЕ НА "+str(key)+" ["+result+"]")
                            else: # Неправильное нажатие
                                if len(reaction.message.reactions) >= 6: # Ожидание наличие как минимум 6 реакций 
                                    print("Reset Game")
                                    result = "-----"
                                    await pasmes.edit(content="НАЖМИТЕ НА "+str(key)+" ["+result+"]")
                                    newExecute("update Messages set OtherInf='"+str(result)+"' where MesID='"+str(reaction.message.id)+"'")
                                    await pasmes.clear_reactions()
                                    green_pos = random.randint(0,5)
                                    reactionsList[green_pos] = "🟩"

                                    for react in reactionsList:
                                        await pasmes.add_reaction(react) # КР, ЗЕЛ
                                    await pasmes.add_reaction(close_em) # КР, ЗЕЛ
                                else:
                                    print("Терпение")
                                    await reaction.message.edit(content="НАЖМИТЕ НА "+str(key)+" ["+result+"]\nТОРОПИТЬСЯ НЕКУДА")
                                    await reaction.remove(user)
                                    await reaction.message.edit(content="НАЖМИТЕ НА "+str(key)+" ["+result+"]")
                elif BDMessages[reaction.message.id] == "Steal_Admin_Message" and user != bot.user: # Проверка хозяина сообщения
                    delmes = await reaction.message.channel.send(user.name+" руки убрал")
                    await reaction.remove(user)
                    time.sleep(0.5)
                    await delmes.delete()

        except Exception as e:
            print(e)

    @bot.event
    async def on_message(mes):
        checkInPointsMas(mes.author.id)
        if mes.author.id not in muted_names:
            await bot.process_commands(mes)
        updateLocalActiveMes()
        try:
            if mes.content != "":
                if len(mes.attachments) == 0 and mes.content[0] == "!":
                    log = time.ctime(time.time())+" "+str(mes.content)+" "+str(mes.author)+" "+str(mes.author.id)
                    with open("logs.txt","a",encoding="utf-8") as f:
                        f.write(log+"\n")
                        print(log)

            if mes.author.id in muted_names and mes.author.id != kolbaskas_id: # Постоянная проверка новых сообщений на наличие автора в забаненом списке
                await mes.delete()
                print("Мистер "+str(mes.author.name)+" попытался сказать: "+str(mes.content))

            if mes.channel.id == 848863391812026448 and mes.author != bot.user: # Обработка шахты
                maxsize = 200
                oneLet = 0.005

                checkInPointsMas(mes.author.id)
                pointsMas[mes.author.id] += oneLet * len(mes.content) if len(mes.content) <= maxsize else oneLet * maxsize # Если сообщение больше maxsize символов то упирается в ограничение
                #updateTablePoints()
                #print(pointsMas,mes.author.name)
        except Exception as e:
            print(e)
    


    @bot.event # Ивент, проверяющий состояние микрофонов на канале
    async def on_voice_state_update(upd_target_member,last_member,new_member):
        global main_target_member,vc
        print(' У '+str(upd_target_member.name)+" изменился микрофон")

        log = time.ctime(time.time())+" "+str(upd_target_member.name)+" "+str(upd_target_member.id)
        with open("logs.txt","a",encoding="utf-8") as f:
            f.write(log+"\n")
            print(log)

        # print(list)
        if main_target_member == upd_target_member and upd_target_member.voice.self_mute == False:
            print("ВЫБРАННАЯ ЦЕЛЬ ВКЛЮЧИЛА МИКРОФОН")
            target_channel = new_member.channel # Выбирается обьект канала
            list = target_channel.members # Список пользователей на канале

            if main_target_member:
                list.remove(main_target_member)
                if upd_target_member.guild.get_member(bot.user.id) in list: # Проверяет наличие самого бота на канале
                    list.remove(upd_target_member.guild.get_member(bot.user.id))

            for memb in list:
                print("Антимут "+str(memb.name))
                await memb.edit(mute = False)

            if upd_target_member.guild.get_member(bot.user.id) in target_channel.members:
                if vc and not vc.is_playing():
                    vc.play(discord.FFmpegPCMAudio(source="soundOnMicroState.mp3"))


        elif main_target_member == upd_target_member and upd_target_member.voice.self_mute == True:
            print("ВЫБРАННАЯ ЦЕЛЬ ВЫКЛЮЧИЛА МИКРОФОН")
            target_channel = new_member.channel
            list = target_channel.members

            if main_target_member:
                list.remove(main_target_member)
                if upd_target_member.guild.get_member(bot.user.id) in list:
                    list.remove(upd_target_member.guild.get_member(bot.user.id))

            for memb in list:
                print("Мут "+str(memb.name))
                await memb.edit(mute = True)

            if upd_target_member.guild.get_member(bot.user.id) in target_channel.members:
                if vc and not vc.is_playing():
                    vc.play(discord.FFmpegPCMAudio(source="soundOnMicroState.mp3"))

    @bot.event
    async def on_command_error(ctx, error):
        await ctx.send('В команду насрали и получилось: '+str(error))

    bot.run(TOKEN)

except Exception as e:
    print(e)