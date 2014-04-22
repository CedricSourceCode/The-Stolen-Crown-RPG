"""
Module for all game observers.
"""
from . import constants as c
from .components import attack
from . import setup

class Battle(object):
    """
    Observes events of battle and passes info to components.
    """
    def __init__(self, level):
        self.level = level
        self.info_box = level.info_box
        self.select_box = level.info_box
        self.arrow = level.arrow
        self.player = level.player
        self.enemies = level.enemy_group
        self.event_dict = self.make_event_dict()

    def make_event_dict(self):
        """
        Make a dictionary of events the Observer can
        receive.
        """
        event_dict = {c.END_BATTLE: self.end_battle,
                      c.SELECT_ACTION: self.select_action,
                      c.SELECT_ITEM: self.select_item,
                      c.SELECT_ENEMY: self.select_enemy,
                      c.ENEMY_ATTACK: self.enemy_attack,
                      c.PLAYER_ATTACK: self.player_attack,
                      c.ATTACK_ANIMATION: self.attack_animation,
                      c.RUN_AWAY: self.run_away,
                      c.BATTLE_WON: self.battle_won,
                      c.PLAYER_FINISHED_ATTACK: self.player_finished_attack}

        return event_dict

    def on_notify(self, event):
        """
        Notify Observer of event.
        """
        if event in self.event_dict:
            self.event_dict[event]()

    def end_battle(self):
        """
        End Battle and flip to previous state.
        """
        self.level.end_battle()

    def select_action(self):
        """
        Set components to select action.
        """
        self.level.state = c.SELECT_ACTION
        self.arrow.index = 0
        self.arrow.state = c.SELECT_ACTION
        self.arrow.image = setup.GFX['smallarrow']
        self.info_box.state = c.SELECT_ACTION

    def select_enemy(self):
        self.level.state = c.SELECT_ENEMY
        self.arrow.state = c.SELECT_ENEMY

    def select_item(self):
        self.level.state = c.SELECT_ITEM
        self.info_box.state = c.SELECT_ITEM

    def enemy_attack(self):
        pass

    def player_attack(self):
        enemy_posx = self.arrow.rect.x + 60
        enemy_posy = self.arrow.rect.y - 20
        enemy_pos = (enemy_posx, enemy_posy)
        enemy_to_attack = None

        for enemy in self.enemies:
            if enemy.rect.topleft == enemy_pos:
                enemy_to_attack = enemy

        self.player.enter_attack_state(enemy_to_attack)
        self.arrow.become_invisible_surface()

    def attack_animation(self):
        """
        Make an attack animation over attacked enemy.
        """
        self.arrow.remove_pos(self.player.attacked_enemy)
        self.level.attack_enemy()
        self.info_box.state = c.ENEMY_HIT

    def run_away(self):
        self.level.end_battle()

    def battle_won(self):
        self.level.end_battle()

    def player_finished_attack(self):
        pass