from ApplicationEngine.src.Physics.RigidBody.RigidBody2D import *
from ApplicationEngine.src.Physics.Primatives._2D.Collider2D import Collider2D
from ApplicationEngine.src.Physics.Primatives._2D.Line2D import Line2D
from ApplicationEngine.src.Physics.Primatives._2D.Circle import Circle
from ApplicationEngine.src.Physics.Primatives._2D.AABB import AABB
from ApplicationEngine.src.Physics.Primatives._2D.Box2D import Box2D
from ApplicationEngine.src.Physics.Primatives._2D.Ray2D import Ray2D
from ApplicationEngine.src.Physics.Primatives._2D.RaycastResult2D import RaycastResult2D


from typing import overload, Union

class IntersectionDetector2D:


    @staticmethod
    def pointOnLine(point : Vec2, line : Line2D) -> bool:
        dx : float  = line.getEnd().x - line.getStart().x
        dy : float  = line.getEnd().y - line.getStart().y

        m  : float = dy / dx

        b : float = line.getEnd().y - (m * line.getEnd().x)
        
        return point.y == m * point.x + b
    


    @staticmethod
    def pointInCircle(point : Vec2 , circle : Circle ) -> bool:
        v = circle.getCentre() - point
        return v.length_squared() <= (circle.getRadius() ** 2)


    @staticmethod
    def pointInAABB(point : Vec2, box : AABB):
        _min = box.getLocalMin()
        _max = box.getLocalMax()


        return point.x <= _max.x and _min.x <= point.x and \
               point.y <= _max.y and _min.y <= point.y 
    

    @staticmethod
    def pointInBox2D(point : Vec2, box : Box2D) -> bool:
        pointLocalBoxSpace : Vec2 = LNLMAths.rotate_vec2(Vec2(*point.get_p()), box.getRigidBody().getPosition(), -box.getRigidBody().getRotation())

        _min : Vec2 = box.getLocalMin()
        _max : Vec2 = box.getLocalMax()

        return point.x <= _max.x and _min.x <= point.x and \
               point.y <= _max.y and _min.y <= point.y 




    @staticmethod
    def lineAndLine(point : Vec2, line : Line2D) -> bool:
        dx : float  = line.getEnd().x - line.getStart().x
        dy : float  = line.getEnd().y - line.getStart().y

        if dx == 0:
            return LNLMAths.compare_f(point.x , line.getEnd().x)
        m  : float = dy / dx

        b : float = line.getEnd().y - (m * line.getEnd().x)
        
        return point.y == m * point.x + b
    


    @staticmethod
    def lineAndCircle(line : Line2D , circle : Circle ) -> bool:
        
        
        ab = line.getEnd() - line.getStart()


        circleCentre = circle.getCentre()
        centreToLineStart = circleCentre - line.getStart()

        t : float = centreToLineStart.dot(ab) / ab.dot(ab)

        if (t < 0.0 or t > 1.0):
            return False
        
        closestPoint = line.getStart() + (ab * t)

        return IntersectionDetector2D.pointInCircle(closestPoint, circle)


    @staticmethod
    def lineAndAABB(line : Line2D, box : AABB) -> bool:
        
        if IntersectionDetector2D.pointInAABB(line.getEnd(), box) or IntersectionDetector2D.pointInAABB(line.getStart(), box):
            return True
        
        
        unitVector = (line.getEnd() - line.getStart()).get_normalized()

        unitVector[0] = (1.0 / unitVector.x) if unitVector.x != 0 else 0.0
        unitVector[1] = (1.0 / unitVector.y) if unitVector.y != 0 else 0.0


        _min = (box.getLocalMin() - line.getStart()) * unitVector
        _max = (box.getLocalMax() - line.getStart()) * unitVector

        tmin : float = max(min(_min.x,_max.x),min(_min.y,_max.y))
        tmax : float = min(max(_min.x,_max.x),max(_min.y,_max.y))

        if tmax < 0 or tmin > tmax:
            return False
        
        t = tmax if tmin < 0 else tmin

        return t > 0.0 and t * t < line.length_squared()

    @staticmethod
    def lineInBox2D(line : Line2D, box : Box2D) -> bool:
        theta : float  = -box.getRigidBody().getRotation()
        centre : Vec2  = box.getRigidBody().getPosition()

        localStart = Vec2(*line.getStart().get_p())
        localEnd   = Vec2(*line.getEnd().get_p())

        localStart = LNLMAths.rotate_vec2(localStart, centre, theta)
        localEnd = LNLMAths.rotate_vec2(localEnd, centre, theta)


        localLine : Line2D = Line2D(localStart, localEnd)
        aabb : AABB = AABB(box.getLocalMin(), box.getLocalMax())

        return IntersectionDetector2D.lineAndAABB(localLine, aabb)
    




    # =============== Raycasts ==================
    @overload
    @staticmethod
    def raycast(colider : Circle, ray : Ray2D, result : RaycastResult2D | None) -> bool: ...

    @overload
    @staticmethod
    def raycast(colider : AABB, ray : Ray2D, result : RaycastResult2D | None) -> bool: ...
     
    @overload
    @staticmethod
    def raycast(colider : Box2D, ray : Ray2D, result : RaycastResult2D | None) -> bool: ...
    



    @staticmethod
    def raycast(colider : Union[Circle, AABB, Box2D], ray : Ray2D, result : RaycastResult2D | None) -> bool:

        
        RaycastResult2D.reset(result)
        if isinstance(colider, Circle):

            originToCircle : Vec2  = colider.getCentre() - ray.getOrigin()
            radiusSquared  : float = colider.getRadius() ** 2

            originToCircleLengthSquared = originToCircle.length_squared()



            # project vector from ray origin onto the direction of the ray
            a : float = originToCircle.dot(ray.getDirection())
            bSq = originToCircleLengthSquared - (a * a)

            if radiusSquared - bSq < 0.0:
                return False


            f : float  = math.sqrt(radiusSquared - bSq)
            t : float  = 0.0
            if originToCircleLengthSquared < radiusSquared:
                t = a + f
            else:
                t = a - f
            
            if result:
                point  : Vec2 = ray.getOrigin() + ( ray.getDirection() * t )
                normal : Vec2 = (point - colider.getCentre()).get_normalized()
                

                result.init(point , normal, t, bool((t >= 0)) )

            return bool((t >= 0))




        elif isinstance(colider, AABB):
        
            unitVector = ray.getDirection()

            unitVector[0] = (1.0 / unitVector.x) if unitVector.x != 0 else 0.0
            unitVector[1] = (1.0 / unitVector.y) if unitVector.y != 0 else 0.0


            _min = (colider.getLocalMin() - ray.getOrigin()) * unitVector
            _max = (colider.getLocalMax() - ray.getOrigin()) * unitVector

            tmin : float = max(min(_min.x,_max.x),min(_min.y,_max.y))
            tmax : float = min(max(_min.x,_max.x),max(_min.y,_max.y))

            if tmax < 0 or tmin > tmax:
                return False
            
            t : float = tmax if tmin < 0 else tmin
            hit : bool = t > 0.0 and t * t < ray.getMaxLen()
            

            if not hit:
                return False


            if result:
                point  : Vec2 = ray.getOrigin() + ( ray.getDirection() * t )
                normal : Vec2 = (ray.getOrigin() - point).get_normalized()
                
                result.init(point , normal, t,  True)
            
            return True


        elif isinstance(colider, Box2D):
        
            xAxis : Vec2 = Vec2(1.0, 0.0)
            yAxis : Vec2 = Vec2(0.0, 1.0)


            xAxis = LNLMAths.rotate_vec2(xAxis, Vec2(0.0, 0.0), -colider.getRigidBody().getRotation())
            yAxis = LNLMAths.rotate_vec2(yAxis, Vec2(0.0, 0.0), -colider.getRigidBody().getRotation())


            p : Vec2 = colider.getRigidBody().getPosition() - ray.getOrigin()
            _f : Vec2 = Vec2(
                xAxis.dot(ray.getDirection()),
                yAxis.dot(ray.getDirection())
            )

            e = Vec2(
                xAxis.dot(p),
                yAxis.dot(p)
            )



            size : Vec2 = colider.getHalfSize()
            _t  = [0.0 ,0.0 ,0.0 , 0.0]

            for i in range(2):
                if LNLMAths.compare_f(_f[i], 0.0):
                    if -e[i] - size[i] > 0 or -e[i] + size[i] < 0:
                        return False
                    _f[i] = 0.000001 # avoid divide by 0 err

                _t[i * 2 + 0] = ( e[i] + (size[i] / _f[i]) )
                _t[i * 2 + 1] = ( e[i] - (size[i] / _f[i]) )

            tmin : float = max(min(_t[0], _t[1]), min(_t[2], _t[3]))
            tmax : float = min(max(_t[0], _t[1]), max(_t[2], _t[3]))

            t : float = tmax if tmin < 0 else tmin
            hit : bool = t > 0.0 and t * t < ray.getMaxLen()
            

            if not hit:
                return False


            if result:
                point  : Vec2 = ray.getOrigin() + ( ray.getDirection() * t )
                normal : Vec2 = (ray.getOrigin() - point).get_normalized()
                
                result.init(point , normal, t, True )
            
            return True



        return False
    



    # ================= Circle vs Primatice ==============

    @staticmethod
    def circleAndLine(circle : Circle , line : Line2D):
        return IntersectionDetector2D.lineAndCircle(line, circle)
    
    @staticmethod
    def circleAndcircle(c1 : Circle, c2 : Circle):

        vSq   = ( c2.getCentre() - c1.getCentre() ).length_squared()
        radSq = ( c2.getRadius() + c1.getRadius() ) ** 2

        return radSq >= vSq
    

    @staticmethod
    def circleAndAABB(circle : Circle, box : AABB) -> bool:
        _min : Vec2 = box.getLocalMin()
        _max : Vec2 = box.getLocalMax()

        closestPointToCircle : Vec2 = Vec2(*circle.getCentre().get_p())

        if closestPointToCircle.x < _min.x:
            closestPointToCircle[0] = _min.x
        if closestPointToCircle.x > _max.x:
            closestPointToCircle[0] = _max.x

        if closestPointToCircle.y < _min.y:
            closestPointToCircle[1] = _min.y
        if closestPointToCircle.x > _max.y:
            closestPointToCircle[1] = _max.y



        circleToBox: Vec2 = circle.getCentre() - closestPointToCircle
        return circleToBox.length_squared() <= ( circle.getRadius() ** 2 )


    @staticmethod
    def circleAndBox2D(circle : Circle, box : AABB) -> bool:
        _min : Vec2 = Vec2()
        _max : Vec2 = Vec2(*box.getHalfSize().get_p()) * 2


        r : Vec2 = circle.getCentre() - box.getRigidBody().getPosition()

        LNLMAths.rotate_vec2(r , Vec2(0.0 , 0.0), -box.getRigidBody().getRotation())

        localCirclePos : Vec2 = r + box.getHalfSize()


        closestPointToCircle : Vec2 = localCirclePos

        if closestPointToCircle.x < _min.x:
            closestPointToCircle[0] = _min.x
        if closestPointToCircle.x > _max.x:
            closestPointToCircle[0] = _max.x

        if closestPointToCircle.y < _min.y:
            closestPointToCircle[1] = _min.y
        if closestPointToCircle.x > _max.y:
            closestPointToCircle[1] = _max.y



        circleToBox: Vec2 = localCirclePos - closestPointToCircle
        return circleToBox.length_squared() <= ( circle.getRadius() ** 2 )
    


    @staticmethod
    def AABBAndcircle(box : AABB, circle : Circle) -> bool:
        return IntersectionDetector2D.circleAndAABB(circle, box)
    

    @overload
    @staticmethod
    def getInterval(rect : AABB, axis : Vec2) -> Vec2: ...

    @overload
    @staticmethod
    def getInterval(rect : Box2D, axis : Vec2) -> Vec2: ...
    

    @staticmethod
    def getInterval(rect : Union[AABB, Box2D], axis : Vec2) -> Vec2:
        result : Vec2 = Vec2()

        vertices : list [Vec2] = []

        if isinstance(rect , AABB):
            _min = rect.getLocalMin()
            _max = rect.getLocalMax()

            vertices : list [Vec2] = [
                Vec2(_min.x, _min.y), Vec2(_min.x, _max.y),
                Vec2(_max.x, _min.y), Vec2(_max.x, _max.y)
            ]


        elif isinstance(rect, Box2D):
            vertices = rect.getVertices()
        
        
        else:
            assert False and "Get interval faliure due to wrong class for rect  : [how did we get here???, something went horribly wrong!! ]"

        result[0] = axis.dot(vertices[0])
        result[1] = result.x

        for i in range(4):
            projection : float = axis.dot(vertices[i])
            if projection < result.x:
                result[0] = projection
            if projection > result.y:
                result[1] = projection

        return result

    @overload
    @staticmethod
    def overlapOnAxis(b1 : AABB, b2 : AABB, axis : Vec2) -> bool:...
    @overload
    @staticmethod
    def overlapOnAxis(b1 : Box2D, b2 : AABB, axis : Vec2) -> bool:...
    @overload
    @staticmethod
    def overlapOnAxis(b1 : AABB, b2 : Box2D, axis : Vec2) -> bool:...
    @overload
    @staticmethod
    def overlapOnAxis(b1 : Box2D, b2 : Box2D, axis : Vec2) -> bool:...
    @staticmethod
    def overlapOnAxis(b1 : Union[AABB,Box2D], b2 : Union[AABB,Box2D], axis : Vec2) -> bool:
        interval1 : Vec2 = IntersectionDetector2D.getInterval(b1, axis)
        interval2 : Vec2 = IntersectionDetector2D.getInterval(b2, axis)

        return (interval2.x <= interval1.y) and (interval1.x <= interval2.y)
    @overload
    @staticmethod
    def getoverlapOnAxis(b1 : AABB, b2 : AABB, axis : Vec2) -> tuple[Vec2, Vec2]:...
    @overload
    @staticmethod
    def getoverlapOnAxis(b1 : Box2D, b2 : AABB, axis : Vec2) -> tuple[Vec2, Vec2]:...
    @overload
    @staticmethod
    def getoverlapOnAxis(b1 : AABB, b2 : Box2D, axis : Vec2) -> tuple[Vec2, Vec2]:...
    @overload
    @staticmethod
    def getoverlapOnAxis(b1 : Box2D, b2 : Box2D, axis : Vec2) -> tuple[Vec2, Vec2]:...
    @staticmethod
    def getoverlapOnAxis(b1 : Union[AABB,Box2D], b2 : Union[AABB,Box2D], axis : Vec2) -> tuple[Vec2, Vec2]:
        interval1 : Vec2 = IntersectionDetector2D.getInterval(b1, axis)
        interval2 : Vec2 = IntersectionDetector2D.getInterval(b2, axis)

        return  interval1, interval2

    @staticmethod
    def AABBAndAABB(box1 : AABB, box2 : AABB) -> bool:
        axesToTest = [
            Vec2(0,1),
            Vec2(1,0),
        ]

        for i in range(len(axesToTest)):
            if not IntersectionDetector2D.overlapOnAxis(box1, box2, axesToTest[i]):
                return False
        return True



    @staticmethod
    def AABBAndBox2D(box1 : AABB, box2 : Box2D) -> bool:
        axesToTest = [
            Vec2(0,1), Vec2(1,0),
            Vec2(0,1), Vec2(1,0)
        ]
        
        axesToTest[2] = LNLMAths.rotate_vec2(axesToTest[2], Vec2(0,0), box2.getRigidBody().getRotation())
        axesToTest[3] = LNLMAths.rotate_vec2(axesToTest[3], Vec2(0,0), box2.getRigidBody().getRotation())

        for i in range(len(axesToTest)):
            if not IntersectionDetector2D.overlapOnAxis(box1, box2, axesToTest[i]):
                return False
        return True
