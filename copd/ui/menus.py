import pygame
import sys
from random import randint

from copd.ui.button import *
from copd.ui.text_box import TextBox
from copd.config import Option, MenuOption
from copd.engine.states import GameStates

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
            if option.type == MenuOption.CAPTION:
                pygame.display.set_caption(option.data)
            elif option.type == MenuOption.PRINT:
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
            elif option.type == MenuOption.HANDLER:
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
            elif option.type == MenuOption.BUTTON:
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
        self.game.state = GameStates.MAIN
        pygame.display.set_caption(self.previous_caption)


class PauseMenu(Menu):
    def __init__(self, game, options=[]):
        # Pause is now fixed
        super().__init__(game, options)
        self.player = game.player
        self.options = options
        self.options.append(Option(MenuOption.CAPTION, "Paused"))
        self.options.append(
            Option(MenuOption.PRINT, dict(size=20, text="PAUSED", pos=(270, 20)))
        )
        self.options.append(
            Option(
                MenuOption.HANDLER,
                dict(
                    event_type=pygame.KEYDOWN,
                    key=pygame.K_p,
                    result=lambda: self.stop(),
                ),
            )
        )

        self.handle_options()
        # self.run()
        self.running = True
        while self.running:
            self.game.screen.fill(Colors.Cyantology)
            self.run_opts()

            # Creating Buttons
            inventory = Button("Inventory", self.game, 242, 70)
            equip = Button("Equipment", self.game, 242, 140)
            close_pause = Button("Close", self.game, 242, 280)

            # Making Buttons Show up
            inventory.show()
            equip.show()
            close_pause.show()

            pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if inventory.butt_rect.collidepoint(e.pos):
                        self.inventory_list()
                    if equip.butt_rect.collidepoint(e.pos):
                        self.equipment_list()
                    if close_pause.butt_rect.collidepoint(e.pos):
                        self.stop()
                else:
                    self.handle_input(e)
        pygame.display.set_caption(self.previous_caption)

    def inventory_list(self):
        self.running = True
        FONT = pygame.font.Font(self.DEFAULT_FONT, 20)
        while self.running:
            self.game.screen.fill(Colors.Cyantology)
            self.run_opts()
            place_holder = 1
            for item in self.game.player.inventory.inventory:
                if place_holder == 1:
                    item1_text = f"{item}"
                    item1 = Button(f"{item}", self.game, 242, 70)
                    item1.show()
                if place_holder == 2:
                    item2_text = f"{item}"
                    item2 = Button(f"{item}", self.game, 242, 140)
                    item2.show()
                if place_holder == 3:
                    item3_text = f"{item}"
                    item3 = Button(f"{item}", self.game, 242, 210)
                    item3.show()
                place_holder += 1
            close_item = Button("Close", self.game, 242, 280)
            close_item.show()

            pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if close_item.butt_rect.collidepoint(e.pos):
                        return
                else:
                    self.handle_input(e)

    def equipment_list(self):
        self.running = True
        FONT = pygame.font.Font(self.DEFAULT_FONT, 20)
        while self.running:
            self.game.screen.fill(Colors.Cyantology)
            self.run_opts()
            place_holder = 1
            for item in self.game.player.equipped.equipped:
                if place_holder == 1:
                    item1_text = f"{item}"
                    item1 = Button(f"{item}", self.game, 172, 70)
                    item1.show()
                    item1_item_text = f"{self.game.player.equipped.equipped[item]}"
                    item1_item = Button(
                        f"{self.game.player.equipped.equipped[item]}",
                        self.game,
                        312,
                        70,
                    )
                    item1_item.show()
                if place_holder == 2:
                    item2_text = f"{item}"
                    item2 = Button(f"{item}", self.game, 172, 140)
                    item2.show()
                    item2_item_text = f"{self.game.player.equipped.equipped[item]}"
                    item2_item = Button(
                        f"{self.game.player.equipped.equipped[item]}",
                        self.game,
                        312,
                        140,
                    )
                    item2_item.show()
                if place_holder == 3:
                    item3_text = f"{item}"
                    item3 = Button(f"{item}", self.game, 172, 210)
                    item3.show()
                    item3_item_text = f"{self.game.player.equipped.equipped[item]}"
                    item3_item = Button(
                        f"{self.game.player.equipped.equipped[item]}",
                        self.game,
                        312,
                        210,
                    )
                    item3_item.show()
                place_holder += 1
            close_item = Button("Close", self.game, 242, 280)
            close_item.show()

            pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if close_item.butt_rect.collidepoint(e.pos):
                        return
                else:
                    self.handle_input(e)


class BattleMenu:
    # New enemy global variable to randomly assign which enemy type is created
    # Fill in the details
    # Defining which enemy class to populate based of the psuedo random number generated

    def __init__(self, game, options={}):
        # super().__init__(screen)
        self.game = game
        self.options = options
        self.DEFAULT_FONT = pygame.font.get_default_font()
        self.player = game.player
        self.monster = (
            game.monster
        )  # added since enemy is generated in overworld. -Roland
        # self.run()

    def run(self):
        self.running = True
        FONT = pygame.font.Font(self.DEFAULT_FONT, 20)

        # self.start_combat()  #commented out for testing random enemy generation on overworld. -Roland

        while self.running:
            self.game.screen.fill(Colors.Snugglepuss)

            height = self.game.screen.get_height()
            width = self.game.screen.get_width()
            monster_info = TextBox(200,100,self.game.screen,10,10)
            monster_info.add_text(self.monster.name,Colors.BLACK,(20,20))
            monster_info.add_border()
            monster_info.draw()
            
            # Create info areas
            # monster_info = pygame.draw.rect(
            #     self.game.screen, "black", [10, 10, 200, 100], 3, border_radius=15
            # )
            player_info = pygame.draw.rect(
                self.game.screen,
                "blue",
                [width - 310, height - 210, 300, 200],
                3,
                border_radius=15,
            )

            # text = self.monster.name
            # self.game.screen.blit(FONT.render(text, False, "black"), (20, 20))
            # self.game.screen.blit(
            #     FONT.render(f"{self.monster.hp}/{self.monster.max_hp}", False, "black"),
            #     (20, 45),
            # )

            # Added player name and hp
            text2 = self.player.name
            self.game.screen.blit(FONT.render(text2, False, "blue"), (340, 160))
            self.game.screen.blit(
                FONT.render(f"{self.player.hp}/{self.player.max_hp}", False, "blue"),
                (340, 185),
            )

            # Button Testing
            fight = Button("Fight", self.game, 340, 210)
            fight.show()
            parry = Button("Parry", self.game, 485, 210)
            parry.show()
            run = Button("Run", self.game, 485, 280)
            run.show()
            items = Button("Inventory", self.game, 340, 280)
            items.show()

            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if fight.butt_rect.collidepoint(e.pos) or parry.butt_rect.collidepoint(e.pos):
                        parrying = False
                        if parry.butt_rect.collidepoint(e.pos):
                            parrying = True
                        self.game.Combat.setup(parry = parrying)
                        self.game.Combat.update()
                        self.running = not self.game.Combat.complete
                    
                        # self.running = combat(self.game,parry=True)
                    if run.butt_rect.collidepoint(e.pos):
                        self.monster.stun = 2
                        self.game.Combat.end()
                        self.running = False
                    if items.butt_rect.collidepoint(e.pos):
                        self.inventory_screen()
                    # self.running = not self.game.Combat.complete
                self.handle_input(e)
        self.game.state = GameStates.MAIN
       

    
    ###TYLER EXPERIMENTAL###

    def inventory_screen(self):
        self.running = True
        FONT = pygame.font.Font(self.DEFAULT_FONT, 20)
        while self.running:
            self.game.screen.fill(Colors.Snugglepuss)
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
            place_holder = 1
            for item in self.game.player.inventory.inventory:
                if place_holder == 1:
                    item1_text = f"{item}"
                    item1 = Button(f"{item}", self.game, 340, 210)
                    item1.show()
                if place_holder == 2:
                    item2_text = f"{item}"
                    item2 = Button(f"{item}", self.game, 485, 210)
                    item2.show()
                if place_holder == 3:
                    item3_text = f"{item}"
                    item3 = Button(f"{item}", self.game, 340, 280)
                    item3.show()
                place_holder += 1
            retbutt = Button("Close", self.game, 485, 280)
            retbutt.show()

            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if retbutt.butt_rect.collidepoint(e.pos):
                        return
                    if item1.butt_rect.collidepoint(e.pos):
                        self.resolve_item(self.player, item1_text)
                        self.player.inventory.use_item(item1_text, 1)
                    if item2.butt_rect.collidepoint(e.pos):
                        self.resolve_item(self.player, item2_text)
                    if item3.butt_rect.collidepoint(e.pos):
                        self.resolve_item(self.player, item3_text)
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


