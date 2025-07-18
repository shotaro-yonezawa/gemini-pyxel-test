import pyxel
import random

class App:
    def __init__(self):
        pyxel.init(256, 256, title="Typing Game")
        
        # 単語リストを読み込む
        try:
            with open("words.txt", "r") as f:
                # 小文字に統一し、空行を無視する
                self.words = [line.strip().lower() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            self.words = ["hello", "world", "python", "pyxel"] # 見つからない場合の単語

        self.score = 0
        self.current_word = ""
        self.word_x = 0
        self.word_y = 0
        self.speed = 0
        
        # 犬のキャラクター
        self.dog_x = 10
        self.dog_char = ">" 
        
        self.new_word()

        pyxel.run(self.update, self.draw)

    def new_word(self):
        """新しい単語を選択し、位置をリセットする"""
        if not self.words:
            self.current_word = "no words found"
        else:
            self.current_word = random.choice(self.words)
        
        self.word_x = 256
        self.word_y = random.randint(10, 240)
        self.speed = random.uniform(0.5, 1.5)

    def update(self):
        """ゲームの状態を更新する"""
        # 単語を動かす
        self.word_x -= self.speed
        
        # 犬に単語が到達したら（ゲームオーバー的な処理）
        if self.word_x < self.dog_x + 8:
            self.new_word()
            self.score -= 5 # ペナルティ
            if self.score < 0: self.score = 0

        # --- キー入力処理 ---
        # aからzまでのキーが押されたかチェック
        for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
            if pyxel.btnp(key):
                typed_char = chr(ord('a') + key - pyxel.KEY_A)
                
                # 入力された文字が単語の先頭文字と一致するか
                if self.current_word and typed_char == self.current_word[0]:
                    # 一致したら単語の先頭文字を削除
                    self.current_word = self.current_word[1:]
                    self.score += 1
                    
                    # 犬が文字を食べたように見せるため、単語を少し右にずらす
                    self.word_x += pyxel.FONT_WIDTH 
                    
                    # 単語をすべて入力し終えたら
                    if not self.current_word:
                        self.score += 5 # ボーナス
                        self.new_word()
                        break # ループを抜ける

    def draw(self):
        """画面を描画する"""
        pyxel.cls(1) # 明るい青色の背景
        
        # 現在の単語を描画
        pyxel.text(self.word_x, self.word_y, self.current_word, 7)
        
        # 犬を描画（単語と同じ高さに表示）
        pyxel.text(self.dog_x, self.word_y, self.dog_char, 8) # 赤色の犬
        
        # スコアを描画
        pyxel.text(5, 5, f"Score: {self.score}", 7)

App()
