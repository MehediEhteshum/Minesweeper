import pygame


class Mode:
    def __init__(self, name, image):
        self.name = name
        self.image = image
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
