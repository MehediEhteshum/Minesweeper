import pygame


class Mode:
    def __init__(self, name, image, mine_tot, rect_numx,
                 rect_numy, wdthPerc, hgtPerc):
        self.name = name
        self.image = image
        self.mine_tot = mine_tot
        self.rect_numx = rect_numx
        self.rect_numy = rect_numy
        self.wdthPerc = wdthPerc
        self.hgtPerc = hgtPerc
        self.factor = image.get_width()/image.get_height()

    def draw_selected(self, banner_h):
        # Draw selected menu item on banner.
        from Minesweeper_test \
            import rect_arm, nodes, screenSurface
        # Scaling image for the banner.
        image = pygame.transform.smoothscale(
            self.image, (int(rect_arm*0.75*self.factor),
                         int(rect_arm*0.75)))
        imgRect = image.get_rect()
        img_h = image.get_height()
        # Setting image top left.
        imgRect.topleft = (
            (nodes[0][0]+rect_arm*0.5),
            (nodes[0][1]-(banner_h/2)-(img_h/2)))
        # Draw menu (selected).
        screenSurface.blit(image, imgRect)
        return imgRect
