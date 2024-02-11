##imports
import pygame, time
from numba import njit
from pygame.locals import *
import numpy as np
##inits
pygame.init()
np.seterr(all="ignore")

##functions
@njit(fastmath = True)
def diffuse(norm, light_dir, a = .2):
    # i = np.dot(norm[:, :], light_dir)
    i = norm[:, :, 0] * light_dir[0] + \
        norm[:, :, 1] * light_dir[1] + \
        norm[:, :, 2] * light_dir[2]
    i = np.maximum(i, 0) + a
    return i/(1 + a)

@njit(fastmath = True)
def dot(a, b):
    r = np.zeros([a.shape[0], a.shape[1]], np.float64)
    r[...] = a[:, :, 0] * b[0] + a[:, :, 1] * b[1] + a[2] * b[2]
    return r

@njit(fastmath = True)
def stamp(norm, dir, r):
    return (norm[:, :, 0] * dir[0] + norm[:, :, 1] * dir[1] + norm[:, :, 2] * dir[2]) > np.sqrt(1-r) * 1

@njit(fastmath = True)
def specular(norm, light_dir, k = 100):
    l = np.sqrt(light_dir[0]**2 + light_dir[1]**2 + (light_dir[2]+1)**2)
    t_h = [light_dir[0]/l, light_dir[1]/l, (light_dir[2]+1)/l]
  
    i = norm[:, :, 0] * t_h[0] + \
        norm[:, :, 1] * t_h[1] + \
        norm[:, :, 2] * t_h[2]
    # i = np.dot(norm[:, :], t_h)
    return i ** k
 
def normalize(v):
    l = np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    return (v[0]/l, v[1]/l, v[2]/l)

@njit(fastmath = True)
def draw_sphere(arr_depth, arr_norm, x, y, z, r, xx, yy):
    circle = np.sqrt((xx-x)**2 + (yy-y) ** 2)
    sphere = np.sqrt(r**2-circle**2) + z
    state = (sphere > arr_depth)
    new_depth = np.where(state, sphere, arr_depth)
    
    new_norm = np.zeros(arr_norm.shape)
    new_norm[..., 0] = (xx-x)/r
    new_norm[..., 1] = (yy-y)/r
    new_norm[..., 2] = np.sqrt(1 - (circle/r) ** 2)

  
    new_norm[..., 0] = np.where(state, new_norm[:, :, 0], arr_norm[:, :, 0])
    new_norm[..., 1] = np.where(state, new_norm[:, :, 1], arr_norm[:, :, 1])
    new_norm[..., 2] = np.where(state, new_norm[:, :, 2], arr_norm[:, :, 2])
    return new_depth, new_norm

def update(mode = 0):
    ## initial values
    pos = pygame.mouse.get_pos()
    d=D.copy()
    n=N.copy()
  
    ## drawing objects
    xx, yy = np.mgrid[:d.shape[0], :d.shape[1]]
    #                        x    y    z     r    xx  yy
    d, n = draw_sphere(d, n, 200, 200, 0,    150, xx, yy)
    d, n = draw_sphere(d, n, 200, 800, -200, 600, xx, yy)
    d, n = draw_sphere(d, n, *c,             100, xx, yy)
    ## processing images
    if mode == 0:
        r = (n+1)/2 * 255
    elif mode == 1:
        r = d.reshape(*d.shape, 1) * (1.5, 1.5, 1.5)
    else:
        light = normalize([pos[0] - screen.get_width()/2, pos[1] - screen.get_height()/2, 100])
        r = diffuse(n, light, .5).reshape(*d.shape, 1) * (0, 100, 100)
        r = r + specular(n, light, 100).reshape(*d.shape, 1) * (255, 255, 255)
        if l:
            light2 = (np.sin(time.time()), 0, np.cos(time.time()))
            r = r + diffuse(n, light2, 0).reshape(*d.shape, 1) * (100, 100, 0)
            r = r + specular(n, light2, 10).reshape(*d.shape, 1) * (255, 255, 255)
            
    s = pygame.pixelcopy.make_surface(np.maximum(np.minimum(r, 255), 0).astype('uint8'))
    screen.blit(s, (0, 0))
    
##constants
WIDTH = 400
HEIGHT = 400
D = np.zeros([WIDTH, HEIGHT], dtype = np.float64)-np.inf
N = np.zeros([WIDTH, HEIGHT, 3], dtype = np.float64)*np.nan
'''#matrices
light = normalize((30,30,50))
d=np.zeros([WIDTH, HEIGHT])-np.inf
n=np.zeros([WIDTH, HEIGHT, 3])*np.nan

#d, n = draw_sphere(d, n, 100,100,100,100)
d, n = draw_sphere(d, n, 300,100,100,100)
d, n = draw_sphere(d, n, 200,200,0,200)
d, n = draw_sphere(d, n, 200,200,150,100)
r = (n+1)/2 * (255, 255, 255)
#r = d.reshape(*d.shape, 1) * (1, 1, 1)
#r = shade(n, light).reshape(*d.shape, 1) * (255, 255, 255)
'''
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
myfont = pygame.font.Font(None, 22)
c = [280, 290, 110]
render_mode = 2
running = 1
l = 1
need_update = 1
screen.blit(pygame.image.load('textures/shaders/Untitled.png'), (0,0))
pygame.display.flip()
##main loop
while running:
    t = time.time()
    for event in pygame.event.get():
        if event.type == QUIT: running = 0
        if event.type == MOUSEMOTION: need_update = 1
        if event.type == KEYUP:
            need_update = 1
            if event.key == K_1:
                render_mode = 0
            if event.key == K_2:
                render_mode = 1
            if event.key == K_3:
                render_mode = 2
            if event.key == K_SPACE:
                l = not l
    if pygame.key.get_pressed()[K_LEFT]:
        c[0] -= 10
        need_update = 1
    if pygame.key.get_pressed()[K_RIGHT]:
        c[0] += 10
        need_update = 1
    if pygame.key.get_pressed()[K_UP]:
        c[1] -= 10
        need_update = 1
    if pygame.key.get_pressed()[K_DOWN]:
        c[1] += 10
        need_update = 1
    if pygame.key.get_pressed()[K_MINUS]:
        c[2] += 10
        need_update = 1
    if pygame.key.get_pressed()[K_EQUALS]:
        c[2] -= 10
        need_update = 1
    if need_update or (l and render_mode == 2):
        update(render_mode)
        screen.blit(myfont.render("FPS: "+str(1/(time.time()-t)), True, (255, 255, 255)), (10,10))
        pygame.display.flip()
    need_update = 0
    clock.tick(30)
pygame.quit()


'''img = Image.fromarray(np.minimum(np.maximum(r, 0), 255).astype('uint8'), 'RGB')
img.show()
'''
