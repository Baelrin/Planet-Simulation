import pygame
import math
from typing import List, Tuple

pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planets")

# Color definitions
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

# Load font settings once and reuse it
FONT_NAME = "comicsans"
FONT_SIZE = 16
FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)


class Planet:
    """Representation of a planet in our solar system."""
    # Astronomical unit in meters, gravitational constant, and scale for visualization.
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day in seconds

    def __init__(self, x, y, radius, color, mass):
        """Initializes the planet with its position, radius, color, mass, and velocity."""
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbit: List[Tuple[float, float]] = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, WINDOW: pygame.Surface):
        """Draw the planet and its orbit."""
        x = self.x * self.SCALE + WIDTH // 2
        y = self.y * self.SCALE + HEIGHT // 2

        if len(self.orbit) > 2:
            updated_points = [(point[0] * self.SCALE + WIDTH // 2,
                               point[1] * self.SCALE + HEIGHT // 2) for point in self.orbit]
            pygame.draw.lines(WINDOW, self.color, False, updated_points, 2)

        pygame.draw.circle(WINDOW, self.color, (int(x), int(y)), self.radius)

        if not self.sun:
            distance_text = FONT.render(
                f"{self.distance_to_sun / 1000:.1f}km", True, WHITE
            )
            WINDOW.blit(distance_text, (x - distance_text.get_width() /
                                        2, y - distance_text.get_height() / 2))

    def attraction(self, other: 'Planet') -> Tuple[float, float]:
        """Calculate the attraction force between this planet and another."""
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / (distance ** 2)
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets: List['Planet']):
        """Update the planet's position based on the gravitational attraction from other planets."""
        total_fx = total_fy = 0
        for planet in planets:
            if self is not planet:
                fx, fy = self.attraction(planet)
                total_fx += fx
                total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    """Main function that initializes and runs the planet simulation."""
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892e30)
    sun.sun = True

    earth = Planet(-Planet.AU, 0, 16, BLUE, 5.9742e24)
    earth.y_vel = 29.783e3  # type: ignore

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39e23)
    mars.y_vel = 24.077e3  # type: ignore

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30e23)
    mercury.y_vel = -47.4e3  # type: ignore

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685e24)
    venus.y_vel = -35.02e3  # type: ignore

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
