from urllib import parse


def fix_params(params):
    print(params.replace('&','\n'))

def fix_assets(params):
    print(params.replace(',','\n'))

def utf8_decode(string):
    print(parse.unquote(string))

def unicode_decode(s):
    s = s.encode('unicode_escape')
    print(s)

def params_dict(para):
    print(dict([line.split("=", 1) for line in para.split("\n")]))

#fix_params(input('pls input params:\n'))
#utf8_decode(input('pls input string:\n'))
fix_assets(input('pls input assets:\n'))
#unicode_decode(input('pls input string:\n'))
raw_para = '''q=
category_730_ItemSet%5B%5D=any
category_730_ProPlayer%5B%5D=any
category_730_StickerCapsule%5B%5D=any
category_730_TournamentTeam%5B%5D=any
category_730_Weapon%5B%5D=any
category_730_Exterior%5B%5D=tag_WearCategory2
category_730_Quality%5B%5D=tag_tournament
category_730_Rarity%5B%5D=tag_Rarity_Common_Weapon
category_730_SprayCapsule%5B%5D=tag_csgo_spray_std2_drops_2
category_730_SprayCategory%5B%5D=tag_TeamLogo
category_730_SprayColorCategory%5B%5D=tag_Tint18
category_730_StickerCategory%5B%5D=tag_TeamLogo
category_730_Tournament%5B%5D=tag_Tournament13
category_730_Type%5B%5D=tag_CSGO_Tool_Sticker
appid=730'''
#params_dict(raw_para)
#params_dict(raw_para.replace('%5B%5D', ''))

