from ursina import Entity, Vec3, color, time, destroy

class Bullet(Entity):
    def __init__(self, position, direction, speed=30, lifetime=5, damage=30, bounciness=0.4, gravity=9.8, **kwargs):
        super().__init__(
            model='sphere',
            color=color.yellow,
            scale=0.1,
            collider='sphere',
            position=position,
            **kwargs
        )
        self.velocity = direction.normalized() * speed
        self.lifetime = lifetime
        self.damage = damage
        self.bounciness = bounciness
        self.gravity = gravity

    def update(self):
        self.velocity += Vec3(0, -self.gravity, 0) * time.dt
        self.position += self.velocity * time.dt #physic cuz thing should move

        self.lifetime -= time.dt
        if self.lifetime <= 0:
            destroy(self)
            return

        # Collision check
        hit_info = self.intersects()
        if not hit_info.hit:
            return

        entity = hit_info.entity

        if hasattr(entity, "hp"):
            entity.hp -= self.damage
            if hasattr(entity, "blink"):
                entity.blink(color.red)
            destroy(self)
            return

        if hit_info.world_normal is not None:
            normal = Vec3(hit_info.world_normal).normalized()

            # Reflect velocity
            self.velocity = self.velocity - (normal * (2 * self.velocity.dot(normal)))
            self.velocity *= self.bounciness

            # Push out of wall a bit
            self.position += normal * 0.05

            # Kill bullet if it’s too slow
            if self.velocity.length() < 1:
                destroy(self)
