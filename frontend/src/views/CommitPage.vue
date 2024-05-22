<template>
    <header>
    <RouterLink to="/repoinfo/1">Repository Infomation</RouterLink>
    <RouterLink to="/prpage">Pull Requests</RouterLink>
    <RouterLink to="/commitpage">Commits</RouterLink>
    <RouterLink to="/commentpage">Comments</RouterLink>

  </header>

  <RouterView />
    <div class="page-container">
      <!-- Header Information -->
      <header>
        <h1 style="font-size: 180%;">Commit Page</h1>
      </header>
  
      <!-- Commit Information and Code Section -->
      <div style="margin-top: 20px;">
        <div style="display: flex; flex-direction: column; align-items: flex-start;">
          <!-- Top Information Boxes -->
          <div style="display: flex; width: 100%;">
            <!-- Commit Message Box -->
            <div style="border: 2px solid blue; padding: 10px; flex-grow: 2; margin-right: 10px;">
              <p><strong>Commit message:</strong> "Initial commit with all base files."</p>  <!--Actual data should be put in here-->
            </div>
            
            <!-- Semantic Score Box -->
            <div style="border: 2px solid blue; padding: 10px; flex-grow: 1; margin-right: 10px; text-align: center;">
              <p><strong>Semantic score:</strong> 0-1</p> <!--Actual data should be put in here-->
            </div>
            
            <!-- Timestamp Box -->
            <div style="border: 2px solid blue; padding: 10px; flex-grow: 1; text-align: center;">
              <p><strong>Time stamp of commit:</strong> Jan 1, 1:00 PM</p> <!--Actual data should be put in here-->
            </div>
          </div>
          
          <!-- Committed Code Box -->
          <div style="border: 2px solid blue; padding: 10px; width: 100%; height: 300px; overflow-y: scroll; margin-top: 10px;">
            <pre> <!--Actual data should be put in here-->
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BLOCK_SIZE = 20
INITIAL_SNAKE_LENGTH = 3
FPS = 10

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Initialize game variables
snake_pos = [100, 50]
snake_body = [[100, 50]]
direction = 'RIGHT'
change_to = direction
score = 0
food_pos = [random.randrange(1, (SCREEN_WIDTH//BLOCK_SIZE)) * BLOCK_SIZE,
            random.randrange(1, (SCREEN_HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]
food_spawn = True

# Game functions
def check_collision(pos, list_of_positions):
    if pos in list_of_positions[:-1]:
        return True
    if pos[0] >= SCREEN_WIDTH or pos[0] < 0 or pos[1] >= SCREEN_HEIGHT or pos[1] < 0:
        return True
    return False

def spawn_food():
    return [random.randrange(1, (SCREEN_WIDTH//BLOCK_SIZE)) * BLOCK_SIZE,
            random.randrange(1, (SCREEN_HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]

def show_score():
    font = pygame.font.SysFont(None, 35)
    score_surf = font.render('Score : ' + str(score), True, (255, 255, 255))
    score_rect = score_surf.get_rect()
    score_rect.midtop = (80, 10)
    screen.blit(score_surf, score_rect)

def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, (255, 0, 0))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
    screen.fill(BACKGROUND_COLOR)
    screen.blit(game_over_surface, game_over_rect)
    show_score()
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    direction = change_to
    if direction == 'UP':
        snake_pos[1] -= BLOCK_SIZE
    elif direction == 'DOWN':
        snake_pos[1] += BLOCK_SIZE
    elif direction == 'LEFT':
        snake_pos[0] -= BLOCK_SIZE
    elif direction == 'RIGHT':
        snake_pos[0] += BLOCK_SIZE

    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = spawn_food()
    food_spawn = True

    screen.fill(BACKGROUND_COLOR)
    for pos in snake_body:
        pygame.draw.rect(screen, SNAKE_COLOR, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, FOOD_COLOR, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

    if check_collision(snake_pos, snake_body):
        game_over()

    show_score()
    pygame.display.update()
    clock.tick(FPS)

            </pre>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "CommitPage",
    // Component Data and Methods would be added here if necessary
  }
  </script>
  
  <style scoped>
  .page-container {
    width: 80%;
    margin: 0 auto;
  }
  </style>
  