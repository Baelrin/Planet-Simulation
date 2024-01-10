import pygame
import math
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planets")

# Color definitions
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

# Font settings
FONT = pygame.font.SysFont("comicsans", 16)


class Planet:
    """Representation of a planet in our solar system."""
    # Astronomical unit in meters, gravitational constant, and scale for visualization.
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24  # 1 day in seconds

    def __init__(self, x, y, radius, color, mass):
        """Initializes the planet with its position, radius, color, mass, and velocity."""
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []           # Track the orbit path
        self.sun = False          # Flag if the planet is the sun
        self.distance_to_sun = 0  # Distance to the sun

        # X and Y components of the planet's velocity
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        """Draw the planet and its orbit."""
        # Convert the planet's position to screen position
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # Draw the orbit if there are enough points
        if len(self.orbit) > 2:
            updated_points = [(point[0] * self.SCALE + WIDTH / 2,
                               point[1] * self.SCALE + HEIGHT / 2) for point in self.orbit]

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        # Draw the planet itself
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        # If the planet is not the sun, render the distance to the sun
        if not self.sun:
            distance_text = FONT.render(
                f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() /
                                     2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        """Calculate the attraction force between this planet and another."""
        # Calculate the distance between the two planets
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        # Update distance to sun for the rendering
        if other.sun:
            self.distance_to_sun = distance

        # Calculate the force of attraction
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        """Update the planet's position based on the gravitational attraction from other planets."""
        # Sum all forces on this planet
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Update the planet's velocity
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # Update the planet's position
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        # Record the new position to the orbit path
        self.orbit.append((self.x, self.y))


def main():
    """Main function that initializes and runs the planet simulation."""
    run = True
    clock = pygame.time.Clock()

    # Instantiate planets
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = int(29.783 * 1000)

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = int(24.077 * 1000)

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = int(-47.4 * 1000)

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = int(-35.02 * 1000)

    # List of planets in the simulation
    planets = [sun, earth, mars, mercury, venus]

    # Main loop of the simulation
    while run:
        # Cap the frame rate to 60 frames per second
        clock.tick(60)
        WIN.fill((0, 0, 0))  # Clear the screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update planet positions and draw them
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        # Update display
        pygame.display.update()

    pygame.quit()  # Quit the game


# Entry point of the application
main()
