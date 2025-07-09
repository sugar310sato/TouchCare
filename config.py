# Copyright (c) 2025 sugar310sato
# This software is released under the MIT License, see LICENSE.
"""
設定ファイル for お世話ぬいぐるみプロジェクト
グローバル変数と設定を管理
"""

import os
from pathlib import Path

# プロジェクトのルートディレクトリ
PROJECT_ROOT = Path(os.path.dirname(os.path.abspath(__file__)))

"""
----------音声ファイルの設定----------
"""
# 音声ファイルのディレクトリ
AUDIO_DIR = PROJECT_ROOT / "audio"

# NFCタグとそれに対応するお世話タイプ
TAG_TO_CARE_TYPE = {
    
    "04:1E:72:12:BD:2A:81": "block",         # 積み木
    "04:56:6B:12:BD:2A:81": "cookie",        # クッキー
    "04:EA:77:12:BD:2A:81": "strawberry",    # イチゴ
    "04:F8:7D:12:BD:2A:81":"sleep",#"bb"    # ねんね
    "04:E7:84:12:BD:2A:81":"medicine",#"aa" # おくすり
    "04:BD:A8:12:BD:2A:81":"curry",#"cc"    # カレー    
    "04:D8:97:12:BD:2A:81":"bread",#"dd"    # パン
    "04:C9:91:12:BD:2A:81":"dentifrice",#"ee" # 歯みがき
    "04:33:9E:12:BD:2A:81":"song",#ff"     #お歌
    "1D:DC:AF:27:0F:10:80":"hamburger_steak",#"gg"#ハンバーグ
    "1D:DB:AF:27:0F:10:80":"going_out",#"hh"#おでかけ
    "1D:DA:AF:27:0F:10:80":"neapolitan",#ii"#ナポリタン
    #"1D:D9:AF:27:0F:10:80":"jj"
    #"1D:D8:AF:27:0F:10:80":"kk"
    #"1D:D7:AF:27:0F:10:80":"ll"
    #"1D:D6:AF:27:0F:10:80":"mm"
    #"1D:74:B0:27:0F:10:80":"nn"
    #"1D:73:B0:27:0F:10:80":"oo"
    #"1D:72:B0:27:0F:10:80":"pp"
    #"1D:71:B0:27:0F:10:80":"qq"
    #"1D:70:B0:27:0F:10:80":"rr"
    #"1D:6F:B0:27:0F:10:80":"ss"
    #"1D:6E:B0:27:0F:10:80":"tt"
    #"1D:6D:B0:27:0F:10:80":"uu"
    #"1D:6C:B0:27:0F:10:80":"vv"
    #"1D:6B:B0:27:0F:10:80":"ww"
    #"1D:6A:B0:27:0F:10:80":"xx"
    #"1D:69:B0:27:0F:10:80":"yy"
    #"1D:68:B0:27:0F:10:80":"zz"
    #"04:95:65:12:BD:2A:81": "abc"
}

# お世話タイプに対応する複数の音声ファイル
CARE_TYPE_AUDIO_FILES = {
    "sleep": [
        "sleep/sleep_01.wav",
        "sleep/sleep_02.wav",
        "sleep/sleep_03.wav"
    ],
    "medicine": [
        #"medicine/medicine_01.wav",
        #"medicine/medicine_02.wav",
        "medicine/medicine_03.wav",
        "medicine/medicine_04.wav",
        "medicine/medicine_05.wav",
    ],
    "curry": [
        "curry/curry_01.wav",
        "curry/curry_02.wav",
        "curry/curry_03.wav"
    ],
    "bread": [
        "bread/bread_01.wav",
        "bread/bread_02.wav",
        "bread/bread_03.wav"
    ],
    "block": [
        "block/block_01.wav",
        "block/block_02.wav",
        "block/block_03.wav"
    ],
    "cookie": [
        "cookie/cookie_01.wav",
        "cookie/cookie_02.wav",
        "cookie/cookie_03.wav"
    ],
    "strawberry": [
        "strawberry/strawberry_01.wav",
        "strawberry/strawberry_02.wav",
        "strawberry/strawberry_03.wav"
    ],
    "dentifrice": [
        "dentifrice/dentifrice_01.wav",
        "dentifrice/dentifrice_02.wav",
        "dentifrice/dentifrice_03.wav"
    ],
    "song": [
        "song/song_01.wav",
        "song/song_02.wav",
        "song/song_03.wav",
        "song/song_04.wav"
    ],
    "hamburger_steak": [
        "hamburger_steak/hamburger_steak_01.wav",
        "hamburger_steak/hamburger_steak_02.wav",
        "hamburger_steak/hamburger_steak_03.wav"
    ],
    "going_out": [
        "going_out/going_out_01.wav",
        "going_out/going_out_02.wav",
        "going_out/going_out_03.wav"
    ],
    "neapolitan": [
        "neapolitan/neapolitan_01.wav",
        "neapolitan/neapolitan_02.wav",
        "neapolitan/neapolitan_03.wav"
    ],
}
# FULL回タグを読み取った時の音声ファイル
FULL_TAG_AUDIO = {
    "sleep": ["status/full_sleep.wav"],
    "medicine": ["status/full_medicine1.wav"],
    "curry": ["status/full_curry.wav"],
    "bread": ["status/full_bread.wav"],
    "block": ["status/full_block.wav"],
    "cookie": ["status/full_cookie.wav"],
    "strawberry": ["status/full_strawberry.wav"],
    "dentifrice": ["status/full_dentifrice.wav"],
    "song": ["status/full_song.wav"],
    "hamburger_steak": ["status/full_hamburger_steak.wav"],
    "going_out": ["status/full_going_out.wav"],
    "neapolitan": ["status/full_neapolitan.wav"],
}

# ステータスの音声ファイル
POWER_ON_AUDIO = "system/power_on.wav"
BATTERY_LOW_AUDIO = "system/battery_low.wav"
HUNGRY_AUDIO = "status/hungry.wav"
LONELY_AUDIO = "status/lonely.wav"
FULL_HUNGRY_AUDIO = "status/full_hungry.wav"
FULL_ATTENTION_AUDIO = "status/full_attention.wav"


LEVEL_AUDIO_BY_LEVEL = {
    2: "status/level2.wav",
    3: "status/level3.wav",
    4: "status/level4.wav",
    5: "status/level5.wav",
}

"""
----------ステータスの定数設定----------
"""
DEFAULT_HUNGER = 10  # 初期空腹状態
DEFAULT_ATTENTION = 10  # 初期仲良し度
MAX_HUNGER = 100  # 満腹状態
MAX_ATTENTION = 100  # べストフレン度

HUNGER_GAIN = 10  # 食事ゲイン
ATTENTION_GAIN = 10  # 遊びゲイン
HUNGER_DECAY = 10  # 空腹
ATTENTION_DECAY = 10  #

STATUS_DECAY_INTERVAL = 60  # 空腹・仲良し度減少ペース[秒]
HUNGER_ALERT_THRESHOLD = 10 # 空腹閾値
ATTENTION_ALERT_THRESHOLD = 0 # 仲良し閾値

SAME_TAG_LIMIT = 5  #同じタグ連続読み取り可能回数

BATTERY_CHECK_INTERVAL = 30        # 秒
BATTERY_ALERT_COOLDOWN = 300       # 秒

LEVEL_UP_CONDITIONS = {
    2: {"care_count": 10, "hunger_ratio": 0.0, "attention_ratio": 0.0},
    3: {"care_count": 20, "hunger_ratio": 0.5, "attention_ratio": 0.5},
    4: {"care_count": 40, "hunger_ratio": 0.8, "attention_ratio": 0.8},
    5: {"care_count": 70, "hunger_ratio": 0.8, "attention_ratio": 0.8},
}



"""
----------起動モードの設定----------
"""
# NFCリーダーのシミュレーション設定
SIMULATE_NFC = False
SIMULATE_NFC_IDS = list(TAG_TO_CARE_TYPE.keys())

# 音声再生設定
AUDIO_VOLUME = 1.0  # 0.0 ~ 1.0

# 省エネ設定
POWER_SAVE_MODE = True
POWER_SAVE_TIMEOUT = 60  # 秒単位、この時間何も操作がなければスリープモードに
SCAN_INTERVAL = 3.0  # NFC読み取り間隔（秒）

# デバッグモード
DEBUG = True

# 設定の概要を表示
def print_config():
    """現在の設定を表示"""
    print("==== お世話ぬいぐるみプロジェクト 設定 ====")
    print(f"音声ディレクトリ: {AUDIO_DIR}")
    print(f"NFCシミュレーション: {'有効' if SIMULATE_NFC else '無効'}")
    print(f"省エネモード: {'有効' if POWER_SAVE_MODE else '無効'}")
    print(f"スキャン間隔: {SCAN_INTERVAL}秒")
    print(f"登録済みタグ数: {len(TAG_TO_CARE_TYPE)}")
    print("登録済みお世話内容:")
    for care_type, files in CARE_TYPE_AUDIO_FILES.items():
        print(f"  - {care_type}: {len(files)}個の音声")
    print("登録済みFULL時お世話内容:")
    for care_type, files in FULL_TAG_AUDIO.items():
        print(f"  - {care_type}: {len(files)}個の音声")
    print("=========================================")



print_config()
