"""
音声再生モジュール for お世話ぬいぐるみプロジェクト
音声ファイルを再生する機能を提供
"""

import os
import time
import threading
from pathlib import Path
from typing import Optional
import pygame
import config

class AudioPlayer:
    """音声再生クラス"""
    
    def __init__(self):
        self.current_audio = None
        self.is_playing = False
        self.play_thread = None
        self.play_history = []

        # PyGameを初期化
        pygame.mixer.init()
        self.set_volume(config.AUDIO_VOLUME)

        
        if config.DEBUG:
            print("音声バックエンド: Pygame")
        
    def set_volume(self, volume: float):
        """音量を設定 (0.0〜1.0)
        
        Args:
            volume: 音量 (0.0=無音、1.0=最大音量)
        """
        # 0.0〜1.0の範囲に制限
        volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(volume)
        
        if config.DEBUG:
            print(f"音量設定: {volume}")
    
    def get_volume(self) -> float:
        """現在の音量を取得
        
        Returns:
            float: 現在の音量 (0.0〜1.0)
        """
        return pygame.mixer.music.get_volume()
    

    def play(self, audio_file: str) -> bool:
        """音声ファイルを再生
        
        Args:
            audio_file: 再生する音声ファイル名
        
        Returns:
            bool: 再生開始に成功したかどうか
        """
        # 既に再生中なら停止
        self.stop()
        
        # 音声ファイルのパスを取得
        audio_path = config.AUDIO_DIR / audio_file
        
        # ファイルが存在するか確認
        if not audio_path.exists():
            if config.DEBUG:
                print(f"エラー: 音声ファイルが見つかりません: {audio_path}")
            return False
        
        self.is_playing = True
        self.current_audio = audio_file
        self.play_history.append(audio_file) 
        if config.DEBUG:
            print(f"再生: {audio_file}")
        try:
            # PyGameで再生
            pygame.mixer.music.load(str(audio_path))
            pygame.mixer.music.play()
            
            # 再生完了を監視するスレッドを開始
            self.play_thread = threading.Thread(
                target=self._pygame_wait_done, 
                daemon=True
            )
            self.play_thread.start()
            return True
           
        except Exception as e:
            if config.DEBUG:
                print(f"再生エラー: {e}")
            self.is_playing = False
            self.current_audio = None
            return False
        
        
        
    def stop(self):
        """現在再生中の音声を停止"""
        if not self.is_playing:
            return
        
        # 再生停止
        pygame.mixer.music.stop()
        self.is_playing = False
        
        # スレッドが終了するのを待つ
        if self.play_thread and self.play_thread.is_alive():
            self.play_thread.join(timeout=0.5)
        
        self.current_audio = None
    
    def _pygame_wait_done(self):
        """PyGameの再生完了を待つ"""
        while self.is_playing and pygame.mixer.music.get_busy():
            time.sleep(0.1)
        self.is_playing = False
    
    def get_current_audio(self) -> Optional[str]:
        """現在再生中の音声ファイル名を取得
        
        Returns:
            str or None: 音声ファイル名、再生中でなければNone
        """
        return self.current_audio if self.is_playing else None
    
    def get_play_history(self):
        return self.play_history
    