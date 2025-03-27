from ApplicationEngine.src.Physics.RigidBody.CollisionManifold import *
from ApplicationEngine.src.Physics.RigidBody.IntersectionDetector2D import *

from ApplicationEngine.src.Physics.Primatives._2D.Collider2D import *



def cross(a: Vec2, b: Vec2) -> float:
    return a.x * b.y - a.y * b.x




class Collisions_temp:
    @staticmethod
    def project_polygon(vertices: list[Vec2], axis: Vec2) -> tuple[float, float]:
        """
        Projects the list of vertices onto the given axis (assumed normalized)
        and returns the minimum and maximum scalar projections.
        """
        projections = [v.dot(axis) for v in vertices]
        return min(projections), max(projections)

    @staticmethod
    def inside(p: Vec2, cp1: Vec2, cp2: Vec2) -> bool:
        """
        Returns True if point p is 'inside' the clip edge from cp1 to cp2.
        (Assumes that being 'inside' means p lies to the left of the directed edge.)
        """
        return cross( (cp2 - cp1), (p - cp1) ) >= 0

    @staticmethod
    def compute_intersection(s: Vec2, e: Vec2, cp1: Vec2, cp2: Vec2) -> Vec2:
        """
        Computes the intersection of the line segment (s, e) with the infinite
        line defined by the clip edge (cp1, cp2). If the lines are nearly parallel,
        returns s as a fallback.
        """
        dc = cp2 - cp1
        dp = s - e
        n1 = cp1.x * cp2.y - cp1.y * cp2.x
        n2 = s.x * e.y - s.y * e.x
        denom = dc.x * dp.y - dc.y * dp.x
        if abs(denom) < 1e-6:
            return s
        x = (n1 * dp.x - n2 * dc.x) / denom
        y = (n1 * dp.y - n2 * dc.y) / denom
        return Vec2(x, y)

    @staticmethod
    def compute_contact_points(subject: list[Vec2], clip: list[Vec2]) -> list[Vec2]:
        """
        Uses the Sutherland–Hodgman algorithm to clip the subject polygon against the clip polygon.
        Returns the list of resulting vertices (contact points).
        Assumes both polygons are convex and their vertices are in counterclockwise order.
        """
        output_list = subject[:]  # copy subject polygon
        cp1 = clip[-1]
        for cp2 in clip:
            input_list = output_list[:]
            output_list = []  # reset for current clip edge
            if not input_list:
                break
            s = input_list[-1]
            for e in input_list:
                if Collisions_temp.inside(e, cp1, cp2):
                    if not Collisions_temp.inside(s, cp1, cp2):
                        output_list.append(Collisions_temp.compute_intersection(s, e, cp1, cp2))
                    output_list.append(e)
                elif Collisions_temp.inside(s, cp1, cp2):
                    output_list.append(Collisions_temp.compute_intersection(s, e, cp1, cp2))
                s = e
            cp1 = cp2
        return output_list

    @staticmethod
    def compute_centroid(vertices: list[Vec2]) -> Vec2:
        """
        Computes the arithmetic centroid (mean position) of the given vertices.
        """
        n = len(vertices)
        sum_x = sum(v.x for v in vertices)
        sum_y = sum(v.y for v in vertices)
        return Vec2(sum_x / n, sum_y / n)

    @staticmethod
    def SAT_collision(verticesA: list[Vec2], verticesB: list[Vec2]) -> tuple[bool, Vec2, float, list[Vec2]]:
        """
        Applies the Separating Axis Theorem (SAT) to two convex polygons.
        
        Parameters:
          verticesA, verticesB: lists of Vec2 (in counterclockwise order)
          
        Returns:
          A tuple containing:
            - collision (bool): True if the polygons intersect, False otherwise.
            - collision_normal (Vec2): The axis (Vec2) with the smallest overlap (pointing from A to B).
            - penetration_depth (float): The minimal overlap along that axis.
            - contact_points (list[Vec2]): The contact points computed by clipping verticesA against verticesB.
        """
        min_overlap = sys.float_info.max
        collision_axis: Vec2 = Vec2(0, 0)  # default initialization

        def test_polygon_edges(vertices1: list[Vec2], vertices2: list[Vec2]) -> bool:
            nonlocal min_overlap, collision_axis
            count = len(vertices1)
            for i in range(count):
                current = vertices1[i]
                nxt = vertices1[(i + 1) % count]
                edge = nxt - current
                axis = Vec2(-edge.y, edge.x).normalize()
                minA, maxA = Collisions_temp.project_polygon(vertices1, axis)
                minB, maxB = Collisions_temp.project_polygon(vertices2, axis)
                overlap = min(maxA, maxB) - max(minA, minB)
                if overlap < 0:
                    return False  # Separating axis found.
                if overlap < min_overlap:
                    min_overlap = overlap
                    collision_axis = axis
            return True

        if not test_polygon_edges(verticesA, verticesB):
            return (False, Vec2(0, 0), 0.0, [])
        if not test_polygon_edges(verticesB, verticesA):
            return (False, Vec2(0, 0), 0.0, [])

        centroidA = Collisions_temp.compute_centroid(verticesA)
        centroidB = Collisions_temp.compute_centroid(verticesB)
        direction = centroidB - centroidA
        if direction.dot(collision_axis) < 0:
            collision_axis = collision_axis * -1

        collision_depth = min_overlap
        contact_points = Collisions_temp.compute_contact_points(verticesA, verticesB)

        return (True, collision_axis, collision_depth, [])

    @staticmethod
    def SAT_circle_polygon(circle_center: Vec2, radius: float, vertices: list[Vec2]) -> tuple[bool, Vec2, float, list[Vec2]]:
        """
        Applies the Separating Axis Theorem to detect collision between a circle and a convex polygon.
        
        Parameters:
          circle_center: Vec2, the center of the circle.
          radius: float, the circle's radius.
          vertices: list of Vec2, vertices of the convex polygon (counterclockwise order).
        
        Returns a tuple:
          (collision: bool, collision_normal: Vec2, penetration_depth: float, contact_points: list[Vec2])
        """
        min_overlap = sys.float_info.max
        collision_axis = Vec2(0, 0)
        n = len(vertices)
        
        # Test each polygon edge's normal as a potential separating axis.
        for i in range(n):
            current = vertices[i]
            nxt = vertices[(i + 1) % n]
            edge = nxt - current
            axis = Vec2(-edge.y, edge.x).normalize()  # Get a perpendicular (normal) axis.
            
            # Project the polygon onto the axis.
            minA, maxA = Collisions_temp.project_polygon(vertices, axis)
            # Project the circle: its projection is center dot axis ± radius.
            circle_proj = circle_center.dot(axis)
            circle_min = circle_proj - radius
            circle_max = circle_proj + radius
            
            # Compute overlap on this axis.
            overlap = min(maxA, circle_max) - max(minA, circle_min)
            if overlap < 0:
                # Separating axis found – no collision.
                return (False, Vec2(0, 0), 0.0, [])
            if overlap < min_overlap:
                min_overlap = overlap
                collision_axis = axis
        
        # Additionally, test the axis from the circle center to the closest polygon vertex.
        closest = min(vertices, key=lambda v: (v - circle_center).length_squared())
        axis2 = (closest - circle_center).normalize()
        minA2, maxA2 = Collisions_temp.project_polygon(vertices, axis2)
        circle_proj2 = circle_center.dot(axis2)
        circle_min2 = circle_proj2 - radius
        circle_max2 = circle_proj2 + radius
        overlap2 = min(maxA2, circle_max2) - max(minA2, circle_min2)
        if overlap2 < 0:
            return (False, Vec2(0, 0), 0.0, [])
        if overlap2 < min_overlap:
            min_overlap = overlap2
            collision_axis = axis2
        
        # Ensure the collision normal points from the polygon (assumed static) to the circle.
        centroid_polygon = Collisions_temp.compute_centroid(vertices)
        direction = circle_center - centroid_polygon
        if direction.dot(collision_axis) < 0:
            collision_axis = collision_axis * -1
        
        penetration_depth = min_overlap
        # For contact points, as a simple approximation, take the point on the circle's boundary along the negative collision normal.
        contact = circle_center - collision_axis * radius
        
        return (True, collision_axis, penetration_depth, [contact])

class Collisions:

    # @staticmethod
    # def clip(normal: Vec2, clipPoints: list[Vec2], refEdgePoint: Vec2, refEdgeDir: Vec2) -> list[Vec2]:
    #     clipped = []
    #     for point in clipPoints:
    #         distance = (point - refEdgePoint).dot(refEdgeDir)
    #         if distance >= 0:
    #             clipped.append(point)
    #     return clipped

    
    @staticmethod
    def projectVertices(vertices : list[Vec2], axis : Vec2) -> tuple[float, float]:
        _min : float = sys.float_info.max
        _max : float = -sys.float_info.max

        for i in range(len(vertices)):
            v = vertices[i]

            proj = v.dot(axis.get_normalized())

            if proj < _min: _min = proj
            if proj > _max: _max = proj


        return (_min , _max)



    

    @staticmethod
    def findArithmeticMean(vertices : list [Vec2]) -> Vec2:
        sumX : float = 0
        sumY : float = 0

        length = len(vertices)
        for i in range(length):
            v = vertices[i]
            sumX += v.x
            sumY += v.y

        return Vec2(sumX / length, sumY / length)

    @staticmethod
    def computeContactPointsPolygon(subjectPolygon: list[Vec2], clipPolygon: list[Vec2]) -> list[Vec2]:
        """Computes the intersection (clipped polygon) of two convex polygons
        using the Sutherland-Hodgman algorithm.
        Assumes both polygons are in counterclockwise order.
        """
        def inside(p: Vec2, cp1: Vec2, cp2: Vec2) -> bool:
            # p is inside if it lies to the left of the edge (cp1 -> cp2)
            return cross(cp2 - cp1, p - cp1) >= 0

        def computeIntersection(s: Vec2, e: Vec2, cp1: Vec2, cp2: Vec2) -> Vec2:
            # Compute intersection point between line segment (s, e) and clip edge (cp1, cp2)
            dc = cp2 - cp1
            dp = s - e
            denom = dc.x * dp.y - dc.y * dp.x
            if abs(denom) < 1e-6:
                return s  # fallback if lines are nearly parallel
            n1 = cp1.x * cp2.y - cp1.y * cp2.x
            n2 = s.x * e.y - s.y * e.x
            x = (n1 * dp.x - n2 * dc.x) / denom
            y = (n1 * dp.y - n2 * dc.y) / denom
            return Vec2(x, y)
        
        outputList = subjectPolygon[:]  # start with the entire subject polygon
        cp1 = clipPolygon[-1]
        # Process each edge of the clip polygon:
        for cp2 in clipPolygon:
            inputList = outputList[:]  # copy current vertices
            outputList = []            # reset outputList for this clip edge
            if not inputList:
                break
            s = inputList[-1]
            for e in inputList:
                if inside(e, cp1, cp2):
                    if not inside(s, cp1, cp2):
                        outputList.append(computeIntersection(s, e, cp1, cp2))
                    outputList.append(e)
                elif inside(s, cp1, cp2):
                    outputList.append(computeIntersection(s, e, cp1, cp2))
                s = e
            cp1 = cp2
        return outputList


    @staticmethod
    def IntersectPolygons(verticesA: list[Vec2], verticesB: list[Vec2]) -> tuple[bool, Vec2 | None, float | None, list[Vec2]]:
        """Calculates the collision manifold for a polygon-polygon collision.
        Returns:
            (hasCollided, collisionNormal, penetrationDepth, contactPoints)
        """
        normal: Vec2 = Vec2()
        depth: float = sys.float_info.max
        contactPoints = []

        # Check axes from polygon A
        for i in range(len(verticesA)):
            va = verticesA[i]
            vb = verticesA[(i + 1) % len(verticesA)]
            edge = va - vb
            axis = Vec2(-edge.y, edge.x).get_normalized()
            minA, maxA = Collisions.projectVertices(verticesA, axis)
            minB, maxB = Collisions.projectVertices(verticesB, axis)
            
            if minA >= maxB or minB >= maxA:
                return False, normal, depth, []
            
            axisDepth = min(maxB - minA, maxA - minB)
            
            if axisDepth < depth:
                depth = axisDepth
                normal = axis

        # Check axes from polygon B
        for i in range(len(verticesB)):
            va = verticesB[i]
            vb = verticesB[(i + 1) % len(verticesB)]
            edge = va - vb
            axis = Vec2(-edge.y, edge.x)
            axis.normalize()  # in-place normalization
            minA, maxA = Collisions.projectVertices(verticesA, axis)
            minB, maxB = Collisions.projectVertices(verticesB, axis)
            if minA >= maxB or minB >= maxA:
                return False, normal, depth, []
            axisDepth = min(maxB - minA, maxA - minB)
            if axisDepth < depth:
                depth = axisDepth
                normal = axis

        # Adjust normal and depth
        nlength = normal.length()
        if nlength == 0:
            nlength = sys.float_info.min
        depth /= nlength
        normal.normalize()

        centreA = Collisions.findArithmeticMean(verticesA)
        centreB = Collisions.findArithmeticMean(verticesB)
        direction = centreB - centreA
        if direction.dot(normal) < 0:
            normal = normal * -1

        # Compute contact points using clipping
        contactPoints = Collisions.computeContactPointsPolygon(verticesA, verticesB)
        
        return True, normal, depth, contactPoints


    @staticmethod
    def projectPointsOntoAxis(vertices : list[Vec2], axis: Vec2):
        
        minimum : float =  sys.float_info.max
        maximum : float = -sys.float_info.max
        
        for i in range(len(vertices)):
            v = vertices[i]

            proj = v.dot(axis.get_normalized())

            if proj < minimum: minimum = proj
            if proj > maximum: maximum = proj


    @staticmethod
    def separatingAxisBoxonBox(a : Box2D, b : Box2D):
        axisToTest = []


        # find all the axis that need to be tested
        aVerts : list[Vec2] = a.getVertices()
        aVertsLen : int     = len(aVerts) # cache the length to asvoid calling len()
        for i in range(aVertsLen):
            p1 : Vec2 = aVerts[i]
            p2 : Vec2 = aVerts[(i + 1) %  aVertsLen]

            edge : Vec2 = p1 - p2 # define the vector p1 -> p2

            axis = Vec2(-edge.y, edge.x).normalize() # find the normal to the edge to use as an axis for sat testing


            axisToTest.append(axis)

        # do the same for object B
        bVerts : list[Vec2] = b.getVertices()
        bVertsLen : int     = len(bVerts) 
        for i in range(bVertsLen):
            p1 : Vec2 = bVerts[i]
            p2 : Vec2 = bVerts[(i + 1) %  aVertsLen]

            edge : Vec2 = p1 - p2

            axis = Vec2(-edge.y, edge.x).normalize()

            axisToTest.append(axis)








    @staticmethod
    def findCollisionFeatures_CircleAndCircle(a : Circle, b : Circle) -> CollisionManifold:
        result : CollisionManifold = CollisionManifold()

        sumRadii : float = a.getRadius() + b.getRadius()
        distance : Vec2 = b.getCentre() - a.getCentre()

        if (distance.length_squared() - (sumRadii ** 2) > 0):
            return result
        

        depth : float = abs(distance.length() - sumRadii) * 0.5
        normal : Vec2 = Vec2(*distance.get_p()).normalize()

        distanceToPoint = a.getRadius() - depth

        contactPoint : Vec2 = a.getCentre() + (normal * distanceToPoint)

        result = CollisionManifold(normal , depth)
        result.addContactPoint(contactPoint)

        return result



    @staticmethod
    def findCollisionFeatures_BoxAndBox(a: Box2D, b: Box2D) -> CollisionManifold:
        result = CollisionManifold()

        # features : tuple[bool, Vec2 | None, float | None, list[Vec2]] = Collisions.IntersectPolygons(a.getVertices(), b.getVertices())
        features : tuple[bool, Vec2 | None, float | None, list[Vec2]] = Collisions_temp.SAT_collision(a.getVertices(), b.getVertices())
        if not features[0]:
            return result
        

        vertsa = a.getVertices()
        vertsb = b.getVertices()
        # print("collision!! ", features)
        # print("collision!! ", a.getVertices())
        # print("collision!! ", b.getVertices())
        result = CollisionManifold(features[1], features[2]) # type: ignore
        # result.contactPoints = features[3]
        result.contactPoints = [a.getRigidBody().getPosition(), b.getRigidBody().getPosition()]
        return result

    @staticmethod
    def findCollisionFeatures_BoxAndCircle(box: Box2D, circle: Circle) -> CollisionManifold:
        result = CollisionManifold()
        closestPoint = Vec2(
            max(box.getLocalMin().x, min(circle.getCentre().x, box.getLocalMax().x)),
            max(box.getLocalMin().y, min(circle.getCentre().y, box.getLocalMax().y))
        )

        distance = circle.getCentre() - closestPoint
        if distance.length_squared() > circle.getRadius() ** 2:
            return result

        normal = distance.normalize()
        depth = circle.getRadius() - distance.length()
        result = CollisionManifold(normal, depth)
        result.addContactPoint(closestPoint)

        return result

    @staticmethod
    def findCollisionFeatures_AABBAndAABB(a: AABB, b: AABB) -> CollisionManifold:
        result = CollisionManifold()
        a_min, a_max = a.getMin(), a.getMax()
        b_min, b_max = b.getMin(), b.getMax()

        overlap_x = (min(a_max.x, b_max.x) - max(a_min.x, b_min.x))
        overlap_y = (min(a_max.y, b_max.y) - max(a_min.y, b_min.y))

        if overlap_x <= 0 or overlap_y <= 0:
            return result

        depth = min(overlap_x, overlap_y)
        normal = Vec2(1, 0) if overlap_x < overlap_y else Vec2(0, 1)
        if a.getRigidBody().getPosition().x > b.getRigidBody().getPosition().x:
            normal.x = -normal.x
        if a.getRigidBody().getPosition().y > b.getRigidBody().getPosition().y:
            normal.y = -normal.y

        result = CollisionManifold(normal, depth)
        result.addContactPoint(Vec2((a.getRigidBody().getPosition().x + b.getRigidBody().getPosition().x) / 2,
                                     (a.getRigidBody().getPosition().y + b.getRigidBody().getPosition().y) / 2))
        return result

    @staticmethod
    def findCollisionFeatures_AABBAndCircle(aabb: AABB, circle: Circle) -> CollisionManifold:
        result = CollisionManifold()
        closestPoint = Vec2(
            max(aabb.getMin().x, min(circle.getCentre().x, aabb.getMax().x)),
            max(aabb.getMin().y, min(circle.getCentre().y, aabb.getMax().y))
        )

        distance = circle.getCentre() - closestPoint
        if distance.length_squared() > circle.getRadius() ** 2:
            return result

        normal = distance.normalize()
        depth = circle.getRadius() - distance.length()
        result = CollisionManifold(normal, depth)
        result.addContactPoint(closestPoint)

        return result


    @staticmethod
    def findCollisionFeatures(a : Collider2D, b : Collider2D) -> CollisionManifold:
        
        if isinstance(a ,Circle) and isinstance(b, Circle):
            return Collisions.findCollisionFeatures_CircleAndCircle(a , b)
        
        elif isinstance(a ,Box2D) and isinstance(b, Box2D):
            return Collisions.findCollisionFeatures_BoxAndBox(a , b)
        
        elif isinstance(a ,Box2D) and isinstance(b, Circle):
            return Collisions.findCollisionFeatures_BoxAndCircle(a , b)
        
        elif isinstance(a ,Circle) and isinstance(b, Box2D):
            manifold = Collisions.findCollisionFeatures_BoxAndCircle(b, a)
            manifold.normal = manifold.normal * -1  # Reverse normal for correct direction
            return manifold
        
        elif isinstance(a, AABB) and isinstance(b, AABB):
            return Collisions.findCollisionFeatures_AABBAndAABB(a, b)
        elif isinstance(a, AABB) and isinstance(b, Circle):
            return Collisions.findCollisionFeatures_AABBAndCircle(a, b)
        elif isinstance(a, Circle) and isinstance(b, AABB):
            manifold = Collisions.findCollisionFeatures_AABBAndCircle(b, a)
            manifold.normal = manifold.normal * -1
            return manifold
        else :
            assert False and "not implemented"