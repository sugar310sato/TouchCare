import time
import threading
from typing import Callable, Optional
import nfc
import config

class NFCReader:
    def __init__(self):
        self.running = False
        self.reader_thread = None
        self.callback = None
        self.clf = None        # 後で開く
        self._retry_count = 0
        self._max_retries = 3

    def start(self, callback: Callable[[str], None]):
         #NFCリーダーの読み取りを開始
         if self.running:
             return
        # まずここで ContactlessFrontend を初期化
         self._ensure_frontend()
         self.callback = callback
         self.running = True
         self.reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
         self.reader_thread.start()
         if config.DEBUG:
             print("NFCリーダーを起動しました")
             
    def stop(self):
        #NFCリーダーの読み取りを停止
        self.running = False
        if self.reader_thread:
            self.reader_thread.join(timeout=1.0)
        if self.clf:
            try:
                self.clf.close()
            except:
                pass
        if config.DEBUG:
            print("NFCリーダーを停止しました")
            
    def _ensure_frontend(self):
        #clf が未作成 or クローズされているなら再オープンを試みる
        if self.clf:
            return
        try:
            self.clf = nfc.ContactlessFrontend('usb')
            if config.DEBUG:
                print("NFC: frontend opened")
        except Exception as e:
            self.clf = None
            if config.DEBUG:
                print(f"NFC init error: {e}")

    def _reader_loop(self):
       while self.running:
            time.sleep(config.SCAN_INTERVAL)
            # 前回 clf が失敗していたら毎ループ再初期化を試み
            if not self.clf:
                self._ensure_frontend()
            tag_id = self._read_tag()
            if not tag_id:
                 continue
            self.callback(tag_id)

    def _read_tag(self) -> Optional[str]:
         #タグ読み取り
         if config.SIMULATE_NFC or not self.clf:
             return None

         try:
             tag = self.clf.connect(rdwr={'on-connect': lambda tag: False})
             self._retry_count = 0
             hex_id = tag.identifier.hex().upper()
             return ':'.join(hex_id[i:i+2] for i in range(0, len(hex_id), 2))
             if config.DEBUG:
                 print(f"NFC read success:{tag_id}")
             return tag_id

         except Exception as e:
             if config.DEBUG:
                print(f"NFC read failed ({self._retry_count+1}/{self._max_retries}): {e}")

             self._retry_count += 1
             if self._retry_count <= self._max_retries:
                 # 再オープンしてリトライ

                try: self.clf.close()
                except: pass
                self.clf = None
                self._ensure_frontend()
                time.sleep(0.1)
                return self._read_tag()
             else:
                 self._retry_count = 0
                 return None

    
    def wake_up(self):
        #スリープモードから強制的に復帰させる
        self.sleep_mode = False
        self.last_activity_time = time.time()
        if config.DEBUG:
            print("省エネモード: 強制的に復帰しました")
