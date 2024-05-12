import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 80
NET_WIDTH = 5
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
ball_speed = [5, 5]
left_paddle_speed = 0
right_paddle_speed = 0
left_score = 0
right_score = 0

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

left_paddle_pos = [50, HEIGHT // 2]
right_paddle_pos = [WIDTH - 50, HEIGHT // 2]
# Create paddles and ball
left_paddle = pygame.draw.polygon(screen, WHITE, [(left_paddle_pos[0], left_paddle_pos[1]), (
left_paddle_pos[0] + PADDLE_WIDTH, left_paddle_pos[1] - PADDLE_HEIGHT // 2), (left_paddle_pos[0] + PADDLE_WIDTH,
                                                                              left_paddle_pos[1] + PADDLE_HEIGHT // 2)])
right_paddle = pygame.draw.polygon(screen, WHITE, [(right_paddle_pos[0], right_paddle_pos[1]), (
right_paddle_pos[0] - PADDLE_WIDTH, right_paddle_pos[1] - PADDLE_HEIGHT // 2), (right_paddle_pos[0] - PADDLE_WIDTH,
                                                                                right_paddle_pos[
                                                                                    1] + PADDLE_HEIGHT // 2)])
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
SHADOW = (128, 128, 128)
pygame.draw.rect(screen, SHADOW, (left_paddle_pos[0] + 5, left_paddle_pos[1] + 5, PADDLE_WIDTH, PADDLE_HEIGHT))
pygame.draw.rect(screen, WHITE, (left_paddle_pos[0], left_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))


# Function to reset the ball position
def reset_ball():
    return pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)


# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

            # Paddle movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                left_paddle_speed = -5
            elif event.key == pygame.K_s:
                left_paddle_speed = 5
            elif event.key == pygame.K_UP:
                right_paddle_speed = -5
            elif event.key == pygame.K_DOWN:
                right_paddle_speed = 5
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):
                    left_paddle_speed = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                right_paddle_speed = 0

        # Update paddles and ball
    left_paddle.y += left_paddle_speed
    right_paddle.y += right_paddle_speed

    # Ensure paddles stay within the screen boundaries
    left_paddle.y = max(0, min(left_paddle.y, HEIGHT - PADDLE_HEIGHT))
    right_paddle.y = max(0, min(right_paddle.y, HEIGHT - PADDLE_HEIGHT))

    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed[0] = -ball_speed[0]

    # Ball out of bounds (scoring)
    if ball.left <= 0:
        right_score += 1
        ball = reset_ball()
    elif ball.right >= WIDTH:
        left_score += 1
        ball = reset_ball()

    # Draw everything
    GREEN = (0, 128, 0)

    # Fill the screen with green
    screen.fill(GREEN)

    # Draw a dashed line down the center of the screen
    for i in range(0, HEIGHT, 20):
        pygame.draw.line(screen, WHITE, (WIDTH // 2, i), (WIDTH // 2, i + 10), 2)

        # Draw net
    for y in range(0, HEIGHT, NET_WIDTH * 2):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - NET_WIDTH // 2, y, NET_WIDTH, NET_WIDTH))

    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    font = pygame.font.Font(None, 36)
    left_score_text = font.render(str(left_score), True, WHITE)
    right_score_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_score_text, (WIDTH // 4, 20))
    screen.blit(right_score_text, (3 * WIDTH // 4 - right_score_text.get_width(), 20))

    pygame.display.flip()
    clock.tick(FPS)
