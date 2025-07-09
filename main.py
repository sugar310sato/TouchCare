# Copyright (c) 2025 sugar310sato
# This software is released under the MIT License, see LICENSE.
# main.py - 本番用お世話ぬいぐるみ起動スクリプト
import time
import random
import threading
import subprocess
from typing import List

import config
from nfc_reader import NFCReader
from audio_player import AudioPlayer

class BatteryMonitor(threading.Thread):
    def __init__(self, player):
        super().__init__(daemon=True)
        self.player = player
        self.last_alert_time = 0

    def run(self):
        while True:
            if self._is_low_voltage():
                now = time.time()
                if now - self.last_alert_time > 300:  # 5分おき
                    #self.player.play("system/battery_low.wav")
                    self.last_alert_time = now
            time.sleep(15)

    def _is_low_voltage(self) -> bool:
        try:
            result = subprocess.check_output(["vcgencmd", "get_throttled"], text=True)
            value = int(result.strip().split('=')[1], 16)
            return (value & 0x1) != 0  # bit0 = 現在低電圧
        except Exception:
            return False

class OsewaNuigurumiMain:
    """お世話ぬいぐるみ 本番運用用クラス"""

    def __init__(self):
        #self.running = False
        self.reader = NFCReader()
        self.player = AudioPlayer()
        self.tag_history: List[str] = []

        # ステータス
        self.hunger = config.DEFAULT_HUNGER
        self.attention = config.DEFAULT_ATTENTION
        self.level = 1
        self.exp = 0
        self.care_count = 0
        self.last_tag = None
        self.same_tag_count = 0
        self.running = False

    def start(self):
        """本番モード開始"""
        config.print_config()
        print("[START] お世話ぬいぐるみが起動しました")

        # 電源オンセリフ
        self.player.play(config.POWER_ON_AUDIO)
        # 電圧チェックスレッド開始
        BatteryMonitor(self.player).start()

        self.running = True
        threading.Thread(target=self._status_loop, daemon=True).start()
        threading.Thread(target=self._decay_loop, daemon=True).start()
        # NFCリーダー読み取り開始
        self.reader.start(callback=self.on_tag_read)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        #停止処理
        self.running = False
        self.reader.stop()
        self.player.stop()
        print("[STOP] お世話ぬいぐるみを終了しました")

    def on_tag_read(self, tag_id: str):
        """タグ読み取り時の処理"""
        if self.player.is_playing:
            return  # 再生中は無視

        care_type = config.TAG_TO_CARE_TYPE.get(tag_id)
        if not care_type:
            print(f"[INFO] 未登録のタグ: {tag_id}")
            return
        
        # 同じタグ連続読み取り
        if tag_id == self.last_tag:
            self.same_tag_count += 1
        else:
            self.last_tag = tag_id
            self.same_tag_count = 1
        full_audio = config.FULL_TAG_AUDIO.get(care_type, [])
        care_audio_files = config.CARE_TYPE_AUDIO_FILES.get(care_type, [])
        # 音声履歴に応じて同じ音声の連続再生を避ける
        play_history = self.player.get_play_history()
        last_played = play_history[-1] if play_history else None

        #ステータス
        if care_type in ["bread", "curry", "cookie", "strawberry", "hamburger_steak","neapolitan"] and self.hunger >= config.MAX_HUNGER:
            self.player.play(config.FULL_HUNGRY_AUDIO)
            print(f"[FULL_HUNGRY] {config.FULL_HUNGRY_AUDIO}")
            return

        if care_type not in ["bread", "curry", "cookie", "strawberry", "hamburger_steak","neapolitan"] and self.attention >= config.MAX_ATTENTION:
            self.player.play(config.FULL_ATTENTION_AUDIO)
            print(f"[FULL_ATTENTION] {config.FULL_ATTENTION_AUDIO}")
            return

        # タグ連続
        if self.same_tag_count >= config.SAME_TAG_LIMIT:
            if full_audio:
                self.player.play(full_audio[0])
                print(f"[FULL_TAG_REPEAT] {care_type} - {full_audio[0]}")
            return

        # 音声履歴に応じて同じ音声の連続再生を避ける
        available_files = [f for f in care_audio_files if f != last_played] or care_audio_files
        selected = random.choice(available_files)
        self.player.play(selected)
        print(f"[PLAY] {care_type} - {selected}")

        # 状態の更新とFULL_xxx処理
        incremented = False

        if care_type in ["bread", "curry", "cookie", "strawberry", "hamburger_steak","neapolitan"]:
            if self.hunger < config.MAX_HUNGER:
                self.hunger = min(config.MAX_HUNGER, self.hunger + config.HUNGER_GAIN)
                incremented = True
        
        else:
            if self.attention < config.MAX_ATTENTION:
                self.attention = min(config.MAX_ATTENTION, self.attention + config.ATTENTION_GAIN)
                incremented = True

        if incremented:
            self.care_count += 1

        self._check_level_up()

    def _decay_loop(self):
        while self.running:
            time.sleep(config.STATUS_DECAY_INTERVAL)
            self.hunger = max(0, self.hunger - config.HUNGER_DECAY)
            self.attention = max(0, self.attention - config.ATTENTION_DECAY)
            if self.hunger < config.HUNGER_ALERT_THRESHOLD:
                if random.random() < 0.3:
                    self.player.play(config.HUNGRY_AUDIO)
            
            if self.attention <= config.ATTENTION_ALERT_THRESHOLD:
                if random.random() < 0.3:
                    self.player.play(config.LONELY_AUDIO)

    def _check_level_up(self):
        thresholds = config.LEVEL_UP_CONDITIONS
        level_audio = config.LEVEL_AUDIO_BY_LEVEL
        next_level = self.level + 1
        if next_level in thresholds:
            condition = thresholds[next_level]
            if self.care_count >= condition['care_count'] and \
               self.hunger >= config.MAX_HUNGER * condition['hunger_ratio'] and \
               self.attention >= config.MAX_ATTENTION * condition['attention_ratio']:
                self.level = next_level
                audio = level_audio.get(next_level, config.LEVEL_AUDIO_BY_LEVEL)
                self.player.play(audio)
                print(f"レベルアップしました → レベル{self.level}")

    def get_status(self):
        return {
            'level': self.level,
            'care_count': self.care_count,
            'exp': self.exp,
            'hunger': self.hunger,
            'attention': self.attention
        }
    
    def _status_loop(self):
        """10秒ごとにステータスを出力するバックグラウンドループ"""
        while self.running:
            status = self.get_status()
            print(f"[STATUS] level={status['level']}, "
                  f"hunger={status['hunger']}, "
                  f"attention={status['attention']}, "
                  f"care_count={status['care_count']}")
            time.sleep(10)

def main():
    app = OsewaNuigurumiMain()
    app.start()


if __name__ == "__main__":
    main()
