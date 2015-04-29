#!/usr/bin/python
#
# This is implementation of COMP mode.
# Computer will play and pocket the balls available on screen, with some factor of intellengece (manually set)
# ----------------------------------------------------------------------------------------------------------
import pygame
import random
from math import *

from classes_and_modules.all_functions import *
from classes_and_modules.env_variables import *
from classes_and_modules.Balls_class import Balls
from operator import *
from pygame.locals import *

pygame.init()
pygame.display.update()
Balls.shadow_img = pygame.image.load("2.png").convert_alpha()
Balls.shading_img = pygame.image.load("1.png").convert_alpha()

# ballsurface = pygame.Surface((50, 50))
# pygame.draw.circle(ballsurface, (0,0,255), (25, 25), 25)
# gameDisplay.blit(ballsurface, (x,y))
# pygame.display.flip()


def gameLoop():
    gameExit = False
    gameOver = False
    
    all_balls = []              # List of balls
    # default_speed = 5
    cue_speed = default_speed # This is initialization of cue distance 
    started = 0

    # The white cue ball positioning and initialization (random for now)
    # for i in xrange(1):
    #     x = random.randint(my_ball_size, dispWidth - my_ball_size)
    #     y = random.randint(my_ball_size, dispHeight - my_ball_size)
    #     white_ball = Balls((x, y), size=my_ball_size, thickness=6, color=WHITE)
    #     white_ball.disp()
    #
    a,b = dispSize
    white_ball = Balls((a/4, b/2), size=my_ball_size, thickness=0, color=WHITE, speed=default_speed)
    # white_ball.disp() 
    #
    # Other balls initialization
    for i in xrange(1,no_of_balls+1):
        all_balls.append(Balls(ball_loc[i], size=my_ball_size, color=ball_num_col_dict[i], number=i))
    # for i in xrange(no_of_balls):
    #     x = random.randint(my_ball_size, dispWidth - my_ball_size)
    #     y = random.randint(my_ball_size, dispHeight - my_ball_size)

    #     c1 = random.randint(0, 255)
    #     c2 = random.randint(0, 255)
    #     c3 = random.randint(0, 255)

    #     all_balls.append(Balls((x, y), size=my_ball_size, color=(c1, c2, c3)))
    # screen = pygame.display.set_mode((dispHeight, dispWidth), 0, 32)
    while not gameExit:
        show_table()
        mouse_current_pos = pygame.mouse.get_pos()
        # mouse_current_pos = [tt[0], tt[1]]

        lineStart = (white_ball.x, white_ball.y)
        # offset = [a - b for a, b in mouse_current_pos, lineStart]
        # offset = mouse_current_pos - lineStart
        # offset = Normalise_this(offset)
        # lineEnd = touple(lineStart + (offset * dispWidth))
        # const_val = 10
        # lineStart += touple(offset * const_val)

        offset = tuple(map(sub, mouse_current_pos, lineStart))
        offset = Normalise_this(offset)
        kk = tuple([ a * dispWidth for a in offset])
        lineEnd = tuple(map(add, lineStart, kk))
        pk = tuple([a* 10 for a in offset])
        mm = tuple(map(add, lineStart, pk))
        lineStart = mm


        pygame.draw.aaline(gameDisplay, WHITE, lineStart, lineEnd)

        temp_all_balls = [my_ball for my_ball in all_balls if my_ball.pocketed==0]
        all_balls = temp_all_balls

        list_of_balls_with_white = all_balls + [white_ball]
        show_my_balls(list_of_balls_with_white)
        pygame.display.update()
        
        if white_ball.pocketed == 1:
            a,b = dispSize
            white_ball = Balls((a/4, b/2), size=my_ball_size, thickness=0, color=WHITE)

        while gameOver:
            gameDisplay.fill(GREEN)
            msg2screen("Game over, press Q to quit or C to continue.")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameOver = True

        
        

        

        if all_balls == []:
            gameOver = 1 # If all balls are pocketed then gameover
            adv_mode_used = 0

        mouse_butt = pygame.mouse.get_pressed()

        # Comp Mode
        if mouse_butt[1] == 1:
            # Pressed by the user manually, to start COMP to hit the right shot
            # Next shot placement, which ball to hit, is decided by the COMP,
            # depending on the some other factors (or may be randomly)

            show_pockets(my_pocket_size)
            pygame.display.update()

            # Following loop will extract hittable balls from all_balls :D
            # Then we will decide which one to hit from those :D
            for my_ball in all_balls:
                # List of other ball except current ball :D
                list_of_other_balls = all_balls[:]
                list_of_other_balls.remove(my_ball)
                balls_to_be_tested = []

                for other_ball in list_of_other_balls:
                    dist_white_other = hypot(white_ball.x-other_ball.x, white_ball.y-other_ball.y)
                    dist_my_other = hypot(my_ball.x-other_ball.x, my_ball.y-other_ball.y)
                    # Distance between white and other ball, and my_ball and other ball

                    dist_my_white = hypot(white_ball.x - my_ball.x, white_ball.y - my_ball.y)
                    if (dist_my_white > dist_white_other) & (dist_my_white > dist_my_other):
                        # then test this other_ball location, since it is in between my_ball and white_ball :D
                        balls_to_be_tested.append(other_ball)
                # p, q = my_ball.x + 10, my_ball.y + 10
                # s = "T: " + str(len(balls_to_be_tested))
                # msg2screen(s, p, q)
                
                # pygame.display.update()

                if len(balls_to_be_tested) == 0:
                    my_ball.ok_to_hit = 1
                else:
                    x1, y1 = white_ball.x, white_ball.y
                    x2, y2 = my_ball.x, my_ball.y

                    # Testing for balls and their distance :D
                    for test_ball in balls_to_be_tested:
                        x3, y3 = test_ball.x, test_ball.y

                        # I will find of the perpendicular distance of point (x3, y3) from the line formed by the two points
                        # (x2, y2), and (x1, y1) :D

                        # Line equation in the form of Ax+ By+ C = 0 formed by the two points
                        # (x2, y2), and (x1, y1) is
                        A = tan(atan2(y2-y1, x2-x1))        # This is nothing but the slope of line :D
                        B = -1
                        C = y1 - A*x1
                        # Above formula is permutation from two point line equation :D

                        # Perpendicular distance is given by 
                        # Reference: goo.gl/mUFJSh 
                        perp_dist = abs(A*x3 + B*y3 + C)/ hypot(A,B)
                        if perp_dist > 2*(test_ball.size + white_ball.size): 
                            # Here the multiplier 2 is taken, to be sure of distance :D
                            my_ball.in_line_with_white_ball = 1
                        else:
                            my_ball.in_line_with_white_ball = 0
                            # Why to break? Beacause this means that some comes in between line of sight, hence can't test, break it :D
                            break

                    if my_ball.in_line_with_white_ball == 1:    # If that ball is hittable after testing will all balls :D
                        my_ball.ok_to_hit = 1
                    else:
                        my_ball.ok_to_hit = 0
                
            
            balls_ok_to_hit = [a_ball for a_ball in all_balls if a_ball.ok_to_hit == 1]
            
            ok_to_hit_but_cannot_be_pocketed = 0

            #==============
            # Clearing the angles and their distances :D
            
            for a_ball in list_of_balls_with_white:
                a_ball.angle = 0
                a_ball.dist = 0
            #==============

            for hit_ball in balls_ok_to_hit:
                white_ball_loc = (white_ball.x, white_ball.y)
                hit_ball_loc = (hit_ball.x, hit_ball.y)

                
                all_balls_except_hit_ball_but_with_white_ball = [a_ball for a_ball in list_of_balls_with_white if a_ball != hit_ball]
                
                # print "No. of Passing balls for tracing is " + str(len(all_balls_except_hit_ball_but_with_white_ball))
                will_it_be_pocketed = trace_for_while_ball_shot(hit_ball_loc, white_ball_loc, all_balls_except_hit_ball_but_with_white_ball)

                #============
                # show_pockets(my_pocket_size)
                # pygame.display.update()
                #============
                if will_it_be_pocketed == 1:
                    
                    temp_angle = get_angle(white_ball_loc, hit_ball)   # Passing the end point and Ball object to get the movement angle
                    move_angle = temp_angle + pi

                    # Here I am giving dist between 50 and 150, it is high distance :D. Its required so that ball can be hit hard :D
                    # rand_dist = random.randint(50,150)
                    rand_dist = 100

                    white_ball.dist = rand_dist
                    white_ball.angle = move_angle

                    move_my_all_balls(list_of_balls_with_white)

                    # p, q = hit_ball.x + 30, hit_ball.y + 30
                    # s = "is being hit :D"
                    # print s
                    # msg2screen(s,p,q)
                    # Why are your breaking?
                    # Ans: Since in one chance COMP hit one ball
                    break;
                else:
                    ok_to_hit_but_cannot_be_pocketed += 1

            
            # Advanced mode:
            if (ok_to_hit_but_cannot_be_pocketed == len(balls_ok_to_hit)) & (len(balls_ok_to_hit) > 0) & ADV_MODE:
                for a_ball in balls_ok_to_hit:
                    a_ball.pk_list = a_ball.give_me_pocket_angles()

                    const_k = 1.6
                    adv_mode_used = 0
                    # This is can be seen as radius of circle with radius = (const_k * r)
                    for t in xrange(0, 360):
                        # ref: http://stackoverflow.com/questions/14829621/formula-to-find-points-on-the-circumference-of-a-circle-given-the-center-of-the
                        x = const_k*a_ball.size*cos(t*pi/180.0) + a_ball.x
                        y = const_k*a_ball.size*sin(t*pi/180.0) + a_ball.y

                        current_ang = get_angle((x,y), a_ball)
                        # if current_ang in a_ball.pk_list:
                        pass_range = random.randint(20, 40)/100.0

                        if is_it_in_my_list(current_ang, a_ball.pk_list, pass_range) & (hypot(x- white_ball.x, y - white_ball.y) < hypot(a_ball.x - white_ball.x, a_ball.y - white_ball.y)):
                            adv_mode_used = 1
                            # pygame.draw.aaline(gameDisplay, GREEN, (white_ball.x, white_ball.y), (x,y))
                            # pygame.draw.line(gameDisplay, GREEN, (white_ball.x, white_ball.y), (x,y), 10)
                            # pygame.display.update()
                            # print "Just drawn a line :D"

                            white_ball.angle = get_angle((x,y), white_ball)
                            white_ball.speed = 10
                            white_ball.dist = random.randint(100, 200)
                            move_my_all_balls(list_of_balls_with_white)
                            print "---------------------------------------"
                            print "I have got it... Advanced COMP mode: %d" %adv_mode_used
                            print "---------------------------------------"
                            break
                        # pygame.draw.aaline(gameDisplay, (0,255,0), (x,y), (white_ball.x, white_ball.y))
                    # pygame.display.update()

                    if adv_mode_used == 1:
                        break
                # pygame.display.update()
            # #===============================
            # Below is random hitting :D
            
            # To enable or disable below if condition "adv_mode_used"
            # if (ok_to_hit_but_cannot_be_pocketed == len(balls_ok_to_hit)) & (len(balls_ok_to_hit) > 0) & (adv_mode_used == 0):
            if (adv_mode_used == 0):                
                
                #============
                show_pockets(my_pocket_size)
                pygame.display.update()
                #============

                # This means that, there is atleast one ball which can be hit, but cannot be pocketed,
                # then, out of those balls_ok_to_hit, choose any one randomly and hit it :D
                
                print "Choosing ball randomly to hit"
                temp_loc = random.randint(0,len(all_balls)-1)
                rand_ball_to_hit = all_balls[temp_loc]

                temp_angle = get_angle(white_ball_loc, rand_ball_to_hit)   # Passing the end point and Ball object to get the movement angle
                move_angle = temp_angle + pi

                # Here I am giving dist between 50 and 150, it is high distance :D. Its required so that ball can be hit hard :D
                # rand_dist = random.randint(50,150)
                rand_dist = 100

                white_ball.dist = rand_dist
                white_ball.angle = move_angle

                move_my_all_balls(list_of_balls_with_white)
            

            if len(balls_ok_to_hit) == 0:
                gameOver = True

            # temp_all_balls = [my_ball for my_ball in all_balls if my_ball.pocketed==0]
            # all_balls = temp_all_balls

            
            # After looping out of the list, I must reassign it, with removing
            # the pocketed balls
            if all_balls == []: # If all balls are pocketed then, quit the game
                gameOver = True
            
            pygame.display.update()
        
        # User mode
        if mouse_butt[2] == 1:
            started = 1
            # If pressed it acts as pulling the cue
            if cue_speed < cue_limit:
                # print "I am still holding the right click"
                cue_speed += 0.25 # If pressed I am increasing it
            else:
                pass
                # print "Please release the right click"
        else:
            if (cue_speed != white_ball.default_speed) & started:
                # print "I have released the right click: Hit dist = %d" %cue_speed
                white_ball.speed = cue_speed

                mouse_current_pos = pygame.mouse.get_pos()
                a, b = white_ball.x, white_ball.y 
                c, d = mouse_current_pos

                white_ball.dist = 2*(hypot(a-c, b-d))
                # I will hit the white ball with cue
                
                # Get mouse location, to hit
                mouse_current_pos = pygame.mouse.get_pos()
                white_ball.angle = get_angle(mouse_current_pos, white_ball)

                move_my_all_balls(list_of_balls_with_white)
                
                # and then I will assign the distance back to default_speed
                cue_speed = white_ball.default_speed 

        clock.tick(FPS)

    pygame.quit()
    print "++++-----------------------------------++++"
    quit()

if __name__ == '__main__':
    gameLoop()
