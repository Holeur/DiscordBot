import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import time
import bestdllever
import os
import youtube_dl
import random
import selenium
from selenium import webdriver
from module1 import *
import pyscreenshot as ImageGrab
import turtle
import pyodbc

try:
    kolbaskas_id = 259670108266430464
    TOKEN = os.getenv("BOT_TOKEN")
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='!',intents=intents, help_command=None)
    #r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'r'DBQ=DB.accdb;'
    connect_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=DB.accdb;') 
    
    
    OpenBD = pyodbc.connect(connect_str) #Открывам базу данных через прописанные данные
    BDCur = OpenBD.cursor() #Обьявляем курсор в базе данных

    admin_names = []
    muted_names = []
    pointsMas = {}
    attack_mas = {} # {(id:time),(id:time)}
    alpNumbers = {"1️⃣":"1","0️⃣":"0","2️":"2","3️⃣":"3","4️⃣":"4","5️⃣":"5","6️⃣":"6","7️⃣":"7","8️⃣":"8","9️⃣":"9","🇦":"A","🇧":"B","🇨":"C","🇩":"D","🇪":"E","🇫":"F"}

    main_target_member = ""
    active_channel_id = ""
    main_guild = ""
    
    browser = webdriver.Chrome()
    
    def timelog():
        return time.ctime(time.time())

    @bot.event
    async def on_ready(): # Ивент срабатывает при запуске бота
        loadTablePoints()

        print("ADMINS:"+str(admin_names))
        print("MUTED_BOYS"+str(muted_names))
        print(bot.user.name)
        print(bot.user.id)
        print(bot.guilds)
        print('------')


#
# НАЙТИ ТЕКСТ С СИНОНИМАМИ
#

    @bot.command()
    async def get_sinonim(ctx,text):
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
# СИСТЕМА ПОИНТОВ
#
    def loadTablePoints(): # Функция проверяет первый элемент в таблице, если есть то собирает строки пока не наткнется на пустую
        tempMas = BDCur.execute("select id,points,AttackTimer,Admin,Chat_muted from Users").fetchall()
        BDCur.commit()
        for user in tempMas:
            pointsMas[int(user[0])] = user[1]
            attack_mas[int(user[0])] = user[2]
            if user[3] == True:
                admin_names.append(int(user[0]))
            if user[4] == True:
                muted_names.append(int(user[0]))
        print(pointsMas)


    #def updateTablePoints(): # Функция обновляет ТАБЛИЦУ по СЛОВАРЮ.

    def checkInPointsMas(id): 
        if id not in pointsMas:
            pointsMas[id] = 0
            BDCur.execute("Insert into Users(ID,Name,AttackTimer,Points,Admin,Chat_muted) values ('"+str(id)+"','"+str(bot.get_user(id).name)+"',0,0,False,False)")
            BDCur.commit()

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
            BDCur.execute("Update Users set Points="+str(pointsMas[ctx.author.id])+" where id='"+str(ctx.author.id)+"';") # Обновляем поинты в БД
            BDCur.execute("Update Users set Points="+str(pointsMas[tar_id])+" where id='"+str(tar_id)+"';")
            BDCur.commit()

            print(str(ctx.author.name)+" передал "+str(ctx.guild.get_member(tar_id).name)+" "+str(amount)+" поинтов")
            await ctx.send(str(ctx.author.name)+" передал "+str(ctx.guild.get_member(tar_id).name)+" "+str(amount)+" поинтов")
        else:
            await ctx.send("Недостаточно поинтов")

    @bot.command()
    async def attack(ctx,name):
        global attack_mas
        try:
            id = ctx.guild.get_member(int(name[3:name.find(">")])).id
            stolen_points = random.randint(0,int(pointsMas[id]))
            dice = random.randint(0,100)
            chance_to_win = 40
            CD = 600 # CoolDown
            price = 100
            descr = "нападение"
            StartTime = int(time.time())

            if ctx.author.id not in attack_mas:
                attack_mas[ctx.author.id] = 0

            if StartTime >= attack_mas[ctx.author.id] + CD:
                if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
                    if dice <= chance_to_win:
                        if pointsMas[id] >= stolen_points:
                            pointsMas[ctx.author.id] += stolen_points
                            pointsMas[id] -= stolen_points

                            await ctx.send(ctx.author.name+" напал на "+ctx.guild.get_member(id).name+" и украл "+str(stolen_points)+" поинтов")
                        else:
                            stolen_points = pointsMas[id]
                            pointsMas[ctx.author.id] += stolen_points
                            pointsMas[id] -= stolen_points

                            await ctx.send(ctx.author.name+" напал на "+ctx.guild.get_member(id).name+" и украл "+str(stolen_points)+" поинтов")
                    else:
                        await ctx.send(ctx.author.name+" напал на "+ctx.guild.get_member(id).name+" и не смог украсть поинты")
                    attack_mas[ctx.author.id] = StartTime
                    print(attack_mas)
                    spendPoints(ctx,price)
                    #updateTablePoints()
                    BDCur.execute("Update Users set Points="+str(pointsMas[ctx.author.id])+" where id='"+str(ctx.author.id)+"';") # Обновляем поинты в БД
                    BDCur.execute("Update Users set AttackTimer="+str(attack_mas[ctx.author.id])+" where id='"+str(ctx.author.id)+"';") # Обновляем поинты в БД
                    BDCur.commit()

                    await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)
                else:
                    await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))
            else:
                await ctx.send("У "+str(ctx.author.name)+" еще перезарядка атаки "+str(time.strftime("%H-%M-%S",time.gmtime((StartTime-attack_mas[ctx.author.id]-CD)*-1))))
                print(attack_mas)
        except Exception as e:
            await ctx.send(e)

    @bot.command()
    async def removeTimer(ctx,name):
        try:
            if ctx.author.id in admin_names:
                target_id = int(name[3:name.find(">")])

                if target_id in attack_mas:
                    del attack_mas[target_id]
                    await ctx.send("У "+str(ctx.guild.get_member(target_id).name)+" был сброшен таймер")
                else:
                    await ctx.send("У "+str(ctx.guild.get_member(target_id).name)+" нету таймера")
            else:
                await ctx.send(ctx.author.name+" не является администратором")
        except Exception as e:
            await ctx.send(e)

    @bot.command()
    async def dai_point(ctx):
        if ctx.author.id not in pointsMas:
            checkInPointsMas(ctx.author.id)
            pointsMas[ctx.author.id] = 500
            BDCur.execute("Update User set Points="+str(pointsMas[ctx.author.id])+" where id='"+str(ctx.author.id)+"';") # Обновляем поинты в БД
            BDCur.commit()
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
                BDCur.execute("Update Users set Points="+str(pointsMas[target_member.id])+" where id='"+str(target_member.id)+"';") # Обновляем поинты в БД
                BDCur.commit()

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
                BDCur.execute("Update Users set Points="+str(pointsMas[target_member.id])+" where id='"+str(target_member.id)+"';") # Обновляем поинты в БД
                BDCur.commit()

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
                BDCur.execute("Update Users set Points="+str(pointsMas[target_member.id])+" where id='"+str(target_member.id)+"';") # Обновляем поинты в БД
                BDCur.commit()

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
                    BDCur.execute("Update Users set Points="+str(pointsMas[ctx.author.id])+" where id='"+str(ctx.author.id)+"';") # Обновляем поинты в БД
                    BDCur.commit()

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
                        BDCur.execute("Update Users set Admin=True where id='"+str(admin_member.id)+"';")
                        BDCur.commit()
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
                        BDCur.execute("Update Users set Admin=False where id='"+str(admin_member.id)+"';")
                        BDCur.commit()
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

        if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
            channel = ctx.channel
            await ctx.send("Потрачено "+str(price)+" поинтов на "+descr)
            await channel.purge(check=is_me)

            spendPoints(ctx,price)
            
        else:
            await ctx.send("Недостаточно поинтов. Цена: "+str(price)+". У вас: "+str(round(pointsMas[ctx.author.id],2)))

    @bot.command()
    async def stealth_mute(ctx,id): # Функция тихого мута пользователя в чате\
        try:
            price = 500
            descr = "мут человека в чате"

            if ctx.author.id in pointsMas and pointsMas[ctx.author.id] >= price:
                target_member = ctx.guild.get_member(int(id[3:id.find(">")])) # Пользователь определеяется по слапу в дискорде
                if target_member.id != kolbaskas_id:

                    if target_member.name not in muted_names:
                        muted_names.append(target_member.name)
                        BDCur.execute("update users set Chat_muted=True where id='"+str(target_member.id)+"';")
                        BDCur.commit()
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
                    if target_member.name in muted_names:
                        del muted_names[muted_names.index(target_member.name)]
                        BDCur.execute("update users set Chat_muted=False where id='"+str(target_member.id)+"';")
                        BDCur.commit()
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
    #        exCom = "INSERT into Users (ID,NAME,AttackTimer,Points) values ('"+str(ctx.author.id)+"','"+str(ctx.author.name)+"',"+str(attack_mas[ctx.author.id] if ctx.author.id in attack_mas else 0)+","+str(pointsMas[ctx.author.id] if ctx.author.id in pointsMas else 0)+");"
    #        print(exCom)
    #        BDCur.execute(exCom)
    #        BDCur.commit()
    #        print("Добавлен в базу данных")
    #    except Exception as e:
    #        print(e)

    @bot.command()
    async def steal_admin(ctx):
        global pasmes,result,green_pos,Main_user
        Main_user = ctx.author
        result = "-----"
        pasmes = await ctx.send("НАЖМИТЕ НА ЗЕЛЕНЫЕ ["+result+"]")
        reactionsList = ["🟥","🟧","🟨","🟦","🟪","🟫"]
        green_pos = random.randint(0,5)
        reactionsList[green_pos] = "🟩"
        for reaction in reactionsList:
            await pasmes.add_reaction(reaction) # КР, ЗЕЛ


    @bot.command()
    async def executeSQL(ctx,com):
        try:
            ret = BDCur.execute(com).fetchall()
            mes = ""
            if ret != None:
                for elem in ret:
                    mes += str(elem)+"\n"
            await ctx.send(mes)
            BDCur.commit()
        except Exception as e:
            await ctx.send("SQL команда не прошла: "+str(e))
#
# ИВЕНТЫ
#

    #def updateHexColor(mas):
    #    global colorName
        
    def choiceHEXLet(mas):
        mes = ""
        for elem in range(0,6):
            try:
                mes += alpNumbers[mas[elem].emoji]
            except IndexError:
                mes += "0"
        return mes

    @bot.event
    async def on_reaction_add(reaction,user):
        global pasmes,result,green_pos,Main_user
        try:
            if user == Main_user:
                if reaction.message == pasmes and user != bot.user:
                    print(reaction)

                    choisen_pos = reaction.message.reactions.index(reaction)
                    reactionsList = ["🟥","🟧","🟨","🟦","🟪","🟫"]

                    print(choisen_pos)
                    print(green_pos)

                    changed_map = [4,1,5,2,0,3]

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
                    if win:

                        if len(reaction.message.reactions) >= 6:
                            result = "X"+result[:4]
                            await pasmes.edit(content="НАЖМИТЕ НА ЗЕЛЕНЫЕ ["+result+"]")
                            await pasmes.clear_reactions()
                            green_pos = random.randint(0,5)
                            reactionsList[green_pos] = "🟩"

                            if result[4] == "X":
                                await pasmes.delete()
                                admin_names.append(user.id)
                                checkInPointsMas(user.id)
                                BDCur.execute("update users set admin=True where id='"+str(user.id)+"';")
                                BDCur.commit()
                                await reaction.message.channel.send(user.name+" становится админом")
                            else:
                                for react in reactionsList:
                                    await pasmes.add_reaction(react) # КР, ЗЕЛ
                        else:
                            print("Терпение")
                            await reaction.message.edit(content="НАЖМИТЕ НА ЗЕЛЕНЫЕ ["+result+"]\nТОРОПИТЬСЯ НЕКУДА")
                            await reaction.remove(user)
                            await reaction.message.edit(content="НАЖМИТЕ НА ЗЕЛЕНЫЕ ["+result+"]")
                    else:
                        if len(reaction.message.reactions) >= 6:
                            print("Reset Game")
                            result = "-----"
                            await pasmes.edit(content="НАЖМИТЕ НА ЗЕЛЕНЫЕ ["+result+"]")
                            await pasmes.clear_reactions()
                            green_pos = random.randint(0,5)
                            reactionsList[green_pos] = "🟩"

                            for react in reactionsList:
                                await pasmes.add_reaction(react) # КР, ЗЕЛ
                        else:
                            print("Терпение")
                            await reaction.message.edit(content="НАЖМИТЕ НА ЗЕЛЕНЫЕ ["+result+"]\nТОРОПИТЬСЯ НЕКУДА")
                            await reaction.remove(user)
                            await reaction.message.edit(content="НАЖМИТЕ НА ЗЕЛЕНЫЕ ["+result+"]")
            elif user != bot.user:
                delmes = await reaction.message.channel.send(user.name+" руки убрал")
                await reaction.remove(user)
                await delmes.delete()

        except Exception as e:
            print(e)

    @bot.event
    async def on_message(mes):
        await bot.process_commands(mes)

        if len(mes.attachments) == 0 and mes.content[0] == "!":
            log = time.ctime(time.time())+" "+str(mes.content)+" "+str(mes.author)+" "+str(mes.author.id)
            with open("logs.txt","a",encoding="utf-8") as f:
                f.write(log+"\n")
                print(log)

        if mes.author.name in muted_names and mes.author.id != kolbaskas_id: # Постоянная проверка новых сообщений на наличие автора в забаненом списке
            await mes.delete()
            print("Мистер "+str(mes.author.name)+" попытался сказать: "+str(mes.content))

        if mes.channel.id == 848863391812026448 and mes.author != bot.user: # Обработка шахты
            maxsize = 200
            oneLet = 0.005

            checkInPointsMas(mes.author.id)
            pointsMas[mes.author.id] += oneLet * len(mes.content) if len(mes.content) <= maxsize else oneLet * maxsize # Если сообщение больше maxsize символов то упирается в ограничение
            updateTablePoints()
            #print(pointsMas,mes.author.name)

    


    @bot.event # Ивент, проверяющий состояние микрофонов на канале
    async def on_voice_state_update(upd_target_member,last_member,new_member):
        global main_target_member,vc
        print(' У '+str(upd_target_member.name)+" изменился микрофон")

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