import math
import pygame


def getPointPos(Amplitude, Lamda, XPos, Speed, Time, Phase, VerticalOffset):
    if Lamda == 0:
        Lamda = 1
    return (Amplitude * math.sin((2 * math.pi * XPos / Lamda) - (Speed * Time) + Phase)) + VerticalOffset

def createWave(Amplitude, Lamda, Speed, Time, Phase, VerticalOffset, Color, Surface, Extend, width):
        points = []
        for i in range (0, Extend):
            points.append(  
                (i * 1, 
                    getPointPos(Amplitude, Lamda, i * 1, Speed, Time * 10, Phase, VerticalOffset)
                )
            )   

        pygame.draw.lines(Surface, Color, False, points, width)