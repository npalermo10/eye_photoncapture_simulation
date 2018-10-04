import pygame as pg
from random import randint,random
import time
import math
from pymunk.vec2d import Vec2d
from tools import Photon, Detector

pg.init()
pg.font.init()
myfont = pg.font.SysFont('Comic Sans MS', 30)

screen_width = 300
screen_height = 500

screen = pg.display.set_mode((screen_width,screen_height))
pg.display.set_caption("photon eye catch cartoon")


photon_blue = (0, 125, 255)
clock = pg.time.Clock()
# -------- Main Program Loop -----------
previousmillis = time.time()
eye_radius = 100 
eye_loc = (int(eye_radius/2), int(screen_height-eye_radius/2))
line_width = 5

angles = linspace(200, 270, 5) 
def pair_angles(edges):
    return array([edges[:-1],edges[1:]]).T

angle_pairs = pair_angles(angles)
detectors = []
for pair in angle_pairs:
    detectors.append(Detector(pair))
    
emitter_loc = (int(eye_loc[0]+eye_radius + 100), -screen_height*3)
emitter_rad = 10
emitter_v = 5
emitter_release_n = 2
photons = []

screen_pig_coords = [Vec2d().unit().rotated_degrees(ang)*(eye_radius)*1.1 for ang in angles]

anim_done = False
while not anim_done: 
# --- Main event loop
    
    for event in pg.event.get(): # User did something 
        turning=False
        local_thrust = False
        global_thrust = False
        rot_dir = False
        if pg.event.EventType == pg.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

# --- Game logic should go here
    currentmillis=time.time()
    t=currentmillis-previousmillis
 # --- Drawing code should go here
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command
    
    screen.fill((255,255,255))
    pg.draw.circle(screen, (0,0,0), eye_loc, eye_radius, line_width)
    screen_pig_coords = [Vec2d().unit().rotated_degrees(ang)*(eye_radius)*1.2 for ang in angles]

    for coord in screen_pig_coords:
        pg.draw.line(screen, (0,0,0), eye_loc, eye_loc + coord, line_width)
        
    emitter_loc = (emitter_loc[0], emitter_loc[1]+emitter_v)
    for n_photon in arange(emitter_release_n):
        photons.append(Photon(screen, emitter_loc, randint(0,180)))

    for p in photons:
        p.move()
        p.draw()
        
        if (eye_loc - p.loc).length <= (screen_pig_coords[0]).length  and (eye_loc - p.loc).length > eye_radius:
            for coord in screen_pig_coords:
                if abs(coord.angle_degrees - (p.loc- eye_loc).angle_degrees) < degrees(arctan2(line_width, screen_pig_coords[0].length)) and p in photons:
                    photons.remove(p)
                    
        if p in photons and p.loc[0] < 0 or p.loc[1]> screen_height*2 :
            photons.remove(p)
        if p in photons and (eye_loc - p.loc).length<= eye_radius:
            where_hit = (p.loc- eye_loc).angle_degrees + 270
            for d in detectors:
                if where_hit > d.boundaries[0] and where_hit < d.boundaries[1]:
                    d.n_photons += 1
            photons.remove(p)

    pg.draw.circle(screen, (0,125,255), (int(emitter_loc[0]),int(emitter_loc[1])), emitter_rad)

    for d in detectors:
        phot_num  = myfont.render(str(d.n_photons), False, photon_blue)
        screen.blit(phot_num, eye_loc + d.label_loc_vec*eye_radius*0.8)
    pg.display.flip()

    clock.tick(60)
    if emitter_loc[1]> screen_height*1.5:
        anim_done = True

pg.quit()

loop = 0
num_loops = 50
trial_data = np.zeros([num_loops, len(detectors)])
while loop < num_loops:
    for d in detectors:
        d.n_photons = 0
    emitter_loc = (int(eye_loc[0]+eye_radius + 100), -screen_height*3)
    photons.clear()
    trial_done = False
    while not trial_done:
        emitter_loc = (emitter_loc[0], emitter_loc[1]+emitter_v)
        for n_photon in arange(emitter_release_n):
            photons.append(Photon(screen, emitter_loc, randint(0,180)))

        for p in photons:
            p.move()
             
            if (eye_loc - p.loc).length <= (screen_pig_coords[0]).length  and (eye_loc - p.loc).length > eye_radius:
                for coord in screen_pig_coords:
                    if abs(coord.angle_degrees - (p.loc- eye_loc).angle_degrees) < degrees(arctan2(line_width, screen_pig_coords[0].length)) and p in photons:
                            photons.remove(p)

            if p in photons and p.loc[0] < 0 or p.loc[1]> screen_height*2  or p.loc[1] < -screen_height*2:
                photons.remove(p)
            if p in photons and (eye_loc - p.loc).length<= eye_radius:
                where_hit = (p.loc- eye_loc).angle_degrees + 270
                for d in detectors:
                    if where_hit > d.boundaries[0] and where_hit < d.boundaries[1]:
                        d.n_photons += 1
                photons.remove(p)
        if emitter_loc[1]> screen_height*1.5:
            trial_data[loop] = [d.n_photons for d in detectors]
            trial_done = True
            loop += 1
means = trial_data.mean(axis = 0)
std = trial_data.std(axis = 0)

plt.errorbar(arange(len(detectors))+1, means, yerr = std, marker = 'o', ms = 9.0, capsize = 2)
plt.xticks([1,2,3,4], ["1", "2", "3", "4"])
plt.xlabel("detector")
plt.ylabel("N photons")
# clf()
# plt.plot(arange(len(detectors))+1, photon_counts)
# savefig('detect_vals.png', format= 'png')
# graph = pg.image.load('detect_vals.png')
# graph = pg.transform.scale(graph, (300,200))
# screen.blit(graph, [screen_width-graph.get_rect()[2], 0])


