import bestdllever

try:
    with open("DiscordBot.py","r",encoding='utf-8') as f:
        a = 0
        for line in f:
            bestdllever.deleten(line)
            print(line)
            if a == 1:
                print(line.split(" ")[2])
                a = 0
            if '@bot.command()' in line:
                print("??????????????????")
                a = 1
            
    input()
except Exception as e:
    input(e)