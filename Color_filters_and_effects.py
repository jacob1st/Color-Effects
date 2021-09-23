import pygame
import sys
import random

# A pixel object that has a pos and color
class Pixel:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.rectangle = pygame.Rect(pos)
    def draw_pixel(self, display):
        pygame.draw.rect(display, self.color, self.rectangle)

# Saves the current pixel colors (Can Undo no more than 25 times back)
def add_backup(current_pixels, current_backup):
    if len(current_backup) > 25:
        current_backup.pop(0)

    all_colors = []
    for i in range(len(current_pixels)):
        for j in range(len(current_pixels[i])):
            all_colors.append(current_pixels[i][j].color)
    current_backup.append(list(all_colors))
    return current_backup

# Resets the pixels colors to whatever is last stored in the backup
def undo(current_pixels, current_backup):
    if len(current_backup) < 1:
        return 0
    index = 0
    for i in range(len(current_pixels)):
        for j in range(len(current_pixels[i])):
            current_pixels[i][j].color = current_backup[-1][index]
            index += 1
    
    current_backup.pop(-1)

# Takes a string and turns it into a tuple with RGB values
def get_color_tuple(text):
    text = text.split(', ')
    for num in range(len(text)):
        if text[num].isdigit():
            text[num] = int(text[num])
        else:
            return (255, 255, 255)
    return (tuple(text))

# Returns a tuple with random RGB values
def get_random_color():
    red = random.randint(0, 225)
    green = random.randint(0, 225)
    blue = random.randint(0, 225)
    return (red, green, blue)

# Not used Yes, but for something later
def average_colors(color1, color2):
    red1, green1, blue1 = color1[0], color1[1], color1[2]
    red2, green2, blue2 = color2[0], color2[1], color2[2]
    print(int(red1+red2/2), int(green1+green2/2), int(blue1+blue2/2))
    return (int((red1+red2)/2), int((green1+green2)/2), int((blue1+blue2)/2))

# depending on if value is positive or negative either lighten the colors or darken them
def darken_or_lighten_color(colors, value):
    colors = list(colors)
    if value < 0:
        for i in range(len(colors)):
            if colors[i] > 10:
                colors[i] -= 10
            else:
                colors[i] = 0
    else:
        for i in range(len(colors)):
            if colors[i] < 245:
                colors[i] += 10
            else:
                colors[i] = 255
    return tuple(colors)

# For every pixel either lighten or darken them
def d_or_l_colors(list_of_pixels, darken_or_lighten):
    for i in range(len(list_of_pixels)):
        for j in range(len(list_of_pixels[i])):
            list_of_pixels[i][j].color = darken_or_lighten_color(list_of_pixels[i][j].color, darken_or_lighten)

# runs for each pixel adding a sepia effect
def sepia(list_of_pixels):
    for i in range(len(list_of_pixels)):
        for j in range(len(list_of_pixels[i])):
            red, green, blue = list_of_pixels[i][j].color[0], list_of_pixels[i][j].color[1], list_of_pixels[i][j].color[2] 
            new_red = int((red * .393) + (green *.769) + (blue * .189))
            new_green = int((red * .349) + (green *.686) + (blue * .168))
            new_blue = int((red * .272) + (green *.534) + (blue * .131))
            if new_red > 255:
                new_red = 255
            if new_green > 255:
                new_green = 255
            if new_blue > 255:
                new_blue = 255
            list_of_pixels[i][j].color = (new_red, new_green, new_blue)

# runs for each pixel adding a greyscale effect
def greyscale(list_of_pixels):
    for i in range(len(list_of_pixels)):
        for j in range(len(list_of_pixels[i])):
            red, green, blue = list_of_pixels[i][j].color[0], list_of_pixels[i][j].color[1], list_of_pixels[i][j].color[2]
            grey = (red * 0.3 + green * 0.59 + blue * 0.11)
            list_of_pixels[i][j].color = (grey, grey, grey)

#Underwater
def underwater(list_of_pixels):
    for i in range(len(list_of_pixels)):
        for j in range(len(list_of_pixels[i])):
            red, green, blue = list_of_pixels[i][j].color[0], list_of_pixels[i][j].color[1], list_of_pixels[i][j].color[2]
            red *= .444
            green *= .444
            blue *= .898
            list_of_pixels[i][j].color = (red, green, blue)
# No Green
def remove_one_color(list_of_pixels, color_to_remove):
    for i in range(len(list_of_pixels)):
        for j in range(len(list_of_pixels[i])):
            red, green, blue = list_of_pixels[i][j].color[0], list_of_pixels[i][j].color[1], list_of_pixels[i][j].color[2]
            if color_to_remove == "red":
                red = 0
            elif color_to_remove == "green":
                green = 0
            elif color_to_remove == "blue":
                blue = 0
            list_of_pixels[i][j].color = (red, green, blue)



#initialize the window
pygame.init()
pygame.display.set_caption("Color Effects")
display = pygame.display.set_mode((1000, 800))

# List of pixels and backup
pixels = []

backup = []

# Make a grid of pixels
starting_x = 100
width_of_pixel = 20
x = starting_x
y = 100
width_of_grid = 20
for i in range(width_of_grid):
    new_column = []
    for j in range(width_of_grid):
        if x > (width_of_grid-1)*width_of_pixel + starting_x:
            x = starting_x
            y += width_of_pixel
        new_column.append(Pixel((x, y, width_of_pixel, width_of_pixel), (255, 255, 255)))
        x += width_of_pixel
    pixels.append(new_column)


# Setup up all the buttons rectangle objects
color_button = pygame.Rect(800, 10, 100, 40)
random_color_button = pygame.Rect(910, 15, 70, 20)
random_gen_button = pygame.Rect(800, 50, 100, 40)
darken_color_button = pygame.Rect(800, 90, 100, 40)
lighten_color_button = pygame.Rect(800, 130, 100, 40)
greyscale_button = pygame.Rect(800, 170, 100, 40)
sepia_button = pygame.Rect(800, 210, 100, 40)
color_white = pygame.Rect(800, 600, 100, 40)
backup_button = pygame.Rect(800, 640, 100, 40)
underwater_button = pygame.Rect(800, 400, 100, 40)
no_red_button = pygame.Rect(800, 440, 100, 40)
no_green_button = pygame.Rect(800, 480, 100, 40)
no_blue_button = pygame.Rect(800, 520, 100, 40)

def main():
    # The global variables
    global pixels
    global backup
    # define the clock and other variables
    clock = pygame.time.Clock()
    color = (255,255,255)
    active = False
    text = ''
    input_text_font = pygame.font.SysFont("Arial", 12)
    notice_text_font = pygame.font.SysFont("Arial", 17)
    font_color = (255, 255, 255)
    mouse_pressed = False

    # Game loop
    while True:
        display.fill((0,0,0))
        clock.tick(60)

        # Draw all the buttons and corresponding text
        pygame.draw.rect(display, color, color_button)
        pygame.draw.rect(display, font_color, random_color_button)
        pygame.draw.rect(display, (120, 54, 200), random_gen_button)
        pygame.draw.rect(display, (12, 140, 200), darken_color_button)
        pygame.draw.rect(display, (14, 200, 154), lighten_color_button)
        pygame.draw.rect(display, (132, 132, 130), greyscale_button)
        pygame.draw.rect(display, (71, 45, 20), sepia_button)    
        pygame.draw.rect(display, (255, 255, 255), color_white) 
        pygame.draw.rect(display, (71, 71, 71), backup_button)
        pygame.draw.rect(display, (0, 0, 255), underwater_button)
        pygame.draw.rect(display, (0, 255, 255), no_red_button)    
        pygame.draw.rect(display, (255, 0, 255), no_green_button) 
        pygame.draw.rect(display, (255, 255, 0), no_blue_button)

        input_text = input_text_font.render(f"{text}", 1, (100, 0, 0))
        label = input_text_font.render("Enter Color in rgb format here: ", 1, font_color)
        label_for_color = input_text_font.render("Random_color", 1, font_color)
        label_for_generate = input_text_font.render("Randomly Color", 1, (255, 255, 255))
        label_for_darken = input_text_font.render("Darken Color", 1, (255, 255, 255))
        label_for_lighten = input_text_font.render("Lighten Color", 1, (255, 255, 255))
        label_for_greyscale = input_text_font.render("GreyScale", 1, (255, 255, 255))
        label_for_sepia = input_text_font.render("Sepia", 1, (255, 255, 255))
        label_for_color_white = input_text_font.render("Color White", 1, (0, 0, 0))
        label_for_backup = input_text_font.render("Undo", 1, (255, 255, 255))
        label_for_test = notice_text_font.render("The Next 4 buttons are random test features! ", 1, (255, 255, 255))
        label_for_underwater = input_text_font.render("Underwater", 1, (255, 0, 255))
        label_for_no_red = input_text_font.render("No Red", 1, (255, 0, 0))
        label_for_no_green = input_text_font.render("No Green", 1, (10, 155, 10))
        label_for_no_blue = input_text_font.render("No Blue", 1, (0, 0, 255))

        display.blit(label, (630, 23))
        display.blit(label_for_color, (910, 3))
        display.blit(input_text, (803, 23))
        display.blit(label_for_generate, (804, 63))
        display.blit(label_for_darken, (804, 103))
        display.blit(label_for_lighten, (804, 143))
        display.blit(label_for_greyscale, (804, 183))
        display.blit(label_for_sepia, (804, 223))
        display.blit(label_for_color_white, (804, 613))
        display.blit(label_for_backup, (804, 653))
        display.blit(label_for_test, (654, 340))        
        display.blit(label_for_underwater, (804, 413))
        display.blit(label_for_no_red, (804, 453))
        display.blit(label_for_no_green, (804, 493))
        display.blit(label_for_no_blue, (804, 533))

        # Draw the pixels
        for i in pixels:
            for j in i:
                j.draw_pixel(display)

        # get events including closing windows or clicking the mouse
        # Before any events that change the pixels, save a backup
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Closed the window
                pygame.quit()
                sys.exit()
            elif ( event.type == pygame.MOUSEBUTTONDOWN ): # If mouse is clicked
                mouse_position = pygame.mouse.get_pos()       
                # Check which button the mouse click collided with      
                if (color_button.collidepoint(mouse_position) ):  
                    color = (200, 200, 200)
                    active = True
                if (random_color_button.collidepoint(mouse_position) ):  
                    font_color = get_random_color()
                    text = str(font_color)
                elif (random_gen_button.collidepoint(mouse_position) ):   
                    add_backup(pixels, backup)
                    for i in pixels:
                        for j in i:
                            j.color = get_random_color()
                elif (darken_color_button.collidepoint(mouse_position) ):    
                    add_backup(pixels, backup)
                    d_or_l_colors(pixels, -10)
                elif (lighten_color_button.collidepoint(mouse_position) ): 
                    add_backup(pixels, backup)  
                    d_or_l_colors(pixels, 10)
                elif (greyscale_button.collidepoint(mouse_position) ):   
                    add_backup(pixels, backup)
                    greyscale(pixels)
                elif (sepia_button.collidepoint(mouse_position) ):  
                    add_backup(pixels, backup)
                    sepia(pixels)
                elif (backup_button.collidepoint(mouse_position) ):  
                    undo(pixels, backup)
                elif (underwater_button.collidepoint(mouse_position) ):  
                    add_backup(pixels, backup)
                    underwater(pixels)
                elif (no_red_button.collidepoint(mouse_position) ):  
                    add_backup(pixels, backup)
                    remove_one_color(pixels, "red")
                elif (no_green_button.collidepoint(mouse_position) ):
                    add_backup(pixels, backup)  
                    remove_one_color(pixels, "green")
                elif (no_blue_button.collidepoint(mouse_position) ): 
                    add_backup(pixels, backup) 
                    remove_one_color(pixels, "blue")
                elif (color_white.collidepoint(mouse_position) ):  
                    for i in range(len(pixels)):
                        for j in range(len(pixels[i])):
                            pixels[i][j].color = (255, 255, 255)
                else:
                    add_backup(pixels, backup)
                    mouse_pressed = True # Otherwise mark the mouse as clicked
            elif ( event.type == pygame.MOUSEBUTTONUP ): # If the mouse is lifted up
                color = (255, 255, 255)
                mouse_pressed = False
            elif(event.type == pygame.KEYDOWN): # If keys are being pressed 
                if active:
                    if event.key == pygame.K_RETURN:
                        font_color = get_color_tuple(text)
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode # Take whatever is being entered into the variable text
            
            if mouse_pressed: # Color anywhere the mouse is hovered over while it is pressed
                for i in pixels:
                        for j in i:
                            if j.rectangle.collidepoint(pygame.mouse.get_pos()):
                                j.color = font_color


        pygame.display.update()

main()

