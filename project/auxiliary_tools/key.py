import pygame


class Key:
    @staticmethod
    def get_code_by_key(key):
        if key == "Q" or key == "q":
            return pygame.K_q
        elif key == "W" or key == "w":
            return pygame.K_w
        elif key == "E" or key == "e":
            return pygame.K_e
        elif key == "R" or key == "r":
            return pygame.K_r
        elif key == "T" or key == "t":
            return pygame.K_t
        elif key == "Y" or key == "y":
            return pygame.K_y
        elif key == "U" or key == "u":
            return pygame.K_u
        elif key == "I" or key == "i":
            return pygame.K_i
        elif key == "O" or key == "o":
            return pygame.K_o
        elif key == "P" or key == "p":
            return pygame.K_p
        elif key == "A" or key == "a":
            return pygame.K_a
        elif key == "S" or key == "s":
            return pygame.K_s
        elif key == "D" or key == "d":
            return pygame.K_d
        elif key == "F" or key == "f":
            return pygame.K_f
        elif key == "G" or key == "g":
            return pygame.K_g
        elif key == "H" or key == "h":
            return pygame.K_h
        elif key == "J" or key == "j":
            return pygame.K_j
        elif key == "K" or key == "k":
            return pygame.K_k
        elif key == "L" or key == "l":
            return pygame.K_l
        elif key == "Z" or key == "z":
            return pygame.K_z
        elif key == "X" or key == "x":
            return pygame.K_x
        elif key == "C" or key == "c":
            return pygame.K_c
        elif key == "V" or key == "v":
            return pygame.K_v
        elif key == "B" or key == "b":
            return pygame.K_b
        elif key == "N" or key == "n":
            return pygame.K_n
        elif key == "M" or key == "m":
            return pygame.K_m
        return None
