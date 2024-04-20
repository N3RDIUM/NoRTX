import taichi as ti
from vectors import Ray, vec3, vec2

@ti.func
def normalize(v: vec3) -> vec3:
    """
    Normalizes a vector to have a length of 1.

    Args:
        v: The vector to normalize (ti.vec3).

    Returns:
        A normalized vector (ti.vec3).
    """
    mag = ti.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)
    return (v / mag) * (mag > 1e-6)+ v * (not mag > 1e-6)

@ti.dataclass
class Camera:
    resolution: vec2
    position: vec3
    rotation: vec3
    fov: ti.f32
    
    @ti.func
    def get_ray(self, pixel: vec2) -> Ray:
        """
        Calculates and returns the ray originating from the camera
        that corresponds to the given pixel on the image plane.

        Args:
            pixel: A vec2 representing the pixel coordinates.

        Returns:
            A Ray object representing the ray corresponding to the pixel.
        """
        ndc = (pixel - self.resolution * 0.5) / self.resolution
        ndc.x *= self.resolution.x / self.resolution.y
        theta = self.fov * 0.5 * ti.math.pi / 180
        uv = ndc * ti.tan(theta)
        yaw, pitch, roll = self.rotation
        
        pitch += ti.random() * 0.1 - 0.05
        yaw += ti.random() * 0.1 - 0.05
        roll += ti.random() * 0.1 - 0.05
        
        yaw = yaw * ti.math.pi / 180
        pitch = pitch * ti.math.pi / 180
        roll = roll * ti.math.pi / 180

        Ry = ti.Matrix([
            [ti.cos(yaw), -ti.sin(yaw), 0],
            [ti.sin(yaw), ti.cos(yaw), 0],
            [0, 0, 1]
        ])
        Rx = ti.Matrix([
            [1, 0, 0],
            [0, ti.cos(pitch), -ti.sin(pitch)],
            [0, ti.sin(pitch), ti.cos(pitch)]
        ])
        Rz = ti.Matrix([
            [ti.cos(roll), -ti.sin(roll), 0],
            [ti.sin(roll), ti.cos(roll), 0],
            [0, 0, 1]
        ])
        
        world_to_camera = Rz @ Rx @ Ry
        uv_rotated = world_to_camera @ vec3(uv.x, uv.y, -1.0)
        origin = self.position
        direction = normalize(uv_rotated)
        return Ray(origin, direction)