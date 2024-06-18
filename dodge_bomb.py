import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRect、または、ばくだんRect
    戻り値:タプル(横方向判定結果、横方向判定結果)
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:  # 横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def load_koukaton() -> dict:
    """
    引数:なし
    戻り値:こうかとんの画像を方向ごとにrotozoomした辞書を返す関数
    """
    kk_img = pg.image.load("fig/3.png")
    kk_imgs = {
        (0, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 90, 2.0),    # 上
        (0, 5): pg.transform.rotozoom(kk_img, 90, 2.0),  # 下
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 2.0),   # 左
        (5, 0): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 0, 2.0),   # 右
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 2.0),  # 左上
        (5, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 45, 2.0),  # 右上
        (-5, 5): pg.transform.rotozoom(kk_img, 45, 2.0),  # 左下
        (5, 5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -45, 2.0)  # 右下
    }
    return kk_imgs


def load_bomb() -> tuple[list[pg.Surface], list[int]]:
    """
    引数:なし
    戻り値:爆弾の拡大と加速度を返す
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]  # 加速度のリスト
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs


def game_over(screen, kk_imgs):  # ファイト！
    """
    引数:
    戻り値:
    """
    blackout = pg.Surface(screen.get_size())
    blackout.set_alpha(150)  # 半透明度を設定（0: 完全透明, 255: 完全不透明）
    blackout.fill((0, 0, 0))  # 黒で塗りつぶす
    crying_kk_img = pg.image.load("fig/8.png")  # 実際の画像ファイル名に合わせて変更が必要です
    font = pg.font.Font(None, 100)
    game_over_text = font.render("Game Over", True, (255, 255, 255))  # 白色のテキストを作成
    screen.blit(blackout, (0, 0))  # ブラックアウトを画面全体に描画
    screen.blit(crying_kk_img, (WIDTH // 2 - crying_kk_img.get_width() // 2, HEIGHT // 2 - crying_kk_img.get_height() // 2))
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + crying_kk_img.get_height() // 2 + 20))
    screen.blit(game_over_text, text_rect)
    pg.display.update()
    pg.time.delay(5000)
    return

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_imgs = load_koukaton()  # こうかとんを読み込み
    kk_img = kk_imgs[(-5, 0)]  # 初期画面の左向きに設定
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_imgs, bb_accs = load_bomb()  # 爆弾を読み込み
    bb_img = bb_imgs[0]  # 爆弾画像の設定
    bb_rct =bb_img.get_rect()  # 爆弾Rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の横方向速度，縦方向速度
    clock = pg.time.Clock()
    tmr = 0
    game_over = False
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                game_over = True
        if kk_rct.colliderect(bb_rct):
            game_over = True
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        if sum_mv != [0, 0]:  # 移動していたらTrue
            kk_img = kk_imgs[tuple(sum_mv)]  # 方向に応じた画像に切り替え
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        avx = vx * bb_accs[min(tmr // 500, 9)]  # 時間経過で爆弾の横軸が加速する
        avy = vy * bb_accs[min(tmr // 500, 9)]  # 時間経過で爆弾の縦軸が加速する
        bb_img = bb_imgs[min(tmr // 500, 9)]  # 時間経過で爆弾が拡大する。
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        if game_over:
            game_over(screen, kk_imgs)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
