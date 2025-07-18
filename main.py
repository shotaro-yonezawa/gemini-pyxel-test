import pyxel
import random

class App:
    # ゲームの状態を定義
    STATE_TITLE = 0
    STATE_PLAYING = 1
    STATE_GAMEOVER = 2

    def __init__(self):
        # ★タイトルを「DOG FOOD TYPING」に変更
        pyxel.init(256, 256, title="DOG FOOD TYPING", quit_key=pyxel.KEY_NONE)
        
        # リソースファイルを読み込む
        pyxel.load("assets.pyxres")

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
        self.difficulty_increase_factor = 0.0005 # 難易度上昇の割合
        self.current_difficulty_speed = 0 # 現在の難易度による速度増加量

        # --- 犬の関連設定 ---
        self.dog_x = 10
        self.dog_anim_frame = 0 
        
        pyxel.run(self.update, self.draw)

    def start_new_game(self):
        """新しいゲームを開始するために変数をリセット"""
        self.score = 0
        self.current_difficulty_speed = 0 # ゲーム開始時に難易度をリセット
        self.new_word()
        self.game_state = self.STATE_PLAYING

    def new_word(self):
        """新しい単語を選択し、位置をリセットする"""
        if not self.words:
            self.current_word = "no words"
        else:
            self.current_word = random.choice(self.words)
        
        self.word_x = 256
        self.word_y = random.randint(10, 240 - 16)
        # 難易度による速度増加量を加算
        self.speed = random.uniform(0.5, 1.5) + self.current_difficulty_speed

    def update(self):
        """ゲームの状態を更新する"""
        if self.dog_anim_frame > 0:
            self.dog_anim_frame -= 1

        if self.game_state == self.STATE_TITLE:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.start_new_game()
        
        elif self.game_state == self.STATE_PLAYING:
            self.update_playing()

        elif self.game_state == self.STATE_GAMEOVER:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.game_state = self.STATE_TITLE

    def update_playing(self):
        """ゲーム中の更新処理"""
        # 難易度を時間経過で上昇させる
        self.current_difficulty_speed += self.difficulty_increase_factor

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game_state = self.STATE_TITLE
            return

        self.word_x -= self.speed
        
        if self.word_x < self.dog_x + 16:
            self.game_state = self.STATE_GAMEOVER

        # キー入力処理
        for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
            if pyxel.btnp(key):
                typed_char = chr(ord('a') + key - pyxel.KEY_A)
                
                if self.current_word and typed_char == self.current_word[0]:
                    # ★正解音
                    pyxel.play(0, 0) 
                    self.current_word = self.current_word[1:]
                    self.score += 1
                    self.word_x += pyxel.FONT_WIDTH 
                    
                    self.dog_anim_frame = 5

                    if not self.current_word:
                        self.score += 5
                        self.new_word()
                        break
                else:
                    # ★不正解音
                    pyxel.play(0, 1)

    def draw(self):
        """画面を描画する"""
        pyxel.cls(1)

        if self.game_state == self.STATE_TITLE:
            # ★タイトル画面の描画
            pyxel.text(88, 110, "DOG FOOD TYPING", 7)
            pyxel.text(100, 130, "PRESS ENTER", pyxel.frame_count % 16)
        
        elif self.game_state == self.STATE_PLAYING:
            self.draw_playing()

        elif self.game_state == self.STATE_GAMEOVER:
            pyxel.text(110, 110, "GAME OVER", 8)
            pyxel.text(104, 120, f"SCORE: {self.score}", 7)
            pyxel.text(80, 130, "PRESS ENTER to return", 7)

    def draw_playing(self):
        """ゲーム中の描画処理"""
        pyxel.text(self.word_x, self.word_y + 6, self.current_word, 7)
        
        dog_sprite_u = 0
        if self.dog_anim_frame > 0:
            dog_sprite_u = 16
        
        pyxel.blt(self.dog_x, self.word_y, 0, dog_sprite_u, 0, 16, 16, 0)
        
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(170, 5, "Press ESC to quit", 7)

App()
