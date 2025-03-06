from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine
import math

from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4
from ApplicationEngine.include.Maths.Matrix.Matrix import Mat2, Mat3, Mat4


class Portal(LNLEngine.GameObject):
    portals : list[Portal] = []
    
    # TODO : Make this impl for 3 component vector and quats
    def __init__(self, Vertex1 : Vec2, Vertex2 : Vec2, col : Vec4, Destination : Portal | None = None, radius : float = 50):
        self.vertices : list[Vec2] = [Vertex1, Vertex2]

        if Destination:
            self.__DestinationPortal : Portal = Destination
        else:
            self.__DestinationPortal : Portal = self
 
        self.radius = radius

        self.alongVec : Vec2 = Vertex2 - Vertex1

        self.tangent = (self.alongVec).normalize()
        
        tanr = self.tangent.copy()
        angleRot = math.radians(90)
        tanr = tanr  * Mat2([
                            [math.cos(angleRot) , -math.sin(angleRot)],
                            [math.sin(angleRot) , math.cos(angleRot)]
                                ])
        tanr = tanr.get_p()
        
        self.normal = Vec2(tanr[0] , tanr[1])
        
        self.depth = 10

        self.colour = col

        Portal.portals.append(self)


    def checkLink(self):
        if self.__DestinationPortal is not self:
            return True
        return False
    
    def LinkPortal(self, newPortal : Portal):
        if isinstance(self.__DestinationPortal, Portal):
            self.__DestinationPortal = newPortal
            newPortal.SetDestination(self)
        else:
            self.__DestinationPortal = self
        
    def SetDestination(self, destPortal : Portal):
        self.__DestinationPortal = destPortal

    def GetDestination(self) -> Portal:
        return self.__DestinationPortal
    
    def intersectsPoint(self, point : Vec2 | Vec3):
        return is_point_in_quad(point, self.vertices[0], self.vertices[1], self.vertices[0] + (self.normal * self.depth), self.vertices[1] + (self.normal * self.depth))
    
    def intersectsQuad(self, points):
        return quad_collision( points , [self.vertices[0].get_p(), self.vertices[1].get_p(), (self.vertices[0] + (self.normal * self.depth)).get_p(), (self.vertices[1] + (self.normal * self.depth)).get_p()])

    def Draw(self):
        LNLEngine.Renderer.DrawTriangle([self.vertices[0], self.vertices[1],self.vertices[1] + (self.normal * self.depth)],self.colour)
        LNLEngine.Renderer.DrawTriangle([self.vertices[0], self.vertices[0] + (self.normal * self.depth),self.vertices[1] + (self.normal * self.depth)], self.colour)



def sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def is_point_in_triangle(pt, a, b, c):
    d1 = sign(pt, a, b)
    d2 = sign(pt, b, c)
    d3 = sign(pt, c, a)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)

def is_point_in_quad(point, v1, v2, v3, v4):
    """
    Check if a point lies within a quadrilateral defined by four vertices.
    :param point: The vertex to check (Vec2).
    :param v1, v2, v3, v4: The four vertices of the quadrilateral (Vec2).
    :return: True if the point is inside the quadrilateral, otherwise False.
    """
    


    # Split quad into two triangles and check if point is in either triangle
    return is_point_in_triangle(point, v1, v2, v3) or is_point_in_triangle(point, v1, v3, v4)


# class cube(LNLEngine.GameObject):
#     def __init__(self):
#         self.Attributes = [CanTravelThroughPortals]
    
#     def _OnUpdate(self):
#         super()._OnUpdate() 





import numpy as np

def project(vertices, axis):
    projections = [np.dot(vertex, axis) for vertex in vertices]
    return min(projections), max(projections)

def overlap(min_a, max_a, min_b, max_b):
    return max_a >= min_b and max_b >= min_a

def get_edges(vertices):
    return [vertices[i] - vertices[i - 1] for i in range(len(vertices))]

def quad_collision(quad1, quad2):
    vertices1 = np.array(quad1)
    vertices2 = np.array(quad2)
    
    edges = get_edges(vertices1) + get_edges(vertices2)
    
    for edge in edges:
        axis = np.array([-edge[1], edge[0]])  # Perpendicular vector
        
        min1, max1 = project(vertices1, axis)
        min2, max2 = project(vertices2, axis)
        
        if not overlap(min1, max1, min2, max2):
            return False
    
    return True