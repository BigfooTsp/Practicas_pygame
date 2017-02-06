import pygame
from pygame.locals import *

class Texto:
    @staticmethod
    def render_textrect(string, font, rect, text_color, background_color, justification=0):
        """
        Takes the following arguments:

        string - the text you wish to render. \n begins a new line.
        font - a Font object
        rect - a rectstyle giving the size of the surface requested.
        text_color - a three-byte tuple of the rgb value of the
        text color. ex (0, 0, 0) = BLACK
        background_color - a three-byte tuple of the rgb value of the surface.
        justification - 0 (default) left-justified
        1 horizontally centered
        2 right-justified

        Returns the following values:

        Success - a surface object with the text rendered onto it.
        Failure - raises a TextRectException if the text won't fit onto the surface.
        """
        final_lines = []
        
        if (type(string).__name__ == "unicode"):        
            requested_lines = string.split("\\n")
        else:
            requested_lines = string.splitlines()
        
        # Create a series of lines that will fit on the provided
        # rectangle.
        for requested_line in requested_lines:
        #    if font.size(requested_line)[0] > rect.width:
        #        rect.width = font.size(requested_line)[0] + 5
            if font.size(requested_line)[1] > rect.height:
                rect.height = font.size(requested_line)[1] + 5

        for requested_line in requested_lines:
            if font.size(requested_line)[0] > rect.width:
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if font.size(word)[0] >= rect.width:
                        print "The word " + word + " is too long to fit in the rect passed."
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.
                    if font.size(test_line)[0] < rect.width:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)
        
        final_height = 0
        for final_line in final_lines:
            final_height += font.size(final_line)[1]
        if final_height > rect.height:
            rect.height = final_height + 5

        # Let's try to write the text out on the surface.

        surface = pygame.Surface(rect.size)
        surface.fill(background_color)
        

        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + font.size(line)[1] >= rect.height:
                pass #print "Once word-wrapped, the text string was too tall to fit in the rect."
            if line != "":
                tempsurface = font.render(line, 1, text_color)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    print "Invalid justification argument: " + str(justification)
            accumulated_height += font.size(line)[1]
        
        
        return surface