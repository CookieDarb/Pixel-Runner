import pygame
from sys import exit
from random import randint

def display_score():
    current_time=(pygame.time.get_ticks()-begin_time)//500
    score_text=test_font.render("Score: "+str(current_time),False,'Dark blue')
    score_rect=score_text.get_rect(midtop=(400,25))
    screen.blit(score_text,score_rect)
    return current_time

def spawn_move(spawn_list,time=0):
    if spawn_list:
        for i in spawn_list:
            i.x-=(5+(time/20))
            if(i.y>200):
                screen.blit(snail,i)
            else:
                screen.blit(fly,i)
        spawn_list=[i for i in spawn_list if i.x>-100]
    return spawn_list

def check_collision(player,spawn_list):
    for i in spawn_list:
        if(player.colliderect(i)):
            return False
    else:
        return True
    
pygame.init()
screen=pygame.display.set_mode((800,400))
pygame.display.set_caption("Tutorial")
f1=open("Leaderboard.txt","r")
top_score=f1.read()
print(type(top_score))
f1.close()

clock=pygame.time.Clock()

sky_surface=pygame.image.load('pygameLib/Sky.png').convert()  #800,300
ground=pygame.image.load('pygameLib/ground.png').convert() #800,168

test_font=pygame.font.Font('pygameLib/Pixeltype.ttf',50)

player_stand=pygame.image.load('pygameLib/player_stand.png').convert_alpha()
player_stand_rect=player_stand.get_rect(bottomleft=(50,300))
player_gravity=0

snail=pygame.image.load('pygameLib/snail1.png').convert_alpha() #72,36
fly=pygame.image.load('pygameLib/Fly1.png').convert_alpha() 
forward=5

spawn_timer=pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer,1400)
spawn_list=[]

#intro screen
score=0
intro_text=test_font.render('Pixel Runner',False,'cyan')
intro_text_rect=intro_text.get_rect(midtop=(400,25))
intro_img=pygame.transform.rotozoom(player_stand,0,2)
intro_img_rect=intro_img.get_rect(center=(400,150))
rules=test_font.render('Press SPACEBAR to run',False,'cyan')
rules_rect=rules.get_rect(midtop=(400,330))
game_active=False
begin_time=0
god_mode=0

while True:
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            pygame.quit()
            exit()

        if(game_active):
            if(event.type==pygame.MOUSEBUTTONDOWN)and(player_stand_rect.collidepoint(event.pos))and(player_stand_rect.bottom==300):
                player_gravity=-20

            if(event.type==spawn_timer):
                if(randint(1,2)==1):
                    spawn_list.append(snail.get_rect(bottomright=(randint(900,1100),300)) )
                else:
                    spawn_list.append(fly.get_rect(bottomright=(randint(900,1100),200)) )
            
            if(event.type==pygame.KEYDOWN)and(event.key==pygame.K_g):
                god_mode+=1
                if(god_mode%2==0):
                    god_mode=0
                else:
                    god_mode=1
                
        else:
            if(event.type==pygame.KEYDOWN)and(event.key==pygame.K_SPACE):
                game_active=True
                spawn_list=[]
                player_stand_rect.bottom=300
                begin_time=pygame.time.get_ticks()

    if (game_active):

        keys=pygame.key.get_pressed()
        if(keys[pygame.K_SPACE])and(player_stand_rect.bottom==300):
            player_gravity=-20
        player_gravity+=1
        screen.blit(sky_surface,(0,0))
        screen.blit(ground,(0,300))
        screen.blit(player_stand,player_stand_rect)

        score=display_score()
        spawn_list=spawn_move(spawn_list,score) 
        
        player_stand_rect.bottom+=player_gravity

        if(player_stand_rect.bottom>=300):
            player_gravity=0
            player_stand_rect.bottom=300

        
        if(god_mode==0):
            game_active=check_collision(player_stand_rect,spawn_list)
    else:
        screen.fill('Royal Blue')
        screen.blit(intro_text,intro_text_rect)
        screen.blit(rules,rules_rect)
        if(score!=0):
            total_score=test_font.render('Total Score: '+str(score),False,'cyan')
            total_score_rect=total_score.get_rect(midtop=(400,250))
            screen.blit(total_score,total_score_rect)
            
            if(score>(int(top_score))):
                top_score=str(score)
                f2=open("Leaderboard.txt","w")
                f2.write(top_score)
                f2.close()

            top_score_render=test_font.render('Top Score: '+str(top_score),False,'cyan')
            top_score_rect=top_score_render.get_rect(midtop=(400,100))
            screen.blit(top_score_render,top_score_rect)            
        
        else:
            screen.blit(intro_img,intro_img_rect)
        

    pygame.display.update()
    clock.tick(60)