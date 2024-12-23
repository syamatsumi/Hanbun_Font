#!fontforge --lang=py -script

import fontforge

def ys_swap_glyph(font, glyph, o_glyphname, s_glyphname):
    if s_glyphname in font:
        # グリフの置換を実行
        font.selection.select(s_glyphname)
        font.copy()
        font.selection.select(o_glyphname)
        font.clear()
        font.paste()
        font.selection.none()

        # 置換成功？ フラグにTrueを返す
        return True
    else:
        # 置換先が無いなら何もせずFalseを返す
        return False



def ys_swaplist(font, glyph):
    swaplist_set = {
        "uni201D": "quotedblright.hwid",  # "
        "uni201C": "quotedblleft.hwid",  # “
        "uni2019": "quoteright.hwid",  # '
        "uni2018": "quoteleft.hwid",  # `
        "uni30F2": "uniFF66",  # ｦ
        "uni30A1": "uniFF67",  # ｧ
        "uni30A3": "uniFF68",  # ｨ
        "uni30A5": "uniFF69",  # ｩ
        "uni30A7": "uniFF6A",  # ｪ
        "uni30A9": "uniFF6B",  # ｫ
        "uni30E3": "uniFF6C",  # ｬ
        "uni30E5": "uniFF6D",  # ｭ
        "uni30E7": "uniFF6E",  # ｮ
        "uni30C3": "uniFF6F",  # ｯ
        "uni30FC": "uniFF70",  # ｰ
        "uni30A2": "uniFF71",  # ｱ
        "uni30A4": "uniFF72",  # ｲ
        "uni30A6": "uniFF73",  # ｳ
        "uni30A8": "uniFF74",  # ｴ
        "uni30AA": "uniFF75",  # ｵ
        "uni30AB": "uniFF76",  # ｶ
        "uni30AD": "uniFF77",  # ｷ
        "uni30AF": "uniFF78",  # ｸ
        "uni30B1": "uniFF79",  # ｹ
        "uni30B3": "uniFF7A",  # ｺ
        "uni30B5": "uniFF7B",  # ｻ
        "uni30B7": "uniFF7C",  # ｼ
        "uni30B9": "uniFF7D",  # ｽ
        "uni30BB": "uniFF7E",  # ｾ
        "uni30BD": "uniFF7F",  # ｿ
        "uni30BF": "uniFF80",  # ﾀ
        "uni30C1": "uniFF81",  # ﾁ
        "uni30C4": "uniFF82",  # ﾂ
        "uni30C6": "uniFF83",  # ﾃ
        "uni30C8": "uniFF84",  # ﾄ
        "uni30CA": "uniFF85",  # ﾅ
        "uni30CB": "uniFF86",  # ﾆ
        "uni30CC": "uniFF87",  # ﾇ
        "uni30CD": "uniFF88",  # ﾈ
        "uni30CE": "uniFF89",  # ﾉ
        "uni30CF": "uniFF8A",  # ﾊ
        "uni30D2": "uniFF8B",  # ﾋ
        "uni30D5": "uniFF8C",  # ﾌ
        "uni30D8": "uniFF8D",  # ﾍ
        "uni30DB": "uniFF8E",  # ﾎ
        "uni30DE": "uniFF8F",  # ﾏ
        "uni30DF": "uniFF90",  # ﾐ
        "uni30E0": "uniFF91",  # ﾑ
        "uni30E1": "uniFF92",  # ﾒ
        "uni30E2": "uniFF93",  # ﾓ
        "uni30E4": "uniFF94",  # ﾔ
        "uni30E6": "uniFF95",  # ﾕ
        "uni30E8": "uniFF96",  # ﾖ
        "uni30E9": "uniFF97",  # ﾗ
        "uni30EA": "uniFF98",  # ﾘ
        "uni30EB": "uniFF99",  # ﾙ
        "uni30EC": "uniFF9A",  # ﾚ
        "uni30ED": "uniFF9B",  # ﾛ
        "uni30EF": "uniFF9C",  # ﾜ
        "uni30F3": "uniFF9D",  # ﾝ
        "uni30F0": "uni30F0.aalt",  # ヰ
        "uni30F1": "uni30F1.aalt",  # ヱ
        "uni30EE": "uni30EE.hwid",  # ヮ
        "uni30F5": "uni30F5.hwid",  # ヵ
        "uni30F6": "uni30F6.hwid",  # ヶ
        "uni30F4": "uni30F4.aalt",  # ヴ
        "uni30AC": "uni30AC.aalt",  # ｶﾞ
        "uni30AE": "uni30AE.aalt",  # ｷﾞ
        "uni30B0": "uni30B0.aalt",  # ｸﾞ
        "uni30B2": "uni30B2.aalt",  # ｹﾞ
        "uni30B4": "uni30B4.aalt",  # ｺﾞ
        "uni30B6": "uni30B6.aalt",  # ｻﾞ
        "uni30B8": "uni30B8.aalt",  # ｼﾞ
        "uni30BA": "uni30BA.aalt",  # ｽﾞ
        "uni30BC": "uni30BC.aalt",  # ｾﾞ
        "uni30BE": "uni30BE.aalt",  # ｿﾞ
        "uni30C0": "uni30C0.aalt",  # ﾀﾞ
        "uni30C2": "uni30C2.aalt",  # ﾁﾞ
        "uni30C5": "uni30C5.aalt",  # ﾂﾞ
        "uni30C7": "uni30C7.aalt",  # ﾃﾞ
        "uni30C9": "uni30C9.aalt",  # ﾄﾞ
        "uni30D0": "uni30D0.aalt",  # ﾊﾞ
        "uni30D1": "uni30D1.aalt",  # ﾊﾟ
        "uni30D3": "uni30D3.aalt",  # ﾋﾞ
        "uni30D4": "uni30D4.aalt",  # ﾋﾟ
        "uni30D6": "uni30D6.aalt",  # ﾌﾞ
        "uni30D7": "uni30D7.aalt",  # ﾌﾟ
        "uni30D9": "uni30D9.aalt",  # ﾍﾞ
        "uni30DA": "uni30DA.aalt",  # ﾍﾟ
        "uni30DC": "uni30DC.aalt",  # ﾎﾞ
        "uni30DD": "uni30DD.aalt",  # ﾎﾟ
        "uni301D": "uni301D.hwid",  # 〝
        "uni301F": "uni301F.hwid",  # 〟
        "uni3014": "uni3014.hwid",  # 〔
        "uni3015": "uni3015.hwid",  # 〕
        "uni3008": "uni3008.hwid",  # 〈
        "uni3009": "uni3009.hwid",  # 〉
        "uni300A": "uni300A.hwid",  # 《
        "uni300B": "uni300B.hwid",  # 》
        "uni300E": "uni300E.hwid",  # 『
        "uni300F": "uni300F.hwid",  # 』
        "uni3010": "uni3010.hwid",  # 【
        "uni3011": "uni3011.hwid",  # 】
        "uniFF0D": "uniFF0D.hwid",  # -
        "uni3092": "uni3092.aalt",  # を
        "uni3041": "uni3041.hwid",  # ぁ
        "uni3043": "uni3043.hwid",  # ぃ
        "uni3045": "uni3045.hwid",  # ぅ
        "uni3047": "uni3047.hwid",  # ぇ
        "uni3049": "uni3049.hwid",  # ぉ
        "uni3083": "uni3083.hwid",  # ゃ
        "uni3085": "uni3085.hwid",  # ゅ
        "uni3087": "uni3087.hwid",  # ょ
        "uni3063": "uni3063.hwid",  # っ
        "uni3042": "uni3042.aalt",  # あ
        "uni3044": "uni3044.aalt",  # い
        "uni3046": "uni3046.aalt",  # う
        "uni3048": "uni3048.aalt",  # え
        "uni304A": "uni304A.aalt",  # お
        "uni304B": "uni304B.aalt",  # か
        "uni304D": "uni304D.aalt",  # き
        "uni304F": "uni304F.aalt",  # く
        "uni3051": "uni3051.aalt",  # け
        "uni3053": "uni3053.aalt",  # こ
        "uni3055": "uni3055.aalt",  # さ
        "uni3057": "uni3057.aalt",  # し
        "uni3059": "uni3059.aalt",  # す
        "uni305B": "uni305B.aalt",  # せ
        "uni305D": "uni305D.aalt",  # そ
        "uni305F": "uni305F.aalt",  # た
        "uni3061": "uni3061.aalt",  # ち
        "uni3064": "uni3064.aalt",  # つ
        "uni3066": "uni3066.aalt",  # て
        "uni3068": "uni3068.aalt",  # と
        "uni306A": "uni306A.aalt",  # な
        "uni306B": "uni306B.aalt",  # に
        "uni306C": "uni306C.aalt",  # ぬ
        "uni306D": "uni306D.aalt",  # ね
        "uni306E": "uni306E.aalt",  # の
        "uni306F": "uni306F.aalt",  # は
        "uni3072": "uni3072.aalt",  # ひ
        "uni3075": "uni3075.aalt",  # ふ
        "uni3078": "uni3078.aalt",  # へ
        "uni307B": "uni307B.aalt",  # ほ
        "uni307E": "uni307E.aalt",  # ま
        "uni307F": "uni307F.aalt",  # み
        "uni3080": "uni3080.aalt",  # む
        "uni3081": "uni3081.aalt",  # め
        "uni3082": "uni3082.aalt",  # も
        "uni3084": "uni3084.aalt",  # や
        "uni3086": "uni3086.aalt",  # ゆ
        "uni3088": "uni3088.aalt",  # よ
        "uni3089": "uni3089.aalt",  # ら
        "uni308A": "uni308A.aalt",  # り
        "uni308B": "uni308B.aalt",  # る
        "uni308C": "uni308C.aalt",  # れ
        "uni308D": "uni308D.aalt",  # ろ
        "uni308F": "uni308F.aalt",  # わ
        "uni3093": "uni3093.aalt",  # ん
        "uni3090": "uni3090.aalt",  # ゐ
        "uni3091": "uni3091.aalt",  # ゑ
        "uni308E": "uni308E.hwid",  # ゎ
        "uni304C": "uni304C.aalt",  # が
        "uni304E": "uni304E.aalt",  # ぎ
        "uni3050": "uni3050.aalt",  # ぐ
        "uni3052": "uni3052.aalt",  # げ
        "uni3054": "uni3054.aalt",  # ご
        "uni3056": "uni3056.aalt",  # ざ
        "uni3058": "uni3058.aalt",  # じ
        "uni305A": "uni305A.aalt",  # ず
        "uni305C": "uni305C.aalt",  # ぜ
        "uni305E": "uni305E.aalt",  # ぞ
        "uni3060": "uni3060.aalt",  # だ
        "uni3062": "uni3062.aalt",  # ぢ
        "uni3065": "uni3065.aalt",  # づ
        "uni3067": "uni3067.aalt",  # で
        "uni3069": "uni3069.aalt",  # ど
        "uni3070": "uni3070.aalt",  # ば
        "uni3071": "uni3071.aalt",  # ぱ
        "uni3073": "uni3073.aalt",  # び
        "uni3074": "uni3074.aalt",  # ぴ
        "uni3076": "uni3076.aalt",  # ぶ
        "uni3077": "uni3077.aalt",  # ぷ
        "uni3079": "uni3079.aalt",  # べ
        "uni307A": "uni307A.aalt",  # ぺ
        "uni307C": "uni307C.aalt",  # ぼ
        "uni307D": "uni307D.aalt",  # ぽ
        "uni2500": "SF100000.hwid",  # ─
        "uni2501": "uni2501.hwid",  # ━
        "uni2502": "SF110000.hwid",  # │
        "uni2503": "uni2503.hwid",  # ┃
        "uni250C": "SF010000.hwid",  # ┌
        "uni250F": "uni250F.hwid",  # ┏
        "uni2510": "SF030000.hwid",  # ┐
        "uni2513": "uni2513.hwid",  # ┓
        "uni2514": "SF020000.hwid",  # └
        "uni2517": "uni2517.hwid",  # ┗
        "uni2518": "SF040000.hwid",  # ┘
        "uni251B": "uni251B.hwid",  # ┛
        "uni251C": "SF080000.hwid",  # ├
        "uni251D": "uni251D.hwid",  # ┝
        "uni2520": "uni2520.hwid",  # ┠
        "uni2523": "uni2523.hwid",  # ┣
        "uni2524": "SF090000.hwid",  # ┤
        "uni2525": "uni2525.hwid",  # ┥
        "uni2528": "uni2528.hwid",  # ┨
        "uni252B": "uni252B.hwid",  # ┫
        "uni252C": "SF060000.hwid",  # ┬
        "uni252F": "uni252F.hwid",  # ┯
        "uni2530": "uni2530.hwid",  # ┰
        "uni2533": "uni2533.hwid",  # ┳
        "uni2534": "SF070000.hwid",  # ┴
        "uni2537": "uni2537.hwid",  # ┷
        "uni2538": "uni2538.hwid",  # ┸
        "uni253B": "uni253B.hwid",  # ┻
        "uni253C": "SF050000.aalt",  # ┼
        "uni253F": "uni253F.hwid",  # ┿
        "uni2542": "uni2542.hwid",  # ╂
        "uni254B": "uni254B.aalt"  # ╋
    }

    # グリフ名がリストにあるかチェック
    o_glyphname = glyph.glyphname
    if o_glyphname in swaplist_set:
        s_glyphname = swaplist_set[o_glyphname]
        # グリフの置換を実施して成功・失敗のフラグを返す
        flag = ys_swap_glyph(font, glyph, o_glyphname, s_glyphname)
        return flag

    # リストに一致しないなら何もせずにFalseを返す
    else:
        return False



def ys_pswaplist(font, glyph):
    swaplist_set = {
        "uni0021": "glyph3",  # !
        "uni0022": "glyph4",  # "
        "uni0023": "glyph5",  # #
        "uni0024": "glyph6",  # $
        "uni0025": "glyph7",  # %
        "uni0026": "glyph8",  # &
        "uni0027": "glyph9",  # '
        "uni0028": "glyph10",  # (
        "uni0029": "glyph11",  # )
        "uni002A": "glyph12",  # *
        "uni002B": "glyph13",  # +
        "uni002C": "glyph14",  # ,
        "uni002D": "glyph15",  # -
        "uni002E": "glyph16",  # .
        "uni002F": "glyph17",  # /
        "uni0030": "glyph18",  # 0
        "uni0031": "glyph19",  # 1
        "uni0032": "glyph20",  # 2
        "uni0033": "glyph21",  # 3
        "uni0034": "glyph22",  # 4
        "uni0035": "glyph23",  # 5
        "uni0036": "glyph24",  # 6
        "uni0037": "glyph25",  # 7
        "uni0038": "glyph26",  # 8
        "uni0039": "glyph27",  # 9
        "uni003A": "glyph28",  # :
        "uni003B": "glyph29",  # ;
        "uni003C": "glyph30",  # <
        "uni003D": "glyph31",  # =
        "uni003E": "glyph32",  # >
        "uni003F": "glyph33",  # ?
        "uni0040": "glyph34",  # @
        "uni0041": "glyph35",  # A
        "uni0042": "glyph36",  # B
        "uni0043": "glyph37",  # C
        "uni0044": "glyph38",  # D
        "uni0045": "glyph39",  # E
        "uni0046": "glyph40",  # F
        "uni0047": "glyph41",  # G
        "uni0048": "glyph42",  # H
        "uni0049": "glyph43",  # I
        "uni004A": "glyph44",  # J
        "uni004B": "glyph45",  # K
        "uni004C": "glyph46",  # L
        "uni004D": "glyph47",  # M
        "uni004E": "glyph48",  # N
        "uni004F": "glyph49",  # O
        "uni0050": "glyph50",  # P
        "uni0051": "glyph51",  # Q
        "uni0052": "glyph52",  # R
        "uni0053": "glyph53",  # S
        "uni0054": "glyph54",  # T
        "uni0055": "glyph55",  # U
        "uni0056": "glyph56",  # V
        "uni0057": "glyph57",  # W
        "uni0058": "glyph58",  # X
        "uni0059": "glyph59",  # Y
        "uni005A": "glyph60",  # Z
        "uni005B": "glyph61",  # [
        "uni005C": "glyph62",  # \
        "uni005D": "glyph63",  # ]
        "uni005E": "glyph64",  # ^
        "uni005F": "glyph65",  # _
        "uni0060": "glyph66",  # `
        "uni0061": "glyph67",  # a
        "uni0062": "glyph68",  # b
        "uni0063": "glyph69",  # c
        "uni0064": "glyph70",  # d
        "uni0065": "glyph71",  # e
        "uni0066": "glyph72",  # f
        "uni0067": "glyph73",  # g
        "uni0068": "glyph74",  # h
        "uni0069": "glyph75",  # i
        "uni006A": "glyph76",  # j
        "uni006B": "glyph77",  # k
        "uni006C": "glyph78",  # l
        "uni006D": "glyph79",  # m
        "uni006E": "glyph80",  # n
        "uni006F": "glyph81",  # o
        "uni0070": "glyph82",  # p
        "uni0071": "glyph83",  # q
        "uni0072": "glyph84",  # r
        "uni0073": "glyph85",  # s
        "uni0074": "glyph86",  # t
        "uni0075": "glyph87",  # u
        "uni0076": "glyph88",  # v
        "uni0077": "glyph89",  # w
        "uni0078": "glyph90",  # x
        "uni0079": "glyph91",  # y
        "uni007A": "glyph92",  # z
        "uni007B": "glyph93",  # {
        "uni007C": "glyph94",  # |
        "uni007D": "glyph95",  # }
        "uni007E": "glyph96",  # ~
        "uni00A1": "glyph818",  # ¡
        "uni00A2": "glyph12264",  # ¢
        "uni00A3": "glyph12265",  # £
        "uni00A4": "glyph820",  # ¤
        "uni00A5": "glyph821",  # ¥
        "uni00A6": "glyph820",  # ¦
        "uni00A8": "glyph1067",  # ¨
        "uni00A9": "glyph821",  # ©
        "uni00AA": "glyph822",  # ª
        "uni00AB": "glyph823",  # «
        "uni00AC": "glyph12267",  # ¬
        "uni00AD": "glyph371",  # ­
        "uni00AE": "glyph824",  # ®
        "uni00AF": "glyph825",  # ¯
        "uni00B2": "glyph827",  # ²
        "uni00B3": "glyph828",  # ³
        "uni00B4": "glyph1052",  # ´
        "uni00B7": "glyph829",  # ·
        "uni00B8": "glyph830",  # ¸
        "uni00B9": "glyph831",  # ¹
        "uni00BA": "glyph832",  # º
        "uni00BB": "glyph833",  # »
        "uni00BC": "glyph834",  # ¼
        "uni00BD": "glyph835",  # ½
        "uni00BE": "glyph836",  # ¾
        "uni00BF": "glyph837",  # ¿
        "uni00C0": "glyph838",  # À
        "uni00C1": "glyph839",  # Á
        "uni00C2": "glyph840",  # Â
        "uni00C3": "glyph841",  # Ã
        "uni00C4": "glyph842",  # Ä
        "uni00C5": "glyph843",  # Å
        "uni00C6": "glyph844",  # Æ
        "uni00C7": "glyph845",  # Ç
        "uni00C8": "glyph846",  # È
        "uni00C9": "glyph847",  # É
        "uni00CA": "glyph848",  # Ê
        "uni00CB": "glyph849",  # Ë
        "uni00CC": "glyph850",  # Ì
        "uni00CD": "glyph851",  # Í
        "uni00CE": "glyph852",  # Î
        "uni00CF": "glyph853",  # Ï
        "uni00D0": "glyph854",  # Ð
        "uni00D1": "glyph855",  # Ñ
        "uni00D2": "glyph856",  # Ò
        "uni00D3": "glyph857",  # Ó
        "uni00D4": "glyph858",  # Ô
        "uni00D5": "glyph859",  # Õ
        "uni00D6": "glyph860",  # Ö
        "uni00D8": "glyph861",  # Ø
        "uni00D9": "glyph862",  # Ù
        "uni00DA": "glyph863",  # Ú
        "uni00DB": "glyph864",  # Û
        "uni00DC": "glyph865",  # Ü
        "uni00DD": "glyph866",  # Ý
        "uni00DE": "glyph867",  # Þ
        "uni00DF": "glyph868",  # ß
        "uni00E0": "glyph869",  # à
        "uni00E1": "glyph870",  # á
        "uni00E2": "glyph871",  # â
        "uni00E3": "glyph872",  # ã
        "uni00E4": "glyph873",  # ä
        "uni00E5": "glyph874",  # å
        "uni00E6": "glyph875",  # æ
        "uni00E7": "glyph876",  # ç
        "uni00E8": "glyph877",  # è
        "uni00E9": "glyph878",  # é
        "uni00EA": "glyph879",  # ê
        "uni00EB": "glyph880",  # ë
        "uni00EC": "glyph881",  # ì
        "uni00ED": "glyph882",  # í
        "uni00EE": "glyph883",  # î
        "uni00EF": "glyph884",  # ï
        "uni00F0": "glyph885",  # ð
        "uni00F1": "glyph886",  # ñ
        "uni00F2": "glyph887",  # ò
        "uni00F3": "glyph888",  # ó
        "uni00F4": "glyph889",  # ô
        "uni00F5": "glyph890",  # õ
        "uni00F6": "glyph891",  # ö
        "uni00F8": "glyph892",  # ø
        "uni00F9": "glyph893",  # ù
        "uni00FA": "glyph894",  # ú
        "uni00FB": "glyph895",  # û
        "uni00FC": "glyph896",  # ü
        "uni00FD": "glyph897",  # ý
        "uni00FE": "glyph898",  # þ
        "uni00FF": "glyph899",  # ÿ
        "uni0100": "glyph900",  # Ā
        "uni0101": "glyph905",  # ā
        "uni0102": "glyph935",  # Ă
        "uni0103": "glyph950",  # ă
        "uni0104": "glyph910",  # Ą
        "uni0105": "glyph921",  # ą
        "uni0106": "glyph937",  # Ć
        "uni0107": "glyph952",  # ć
        "uni0108": "glyph966",  # Ĉ
        "uni0109": "glyph972",  # ĉ
        "uni010C": "glyph938",  # Č
        "uni010D": "glyph953",  # č
        "uni010E": "glyph941",  # Ď
        "uni010F": "glyph956",  # ď
        "uni0110": "glyph854",  # Đ
        "uni0111": "glyph957",  # đ
        "uni0112": "glyph903",  # Ē
        "uni0113": "glyph908",  # ē
        "uni0118": "glyph939",  # Ę
        "uni0119": "glyph954",  # ę
        "uni011A": "glyph940",  # Ě
        "uni011B": "glyph955",  # ě
        "uni011C": "glyph967",  # Ĝ
        "uni011D": "glyph973",  # ĝ
        "uni0124": "glyph968",  # Ĥ
        "uni0125": "glyph974",  # ĥ
        "uni0127": "glyph1002",  # ħ
        "uni012A": "glyph901",  # Ī
        "uni012B": "glyph906",  # ī
        "uni0134": "glyph969",  # Ĵ
        "uni0135": "glyph975",  # ĵ
        "uni0139": "glyph936",  # Ĺ
        "uni013A": "glyph951",  # ĺ
        "uni013D": "glyph913",  # Ľ
        "uni013E": "glyph924",  # ľ
        "uni0141": "glyph912",  # Ł
        "uni0142": "glyph923",  # ł
        "uni0143": "glyph942",  # Ń
        "uni0144": "glyph958",  # ń
        "uni0147": "glyph943",  # Ň
        "uni0148": "glyph959",  # ň
        "uni014B": "glyph999",  # ŋ
        "uni014C": "glyph904",  # Ō
        "uni014D": "glyph909",  # ō
        "uni0150": "glyph944",  # Ő
        "uni0151": "glyph960",  # ő
        "uni0152": "glyph1014",  # Œ
        "uni0153": "glyph1013",  # œ
        "uni0154": "glyph934",  # Ŕ
        "uni0155": "glyph949",  # ŕ
        "uni0158": "glyph945",  # Ř
        "uni0159": "glyph961",  # ř
        "uni015A": "glyph914",  # Ś
        "uni015B": "glyph925",  # ś
        "uni015C": "glyph970",  # Ŝ
        "uni015D": "glyph976",  # ŝ
        "uni015E": "glyph916",  # Ş
        "uni015F": "glyph928",  # ş
        "uni0160": "glyph915",  # Š
        "uni0161": "glyph927",  # š
        "uni0162": "glyph948",  # Ţ
        "uni0163": "glyph964",  # ţ
        "uni0164": "glyph917",  # Ť
        "uni0165": "glyph929",  # ť
        "uni016A": "glyph902",  # Ū
        "uni016B": "glyph907",  # ū
        "uni016C": "glyph971",  # Ŭ
        "uni016D": "glyph977",  # ŭ
        "uni016E": "glyph946",  # Ů
        "uni016F": "glyph962",  # ů
        "uni0170": "glyph947",  # Ű
        "uni0171": "glyph963",  # ű
        "uni0179": "glyph918",  # Ź
        "uni017A": "glyph930",  # ź
        "uni017B": "glyph920",  # Ż
        "uni017C": "glyph933",  # ż
        "uni017D": "glyph919",  # Ž
        "uni017E": "glyph932",  # ž
        "uni0193": "glyph1012",  # Ɠ
        "uni01C2": "glyph1007",  # ǂ
        "uni01F8": "glyph808",  # Ǹ
        "uni01F9": "glyph809",  # ǹ
        "uni01FD": "glyph1039",  # ǽ
        "uni0250": "glyph1022",  # ɐ
        "uni0251": "glyph1028",  # ɑ
        "uni0252": "glyph1029",  # ɒ
        "uni0253": "glyph1008",  # ɓ
        "uni0254": "glyph1027",  # ɔ
        "uni0255": "glyph1034",  # ɕ
        "uni0256": "glyph987",  # ɖ
        "uni0257": "glyph1009",  # ɗ
        "uni0258": "glyph1017",  # ɘ
        "uni0259": "glyph1019",  # ə
        "uni025A": "glyph1038",  # ɚ
        "uni025C": "glyph1020",  # ɜ
        "uni025E": "glyph1021",  # ɞ
        "uni025F": "glyph994",  # ɟ
        "uni0260": "glyph1011",  # ɠ
        "uni0261": "glyph998",  # ɡ
        "uni0264": "glyph1025",  # ɤ
        "uni0265": "glyph1031",  # ɥ
        "uni0266": "glyph1005",  # ɦ
        "uni0267": "glyph1037",  # ɧ
        "uni0268": "glyph1015",  # ɨ
        "uni026C": "glyph983",  # ɬ
        "uni026D": "glyph993",  # ɭ
        "uni026E": "glyph984",  # ɮ
        "uni026F": "glyph1023",  # ɯ
        "uni0270": "glyph1000",  # ɰ
        "uni0271": "glyph978",  # ɱ
        "uni0272": "glyph995",  # ɲ
        "uni0273": "glyph988",  # ɳ
        "uni0275": "glyph1018",  # ɵ
        "uni0279": "glyph985",  # ɹ
        "uni027A": "glyph1036",  # ɺ
        "uni027B": "glyph992",  # ɻ
        "uni027D": "glyph989",  # ɽ
        "uni027E": "glyph980",  # ɾ
        "uni0281": "glyph1001",  # ʁ
        "uni0282": "glyph990",  # ʂ
        "uni0283": "glyph981",  # ʃ
        "uni0284": "glyph1010",  # ʄ
        "uni0288": "glyph986",  # ʈ
        "uni0289": "glyph1016",  # ʉ
        "uni028A": "glyph1024",  # ʊ
        "uni028B": "glyph979",  # ʋ
        "uni028C": "glyph1026",  # ʌ
        "uni028D": "glyph1030",  # ʍ
        "uni028E": "glyph997",  # ʎ
        "uni0290": "glyph991",  # ʐ
        "uni0291": "glyph1035",  # ʑ
        "uni0292": "glyph982",  # ʒ
        "uni0294": "glyph1004",  # ʔ
        "uni0295": "glyph1003",  # ʕ
        "uni0298": "glyph1006",  # ʘ
        "uni029D": "glyph996",  # ʝ
        "uni02A1": "glyph1033",  # ʡ
        "uni02A2": "glyph1032",  # ʢ
        "uni02C6": "glyph1055",  # ˆ
        "uni02C7": "glyph926",  # ˇ
        "uni02C8": "glyph1045",  # ˈ
        "uni02CC": "glyph1069",  # ˌ
        "uni02D0": "glyph1047",  # ː
        "uni02D1": "glyph1048",  # ˑ
        "uni02D4": "glyph1076",  # ˔
        "uni02D5": "glyph1077",  # ˕
        "uni02D6": "glyph1065",  # ˖
        "uni02D7": "glyph1066",  # ˗
        "uni02D8": "glyph911",  # ˘
        "uni02D9": "glyph965",  # ˙
        "uni02DB": "glyph922",  # ˛
        "uni02DC": "glyph1083",  # ˜
        "uni02DD": "glyph931",  # ˝
        "uni02DE": "glyph1071",  # ˞
        "uni02E5": "glyph1056",  # ˥
        "uni02E6": "glyph1057",  # ˦
        "uni02E7": "glyph1058",  # ˧
        "uni02E8": "glyph1059",  # ˨
        "uni02E9": "glyph1060",  # ˩
        "uni0300": "glyph1307",  # ̀
        "uni0301": "glyph1052",  # ́
        "uni0302": "glyph1055",  # ̂
        "uni0303": "glyph1083",  # ̃
        "uni0304": "glyph825",  # ̄
        "uni0305": "glyph826",  # ̅
        "uni0306": "glyph1049",  # ̆
        "uni0308": "glyph1067",  # ̈
        "uni030B": "glyph1051",  # ̋
        "uni030C": "glyph1054",  # ̌
        "uni030F": "glyph1053",  # ̏
        "uni0318": "glyph1078",  # ̘
        "uni0319": "glyph1079",  # ̙
        "uni031A": "glyph1084",  # ̚
        "uni031C": "glyph1064",  # ̜
        "uni031D": "glyph1076",  # ̝
        "uni031E": "glyph1077",  # ̞
        "uni031F": "glyph1065",  # ̟
        "uni0320": "glyph1066",  # ̠
        "uni0324": "glyph1072",  # ̤
        "uni0325": "glyph1061",  # ̥
        "uni0329": "glyph1046",  # ̩
        "uni032A": "glyph1080",  # ̪
        "uni032C": "glyph1062",  # ̬
        "uni032F": "glyph1070",  # ̯
        "uni0330": "glyph1073",  # ̰
        "uni0334": "glyph1075",  # ̴
        "uni0339": "glyph1063",  # ̹
        "uni033A": "glyph1081",  # ̺
        "uni033B": "glyph1082",  # ̻
        "uni033C": "glyph1074",  # ̼
        "uni033D": "glyph1068",  # ̽
        "uni1E3E": "glyph806",  # Ḿ
        "uni1E3F": "glyph807",  # ḿ
        "uni1F70": "glyph1040",  # ὰ
        "uni1F71": "glyph1041",  # ά
        "uni1F72": "glyph1042",  # ὲ
        "uni1F73": "glyph1043",  # έ
        "uni2010": "glyph1252",  # ‐
        "uni2018": "glyph12882",  # `
        "uni2019": "glyph12881",  # '
        "uni201C": "glyph12950",  # “
        "uni201D": "glyph12880",  # "
        "uni2022": "glyph311",  # •
        "uni203C": "glyph799",  # ‼
        "uni203F": "glyph1050",  # ‿
        "uni2042": "glyph1169",  # ⁂
        "uni2047": "glyph800",  # ⁇
        "uni2048": "glyph801",  # ⁈
        "uni2049": "glyph802",  # ⁉
        "uni20AC": "glyph817",  # €
        "uni210F": "glyph340",  # ℏ
        "uni2113": "glyph342",  # ℓ
        "uni2127": "glyph343",  # ℧
        "uni2135": "glyph339",  # ℵ
        "uni2153": "glyph726",  # ⅓
        "uni2154": "glyph727",  # ⅔
        "uni2155": "glyph728",  # ⅕
        "uni2194": "glyph266",  # ↔
        "uni2196": "glyph286",  # ↖
        "uni2197": "glyph284",  # ↗
        "uni2198": "glyph285",  # ↘
        "uni2199": "glyph287",  # ↙
        "uni21C4": "glyph288",  # ⇄
        "uni2500": "glyph12918",  # ─
        "uni2501": "glyph12919",  # ━
        "uni2502": "glyph12920",  # │
        "uni2503": "glyph12921",  # ┃
        "uni250C": "glyph12922",  # ┌
        "uni250F": "glyph12923",  # ┏
        "uni2510": "glyph12924",  # ┐
        "uni2513": "glyph12925",  # ┓
        "uni2514": "glyph12926",  # └
        "uni2517": "glyph12927",  # ┗
        "uni2518": "glyph12928",  # ┘
        "uni251B": "glyph12929",  # ┛
        "uni251C": "glyph12930",  # ├
        "uni251D": "glyph12931",  # ┝
        "uni2520": "glyph12932",  # ┠
        "uni2523": "glyph12933",  # ┣
        "uni2524": "glyph12934",  # ┤
        "uni2525": "glyph12935",  # ┥
        "uni2528": "glyph12936",  # ┨
        "uni252B": "glyph12937",  # ┫
        "uni252C": "glyph12938",  # ┬
        "uni252F": "glyph12939",  # ┯
        "uni2530": "glyph12940",  # ┰
        "uni2533": "glyph12941",  # ┳
        "uni2534": "glyph12942",  # ┴
        "uni2537": "glyph12943",  # ┷
        "uni2538": "glyph12944",  # ┸
        "uni253B": "glyph12945",  # ┻
        "uni253C": "glyph12946",  # ┼
        "uni253F": "glyph12947",  # ┿
        "uni2542": "glyph12948",  # ╂
        "uni254B": "glyph12949",  # ╋
        "uni25E6": "glyph310",  # ◦
        "uni3002": "uniFF61",  # ｡
        "uni3008": "glyph12953",  # 〈
        "uni3009": "glyph12954",  # 〉
        "uni300A": "glyph12955",  # 《
        "uni300B": "glyph12956",  # 》
        "uni300C": "uniFF62",  # ｢
        "uni300D": "uniFF63",  # ｣
        "uni300E": "glyph12957",  # 『
        "uni300F": "glyph12958",  # 』
        "uni3010": "glyph12959",  # 【
        "uni3011": "glyph12960",  # 】
        "uni3014": "glyph12951",  # 〔
        "uni3015": "glyph12952",  # 〕
        "uni301C": "glyph13048",  # 〜
        "uni301D": "glyph12916",  # 〝
        "uni301E": "glyph12917",  # 〞
        "uni302E": "uniFF65",  # 〮
        "uni3092": "glyph12963",  # を
        "uni3041": "glyph12964",  # ぁ
        "uni3043": "glyph12965",  # ぃ
        "uni3045": "glyph12966",  # ぅ
        "uni3047": "glyph12967",  # ぇ
        "uni3049": "glyph12968",  # ぉ
        "uni3083": "glyph12969",  # ゃ
        "uni3085": "glyph12970",  # ゅ
        "uni3087": "glyph12971",  # ょ
        "uni3063": "glyph12972",  # っ
        "uni3042": "glyph12973",  # あ
        "uni3044": "glyph12974",  # い
        "uni3046": "glyph12975",  # う
        "uni3048": "glyph12976",  # え
        "uni304A": "glyph12977",  # お
        "uni304B": "glyph12978",  # か
        "uni304D": "glyph12979",  # き
        "uni304F": "glyph12980",  # く
        "uni3051": "glyph12981",  # け
        "uni3053": "glyph12982",  # こ
        "uni3055": "glyph12983",  # さ
        "uni3057": "glyph12984",  # し
        "uni3059": "glyph12985",  # す
        "uni305B": "glyph12986",  # せ
        "uni305D": "glyph12987",  # そ
        "uni305F": "glyph12988",  # た
        "uni3061": "glyph12989",  # ち
        "uni3064": "glyph12990",  # つ
        "uni3066": "glyph12991",  # て
        "uni3068": "glyph12992",  # と
        "uni306A": "glyph12993",  # な
        "uni306B": "glyph12994",  # に
        "uni306C": "glyph12995",  # ぬ
        "uni306D": "glyph12996",  # ね
        "uni306E": "glyph12997",  # の
        "uni306F": "glyph12998",  # は
        "uni3072": "glyph12999",  # ひ
        "uni3075": "glyph13000",  # ふ
        "uni3078": "glyph13001",  # へ
        "uni307B": "glyph13002",  # ほ
        "uni307E": "glyph13003",  # ま
        "uni307F": "glyph13004",  # み
        "uni3080": "glyph13005",  # む
        "uni3081": "glyph13006",  # め
        "uni3082": "glyph13007",  # も
        "uni3084": "glyph13008",  # や
        "uni3086": "glyph13009",  # ゆ
        "uni3088": "glyph13010",  # よ
        "uni3089": "glyph13011",  # ら
        "uni308A": "glyph13012",  # り
        "uni308B": "glyph13013",  # る
        "uni308C": "glyph13014",  # れ
        "uni308D": "glyph13015",  # ろ
        "uni308F": "glyph13016",  # わ
        "uni3093": "glyph13017",  # ん
        "uni3090": "glyph13018",  # ゐ
        "uni3091": "glyph13019",  # ゑ
        "uni308E": "glyph13020",  # ゎ
        "uni304C": "glyph13021",  # が
        "uni304E": "glyph13022",  # ぎ
        "uni3050": "glyph13023",  # ぐ
        "uni3052": "glyph13024",  # げ
        "uni3054": "glyph13025",  # ご
        "uni3056": "glyph13026",  # ざ
        "uni3058": "glyph13027",  # じ
        "uni305A": "glyph13028",  # ず
        "uni305C": "glyph13029",  # ぜ
        "uni305E": "glyph13030",  # ぞ
        "uni3060": "glyph13031",  # だ
        "uni3062": "glyph13032",  # ぢ
        "uni3065": "glyph13033",  # づ
        "uni3067": "glyph13034",  # で
        "uni3069": "glyph13035",  # ど
        "uni3070": "glyph13036",  # ば
        "uni3071": "glyph13037",  # ぱ
        "uni3073": "glyph13038",  # び
        "uni3074": "glyph13039",  # ぴ
        "uni3076": "glyph13040",  # ぶ
        "uni3077": "glyph13041",  # ぷ
        "uni3079": "glyph13042",  # べ
        "uni307A": "glyph13043",  # ぺ
        "uni307C": "glyph13044",  # ぼ
        "uni307D": "glyph13045",  # ぽ
        "uni3099": "uniFF9E",  # ゙
        "uni309A": "uniFF9F",  # ゚
        "uni309B": "uniFF9E",  # ﾞ
        "uni309C": "uniFF9F",  # ﾟ
        "uni30FB": "uniFF65",  # ･
        "uni30F2": "uniFF66",  # ｦ
        "uni30A1": "glyphFF67",  # ｧ
        "uni30A3": "glyphFF68",  # ｨ
        "uni30A5": "glyphFF69",  # ｩ
        "uni30A7": "glyphFF6A",  # ｪ
        "uni30A9": "glyphFF6B",  # ｫ
        "uni30E3": "glyphFF6C",  # ｬ
        "uni30E5": "glyphFF6D",  # ｭ
        "uni30E7": "glyphFF6E",  # ｮ
        "uni30C3": "glyphFF6F",  # ｯ
        "uni30FC": "uniFF70",  # ｰ
        "uni30A2": "glyphFF71",  # ｱ
        "uni30A4": "glyphFF72",  # ｲ
        "uni30A6": "glyphFF73",  # ｳ
        "uni30A8": "glyphFF74",  # ｴ
        "uni30AA": "glyphFF75",  # ｵ
        "uni30AB": "glyphFF76",  # ｶ
        "uni30AD": "glyphFF77",  # ｷ
        "uni30AF": "glyphFF78",  # ｸ
        "uni30B1": "glyphFF79",  # ｹ
        "uni30B3": "glyphFF7A",  # ｺ
        "uni30B5": "glyphFF7B",  # ｻ
        "uni30B7": "glyphFF7C",  # ｼ
        "uni30B9": "glyphFF7D",  # ｽ
        "uni30BB": "glyphFF7E",  # ｾ
        "uni30BD": "glyphFF7F",  # ｿ
        "uni30BF": "glyphFF80",  # ﾀ
        "uni30C1": "glyphFF81",  # ﾁ
        "uni30C4": "glyphFF82",  # ﾂ
        "uni30C6": "glyphFF83",  # ﾃ
        "uni30C8": "glyphFF84",  # ﾄ
        "uni30CA": "glyphFF85",  # ﾅ
        "uni30CB": "glyphFF86",  # ﾆ
        "uni30CC": "glyphFF87",  # ﾇ
        "uni30CD": "glyphFF88",  # ﾈ
        "uni30CE": "glyphFF89",  # ﾉ
        "uni30CF": "glyphFF8A",  # ﾊ
        "uni30D2": "glyphFF8B",  # ﾋ
        "uni30D5": "glyphFF8C",  # ﾌ
        "uni30D8": "glyphFF8D",  # ﾍ
        "uni30DB": "glyphFF8E",  # ﾎ
        "uni30DE": "glyphFF8F",  # ﾏ
        "uni30DF": "glyphFF90",  # ﾐ
        "uni30E0": "glyphFF91",  # ﾑ
        "uni30E1": "glyphFF92",  # ﾒ
        "uni30E2": "glyphFF93",  # ﾓ
        "uni30E4": "glyphFF94",  # ﾔ
        "uni30E6": "glyphFF95",  # ﾕ
        "uni30E8": "glyphFF96",  # ﾖ
        "uni30E9": "glyphFF97",  # ﾗ
        "uni30EA": "glyphFF98",  # ﾘ
        "uni30EB": "glyphFF99",  # ﾙ
        "uni30EC": "glyphFF9A",  # ﾚ
        "uni30ED": "glyphFF9B",  # ﾛ
        "uni30EF": "glyphFF9C",  # ﾜ
        "uni30F3": "glyphFF9D",  # ﾝ
        "uni30EE": "glyph12886",  # ヮ
        "uni30F0": "glyph12884",  # ヰ
        "uni30F1": "glyph12885",  # ヱ
        "uni30AC": "glyph12890",  # ｶﾞ
        "uni30AE": "glyph12891",  # ｷﾞ
        "uni30B0": "glyph12892",  # ｸﾞ
        "uni30B2": "glyph12893",  # ｹﾞ
        "uni30B4": "glyph12894",  # ｺﾞ
        "uni30B6": "glyph12895",  # ｻﾞ
        "uni30B8": "glyph12896",  # ｼﾞ
        "uni30BA": "glyph12897",  # ｽﾞ
        "uni30BC": "glyph12898",  # ｾﾞ
        "uni30BE": "glyph12899",  # ｿﾞ
        "uni30C0": "glyph12900",  # ﾀﾞ
        "uni30C2": "glyph12901",  # ﾁﾞ
        "uni30C5": "glyph12902",  # ﾂﾞ
        "uni30C7": "glyph12903",  # ﾃﾞ
        "uni30C9": "glyph12904",  # ﾄﾞ
        "uni30D0": "glyph12905",  # ﾊﾞ
        "uni30D1": "glyph12906",  # ﾊﾟ
        "uni30D3": "glyph12907",  # ﾋﾞ
        "uni30D4": "glyph12908",  # ﾋﾟ
        "uni30D6": "glyph12909",  # ﾌﾞ
        "uni30D7": "glyph12910",  # ﾌﾟ
        "uni30D9": "glyph12911",  # ﾍﾞ
        "uni30DA": "glyph12912",  # ﾍﾟ
        "uni30DC": "glyph12913",  # ﾎﾞ
        "uni30DD": "glyph12914",  # ﾎﾟ
        "uni30F4": "glyph12889",  # ヴ
        "uni30F5": "glyph12887",  # ヵ
        "uni30F6": "glyph12888",  # ヶ
        "uniFF01": "glyph3",  # !
        "uniFF02": "glyph4",  # "
        "uniFF03": "glyph5",  # #
        "uniFF04": "glyph6",  # $
        "uniFF05": "glyph7",  # %
        "uniFF06": "glyph8",  # &
        "uniFF07": "glyph9",  # '
        "uniFF08": "glyph10",  # (
        "uniFF09": "glyph11",  # )
        "uniFF0A": "glyph12",  # *
        "uniFF0B": "glyph13",  # +
        "uniFF0C": "glyph14",  # ,
        "uniFF0D": "glyph15",  # -
        "uniFF0E": "glyph16",  # .
        "uniFF0F": "glyph17",  # /
        "uniFF10": "glyph18",  # 0
        "uniFF11": "glyph19",  # 1
        "uniFF12": "glyph20",  # 2
        "uniFF13": "glyph21",  # 3
        "uniFF14": "glyph22",  # 4
        "uniFF15": "glyph23",  # 5
        "uniFF16": "glyph24",  # 6
        "uniFF17": "glyph25",  # 7
        "uniFF18": "glyph26",  # 8
        "uniFF19": "glyph27",  # 9
        "uniFF1A": "glyph28",  # :
        "uniFF1B": "glyph29",  # ;
        "uniFF1C": "glyph30",  # <
        "uniFF1D": "glyph31",  # =
        "uniFF1E": "glyph32",  # >
        "uniFF1F": "glyph33",  # ?
        "uniFF20": "glyph34",  # @
        "uniFF21": "glyph35",  # A
        "uniFF22": "glyph36",  # B
        "uniFF23": "glyph37",  # C
        "uniFF24": "glyph38",  # D
        "uniFF25": "glyph39",  # E
        "uniFF26": "glyph40",  # F
        "uniFF27": "glyph41",  # G
        "uniFF28": "glyph42",  # H
        "uniFF29": "glyph43",  # I
        "uniFF2A": "glyph44",  # J
        "uniFF2B": "glyph45",  # K
        "uniFF2C": "glyph46",  # L
        "uniFF2D": "glyph47",  # M
        "uniFF2E": "glyph48",  # N
        "uniFF2F": "glyph49",  # O
        "uniFF30": "glyph50",  # P
        "uniFF31": "glyph51",  # Q
        "uniFF32": "glyph52",  # R
        "uniFF33": "glyph53",  # S
        "uniFF34": "glyph54",  # T
        "uniFF35": "glyph55",  # U
        "uniFF36": "glyph56",  # V
        "uniFF37": "glyph57",  # W
        "uniFF38": "glyph58",  # X
        "uniFF39": "glyph59",  # Y
        "uniFF3A": "glyph60",  # Z
        "uniFF3B": "glyph61",  # [
        "uniFF3C": "glyph62",  # \
        "uniFF3D": "glyph63",  # ]
        "uniFF3E": "glyph64",  # ^
        "uniFF3F": "glyph65",  # _
        "uniFF40": "glyph66",  # `
        "uniFF41": "glyph67",  # a
        "uniFF42": "glyph68",  # b
        "uniFF43": "glyph69",  # c
        "uniFF44": "glyph70",  # d
        "uniFF45": "glyph71",  # e
        "uniFF46": "glyph72",  # f
        "uniFF47": "glyph73",  # g
        "uniFF48": "glyph74",  # h
        "uniFF49": "glyph75",  # i
        "uniFF4A": "glyph76",  # j
        "uniFF4B": "glyph77",  # k
        "uniFF4C": "glyph78",  # l
        "uniFF4D": "glyph79",  # m
        "uniFF4E": "glyph80",  # n
        "uniFF4F": "glyph81",  # o
        "uniFF50": "glyph82",  # p
        "uniFF51": "glyph83",  # q
        "uniFF52": "glyph84",  # r
        "uniFF53": "glyph85",  # s
        "uniFF54": "glyph86",  # t
        "uniFF55": "glyph87",  # u
        "uniFF56": "glyph88",  # v
        "uniFF57": "glyph89",  # w
        "uniFF58": "glyph90",  # x
        "uniFF59": "glyph91",  # y
        "uniFF5A": "glyph92",  # z
        "uniFF5B": "glyph93",  # {
        "uniFF5C": "glyph94",  # |
        "uniFF5D": "glyph95",  # }
        "uniFF5E": "glyph96"  # ~
    }

    # グリフ名がリストにあるかチェック
    o_glyphname = glyph.glyphname
    if o_glyphname in swaplist_set:
        s_glyphname = swaplist_set[o_glyphname]
        # グリフの置換を実施して成功・失敗のフラグを返す
        flag = ys_swap_glyph(font, glyph, o_glyphname, s_glyphname)
        return flag

    # リストに一致しないなら何もせずにFalseを返す
    else:
        return False


if __name__ == "__main__":
    ys_swaplist(font, glyph)
