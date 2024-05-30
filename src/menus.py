import pygame
import sys
from dataclasses import dataclass
from enum import Enum
from input_handlers import OPTIONS, Option
from entities import *
from button import *
from typing import Tuple
from random import randint
import time


class Menu:
    def __init__(self, game, options):
        self.game = game
        self.options = options
        self.previous_caption = pygame.display.get_caption()[0]
        self.DEFAULT_FONT = pygame.font.get_default_font()
        self.runnable_opts = []
        self.handlers = []
        # TODO: Add a layer option or some what to say if this will just overlay another menu or if it takes over the screen

    def handle_options(self) -> None:
        for option in self.options:
            if option.type == OPTIONS.CAPTION:
                pygame.display.set_caption(option.data)
            elif option.type == OPTIONS.PRINT:
                size = option.data["size"]
                text = option.data["text"]
                pos = option.data["pos"]
                font = (
                    option.data["font"] if "font" in option.data else self.DEFAULT_FONT
                )
                FONT = pygame.font.Font(font, size)
                self.runnable_opts.append(
                    lambda: self.game.screen.blit(
                        FONT.render(text, False, (255, 255, 255)), pos
                    )
                )
            elif option.type == OPTIONS.HANDLER:
                event_type = option.data.get("event_type")
                if event_type in [pygame.KEYDOWN, pygame.KEYUP]:
                    key = option.data.get("key")
                    result = option.data.get("result")
                    self.handlers.append(
                        {
                            "type": event_type,
                            "func": lambda x: result() if x.key == key else ...,
                        }
                    )
            elif option.type == OPTIONS.BUTTON:
                text = option.data["text"]
                position = option.data["position"]
                on_click = option.data["on_click"]
                button = Button(text, position[0], position[1])
                button.button_surface.blit(button.text, button.rect)
                button.set_on_click(on_click)
                self.clickable.append(button)
                self.runnable_opts.append(
                    lambda: self.game.screen.blit(
                        button.button_surface, (button.butt_rect.x, button.butt_rect.y)
                    )
                )

    def handle_input(self, input) -> None:
        for handler in self.handlers:
            if input.type == handler["type"]:
                handler["func"](input)
        if input.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def run_opts(self) -> None:
        for opt in self.runnable_opts:
            opt()

    def stop(self) -> None:
        self.running = False

    def run(self) -> None:
        self.running = True
        while self.running:
            self.game.screen.fill((0, 0, 0))
            self.run_opts()
            pygame.display.update()
            for e in pygame.event.get():
                self.handle_input(e)
        pygame.display.set_caption(self.previous_caption)


class PauseMenu(Menu):
    def __init__(self, game, options=[]):
        super().__init__(game, options)
        self.options = options
        self.options.append(Option(OPTIONS.CAPTION, "Paused"))
        self.options.append(
            Option(OPTIONS.PRINT, dict(size=20, text="PAUSED", pos=(100, 100)))
        )
        self.options.append(
            Option(
                OPTIONS.HANDLER,
                dict(
                    event_type=pygame.KEYDOWN,
                    key=pygame.K_p,
                    result=lambda: self.stop(),
                ),
            )
        )
        self.handle_options()
        self.run()


class BattleMenu:
    # New enemy global variable to randomly assign which enemy type is created
    # Fill in the details
    # Defining which enemy class to populate based of the psuedo random number generated
    global player
    global enemy
    global monster

    def __init__(self, game, options={}):
        # super().__init__(screen)
        self.game = game
        self.options = options
        self.DEFAULT_FONT = pygame.font.get_default_font()
        self.player = game.player
        self.run()

    def start_combat(self):
        num = random.randint(1, 3)
        if num == 1:
            self.monster = Goblin()
        if num == 2:
            self.monster = HobGoblin()
        if num == 3:
            self.monster = Ogre()
        self.player.update()

    def run(self):
        self.running = True
        FONT = pygame.font.Font(self.DEFAULT_FONT, 20)

        self.start_combat()

        while self.running:
            self.game.screen.fill("white")
            height = self.game.screen.get_height()
            width = self.game.screen.get_width()
            # Create info areas
            monster_info = pygame.draw.rect(
                self.game.screen, "black", [10, 10, 200, 100], 3, border_radius=15
            )
            player_info = pygame.draw.rect(
                self.game.screen,
                "blue",
                [width - 310, height - 210, 300, 200],
                3,
                border_radius=15,
            )

            text = self.monster.name
            self.game.screen.blit(FONT.render(text, False, "black"), (20, 20))
            self.game.screen.blit(
                FONT.render(f"{self.monster.hp}/{self.monster.max_hp}", False, "black"),
                (20, 45),
            )

            # Added player name and hp
            text2 = self.player.name
            self.game.screen.blit(FONT.render(text2, False, "blue"), (340, 160))
            self.game.screen.blit(
                FONT.render(f"{self.player.hp}/{self.player.max_hp}", False, "blue"),
                (340, 185),
            )

            # Button Testing
            fight = Button("Fight", self.game, 340, 210)

            defend = Button("Defend", self.game, 485, 210)

            run = Button("Run", self.game, 485, 280)

            items = Button("Inventory", self.game, 340, 280)

            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if fight.butt_rect.collidepoint(e.pos):
                        combat(self, self.player, self.monster, False)
                    if defend.butt_rect.collidepoint(e.pos):
                        combat(self, self.player, self.monster, True)
                    if run.butt_rect.collidepoint(e.pos):
                        self.player.game.update()
                        self.running = False
                    if items.butt_rect.collidepoint(e.pos):
                        if self.player.inventory.inventory == {}:
                            pass
                        else:
                            self.inventory_screen()
                self.handle_input(e)

    global combat

    def combat(self, player, monster, defend):
        # Just a basic Combat system can be better later
        if defend == True:
            player.hp = player.hp - int(monster.atk / 2)
            parry_chance = random.randint(1, 2)
            if parry_chance == 2:
                monster.hp = monster.hp - player.atk
            else:
                pass
        elif defend == False:
            monster.hp = monster.hp - player.atk
            player.hp = player.hp - monster.atk
        if player.hp <= 0:
            pygame.quit()
            sys.exit()
        elif monster.hp <= 0:
            player.game.update()
            player.inventory.update_item(monster.item, 1)
            self.running = False

    def inventory_screen(self):
        self.running = True
        FONT = pygame.font.Font(self.DEFAULT_FONT, 20)
        while self.running:
            self.game.screen.fill("white")
            height = self.game.screen.get_height()
            width = self.game.screen.get_width()
            # Create info areas
            monster_info = pygame.draw.rect(
                self.game.screen, "black", [10, 10, 200, 100], 3, border_radius=15
            )
            player_info = pygame.draw.rect(
                self.game.screen,
                "blue",
                [width - 310, height - 210, 300, 200],
                3,
                border_radius=15,
            )

            text = self.monster.name
            self.game.screen.blit(FONT.render(text, False, "black"), (20, 20))
            self.game.screen.blit(
                FONT.render(f"{self.monster.hp}/{self.monster.max_hp}", False, "black"),
                (20, 45),
            )

            # Added player name and hp
            text2 = self.player.name
            self.game.screen.blit(FONT.render(text2, False, "blue"), (340, 160))
            self.game.screen.blit(
                FONT.render(f"{self.player.hp}/{self.player.max_hp}", False, "blue"),
                (340, 185),
            )

            # Inventory Testing
            i = 1
            for item in self.player.inventory.inventory:
                if i == 1:
                    item1_text = f"{item}"
                    item1 = Button(f"{item}", self.game, 340, 210)

                    item2 = Button("No Item", self.game, 485, 210)

                    item3 = Button("No Item", self.game, 340, 280)

                if i == 2:
                    item2_text = f"{item}"
                    item2 = Button(f"{item}", self.game, 485, 210)

                    item3 = Button("No Item", self.game, 340, 280)

                if i == 3:
                    item3_text = f"{item}"
                    item3 = Button(f"{item}", self.game, 340, 280)

                i += 1

            retbutt = Button("Close", self.game, 485, 280)

            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if item1.butt_rect.collidepoint(e.pos):
                        self.resolve_item(self.player, item1_text)
                        self.player.inventory.use_item(item1_text, 1)
                    if item2.butt_rect.collidepoint(e.pos):
                        self.resolve_item(self.player, item2_text)
                    if item3.butt_rect.collidepoint(e.pos):
                        self.resolve_item(self.player, item3_text)
                    if retbutt.butt_rect.collidepoint(e.pos):
                        return
                self.handle_input(e)

    def resolve_item(self, player, item):
        if item == "L HP Pot":
            player.hp += 10
            if player.hp > player.max_hp:
                player.hp = player.max_hp
        elif item == "M HP Pot":
            player.hp += 8
            if player.hp > player.max_hp:
                player.hp = player.max_hp
        elif item == "S HP Pot":
            player.hp += 5
            if player.hp > player.max_hp:
                player.hp = player.max_hp

    def handle_input(self, input) -> None:
        if input.type == pygame.KEYDOWN:
            if input.key == pygame.K_q:
                self.running = False
        if input.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# class InfoBox:
#     def __init__(self,screen,position:Tuple[int,int],height:int=-1,width:int=-1):
#         self.game.screen = screen
#         self.x, self.y  = position
#         self.FONT_STYLE = pygame.font.get_default_font()
#         self.text = []
#         # self.static_height = True if height != -1 else False
#         # self.static_width = True if width != -1 else False
#         # self.height = 20 if height == -1 else height # 10 px on each side default
#         # self.width = 20 if width == -1 else width # 10 px on each side default
#         self.height = height
#         self.width = width
#         self.text_buffer = 5
#         self.border_buffer = 10


#     def add_text(self,text:str,size : int = 20,color: str = "black") -> None:
#         FONT = pygame.font.Font(self.DEFAULT_FONT,size)
#         new_text = FONT.render(text,False,color)
#         h = new_text.get_height()
#         w = new_text.get_width()
#         # self.height += h + 5 # 5px buffer between text items
#         # self.width = max(self.width, w+20) # Expand width depending on max text size
#         self.text.append(dict(text=new_text,size=(h,w)))

#     def display(self):
#         border = pygame.draw.rect(self.game.screen, "black", [self.x,self.y, self.width, self.height], 3,border_radius = 15)
#         x = self.x + self.border_buffer
#         y = self.y + self.border_buffer
#         for text in self.text:
#             self.game.screen.blit(text['text'],(x,y))
#             self.game.screen.blit(FONT.render(f"{monster.hp}/{monster.max_hp}",False,"black"),(20,45))
#             x+=text.
