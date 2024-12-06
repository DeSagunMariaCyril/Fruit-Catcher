import pygame
from settings import screen, background, logo_img, start_button_img


def main_menu():
    """
    Dit is de menu die je te zien krijgt voordat de game start, als je op de button klikt dan begint het spelletje
    """
    pygame.init()
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                button_x = screen.get_width() // 2 - start_button_img.get_width() // 2
                button_y = screen.get_height() // 2 - start_button_img.get_height() // 2
                if (
                    button_x <= mouse_x <= button_x + start_button_img.get_width()
                    and button_y <= mouse_y <= button_y + start_button_img.get_height()
                ):
                    menu = False

        screen.blit(background, (0, 0))

        title = pygame.font.SysFont(None, 55).render(
            "Best Education B.V.", True, (0, 0, 0)
        )
        paragraph = pygame.font.SysFont(None, 30).render(
            "Wij lanceren je de toekomst in!", True, (0, 0, 0)
        )
        screen.blit(
            title,
            (
                screen.get_width() // 2 - title.get_width() // 2,
                screen.get_height() // 3,
            ),
        )
        screen.blit(
            paragraph,
            (
                screen.get_width() // 2 - paragraph.get_width() // 2,
                screen.get_height() // 3 + 50,
            ),
        )

        button_x = screen.get_width() // 2 - start_button_img.get_width() // 2
        button_y = screen.get_height() // 2 - start_button_img.get_height() // 2
        screen.blit(start_button_img, (button_x, button_y))

        logo_x = screen.get_width() - logo_img.get_width() - 10
        logo_y = 10
        screen.blit(logo_img, (logo_x, logo_y))

        pygame.display.update()

    return True


def end_menu():
    """
    Dit is het menu die je te zien krijgt na de afloop van de game, je kan het spelletje opnieuw opstarten.
    """
    pygame.init()
    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                button_x = screen.get_width() // 2 - start_button_img.get_width() // 2
                button_y = screen.get_height() // 2 + 50
                if (
                    button_x <= mouse_x <= button_x + start_button_img.get_width()
                    and button_y <= mouse_y <= button_y + start_button_img.get_height()
                ):
                    return True

        screen.blit(background, (0, 0))

        title = pygame.font.SysFont(None, 55).render("Game Over", True, (255, 0, 0))
        paragraph = pygame.font.SysFont(None, 30).render(
            "Bedankt voor het spelen!", True, (0, 0, 0)
        )
        screen.blit(
            title,
            (
                screen.get_width() // 2 - title.get_width() // 2,
                screen.get_height() // 3,
            ),
        )
        screen.blit(
            paragraph,
            (
                screen.get_width() // 2 - paragraph.get_width() // 2,
                screen.get_height() // 3 + 50,
            ),
        )

        button_x = screen.get_width() // 2 - start_button_img.get_width() // 2
        button_y = screen.get_height() // 2 + 50
        screen.blit(start_button_img, (button_x, button_y))

        pygame.display.update()

    return True
