#!fontforge --lang=py -script
import configparser
import logging
import os
import sys
import gc

import fontforge
import psMat
import math

from utils import ys_repair_Self_Insec, ys_rm_little_line, ys_rm_small_poly
from utils import ys_closepath, ys_repair_si_chain, ys_rescale_chain, ys_simplify
from utils import ys_widestroke
from bz_narow_set import shorten_style_rd, write_property

# コマンドライン引数の処理
if len(sys.argv) < 4:
    print("Usage: script.py <input_fontstyles> <output_name> <vshrink_ratio>", flush=True)
    sys.exit(1)    
try:
    INPUT_FONTSTYLES = sys.argv[1]  # 入力ファイル
    OUTPUT_NAME = sys.argv[2]  # 出力ファイル
    # OUTPUT_NAME = f"{OUTPUT_NAME}"  # 出力ファイルの形式 ゴミかも？　あとで消す。
    VSHRINK_RATIO = float(sys.argv[3])  # 横に縮める比率（数値に変換）
except ValueError:
    print("Error: <stroke_width> and <VSHRINK_RATIO> must be numbers.", flush=True)
    sys.exit(1)

# カレントディレクトリを保存する
current_dir = os.getcwd()

# 一旦、情報収集のためにスクリプトの場所をカレントディレクトリに設定する。
this_script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_script_dir)

# 設定ファイルの名前は自分の名前の拡張子違い
this_script_name = os.path.basename(__file__)  # 現在のスクリプト名を取得
ini_name = os.path.splitext(this_script_name)[0] + ".ini"  # 拡張子を .ini に変更
ini_path = os.path.join(this_script_dir, ini_name)

# 設定ファイルを読み込む
settings = configparser.ConfigParser()
settings.read(ini_path, encoding="utf-8")

FFSCR = settings.get("DEFAULT", "ffscr")
SOURCE_FONTS_DIR = settings.get("DEFAULT", "Source_Fonts_Dir")
BUILD_FONTS_DIR  = settings.get("DEFAULT", "Build_Fonts_Dir")
STROKE_WIDTH_SF  = float(settings.get("DEFAULT", "Stroke_Width_SF"))
STROKE_WIDTH_MIN = float(settings.get("DEFAULT", "Stroke_Width_Min"))
STOROKE_HEIGHT   = float(settings.get("DEFAULT", "Storoke_Height"))
STRWR_WEIGHT_HI  = float(settings.get("DEFAULT", "StrWR_Weight_Hi"))
STRWR_WEIGHT_LO  = float(settings.get("DEFAULT", "StrWR_Weight_Lo"))
STRWR_POINTS_HI  = float(settings.get("DEFAULT", "StrWR_Points_Hi"))
STRWR_POINTS_LO  = float(settings.get("DEFAULT", "StrWR_Points_Lo"))
REDUCE_RATIO_HI  = float(settings.get("DEFAULT", "Reduce_Ratio_Hi"))
REDUCE_RATIO_LO  = float(settings.get("DEFAULT", "Reduce_Ratio_Lo"))

PRESAVE_INTERVAL = int(settings.get("DEFAULT", "Presave_Interval"))
IS_PROPORTIONAL_CUTOFF_VARIANCE = int(settings.get("DEFAULT", "is_proportional_cutoff_variance"))
PROPOTIONAL_SIDEBEARING_DIVISOR  = float(settings.get("DEFAULT", "propotional_sidebearing_divisor"))

# main関数内でlocal_setup_logger(OUTPUT_NAME) 使って設定。
logger = logging.getLogger()

class StreamToLogger:  # 書き込みをロガーに転送するクラス。
    def __init__(self, logger, log_level=logging.WARNING):
        self.logger = logger
        self.log_level = log_level
        self.buffer = ''
    def write(self, message):
        # メッセージを行ごとに分割してロガーに送信
        for line in message.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
    def flush(self):
        pass  # バッファのフラッシュは不要

def local_setup_logger(OUTPUT_NAME):
    global logger  # グローバルでロガーの設定をする。
    logger = logging.getLogger("custom_logger")
    logger.setLevel(logging.DEBUG)  # 全てのログを記録対象にする
    # ログファイルの記録先
    Log_file_path = os.path.join(BUILD_FONTS_DIR, f"{OUTPUT_NAME}.log")
    # ファイルハンドラ: INFO以上をファイルに記録
    file_handler = logging.FileHandler(Log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
    logger.addHandler(file_handler)
    # コンソールハンドラ: INFO以下を通常出力（標準出力）
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.addFilter(lambda record: record.levelno < logging.WARNING)
    stdout_handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
    logger.addHandler(stdout_handler)
    # コンソールハンドラ: WARNING以上をエラー出力（標準エラー出力）
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
    logger.addHandler(stderr_handler)
    return logger

def setup():
    os.makedirs(BUILD_FONTS_DIR, exist_ok=True)  # 作業用のディレクトリを作成
    logger = local_setup_logger(OUTPUT_NAME)  # ログ出力の設定
    # 読み込むフォントのディレクトリまで確定させる
    input_fontname = shorten_style_rd(INPUT_FONTSTYLES)[0]
    input_fontfile = os.path.join(SOURCE_FONTS_DIR, input_fontname)
    print (f"\r input_fontfile \r", end=" ", flush=True)
    font = fontforge.open(input_fontfile)  # フォントを開く
    #一通り情報を集め終わったので元のカレントディレクトリに戻る
    os.chdir(current_dir)
    # 一時ファイル名を付けてパスを確認
    temp_file = f"{OUTPUT_NAME}_temp_0.sfd"
    temp_file_path = os.path.join(BUILD_FONTS_DIR, temp_file)
    del_file = temp_file  # あとで消す時用
    return font, del_file, temp_file, temp_file_path

def save_and_open(font, filepath):
    print(f"\r 保存して開きなおす。file: {filepath}", end=" ", flush=True)
    font.save(filepath)
    font.close()
    font = fontforge.open(filepath)
    print(f"\r 開きなおした file: {filepath}", end=" ", flush=True)
    sys.stdout = sys.__stdout__  # 標準出力が狂うかもなので一応初期化。
    return font

def isprop(font):
    # ASCII範囲に基づいてフォントがプロポーショナルかを判定
    widths = set()  # 空のセットを初期化
    for i in range(32, 127):  # ASCII範囲をループ
        char = chr(i)
        if char in font:  # グリフが存在するか確認
            glyph = font[char]
            if hasattr(glyph, "width"):  # 幅の属性があるか検証
                widths.add(glyph.width)  # 幅をセットに追加
    # 幅のバリエーション数が閾値以上ならプロポーショナル
    if len(widths) >= IS_PROPORTIONAL_CUTOFF_VARIANCE:
        style_is_prop = True
    else:
        style_is_prop = False
    return style_is_prop

def Local_snapshot_sfd (font, glyph, proc_cnt, del_file):
    try:
    # savefreq個処理してたら一旦保存
        if proc_cnt % PRESAVE_INTERVAL == 1:
            print(f"\r 作業前保存中のグリフ： {glyph.glyphname} \r", end=" ", flush=True)
            temp_file = f"{OUTPUT_NAME}_temp_{proc_cnt}.sfd"
            temp_file_path = os.path.join(BUILD_FONTS_DIR, temp_file)
            font.save(temp_file_path)
            # 前回の仮保存ファイルを削除
            print(f"\r 前の一時ファイルを削除： {del_file} \r", end=" ", flush=True)
            del_file_path = os.path.join(BUILD_FONTS_DIR, del_file)
            os.remove(del_file_path)
            # 次の削除対象ファイル名を保存
            del_file = temp_file
            # ついでにログもフラッシュしておく。
            for handler in logging.getLogger().handlers:
                if hasattr(handler, 'flush'):
                    handler.flush()
            gc.collect()  # ガベージコレクションの実行
    except IOError as e:
        print(f"保存か削除に失敗したかも？　多分削除に……： {del_file} \r", flush=True)
    return del_file

def is_halfwidth(glyph, em_size):
    # グリフ幅がジャスト半分ならそのことを覚えておく
    if glyph.width ==  em_size / 2:
        halfwidth_glyph_flag = True
    else :
        halfwidth_glyph_flag = False
    return halfwidth_glyph_flag

def custom_stroke_width(glyph, font_weight, base_stroke_width):
    # フォントウエイトと確認中グリフのポイント数を勘案してストロークの幅を変える
    point_count = sum(len(contour) for contour in glyph.layers["Fore"])
    if point_count > STRWR_POINTS_HI or font_weight > STRWR_WEIGHT_HI:
        stroke_width = round(base_stroke_width * REDUCE_RATIO_HI)
    elif point_count > STRWR_POINTS_LO and font_weight > STRWR_WEIGHT_LO:
        stroke_width = round(base_stroke_width * REDUCE_RATIO_LO)
    else :
        stroke_width = base_stroke_width
    return point_count, stroke_width

def upscale(glyph):
    glyph.transform((1, 0, 0, 8, 0, 0))
    glyph.addExtrema("all") # 極点を追加

def downscale(glyph):
    glyph.transform((1, 0, 0, 0.125, 0, 0))
    glyph.addExtrema("all")

def anomality_repair(glyph):
    # 加工後は何かしらの異常が発生するので修復を試みる
    glyph.round()  # 整数化
    glyph.removeOverlap()
    if glyph.validate(1) & 0x01:  # 開いたパスがある場合
        ys_closepath(glyph)
    glyph.simplify(0.1) # 単純化
    ys_repair_Self_Insec(glyph, 2)  # 自己交差の修復試行&ツノ折り
    glyph.round()
    glyph.removeOverlap()
    glyph.addExtrema("all")

def shapeup_outline(glyph, em_size, stroke_width):
    # 幅のストロークで太ったアウトラインを引き締める。
    # サイドベアリングを弄りたくないので拡大縮小の原点はグリフの中心にする。
    # グリフの幅まで変わると困るのでレイヤー単位で操作
    bbox = glyph.boundingBox()
    xmin, ymin, xmax, ymax = bbox  # グリフの大きさを取得
    xcenter = xmin + (xmax - xmin) / 2
    stroke_shrink = 1 - (stroke_width / em_size)
    glyph.foreground.transform((1, 0, 0, 1, -xcenter, 0))
    glyph.foreground.transform((stroke_shrink, 0, 0, 1, 0, 0))
    glyph.foreground.transform((1, 0, 0, 1, xcenter, 0))
    glyph.addExtrema("all")

def vshrink(glyph):
    # 指定の縮小率に従って縦横比変更
    glyph.transform((VSHRINK_RATIO, 0, 0, 1, 0, 0))
    glyph.addExtrema("all")

def monospacewidth(glyph, style_is_prop, halfwidth_glyph_flag, em_size):
    # 半角フォントのグリフ幅を設定する(念の為って性格が強い)
    if not style_is_prop:
        if halfwidth_glyph_flag:
            glyph.width = round(em_size / 2 * VSHRINK_RATIO)
        else:
            glyph.width = round(em_size * VSHRINK_RATIO)

def finish_optimise(glyph):
    # 最後にTTFの仕様に合わせた最適化を実施
    if glyph.validate(1) & 0x01:  # 開いたパスがある場合
        ys_repair_si_chain(glyph, proc_cnt)  # 自己交差の修復試行&ツノ折り(パスも閉じてくれるし)
    glyph.round()
    glyph.simplify()
    ys_repair_Self_Insec(glyph, 1)
    glyph.round()
    glyph.removeOverlap()
    glyph.round()
    glyph.addExtrema("all")

def Local_validate_notice(glyph, note, loglevel):
    log_func = getattr(logger, loglevel, None)  # 動的にログレベルを取得
    if glyph.validate(1) & 0x01:  # 開いたパスがある
        log_func(f"{note}のグリフ '{glyph.glyphname}' に開いたパス")
    if glyph.validate(1) & 0x02:  # 外側に時計回のパスがある
        logger.info(f"{note}のグリフ '{glyph.glyphname}' の外側に時計回りのパス")
    if glyph.validate(1) & 0x04:  # 交差がある
        logger.info(f"{note}のグリフ '{glyph.glyphname}' に交差がある")
    if glyph.validate(1) & 0x08:  # 参照が不正
        logger.info(f"{note}のグリフ '{glyph.glyphname}' の参照が不正")
    if glyph.validate(1) & 0x10:  # ヒントが不正
        logger.info(f"{note}のグリフ '{glyph.glyphname}' のヒントが不正")
    if glyph.validate(1) & 0x20:  # 自己交差がある
        log_func(f"{note}のグリフ '{glyph.glyphname}' に自己交差がある")
    if glyph.validate(1) & 0x40:  # その他のエラーがある
        log_func(f"{note}後のグリフ '{glyph.glyphname}' にその他のエラー")



######################################################################
#                             メイン関数                             #
######################################################################
def main():
    font, del_file, temp_file, temp_file_path = setup()  # セットアップ
    font = save_and_open(font, temp_file_path)  # SFDに変えて開き直し
    style_is_prop = isprop(font)  # プロポーショナルか判定
    font_weight = font.os2_weight  # フォントの元情報を把握
    em_size = font.em  # ↓矢印ストローク幅のセッティング
    base_stroke_width = STROKE_WIDTH_MIN + STROKE_WIDTH_SF * (1 - VSHRINK_RATIO)
    proc_cnt: int = 0  # カウンタをセット
    # フォントのプロパティを書き換える
    write_property(ini_name, INPUT_FONTSTYLES, VSHRINK_RATIO, font)

    for glyph in font.glyphs():  # 全グリフをループ処理
        if not glyph.isWorthOutputting():
            print(f"\r 出力しないグリフをスキップ： {glyph.glyphname}", end=" ", flush=True)
            continue
        if len(glyph.references) > 0:
            print(f"\r 合成グリフをスキップ： {glyph.glyphname}", end=" ", flush=True)
            continue
        ep = True
        if glyph.glyphname == ["uni2756"]:  ep = False  #   ❖  10070   2756
        if glyph.glyphname == ["uni2776"]:  ep = False  #   ❶  10102   2776
        if glyph.glyphname == ["uni2777"]:  ep = False  #   ❷  10103   2777
        if glyph.glyphname == ["uni2778"]:  ep = False  #   ❸  10104   2778
        if glyph.glyphname == ["uni2779"]:  ep = False  #   ❹  10105   2779
        if glyph.glyphname == ["uni277A"]:  ep = False  #   ❺  10106   277A
        if glyph.glyphname == ["uni277B"]:  ep = False  #   ❻  10107   277B
        if glyph.glyphname == ["uni277C"]:  ep = False  #   ❼  10108   277C
        if glyph.glyphname == ["uni277D"]:  ep = False  #   ❽  10109   277D
        if glyph.glyphname == ["uni277E"]:  ep = False  #   ❾  10110   277E
        if glyph.glyphname == ["uni277F"]:  ep = False  #   ❿  10111   277F
        if glyph.glyphname == ["uni24EB"]:  ep = False  #   ⓫  9451    24EB
        if glyph.glyphname == ["uni24EC"]:  ep = False  #   ⓬  9452    24EC
        if glyph.glyphname == ["uni24ED"]:  ep = False  #   ⓭  9453    24ED
        if glyph.glyphname == ["uni24EE"]:  ep = False  #   ⓮  9454    24EE
        if glyph.glyphname == ["uni24EF"]:  ep = False  #   ⓯  9455    24EF
        if glyph.glyphname == ["uni24F0"]:  ep = False  #   ⓰  9456    24F0
        if glyph.glyphname == ["uni24F1"]:  ep = False  #   ⓱  9457    24F1
        if glyph.glyphname == ["uni24F2"]:  ep = False  #   ⓲  9458    24F2
        if glyph.glyphname == ["uni24F3"]:  ep = False  #   ⓳  9459    24F3
        if glyph.glyphname == ["uni24F4"]:  ep = False  #   ⓴  9460    24F4
        
        print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Start processing          ", end=" ", flush=True)
        # glyph.background = glyph.foreground  # バックグラウンドにグリフをコピー
        proc_cnt += 1  # 処理中グリフのカウントアップ
        del_file = Local_snapshot_sfd(font, glyph, proc_cnt, del_file)  # 中途保存
        halfwidth_glyph_flag = is_halfwidth(glyph, em_size)  # グリフ幅のチェック
        point_count, stroke_width = custom_stroke_width(glyph, font_weight, base_stroke_width)
        print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Point Count {point_count:<6}        ", end=" ", flush=True)
        upscale(glyph)  # 縦に拡大する
        print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Wider stroke              \r", end=" ", flush=True)
        if ep:
            ys_widestroke(glyph, stroke_width, STOROKE_HEIGHT)  # 拡幅処理
        downscale(glyph)  # 幅を縮小＆最初に縦に伸ばした奴を元に戻す
        print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Anomality Repair          \r", end=" ", flush=True)
        anomality_repair(glyph)
        print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Anomality Repair Plus     \r", end=" ", flush=True)
        if glyph.validate(1) & 0x22: ys_rescale_chain(glyph) # 変形、精度劣化を伴う修復試行を行う。
        print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Overflow treatment        \r", end=" ", flush=True)
        if ep:
            shapeup_outline(glyph, em_size, stroke_width)  # アウトラインの引き締め
        vshrink(glyph)  # 指定の縮小率に従って縦横比変更
        print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Half-width processing     ", end=" ", flush=True)
        monospacewidth(glyph, style_is_prop, halfwidth_glyph_flag, em_size)
        print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Finish optimization       \r", end=" ", flush=True)
        finish_optimise(glyph)
        # Local_validate_notice(glyph, "仕上げ処理後", "warning")  # 仕上げ後の検査(デバッグ用)
        print(f"\r now:{proc_cnt:<5}:{glyph.glyphname:<15} Process Completed!        ", end=" ", flush=True)
    ######################################################################
    #                    各グリフのループ処理ここまで                    #
    ######################################################################
    try:
        # SFDファイルの保存
        output_sfd = f"{OUTPUT_NAME}.sfd"
        output_sfd_path = os.path.join(BUILD_FONTS_DIR, output_sfd)
        print(f"\r 完成したフォントを保存： {output_sfd_path} \r", end=" ", flush=True)
        font.save(output_sfd_path)  # SFD形式で保存
        
        # TTFファイルの保存
        output_ttf = f"{OUTPUT_NAME}.ttf"
        output_ttf_path = os.path.join(BUILD_FONTS_DIR, output_ttf)
        print(f"\r 完成したフォントを保存： {output_ttf_path} \r", end=" ", flush=True)
        font.generate(output_ttf_path)  # TTF形式で保存

        # TTFファイルを開き直し
        print(f"\r TTFに変更して再開する。file:{output_ttf_path} \r", end=" ", flush=True)
        font.close() # SFDフォントを閉じる
        import time  # 書き込みが完了するまで少し待つ
        time.sleep(0.1)
        font = fontforge.open(output_ttf_path) # TTFを開きなおす
        print(f"\r TTFを開きなおした。 file: {output_ttf_path} \r", end=" ", flush=True)
        sys.stdout = sys.__stdout__

        # 最後に全グリフを一斉に見直し
        for glyph in font.glyphs():
            if not glyph.isWorthOutputting():
                continue  # 出力しないグリフはスキップ
            if len(glyph.references) > 0:
                print(f"\r 合成グリフをスキップ： {glyph.glyphname} \r", end=" ", flush=True)
                continue  # コンポジットグリフはスキップ
            Local_validate_notice(glyph, "最終チェック", "warning")

    except IOError as e:
        print(f"保存に失敗しました: {e}")

    else:
        if del_file != f"temp_0_{OUTPUT_NAME}.sfd":
            del_file_path = os.path.join(BUILD_FONTS_DIR, del_file)
            print(f"\r 前の一時ファイルを削除： {del_file_path} \r", end=" ", flush=True)
            os.remove(del_file_path)
    
    font.close()

if __name__ == "__main__":
    main()
