import pyxel
import random

class App:
    # ゲームの状態を定義
    STATE_TITLE = 0
    STATE_PLAYING = 1
    STATE_GAMEOVER = 2

    # 定数
    WORD_HEIGHT = 8  # Pyxelのフォントの高さ
    DOG_WIDTH = 16
    DOG_HEIGHT = 16
    STACK_BOTTOM_Y = 120 # 一番下の単語のY座標 (画面中央に調整)
    WORD_SPAWN_INTERVAL = 120 # 2秒ごとに新しいワードを生成 (60FPS想定)

    def __init__(self):
        pyxel.init(256, 256, title="DOG FOOD TYPING", quit_key=pyxel.KEY_NONE)
        pyxel.load("assets.pyxres")

        try:
            with open("words.txt", "r") as f:
                self.words = [line.strip().lower() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            self.words = ["hello", "world", "python", "pyxel"]

        self.game_state = self.STATE_TITLE
        self.score = 0
        self.word_stack = [] # 画面上の単語を管理するリスト
        self.dog_x = 64 # ★犬のX座標を画面の1/4の位置に固定
        self.dog_anim_frame = 0 
        self.word_spawn_timer = 0 # ワード生成タイマーを再導入 
        
        pyxel.run(self.update, self.draw)

    def start_new_game(self):
        """新しいゲームを開始するために変数をリセット"""
        self.score = 0
        self.word_stack = [] # 単語スタックをクリア
        self._add_new_word_to_stack(initial=True) # 最初の単語を一番下に配置
        self.word_spawn_timer = 30 # ★2ワード目が0.5秒後に降ってくるように初期化
        self.game_state = self.STATE_PLAYING

    def _add_new_word_to_stack(self, initial=False):
        """新しい単語をスタックに追加する"""
        if not self.words:
            new_word_text = "no words"
        else:
            new_word_text = random.choice(self.words)
        
        # 横方向は常に中央に配置
        # Pyxelのtext関数は左上基準なので、文字の幅を考慮して中央寄せ
        text_width = len(new_word_text) * pyxel.FONT_WIDTH
        word_x = (pyxel.width - text_width) // 2 
        
        fall_speed = random.uniform(0.5, 1.5) # 落下速度

        if initial:
            # 最初の単語は指定された一番下のY座標に配置
            word_y = self.STACK_BOTTOM_Y
            is_falling = False
        else:
            # 新しい単語は画面上部から落下
            word_y = random.randint(-50, -20) # 画面外の上から
            is_falling = True

        self.word_stack.append({
            "text": new_word_text,
            "x": word_x,
            "y": word_y,
            "fall_speed": fall_speed,
            "typed_count": 0, # 入力済みの文字数
            "is_falling": is_falling # 落下中かどうか
        })

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
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game_state = self.STATE_TITLE
            return

        # ★ワード生成タイマーの更新
        self.word_spawn_timer -= 1
        if self.word_spawn_timer <= 0:
            self._add_new_word_to_stack()
            self.word_spawn_timer = self.WORD_SPAWN_INTERVAL

        # 各単語の位置を更新
        for i, word_data in enumerate(self.word_stack):
            # 横移動は行いません

            # 落下中の単語の縦移動
            if word_data["is_falling"]:
                # 落下目標Y座標 (スタックの高さに応じて計算)
                # iはスタックの底からの位置を示す
                target_y = self.STACK_BOTTOM_Y - i * self.WORD_HEIGHT
                if word_data["y"] < target_y:
                    word_data["y"] += 1 # 落下速度
                else:
                    word_data["y"] = target_y
                    word_data["is_falling"] = False # 落下停止

        # ゲームオーバー条件: スタックされている単語が3つ以上
        if len(self.word_stack) >= 3:
            self.game_state = self.STATE_GAMEOVER
            return

        # キー入力処理 (一番下の単語のみを対象)
        if self.word_stack:
            current_typing_word = self.word_stack[0]
            
            for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
                if pyxel.btnp(key):
                    typed_char = chr(ord('a') + key - pyxel.KEY_A)
                    
                    # 入力された文字が現在の単語の次の文字と一致するか
                    if current_typing_word["typed_count"] < len(current_typing_word["text"]) and \
                       typed_char == current_typing_word["text"][current_typing_word["typed_count"]]:
                        
                        current_typing_word["typed_count"] += 1
                        self.dog_anim_frame = 5 # 口パクアニメーション開始
                        self.score += 1
                        
                        # 単語をすべて入力し終えたら
                        if current_typing_word["typed_count"] == len(current_typing_word["text"]):
                            self.score += 5 # ボーナス
                            self.word_stack.pop(0) # 完了した単語をスタックから削除
                            self._add_new_word_to_stack() # 新しい単語を上から追加
                            
                            # 残りの単語を下にシフト
                            for word_data in self.word_stack:
                                word_data["y"] += self.WORD_HEIGHT
                            break # キー入力ループを抜ける

    def draw(self):
        """画面を描画する"""
        pyxel.cls(1)

        if self.game_state == self.STATE_TITLE:
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
        # スタック内のすべての単語を描画
        for word_data in self.word_stack:
            # 入力済みの部分を除いて描画
            pyxel.text(word_data["x"], word_data["y"] + (self.DOG_HEIGHT - self.WORD_HEIGHT) // 2,
                       word_data["text"][word_data["typed_count"]:], 7)
        
        # 犬を描画 (一番下の単語のY座標に合わせる)
        if self.word_stack:
            dog_y_pos = self.STACK_BOTTOM_Y # ★犬のY座標を固定
            dog_sprite_u = 0
            if self.dog_anim_frame > 0:
                dog_sprite_u = 16
            
            pyxel.blt(self.dog_x, dog_y_pos, 0, dog_sprite_u, 0, self.DOG_WIDTH, self.DOG_HEIGHT, 0)
        
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(170, 5, "Press ESC to quit", 7)

App()
