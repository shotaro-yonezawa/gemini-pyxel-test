import pyxel
import random

class App:
    # ゲームの状態を定義
    STATE_TITLE = 0
    STATE_PLAYING = 1
    STATE_GAMEOVER = 2

    def __init__(self):
        # ESCキーでゲームが終了しないように設定
        pyxel.init(256, 256, title="Typing Game", quit_key=pyxel.KEY_NONE)
        
        # 単語リストを読み込む
        try:
            with open("words.txt", "r") as f:
                self.words = [line.strip().lower() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            self.words = ["hello", "world", "python", "pyxel"]

        # ゲームの状態を初期化
        self.game_state = self.STATE_TITLE
        
        self.score = 0
        self.current_word = ""
        self.word_x = 0
        self.word_y = 0
        self.speed = 0
        self.dog_x = 10
        self.dog_char = ">"
        
        pyxel.run(self.update, self.draw)

    def start_new_game(self):
        """新しいゲームを開始するために変数をリセット"""
        self.score = 0
        self.new_word()
        self.game_state = self.STATE_PLAYING

    def new_word(self):
        """新しい単語を選択し、位置をリセットする"""
        if not self.words:
            self.current_word = "no words"
        else:
            self.current_word = random.choice(self.words)
        
        self.word_x = 256
        self.word_y = random.randint(10, 240)
        self.speed = random.uniform(0.5, 1.5)

    def update(self):
        """ゲームの状態を更新する"""
        if self.game_state == self.STATE_TITLE:
            # タイトル画面でエンターキーが押されたらゲーム開始
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.start_new_game()
        
        elif self.game_state == self.STATE_PLAYING:
            self.update_playing()

        elif self.game_state == self.STATE_GAMEOVER:
            # ゲームオーバー画面でエンターキーが押されたらタイトルへ
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.game_state = self.STATE_TITLE

    def update_playing(self):
        """ゲーム中の更新処理"""
        # ESCキーでタイトルに戻る
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game_state = self.STATE_TITLE
            return

        # 単語を動かす
        self.word_x -= self.speed
        
        # 犬に単語が到達したらゲームオーバー
        if self.word_x < self.dog_x + 8:
            self.game_state = self.STATE_GAMEOVER

        # キー入力処理
        for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
            if pyxel.btnp(key):
                typed_char = chr(ord('a') + key - pyxel.KEY_A)
                
                if self.current_word and typed_char == self.current_word[0]:
                    self.current_word = self.current_word[1:]
                    self.score += 1
                    self.word_x += pyxel.FONT_WIDTH 
                    
                    if not self.current_word:
                        self.score += 5 # ボーナス
                        self.new_word()
                        break

    def draw(self):
        """画面を描画する"""
        pyxel.cls(1) # 明るい青色の背景

        if self.game_state == self.STATE_TITLE:
            pyxel.text(100, 120, "PRESS ENTER", pyxel.frame_count % 16)
        
        elif self.game_state == self.STATE_PLAYING:
            self.draw_playing()

        elif self.game_state == self.STATE_GAMEOVER:
            pyxel.text(110, 110, "GAME OVER", 8)
            pyxel.text(104, 120, f"SCORE: {self.score}", 7)
            pyxel.text(80, 130, "PRESS ENTER to return", 7)

    def draw_playing(self):
        """ゲーム中の描画処理"""
        # 現在の単語を描画
        pyxel.text(self.word_x, self.word_y, self.current_word, 7)
        
        # 犬を描画
        pyxel.text(self.dog_x, self.word_y, self.dog_char, 8)
        
        # スコアを描画
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        # 操作説明
        pyxel.text(170, 5, "Press ESC to quit", 7)

App()
