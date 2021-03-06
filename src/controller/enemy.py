from random import randint
from pygame import math
from math import exp

from classes.entity import Entity

from environment import config
from environment.instances import window, store

wave = 0
store.dispatch("enemy_mtx", value=[])
store.dispatch("wave", value=0)


def reset():
    global enemy_type
    global wave

    store.dispatch("enemy_mtx", value=[])
    store.dispatch("wave", value=0)
    wave = 0
    enemy_type = 0


def run():
    global wave

    # SPAWN
    if len(store.get("enemy_mtx")) == 0:
        wave += 1
        enemy_mtx = []
        level = randint(1, 3)
        enemy_type = randint(1, 5)
        boss_type = randint(1, 2)
        level_constructor = open("./src/assets/levels/level" + str(level) + ".txt", "r")
        line = level_constructor.readline()
        lin = 0
        while lin < 17:
            for col in range(len(line)):
                if line[col] == "1" or (line[col] == "2" and wave % 3 == 0):
                    if line[col] == "1":
                        enemy = Entity(
                            window,
                            "./src/assets/actors/enemies/minion{}/running_right.png".format(
                                enemy_type
                            ),
                            8,
                        )
                        enemy.strenght = config.ENEMY_DAMAGE + get_strenght_minion(wave)
                        enemy.velocity = config.ENEMY_VELOCITY + get_velocity(wave)
                        enemy.life = config.ENEMY_LIFE + get_life_minion(wave)

                    elif line[col] == "2" and wave % 3 == 0:
                        enemy = Entity(
                            window,
                            "./src/assets/actors/enemies/boss{}/running_right.png".format(
                                boss_type
                            ),
                            8,
                        )
                        enemy.strenght = config.BOSS_DAMAGE + get_strenght_boss(wave)
                        enemy.life = config.BOSS_LIFE + get_life_boss(wave)
                        enemy.velocity = config.BOSS_VELOCITY + get_velocity(wave)
                        enemy.is_boss = True

                    enemy.set_position(
                        col * (config.WIDTH / 22)
                        + (config.WIDTH / 22) / 2
                        - enemy.animation.width / 2,
                        lin * (config.HEIGHT / 17)
                        + (config.HEIGHT / 17) / 2
                        - enemy.animation.height,
                    )
                    enemy_mtx.append(enemy)

            line = level_constructor.readline()
            lin += 1

        store.dispatch("enemy_mtx", value=enemy_mtx)

    # MOVEMENT
    for enemy in store.get("enemy_mtx"):
        enemy_direction = math.Vector2(
            store.get("player").animation.x - enemy.animation.x,
            store.get("player").animation.y - enemy.animation.y,
        )
        enemy_direction.normalize_ip()
        enemy_direction *= enemy.velocity + wave
        enemy.move(enemy_direction)

    # COLISSION
    for enemy1 in range(len(store.get("enemy_mtx"))):
        for enemy2 in range(enemy1 + 1, len(store.get("enemy_mtx"))):
            if store.get("enemy_mtx")[enemy1].animation.collided(
                store.get("enemy_mtx")[enemy2].animation
            ):
                if store.get("enemy_mtx")[enemy1].distance_to(
                    store.get("player")
                ) < store.get("enemy_mtx")[enemy2].distance_to(store.get("player")):
                    new_vel_length = (
                        store.get("enemy_mtx")[enemy2].velocity_vector.length() - 30
                    )
                    if new_vel_length == 0:
                        new_vel_length = 1
                    store.get("enemy_mtx")[enemy2].velocity_vector.normalize_ip()
                    store.get("enemy_mtx")[enemy2].velocity_vector *= new_vel_length
                    store.get("enemy_mtx")[enemy2].move(
                        store.get("enemy_mtx")[enemy2].velocity_vector
                    )
                else:
                    new_vel_length = (
                        store.get("enemy_mtx")[enemy1].velocity_vector.length() - 30
                    )
                    if new_vel_length == 0:
                        new_vel_length = 1
                    store.get("enemy_mtx")[enemy1].velocity_vector.normalize_ip()
                    store.get("enemy_mtx")[enemy1].velocity_vector *= new_vel_length
                    store.get("enemy_mtx")[enemy1].move(
                        store.get("enemy_mtx")[enemy1].velocity_vector
                    )

    # DRAW
    for enemy in store.get("enemy_mtx"):
        enemy.update()
        enemy.render()

    store.dispatch("wave", value=wave)


def get_velocity(x):
    if x <= 30:
        return int(exp(0.13 * x))
    else:
        return 50


def get_strenght_minion(x):
    if x <= 30:
        return int(0.87 * exp(0.14 * x))
    else:
        return 60


def get_strenght_boss(x):
    if x <= 30:
        return int(0.85 * exp(0.16 * x))
    else:
        return 110


def get_life_boss(x):
    if x <= 30:
        return int(0.79 * exp(0.24 * x))
    else:
        return 1100


def get_life_minion(x):
    if x <= 30:
        return int(0.83 * exp(0.18 * x))
    else:
        return 200
