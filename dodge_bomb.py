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


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_imgs = load_koukaton()  # こうかとんを読み込み
    kk_img = kk_imgs[(-5, 0)]  # 初期画面の上向きに設定
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))  # 1辺が20の空のSarfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 空のSurfaceに赤い円を描く
    bb_img.set_colorkey((0, 0, 0))
    bb_rct =bb_img.get_rect()  # 爆弾Rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の横方向速度，縦方向速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            return  # ゲームオーバー
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
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
